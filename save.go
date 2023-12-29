// package main

// import (
// 	"encoding/base64"
// 	"fmt"
// 	"io/ioutil"
// 	"strings"
// )

// // DecodeBase64Chunks decodes base64-encoded chunks from a file and returns them as a byte array.
// func DecodeBase64Chunks(filePath string) ([]byte, error) {
// 	content, err := ioutil.ReadFile(filePath)
// 	fmt.Println("Size of content:", len(content))

// 	if err != nil {
// 		return nil, err
// 	}

// 	var decodedBytes []byte

// 	lines := strings.Split(string(content), "\n")
// 	for _, line := range lines {
// 		if line == "" {
// 			continue // Skip empty lines
// 		}

// 		decodedChunk, err := base64.StdEncoding.DecodeString(line)
// 		if err != nil {
// 			return nil, err
// 		}

// 		decodedBytes = append(decodedBytes, decodedChunk...)
// 	}

// 	return decodedBytes, nil
// }



// func main() {
// 	// Replace "path/to/your/base64_chunks.txt" with the actual path to your file.
// 	filePath := "1.txt"

// 	// Decode base64-encoded chunks from the file.
// 	decodedBytes, err := DecodeBase64Chunks(filePath)
// 	if err != nil {
// 		fmt.Println("Error:", err)
// 		return
// 	}

// 	// Now you have the decoded bytes in the `decodedBytes` variable.
// 	// You can use these bytes as needed.
// 	fmt.Println("Size of decodedBytes:", len(decodedBytes))

// 	// For example, you can print the decoded bytes:
// 	//fmt.Println("Decoded Bytes:", decodedBytes)
// }


package main

import (
	"encoding/base64"
	"fmt"
	"io/ioutil"
	"strings"
)

// DecodeBase64Chunks decodes base64-encoded chunks from a file and returns them as a byte array.
func DecodeBase64Chunks(filePath string) ([]byte, error) {
	content, err := ioutil.ReadFile(filePath)
	fmt.Println("Size of rescived base64:", len(content))

	if err != nil {
		return nil, err
	}

	var decodedBytes []byte

	lines := strings.Split(string(content), "\n")
	for _, line := range lines {
		if line == "" {
			continue // Skip empty lines
		}

		decodedChunk, err := base64.StdEncoding.DecodeString(line)
		if err != nil {
			return nil, err
		}

		decodedBytes = append(decodedBytes, decodedChunk...)
	}

	return decodedBytes, nil
}

// EncodeToBase64Chunks encodes bytes to base64 in chunks and returns a string
// where each line represents a base64-encoded chunk.
func EncodeToBase64Chunks(data []byte, chunkSize int) string {
	var result string

	for i := 0; i < len(data); i += chunkSize {
		end := i + chunkSize
		if end > len(data) {
			end = len(data)
		}

		chunk := data[i:end]
		encodedChunk := base64.StdEncoding.EncodeToString(chunk)

		result += encodedChunk + "\n"
	}

	return result
}

func main() {
	// Replace "path/to/your/base64_chunks.txt" with the actual path to your file.
	filePath := "splitOutPut.txt"
	outputFilePath := "GoOutPutBase64.txt"
	// Decode base64-encoded chunks from the file.
	decodedBytes, err := DecodeBase64Chunks(filePath)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	// Now you have the decoded bytes in the `decodedBytes` variable.
	// You can use these bytes as needed.
	fmt.Println("Size of decodedBytes:", len(decodedBytes))

	// Encode the bytes to base64 and get a string where each line represents a base64-encoded chunk.
	base64String := EncodeToBase64Chunks(decodedBytes, 2048) // 76 characters per line is a common line length for base64 encoding.
	fmt.Println("Size returned base64:", len(base64String))

	// Print the base64 string (optional).
	//fmt.Println("Base64 String:")
	//fmt.Println(base64String)
	err = ioutil.WriteFile(outputFilePath, []byte(base64String), 0644)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
}
