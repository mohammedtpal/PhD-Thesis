/*
 * Copyright IBM Corp. All Rights Reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

import * as grpc from '@grpc/grpc-js';
import { connect, Contract, Identity, Signer, signers } from '@hyperledger/fabric-gateway';
import * as crypto from 'crypto';
import { promises as fs } from 'fs';
import * as path from 'path';
import { TextDecoder } from 'util';
//mst

import { readFileSync } from 'fs';
import { writeFileSync } from 'fs';

const channelName = envOrDefault('CHANNEL_NAME', 'mychannel');
const chaincodeName = envOrDefault('CHAINCODE_NAME', 'basic');
const chaincodeName2 = envOrDefault('CHAINCODE_NAME', 'basic1');

const mspId = envOrDefault('MSP_ID', 'Org1MSP');

// Path to crypto materials.
const cryptoPath = envOrDefault('CRYPTO_PATH', path.resolve(__dirname, '..', '..', '..', 'test-network', 'organizations', 'peerOrganizations', 'org1.example.com'));

// Path to user private key directory.
const keyDirectoryPath = envOrDefault('KEY_DIRECTORY_PATH', path.resolve(cryptoPath, 'users', 'User1@org1.example.com', 'msp', 'keystore'));

// Path to user certificate.
const certPath = envOrDefault('CERT_PATH', path.resolve(cryptoPath, 'users', 'User1@org1.example.com', 'msp', 'signcerts', 'cert.pem'));

// Path to peer tls certificate.
const tlsCertPath = envOrDefault('TLS_CERT_PATH', path.resolve(cryptoPath, 'peers', 'peer0.org1.example.com', 'tls', 'ca.crt'));

// Gateway peer endpoint.
const peerEndpoint = envOrDefault('PEER_ENDPOINT', 'localhost:7051');

// Gateway peer SSL host name override.
const peerHostAlias = envOrDefault('PEER_HOST_ALIAS', 'peer0.org1.example.com');

const utf8Decoder = new TextDecoder();
const assetId = `asset${Date.now()}`;

async function main(): Promise<void> {

    //await displayInputParameters();

    // The gRPC client connection should be shared by all Gateway connections to this endpoint.
    const client = await newGrpcConnection();

    const gateway = connect({
        client,
        identity: await newIdentity(),
        signer: await newSigner(),
        // Default timeouts for different gRPC calls
        evaluateOptions: () => {
            return { deadline: Date.now() + 5000 }; // 5 seconds
        },
        endorseOptions: () => {
            return { deadline: Date.now() + 15000 }; // 15 seconds
        },
        submitOptions: () => {
            return { deadline: Date.now() + 5000 }; // 5 seconds
        },
        commitStatusOptions: () => {
            return { deadline: Date.now() + 60000 }; // 1 minute
        },
    });

    try {
        // Get a network instance representing the channel where the smart contract is deployed.
        const network = gateway.getNetwork(channelName);

        // Get the smart contract from the network.
        const contract = network.getContract(chaincodeName);
        const contract2 = network.getContract(chaincodeName2);

        // Initialize a set of asset data on the ledger using the chaincode 'InitLedger' function.
      // await initLedger(contract);

        // Return all the current assets on the ledger.
       // await getAllAssets(contract);
        const startTime = Date.now(); // Record start time
        const fileId = readFileSync('filename.txt', 'utf-8').trim(); // Read and trim whitespace; // Replace with the actual file ID

        // Create a new asset on the ledger.
        // await SaveChunks(contract,fileId);

        //Get file chunkCount
        // await GetFileData(contract2);
        // await SaveFileMetaData(contract2,fileId,"38")
        const chunkCount = await GetFileMeatData(contract2, fileId);

        const endTime = Date.now();// to clac the consumed time
        const totalTime = endTime - startTime;// to clac the consumed time
        console.log(`Total save time taken: ${totalTime} milliseconds`);// to clac the consumed time

       

        // Get the asset details by assetID.
       //await readAssetByID(contract);
        RetrieveFileChunks(contract2,fileId);

        // Update an asset which does not exist.
        //await updateNonExistentAsset(contract)
    } finally {
        gateway.close();
        client.close();
    }
}

main().catch(error => {
    console.error('******** FAILED to run the application:', error);
    process.exitCode = 1;
});

async function newGrpcConnection(): Promise<grpc.Client> {
    const tlsRootCert = await fs.readFile(tlsCertPath);
    const tlsCredentials = grpc.credentials.createSsl(tlsRootCert);
    return new grpc.Client(peerEndpoint, tlsCredentials, {
        'grpc.ssl_target_name_override': peerHostAlias,
    });
}

async function newIdentity(): Promise<Identity> {
    const credentials = await fs.readFile(certPath);
    return { mspId, credentials };
}

async function newSigner(): Promise<Signer> {
    const files = await fs.readdir(keyDirectoryPath);
    const keyPath = path.resolve(keyDirectoryPath, files[0]);
    const privateKeyPem = await fs.readFile(keyPath);
    const privateKey = crypto.createPrivateKey(privateKeyPem);
    return signers.newPrivateKeySigner(privateKey);
}


async function SaveFileMetaData(contract2: Contract,fileId: string,ChunkesCount: string): Promise<void> {
    console.log('\n--> Submit Transaction: SaveFileMetaData, creates new File MetaData .........');
    
            await contract2.submitTransaction('SaveFileEntry',  fileId,ChunkesCount);
            console.log(`*** Transaction for asset ${fileId} committed successfully`);
        
    

    console.log('*** All transactions committed successfully');
}

async function GetFileMeatData(contract2: Contract, fileId: string): Promise<number | null> {
    console.log('\n--> Evaluate Transaction: GetFileEntry, function returns file entry attributes');

    // Perform the chaincode query
    const resultBytes = await contract2.evaluateTransaction('GetFileEntry', fileId); // Ensure to replace 'fileID123' with the actual file ID you need to query

    // Decode the result from bytes to a UTF-8 string
    const resultJson = utf8Decoder.decode(resultBytes);

    // Check if the result is not empty
    if (resultJson) {
        // Parse the JSON string into a JavaScript object
        const result = JSON.parse(resultJson);

        // Log the entire result object
        console.log('*** Result:', result);

        // Example of accessing specific properties of the result object
        console.log(`File ID: ${result.fileID}, Chunk Count: ${result.chunksCount}`);
        if (result.chunksCount !== undefined && typeof result.chunksCount === 'number') {
            return result.chunksCount;
        } else {
            console.log('Chunk count not found in the result for the provided file ID.');
            return null;
        }
       
    } else {
        console.log('No entry found for the provided file ID.');
        return null;
    }
}




async function SaveChunks(contract: Contract,fileId: string): Promise<void> {
    console.log('\n--> Submit Transaction: CreateAsset, creates new asset .........');

    // Read the file synchronously, assuming one base64 string per line
    const base64Strings: string[] = readFileSync('256KB-CHUNK/10.5MB.txt', 'utf-8').split('\n');

    // Loop through each base64 string and submit a transaction for each
    for (let i = 0; i < base64Strings.length; i++) {
        const base64String = base64Strings[i];
        if (base64String.trim() !== '') {
            const assetId = i+2000 ; // Use the loop index as the assetId
            await contract.submitTransaction('SaveAsset', base64String, fileId,assetId.toString());
            console.log(`*** Transaction for asset ${assetId} committed successfully`);
        }
    }

    console.log('*** All transactions committed successfully');
}


/**
 * Submit transaction asynchronously, allowing the application to process the smart contract response (e.g. update a UI)
 * while waiting for the commit notification.
 */


