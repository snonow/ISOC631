from flask import Flask, request, jsonify

app = Flask(__name__)

# Variables d'état du jeu (à remplir avec les valeurs appropriées)
contract_balance = 0
game_state = {
    "player1_id": None,
    "player2_id": None,
    "bet_min": 100,  # Exemple de montant minimal du pari
    "reveal_timeout": 600  # Exemple de délai de révélation en secondes
}

# Endpoint d'enregistrement des joueurs
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    player_id = data.get('playerId')
    bet_amount = data.get('betAmount')
    
    # Vérifier si le montant du pari est valide
    if bet_amount < game_state['bet_min']:
        return jsonify({'error': 'Montant du pari inférieur au minimum requis'}), 400
    
    # Enregistrer le joueur et mettre à jour l'état du jeu
    if game_state['player1_id'] is None:
        game_state['player1_id'] = player_id
    elif game_state['player2_id'] is None:
        game_state['player2_id'] = player_id
    else:
        return jsonify({'error': 'Deux joueurs déjà enregistrés'}), 400
    
    return jsonify({'message': 'Joueur enregistré avec succès'}), 200

# Endpoint pour placer un pari
@app.route('/bet', methods=['POST'])
def bet():
    # Implémentez la logique pour placer un pari
    pass

# Endpoint pour révéler le coup
@app.route('/reveal', methods=['POST'])
def reveal():
    # Implémentez la logique pour révéler le coup
    pass

# Endpoint pour obtenir l'état du jeu
@app.route('/game-state', methods=['GET'])
def get_game_state():
    return jsonify(game_state), 200

# Endpoint pour obtenir le solde du contrat
@app.route('/contract-balance', methods=['GET'])
def get_contract_balance():
    global contract_balance
    return jsonify({'contractBalance': contract_balance}), 200

if __name__ == '__main__':
    app.run(debug=True)
