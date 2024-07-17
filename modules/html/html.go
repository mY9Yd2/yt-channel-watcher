package html

import (
	"fmt"
	"html/template"
	"log"
	"os"

	"github.com/mY9Yd2/yt-channel-watcher/modules/videoinfo"
)

func WriteHtml(videoInfos []videoinfo.VideoInfo) {
	tmpl := template.Must(template.ParseFiles("templates/base.html"))

	err := os.Mkdir("dist", 0755)
	if err != nil && !os.IsExist(err) {
		log.Fatalf("Failed to create 'dist' directory: %v", err)
	}

	file, err := os.Create("dist/index.html")
	if err != nil {
		log.Fatalf("Failed to create index.html file in dist/: %v", err)
	}
	defer file.Close()

	err = tmpl.Execute(file, videoInfos)
	if err != nil {
		log.Fatalf("Failed to execute template: %v", err)
	}

	fmt.Println("\nSuccessfully generated at dist/index.html")
}
