package main

import (
	"fmt"
	"sort"

	"github.com/mY9Yd2/yt-channel-watcher/modules/channels"
	"github.com/mY9Yd2/yt-channel-watcher/modules/config"
	"github.com/mY9Yd2/yt-channel-watcher/modules/download"
	"github.com/mY9Yd2/yt-channel-watcher/modules/html"
	"github.com/mY9Yd2/yt-channel-watcher/modules/videoinfo"
)

func main() {
	config.Init()

	var categories = channels.FromJson("channels.json")
	videoInfos := []videoinfo.VideoInfo{}

	for index, category := range categories {
		fmt.Printf("\t\n--- %s (%d/%d) ---\n", category[0], index+1, len(categories))
		for i := 1; i < len(category); i++ {
			fmt.Printf("\n~ Channels (%d/%d)\n", i, len(category)-1)

			fmt.Printf("\nDownloading %s %s\n", category[i], download.Videos)
			videoInfos = append(videoInfos, download.DownloadVideoInfos(category[i], download.Videos)...)

			fmt.Printf("\nDownloading %s %s\n", category[i], download.Shorts)
			videoInfos = append(videoInfos, download.DownloadVideoInfos(category[i], download.Shorts)...)
		}
	}

	sort.Slice(videoInfos, func(i, j int) bool {
		return videoInfos[i].Timestamp.After(videoInfos[j].Timestamp)
	})

	html.WriteHtml(videoInfos)
}
