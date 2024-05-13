from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from web3 import Web3

app = FastAPI()

# Configuration de Web3 pour se connecter à votre nœud Ethereum
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  # Mettez l'URL de votre nœud Ethereum

# Modèle Pydantic pour la soumission de mouvement
class MoveSubmission(BaseModel):
    player: str
    moveHash: str

# Adresse du contrat et ABI (Application Binary Interface)
contract_address = "YOUR_CONTRACT_ADDRESS"
contract_abi = [
    {
        "constant": False,
        "inputs": [
            {"name": "_moveHash", "type": "bytes32"}
        ],
        "name": "submitMove",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    # Ajoutez d'autres fonctions du contrat ici...
]

# Chargement du contrat
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Endpoint pour enregistrer un joueur
@app.post("/register")
async def register():
    # Votre logique pour enregistrer un joueur et envoyer la transaction Ethereum
    pass

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
