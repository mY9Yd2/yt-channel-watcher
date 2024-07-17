package videoinfo

import (
	"encoding/json"
	"time"
)

type VideoInfo struct {
	UploaderId     string    `json:"uploader_id"`
	ChannelId      string    `json:"channel_id"`
	Channel        string    `json:"channel"`
	Timestamp      time.Time `json:"timestamp"`
	FullTitle      string    `json:"fulltitle"`
	DisplayId      string    `json:"display_id"`
	WebpageUrl     string    `json:"webpage_url"`
	Thumbnail      string    `json:"thumbnail"`
	Duration       uint32    `json:"duration"`
	DurationString string    `json:"duration_string"`
}

func (d *VideoInfo) UnmarshalJSON(data []byte) error {
	type Alias VideoInfo

	aux := &struct {
		Timestamp int64 `json:"timestamp"`
		*Alias
	}{
		Alias: (*Alias)(d),
	}

	if err := json.Unmarshal(data, &aux); err != nil {
		return err
	}

	d.Timestamp = time.Unix(aux.Timestamp, 0)

	return nil
}

func (d VideoInfo) MarshalJSON() ([]byte, error) {
	return json.Marshal(struct {
		Timestamp int64 `json:"timestamp"`
	}{
		Timestamp: d.Timestamp.Unix(),
	})
}
