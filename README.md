**README**

# Projet de Serveur de Jeu - Jeu d'Axelrod

Ce projet implémente un contrat intelligent permettant de jouer au jeu du dilemme du prisonnier, également connu sous le nom de jeu d’Axelrod, en utilisant Solidity pour la blockchain Ethereum. Le jeu est conçu pour être sécurisé, transparent et facilement accessible via une API REST.

## Installation

Pour que le projet fonctionne correctement, assurez-vous d'avoir installé les modules Python suivants :

- `fastapi` : Un framework web pour construire des APIs REST avec Python rapidement.
- `pydantic` : Une bibliothèque pour la validation des données dans Python.
- `web3` : Une bibliothèque Python pour se connecter à une blockchain Ethereum.
- `sympy`

Vous pouvez installer ces modules en utilisant `pip` avec la commande suivante :

```
pip install fastapi pydantic web3 sympy
```

## Phase 1 - Mise en Place du Contrat Intelligent

La phase 1 consiste à mettre en place le contrat intelligent pour jouer au jeu d'Axelrod sur la blockchain Ethereum. Voici les principales fonctionnalités du contrat :

- Enregistrement des joueurs avec une mise minimale.
- Engagement des joueurs en choisissant un coup et en fournissant un mot de passe.
- Révélation des coups et vérification de leur validité.
- Détermination du gagnant et distribution des récompenses.

Le contrat intelligent est écrit en Solidity et peut être déployé sur la blockchain Ethereum.

## Phase 2 - Compétition d’Axelrod

Dans la phase 2, les participants développeront un code Python interagissant avec l'API REST pour jouer 200 fois le jeu d'Axelrod. Ils implémenteront une stratégie de jeu basée sur les concepts décrits dans le livre d'Axelrod.

Les "battles" entre les différents groupes permettront de déterminer quelle stratégie est la plus efficace dans le jeu d'Axelrod.

## Interaction avec le Jeu via une API REST

L'interaction avec le jeu se fait à travers une API REST. Les endpoints implémentent les fonctionnalités disponibles ainsi que les variables d'état du jeu. Les participants doivent convenir des URLs correspondantes pour la phase 2.

## Auteur

Ce projet a été développé par DEGOUEY Corentin - SOLDAN Maxens - RENAND Baptiste - BERCIER Thomas - WHILLEM Arno.


## Deployer le  contrat 
Dans l'invité de commande :<br> 
initialiser yarn : yarn <br>
lancer le noeud local: npx hardhat node <br> 
compile le contrat :npx hardhat compile <br> 
deployer le contrat : yarn hardhat ignition deploy ./ignition/modules/AxelrodGame_contrat.js --network localhost

recupérer l'adresse du contrat et la modifié dans le script API_script.py
lancer l'api : uvicorn API_script:app --reload
