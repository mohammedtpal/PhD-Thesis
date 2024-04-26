package chaincode

import (
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// FileEntry represents the structure of file entry stored in the ledger
type FileEntry struct {
	FileID      string `json:"fileID"`
	ChunksCount int    `json:"chunksCount"`
}

// QueryResponse represents the response structure for QueryAsset
type QueryResponse struct {
	FileID      string `json:"fileID"`
	ChunksCount int    `json:"chunksCount"`
	}

// SmartContract is the smart contract
type SmartContract struct {
	contractapi.Contract
}

// SaveFileEntry saves the file entry to the ledger
func (c *SmartContract) SaveFileEntry(ctx contractapi.TransactionContextInterface, fileID string, chunksCount int) error {
	// Check if fileID already exists
	existingEntry, err := c.GetFileEntry(ctx, fileID)
	if err == nil && existingEntry != nil {
		return fmt.Errorf("fileID %s already exists", fileID)
	}

	// Create a new file entry
	entry := FileEntry{
		FileID:      fileID,
		ChunksCount: chunksCount,
	}

	// Serialize the entry to JSON
	entryJSON, err := json.Marshal(entry)
	if err != nil {
		return fmt.Errorf("failed to marshal entry to JSON: %v", err)
	}

	// Save the entry to the ledger
	err = ctx.GetStub().PutState(fileID, entryJSON)
	if err != nil {
		return fmt.Errorf("failed to put entry on the ledger: %v", err)
	}
	fmt.Printf("okkkk")
	return nil
}

// GetFileEntry retrieves the file entry from the ledger based on fileID
func (c *SmartContract) GetFileEntry(ctx contractapi.TransactionContextInterface, fileID string) (*FileEntry, error) {
	// Retrieve the entry from the ledger
	entryJSON, err := ctx.GetStub().GetState(fileID)
	if err != nil {
		return nil, fmt.Errorf("failed to read entry from the ledger: %v", err)
	}

	// Check if the entry exists
	if entryJSON == nil {
		return nil, nil
	}

	// Deserialize the entry from JSON
	var entry FileEntry
	err = json.Unmarshal(entryJSON, &entry)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal entry from JSON: %v", err)
	}

	return &entry, nil
}

// GetChunksCount retrieves the chunks count for the fileID from the ledger
func (c *SmartContract) GetChunksCount(ctx contractapi.TransactionContextInterface, fileID string) (int, error) {
	// Retrieve the entry from the ledger
	entry, err := c.GetFileEntry(ctx, fileID)
	if err != nil {
		return 0, err
	}

	// Check if the entry exists
	if entry == nil {
		return 0, fmt.Errorf("fileID %s does not exist", fileID)
	}

	return entry.ChunksCount, nil
}

func main() {
	chaincode, err := contractapi.NewChaincode(&SmartContract{})
	if err != nil {
		fmt.Printf("Error creating SmartContract chaincode: %v", err)
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting SmartContract chaincode: %v", err)
	}
}

