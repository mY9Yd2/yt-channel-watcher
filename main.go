package main

import (
	"fmt"
	"log"
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

	for categoryIdx, category := range categories {
		for channelIdx := 1; channelIdx < len(category); channelIdx++ {
			fmt.Printf("\t\n--- %s (%d/%d)->[%d/%d] ---\n", category[0], categoryIdx+1, len(categories), channelIdx, len(category)-1)

			for _, youtubePath := range []download.YoutubePath{download.Videos, download.Shorts} {
				fmt.Printf("\nDownloading %s %s\n", category[channelIdx], youtubePath)

				result, err := download.DownloadVideoInfos(category[channelIdx], youtubePath)
				if err != nil {
					log.Println(err)
				}

				videoInfos = append(videoInfos, result...)
			}
		}
	}

	sort.Slice(videoInfos, func(i, j int) bool {
		return videoInfos[i].Timestamp.After(videoInfos[j].Timestamp)
	})

	html.WriteHtml(videoInfos)
}
