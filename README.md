# Projet de Serveur de Jeu - Jeu d'Axelrod

Ce projet implémente un contrat intelligent permettant de jouer au jeu du dilemme du prisonnier, également connu sous le nom de jeu d’Axelrod, en utilisant Solidity pour la blockchain Ethereum. Le jeu est conçu pour être sécurisé, transparent et facilement accessible via une API REST.

## Installation

Pour que le projet fonctionne correctement, assurez-vous d'avoir installé les modules Python suivants :

- `fastapi` : Un framework web pour construire des APIs REST avec Python rapidement.
- `pydantic` : Une bibliothèque pour la validation des données dans Python.
- `web3` : Une bibliothèque Python pour se connecter à une blockchain Ethereum.
- `sympy` : Une bibliothèque pour la manipulation de symboles mathématiques.

Vous pouvez installer ces modules en utilisant la commande suivante :

```bash
pip install fastapi pydantic web3 sympy
```

## Phase 1 - Mise en Place du Contrat Intelligent

La phase 1 consiste à déployer le contrat intelligent pour jouer au jeu d'Axelrod sur la blockchain Ethereum. Les principales fonctionnalités du contrat incluent :

- Enregistrement des joueurs avec une mise minimale.
- Engagement des joueurs en choisissant un coup et en fournissant un mot de passe.
- Révélation des coups et vérification de leur validité.
- Détermination du gagnant et distribution des récompenses.

Le contrat intelligent est écrit en Solidity et peut être déployé sur la blockchain Ethereum.

## Phase 2 - Compétition d’Axelrod

Dans la phase 2, les participants développeront un code Python interagissant avec l'API REST pour jouer 200 fois au jeu d'Axelrod. Ils implémenteront une stratégie de jeu basée sur les concepts décrits dans le livre d'Axelrod.

Les "battles" entre les différents groupes détermineront quelle stratégie est la plus efficace dans le jeu d'Axelrod.

## Interaction avec le Jeu via une API REST

L'interaction avec le jeu se fait à travers une API REST. Les endpoints implémentent les fonctionnalités disponibles ainsi que les variables d'état du jeu. Les participants doivent convenir des URLs correspondantes pour la phase 2.

## Déploiement du Contrat

Pour déployer le contrat, suivez les étapes ci-dessous :

1. Initialiser yarn dans le dossier hardhat:
   ```bash
   yarn
   ```
2. Lancer le nœud local :
   ```bash
   npx hardhat node
   ```
3. Dans un nouveau terminal, compiler le contrat :
   ```bash
   npx hardhat compile
   ```
4. Déployer le contrat :
   ```bash
   yarn hardhat ignition deploy ./ignition/modules/AxelrodGame_contrat.js --network localhost
   ```
5. Récupérer l'adresse du contrat et la modifier dans le script `API_script.py`.

6. Lancer l'API :
   ```bash
   uvicorn API_script:app --reload
   ```
   ## Auteur

Ce projet a été développé par DEGOUEY Corentin, SOLDAN Maxens, RENAND Baptiste, BERCIER Thomas et WHILLEM Arno.

