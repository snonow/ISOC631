from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sympy import false
from web3 import Web3

app = FastAPI()

# Configuration de Web3 pour se connecter à votre nœud Ethereum
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  # Mettez l'URL de votre nœud Ethereum


# Modèle Pydantic pour la soumission de mouvement
class MoveSubmission(BaseModel):
    player: str
    moveHash: str


# Adresse du contrat et ABI (Application Binary Interface)
contract_address = "0x43D218197E8c5FBC0527769821503660861c7045"
contract_abi = [
    {
				"inputs": [
					{
						"internalType": "uint256",
						"name": "_betMin",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "_revealTimeout",
						"type": "uint256"
					}
				],
				"stateMutability": "nonpayable",
				"type": "constructor"
			},
			{
				"anonymous": false,
				"inputs": [
					{
						"indexed": false,
						"internalType": "address",
						"name": "winner",
						"type": "address"
					},
					{
						"indexed": false,
						"internalType": "uint256",
						"name": "winnings",
						"type": "uint256"
					}
				],
				"name": "GameEnded",
				"type": "event"
			},
			{
				"anonymous": false,
				"inputs": [
					{
						"indexed": false,
						"internalType": "address",
						"name": "player1",
						"type": "address"
					},
					{
						"indexed": false,
						"internalType": "address",
						"name": "player2",
						"type": "address"
					},
					{
						"indexed": false,
						"internalType": "uint256",
						"name": "bet",
						"type": "uint256"
					}
				],
				"name": "GameStarted",
				"type": "event"
			},
			{
				"anonymous": false,
				"inputs": [
					{
						"indexed": false,
						"internalType": "address",
						"name": "player",
						"type": "address"
					}
				],
				"name": "MoveSubmitted",
				"type": "event"
			},
			{
				"inputs": [],
				"name": "betMin",
				"outputs": [
					{
						"internalType": "uint256",
						"name": "",
						"type": "uint256"
					}
				],
				"stateMutability": "view",
				"type": "function"
			},
			{
				"inputs": [],
				"name": "getContractBalance",
				"outputs": [
					{
						"internalType": "uint256",
						"name": "",
						"type": "uint256"
					}
				],
				"stateMutability": "view",
				"type": "function"
			},
			{
				"inputs": [],
				"name": "initialBet",
				"outputs": [
					{
						"internalType": "uint256",
						"name": "",
						"type": "uint256"
					}
				],
				"stateMutability": "view",
				"type": "function"
			},
			{
				"inputs": [],
				"name": "player1",
				"outputs": [
					{
						"internalType": "address",
						"name": "",
						"type": "address"
					}
				],
				"stateMutability": "view",
				"type": "function"
			},
			{
				"inputs": [],
				"name": "player2",
				"outputs": [
					{
						"internalType": "address",
						"name": "",
						"type": "address"
					}
				],
				"stateMutability": "view",
				"type": "function"
			},
			{
				"inputs": [
					{
						"internalType": "address",
						"name": "",
						"type": "address"
					}
				],
				"name": "players",
				"outputs": [
					{
						"internalType": "bytes32",
						"name": "moveHash",
						"type": "bytes32"
					},
					{
						"internalType": "bool",
						"name": "revealed",
						"type": "bool"
					},
					{
						"internalType": "uint256",
						"name": "bet",
						"type": "uint256"
					}
				],
				"stateMutability": "view",
				"type": "function"
			},
			{
				"inputs": [],
				"name": "register",
				"outputs": [],
				"stateMutability": "payable",
				"type": "function"
			},
			{
				"inputs": [
					{
						"internalType": "bytes32",
						"name": "_password",
						"type": "bytes32"
					}
				],
				"name": "revealMove",
				"outputs": [],
				"stateMutability": "nonpayable",
				"type": "function"
			},
			{
				"inputs": [],
				"name": "revealTimeout",
				"outputs": [
					{
						"internalType": "uint256",
						"name": "",
						"type": "uint256"
					}
				],
				"stateMutability": "view",
				"type": "function"
			},
			{
				"inputs": [
					{
						"internalType": "bytes32",
						"name": "_moveHash",
						"type": "bytes32"
					}
				],
				"name": "submitMove",
				"outputs": [],
				"stateMutability": "nonpayable",
				"type": "function"
			}
	
    
]

# Chargement du contrat
contract = w3.eth.contract(address=contract_address, abi=contract_abi)


# Endpoint pour enregistrer un joueur
@app.post("/register/{player_address}")
async def register(player_address: str, bet_amount: int):
    try:
        # Convertir l'adresse en format checksum pour Ethereum
        player_address = w3.toChecksumAddress(player_address)

        # Enregistrer le joueur en appelant la fonction register du contrat Ethereum
        tx_hash = contract.functions.register().transact({'from': player_address, 'value': bet_amount})

        # Attendre la confirmation de la transaction
        w3.eth.waitForTransactionReceipt(tx_hash)

        return {"message": "Player registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint pour soumettre un mouvement
@app.post("/submit-move")
async def submit_move(move: MoveSubmission):
    try:
        # Convertir l'adresse en format checksum pour Ethereum
        player_address = w3.toChecksumAddress(move.player)

        # Soumettre le mouvement au contrat Ethereum
        tx_hash = contract.functions.submitMove(move.moveHash).transact({'from': player_address})

        # Attendre la confirmation de la transaction
        w3.eth.waitForTransactionReceipt(tx_hash)

        return {"message": "Move submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Point d'entrée pour exécuter le serveur
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
