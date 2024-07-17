package channels

import (
	"encoding/json"
	"log"
	"os"
)

func decode(file *os.File) [][]string {
	var categories map[string][]string

	if err := json.NewDecoder(file).Decode(&categories); err != nil {
		log.Fatalf("Failed to parse channels.json: %v", err)
	}

	var result [][]string
	for category, channels := range categories {
		categorySlice := []string{category}
		categorySlice = append(categorySlice, channels...)
		result = append(result, categorySlice)
	}

	return result
}

func FromJson(path string) [][]string {
	file, err := os.Open(path)
	if err != nil {
		log.Fatalf("Failed to open channels.json: %v", err)
	}
	defer file.Close()

	return decode(file)
}
