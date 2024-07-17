package config

import (
	"encoding/json"
	"log"
	"os"
)

type configuration struct {
	MaxDownloadsPerTab uint `json:"maxDownloadsPerTab"`
	MaxVideoAgeInDays  uint `json:"maxVideoAgeInDays"`
}

var MaxDownloadsPerTab uint
var MaxVideoAgeInDays uint

func Init() {
	file, err := os.Open("config.json")
	if err != nil {
		log.Fatalf("Failed to open config.json: %v", err)
	}
	defer file.Close()

	var config configuration
	if err := json.NewDecoder(file).Decode(&config); err != nil {
		log.Fatalf("Failed to parse config.json: %v", err)
	}

	MaxDownloadsPerTab = config.MaxDownloadsPerTab
	MaxVideoAgeInDays = config.MaxVideoAgeInDays
}
