package chaincode

import (
	"encoding/base64"
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// Asset represents the structure of the asset stored in the ledger
type Asset struct {
	ChunkID   string `json:"chunkid"`
	ChunkData []byte `json:"chunkdata"`

}


// QueryResponse represents the response structure for QueryAsset
type QueryResponse struct {
	ChunkID   string `json:"chunkid"`
	ChunkData string `json:"chunkdata"`
}
// SmartContract is the smart contract
type SmartContract struct {
	contractapi.Contract
}

// SaveAsset saves the base64-encoded string in the ledger
func (c *SmartContract) SaveAsset(ctx contractapi.TransactionContextInterface, base64String string, chunkID string) error {
	// Convert base64 string to bytes
	exists, err := c.AssetExists(ctx, chunkID)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the asset %s already exists", chunkID)
	}
	
	chunkData, err := base64.StdEncoding.DecodeString(base64String)
	if err != nil {
		return fmt.Errorf("failed to decode base64 string: %v", err)
	}

	// Create a new asset
	asset := Asset{
		ChunkID:   chunkID,
		ChunkData: chunkData,
	}

	// Serialize the asset to JSON
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return fmt.Errorf("failed to marshal asset to JSON: %v", err)
	}

	// Save the asset to the ledger
	err = ctx.GetStub().PutState(chunkID, assetJSON)
	if err != nil {
		return fmt.Errorf("failed to put asset on the ledger: %v", err)
	}

	return nil
}

// QueryAsset retrieves the asset from the ledger based on chunk ID
// QueryAsset retrieves the asset from the ledger based on chunk ID
// QueryAsset retrieves the asset from the ledger based on chunk ID
// QueryAsset retrieves the asset from the ledger based on chunk ID


func (c *SmartContract) QueryAsset(ctx contractapi.TransactionContextInterface, chunkID string) (*QueryResponse, error) {
	// Retrieve the asset from the ledger
	assetJSON, err := ctx.GetStub().GetState(chunkID)
	if err != nil {
		return nil, fmt.Errorf("failed to read asset from the ledger: %v", err)
	}

	// Check if the asset exists
	if assetJSON == nil {
		return nil, fmt.Errorf("asset not found for chunk ID %s", chunkID)
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
		ChunkID:   asset.ChunkID,
		ChunkData: encodedChunkData,
	}

	return response, nil
}

// AssetExists returns true when asset with given ID exists in world state
func (s *SmartContract) AssetExists(ctx contractapi.TransactionContextInterface, id string) (bool, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return assetJSON != nil, nil
}

