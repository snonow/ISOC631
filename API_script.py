from fastapi import FastAPI, HTTPException, Query
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

###############################################################
#    modifié avec l'adresse du contrat une fois compilé
contract_address = "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0"
###############################################################




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
@app.get("/register")
async def register(player_address: str = Query(..., title="Player Address", description="The address of the player"),
                   bet_amount: int = Query(..., title="Bet Amount", description="The amount of the bet in wei")):
    try:
    


        # Vérifier si le montant de la mise est suffisant
        if bet_amount < contract.functions.betMin().call():
            raise ValueError("Bet amount is less than minimum bet required")

        # Enregistrer le joueur en appelant la fonction register du contrat Ethereum
        tx_hash = contract.functions.register().transact({'from': player_address, 'value': bet_amount})

        # Attendre la confirmation de la transaction
        w3.eth.waitForTransactionReceipt(tx_hash)

        return {"message": "Player registered successfully"}
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Point d'entrée pour exécuter le serveur
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
