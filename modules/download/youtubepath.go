package download

import "fmt"

const (
	Videos youtubePath = iota
	Shorts
)

type youtubePath int

func (y youtubePath) String() string {
	switch y {
	case Videos:
		return "/videos"
	case Shorts:
		return "/shorts"
	default:
		panic(fmt.Errorf("unknown 'YoutubePath' state"))
	}
}
