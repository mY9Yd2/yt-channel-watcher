package download

import "fmt"

const (
	Videos YoutubePath = iota
	Shorts
)

type YoutubePath int

func (y YoutubePath) String() string {
	switch y {
	case Videos:
		return "/videos"
	case Shorts:
		return "/shorts"
	default:
		panic(fmt.Errorf("unknown 'YoutubePath' state"))
	}
}
