from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from sympy import false
from web3 import Web3
from config_api import contract_abi, contract_address


app = FastAPI()

# Configuration de Web3 pour se connecter à votre nœud Ethereum
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  # Mettez l'URL de votre nœud Ethereum


# Modèle Pydantic pour la soumission de mouvement
class MoveSubmission(BaseModel):
    player: str
    moveHash: str

# Chargement du contrat
contract = w3.eth.contract(address=contract_address, abi=contract_abi)


# Endpoint pour enregistrer un joueur
@app.get("/register/")
async def register(player_address: str = Query(..., title="Player Address", description="The address of the player"),
                   bet_amount: int = Query(..., title="Bet Amount", description="The amount of the bet in wei")):
    try:
    
        # Enregistrer le joueur en appelant la fonction register du contrat Ethereum
        contract.functions.register().transact({'from': player_address, 'value': bet_amount})

        return {"message": "Player registered successfully"}
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Définir les endpoints de votre API
@app.get("/avoir_movehash/")
async def avoir_movehash(password: str = Query(...)):
    # Appeler la fonction avoir_movehash de votre contrat Solidity
    try:
        result_bytes32 = contract.functions.avoir_movehash(password).call()
        # Convertir bytes32 en hexadécimal
        result_hex = bytes(result_bytes32, 'utf-8')
        return {"moveHash": result_hex}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/submit_move/")
async def submit_move(player_address: str = Query(...), move_hash: str = Query(...)):
    try:
        move_hash_bytes32 = bytes.fromhex(move_hash)
        
        tx = contract.functions.submitMove(move_hash_bytes32).transact({'from': player_address})
        return {"message": "Move submitted successfully", "transaction": tx.hex(),"Hahce":move_hash_bytes32.hex()}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




@app.get("/reveal_move/")
async def reveal_move(player_address: str = Query(...), password: str = Query(...)):
    try:
        tx = contract.functions.revealMove(password).transact({'from': player_address})
        return {"message": "Move revealed successfully"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Définir les endpoints de votre API
@app.get("/both_revealed/")
async def both_revealed():
    # Appeler la fonction bothRevealed du contrat Solidity
    try:
        result = contract.functions.bothRevealed().call()
        return {"bothRevealed": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Définir les endpoints de votre API
@app.get("/both_played/")
async def both_revealed():
    # Appeler la fonction bothRevealed du contrat Solidity
    try:
        result = contract.functions.bothPlayed().call()
        return {"bothPlayed": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Définir les endpoints de votre API
@app.get("/get_outcome/")
async def get_outcome():
    # Appeler la fonction bothRevealed du contrat Solidity
    try:
        result = contract.functions.getOutcome().call()
        return{"Jeu terminé "}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_contrat_balance/")
async def get_balance():
   
    try:
        result = contract.functions.getContractBalance().call()
        return {"Balance:",result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/who_am_i/")
async def who_am_i(player_address: str = Query(...)):
    try:
        # Appelez la fonction whoAmI du contrat en utilisant call() pour lire la valeur
        result = contract.functions.whoAmI().call({'from': player_address})
        return {"playerId": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Point d'entrée pour exécuter le serveur

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