async function RetrieveFileChunks(contract: Contract,fileId: string): Promise<void> {
    console.log('\n--> Evaluate Transaction: RetrieveFileChunks, function returns file chunks...');
    console.log('\n--> Evaluate Transaction: ReadAsset, function returns asset attributes');

    const resultBytes = await contract.evaluateTransaction('QueryAsset', '5c782bf268c13893b7d1c7ffbbff0b2945778af13ab9b1c37cf89a939c945798','2001');

    const resultJson = utf8Decoder.decode(resultBytes);
    const result = JSON.parse(resultJson);
    console.log('*** Result:', result);
    writeFileSync('result.txt', JSON.stringify(result, null, 2));
    console.log('Result saved to result.txt');
}

/**
 * submitTransaction() will throw an error containing details of any error responses from the smart contract.
 */


/**
 * envOrDefault() will return the value of an environment variable, or a default value if the variable is undefined.
 */
function envOrDefault(key: string, defaultValue: string): string {
    return process.env[key] || defaultValue;
}

/**
 * displayInputParameters() will print the global scope parameters used by the main driver routine.
 */
async function displayInputParameters(): Promise<void> {
    console.log(`channelName:       ${channelName}`);
    console.log(`chaincodeName:     ${chaincodeName}`);
    console.log(`mspId:             ${mspId}`);
    console.log(`cryptoPath:        ${cryptoPath}`);
    console.log(`keyDirectoryPath:  ${keyDirectoryPath}`);
    console.log(`certPath:          ${certPath}`);
    console.log(`tlsCertPath:       ${tlsCertPath}`);
    console.log(`peerEndpoint:      ${peerEndpoint}`);
    console.log(`peerHostAlias:     ${peerHostAlias}`);
}