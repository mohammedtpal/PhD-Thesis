package chaincode

import (
	"encoding/base64"
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// Asset represents the structure of the asset stored in the ledger
type Asset struct {
	FileID    string `json:"fileID"`
	ChunkID   string `json:"chunkID"`
	ChunkData []byte `json:"chunkData"`
}

// QueryResponse represents the response structure for QueryAsset
type QueryResponse struct {
	FileID    string `json:"fileID"`
	ChunkID   string `json:"chunkID"`
	ChunkData string `json:"chunkData"`
}

// SmartContract is the smart contract
type SmartContract struct {
	contractapi.Contract
}

// SaveAsset saves the base64-encoded string in the ledger
func (c *SmartContract) SaveAsset(ctx contractapi.TransactionContextInterface, base64String string, fileID string, chunkID string) error {
	// Generate composite key
	compositeKey, err := ctx.GetStub().CreateCompositeKey("fileID~chunkID", []string{fileID, chunkID})
	if err != nil {
		return fmt.Errorf("failed to create composite key: %v", err)
	}

	// Check if asset already exists
	exists, err := c.AssetExists(ctx, fileID, chunkID)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the asset with fileID %s and chunkID %s already exists", fileID, chunkID)
	}

	// Convert base64 string to bytes
	chunkData, err := base64.StdEncoding.DecodeString(base64String)
	if err != nil {
		return fmt.Errorf("failed to decode base64 string: %v", err)
	}

	// Create a new asset
	asset := Asset{
		FileID:    fileID,
		ChunkID:   chunkID,
		ChunkData: chunkData,
	}

	// Serialize the asset to JSON
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return fmt.Errorf("failed to marshal asset to JSON: %v", err)
	}

	// Save the asset to the ledger
	err = ctx.GetStub().PutState(compositeKey, assetJSON)
	if err != nil {
		return fmt.Errorf("failed to put asset on the ledger: %v", err)
	}

	return nil
}

// QueryAsset retrieves the asset from the ledger based on fileID and chunkID
func (c *SmartContract) QueryAsset(ctx contractapi.TransactionContextInterface, fileID string, chunkID string) (*QueryResponse, error) {
	// Generate composite key
	compositeKey, err := ctx.GetStub().CreateCompositeKey("fileID~chunkID", []string{fileID, chunkID})
	if err != nil {
		return nil, fmt.Errorf("failed to create composite key: %v", err)
	}

	// Retrieve the asset from the ledger
	assetJSON, err := ctx.GetStub().GetState(compositeKey)
	if err != nil {
		return nil, fmt.Errorf("failed to read asset from the ledger: %v", err)
	}

	// Check if the asset exists
	if assetJSON == nil {
		return nil, fmt.Errorf("asset not found for fileID %s and chunkID %s", fileID, chunkID)
	}

	// Deserialize the asset from JSON
	var asset Asset
	err = json.Unmarshal(assetJSON, &asset)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal asset from JSON: %v", err)
	}

	// Encode ChunkData to base64
	encodedChunkData := base64.StdEncoding.EncodeToString(asset.ChunkData)

	// Create and return QueryResponse
	response := &QueryResponse{
		FileID:    asset.FileID,
		ChunkID:   asset.ChunkID,
		ChunkData: encodedChunkData,
	}

	return response, nil
}

// AssetExists returns true when asset with given fileID and chunkID exists in world state
func (c *SmartContract) AssetExists(ctx contractapi.TransactionContextInterface, fileID string, chunkID string) (bool, error) {
	// Generate composite key
	compositeKey, err := ctx.GetStub().CreateCompositeKey("fileID~chunkID", []string{fileID, chunkID})
	if err != nil {
		return false, fmt.Errorf("failed to create composite key: %v", err)
	}

	assetJSON, err := ctx.GetStub().GetState(compositeKey)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return assetJSON != nil, nil
}
