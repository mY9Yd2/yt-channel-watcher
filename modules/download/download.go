package download

import (
	"bufio"
	"encoding/json"
	"log"
	"net/url"
	"os/exec"
	"strconv"
	"sync"
	"syscall"
	"time"

	"github.com/mY9Yd2/yt-channel-watcher/modules/config"
	"github.com/mY9Yd2/yt-channel-watcher/modules/videoinfo"
)

func processYtDlpError(scanner *bufio.Scanner, wg *sync.WaitGroup) {
	defer wg.Done()

	for scanner.Scan() {
		log.Printf("stderr: %s", scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		// TODO: read |0: file already closed
		// Should this code call Fatalf or Printf is fine in this case?
		// 2024/07/15 10:30:04 Error reading stderr: read |0: file already closed
		//log.Fatalf("Error reading stderr: %v", err)
		log.Printf("Error reading stderr: %v", err)
	}
}

func processYtDlpExiStatus(exitErr *exec.ExitError) {
	if status, ok := exitErr.Sys().(syscall.WaitStatus); ok {
		// Error codes
		// https://github.com/yt-dlp/yt-dlp/issues/4262#issuecomment-1173133105
		exitStatus := status.ExitStatus()

		if exitStatus != 101 {
			log.Printf("Command exited with status code: %d", status.ExitStatus())
		}
	}
}

func processYtDlpJson(scanner *bufio.Scanner, wg *sync.WaitGroup, cmd *exec.Cmd, videoInfos *[]videoinfo.VideoInfo) {
	defer wg.Done()

	for scanner.Scan() {
		line := scanner.Text()

		if line == "" {
			continue
		}

		var videoInfo videoinfo.VideoInfo
		if err := json.Unmarshal([]byte(line), &videoInfo); err != nil {
			log.Printf("Failed to parse yt-dlp JSON: %v", err)
			continue
		}

		maxVideoAge := time.Duration(config.MaxVideoAgeInDays) * 24 * time.Hour
		if time.Since(videoInfo.Timestamp) > maxVideoAge {
			err := cmd.Process.Signal(syscall.SIGINT)
			if err != nil {
				log.Printf("Error sending signal to process: %v", err)
			}
		} else {
			*videoInfos = append(*videoInfos, videoInfo)
		}
	}
	if err := scanner.Err(); err != nil {
		// TODO: read |0: file already closed
		// Should this code call Fatalf or Printf is fine in this case?
		// 2024/07/15 10:07:19 Error reading output: read |0: file already closed
		//log.Fatalf("Error reading output: %v", err)
		log.Printf("Error reading output: %v", err)
	}
}

func DownloadVideoInfos(channel string, path YoutubePath) ([]videoinfo.VideoInfo, error) {
	videoInfos := []videoinfo.VideoInfo{}

	channelUrl, err := url.ParseRequestURI("https://www.youtube.com/" + url.PathEscape(channel) + path.String())
	if err != nil {
		return videoInfos, err
	}

	cmd := exec.Command(
		"yt-dlp",
		"--quiet",
		"--no-simulate",
		"--skip-download",
		"--max-downloads",
		strconv.FormatUint(uint64(config.MaxDownloadsPerTab), 10),
		"--print",
		`{"fulltitle": %(fulltitle)+j, "webpage_url": %(webpage_url)j, "thumbnail": %(thumbnail)j, "channel": %(channel)+j, "timestamp": %(timestamp)j, "duration_string": %(duration_string)j, "channel_id": %(channel_id)j, "display_id": %(display_id)j, "uploader_id": %(uploader_id)+j}`,
		channelUrl.String(),
	)

	stdout, err := cmd.StdoutPipe()
	if err != nil {
		log.Fatalf("Failed to get stdout pipe: %v", err)
	}

	stderr, err := cmd.StderrPipe()
	if err != nil {
		log.Fatalf("Failed to get stderr pipe: %v", err)
	}

	if err := cmd.Start(); err != nil {
		log.Fatalf("Failed to start command: %v", err)
	}

	var wg sync.WaitGroup
	wg.Add(2)

	scanner := bufio.NewScanner(stdout)
	go processYtDlpJson(scanner, &wg, cmd, &videoInfos)

	errScanner := bufio.NewScanner(stderr)
	go processYtDlpError(errScanner, &wg)

	if err := cmd.Wait(); err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			processYtDlpExiStatus(exitErr)
		} else {
			log.Fatalf("Command finished with error: %v", err)
		}
	}

	wg.Wait()

	return videoInfos, nil
}
