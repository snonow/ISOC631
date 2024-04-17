pragma solidity ^0.8.24;

contract AxelrodGame {
    // Variables d'état
    uint public constant BET_MIN = 1 finney; // Mise minimale
    uint public constant REVEAL_TIMEOUT = 600; // 10 minutes en secondes
    address public player1;
    address public player2;
    bytes32 public hashedMovePlayer1;
    bytes32 public hashedMovePlayer2;
    uint public betAmountPlayer1;
    uint public betAmountPlayer2;
    uint public revealDeadline;
    uint public movePlayer1;
    uint public movePlayer2;

    // Modificateurs
    modifier onlyRegisteredPlayer() {
        require(msg.sender == player1 || msg.sender == player2, "You are not a registered player.");
        _;
    }

    modifier onlyBeforeRevealDeadline() {
        require(block.timestamp < revealDeadline, "Reveal deadline has passed.");
        _;
    }

    // Fonction d'enregistrement des joueurs
    function register() external payable {
        require(msg.value >= BET_MIN, "Insufficient bet amount.");
        if (player1 == address(0)) {
            player1 = msg.sender;
            betAmountPlayer1 = msg.value;
        } else if (player2 == address(0)) {
            require(msg.value > betAmountPlayer1, "Bet amount must be greater than player1's bet.");
            player2 = msg.sender;
            betAmountPlayer2 = msg.value;
            revealDeadline = block.timestamp + REVEAL_TIMEOUT;
        }
    }

    // Fonction de placement du coup (hashé)
    function commitMove(bytes32 _hashedMove) external onlyRegisteredPlayer {
        require(block.timestamp < revealDeadline, "Reveal deadline has passed.");
        if (msg.sender == player1) {
            hashedMovePlayer1 = _hashedMove;
        } else {
            hashedMovePlayer2 = _hashedMove;
        }
    }

    // Fonction de révélation du coup
    function revealMove(uint _move, string memory _password) external onlyRegisteredPlayer onlyBeforeRevealDeadline {
        bytes32 hashedMove;
        if (msg.sender == player1) {
            hashedMove = keccak256(abi.encodePacked(_move, _password));
            require(hashedMove == hashedMovePlayer1, "Invalid move or password.");
            movePlayer1 = _move;
        } else {
            hashedMove = keccak256(abi.encodePacked(_move, _password));
            require(hashedMove == hashedMovePlayer2, "Invalid move or password.");
            movePlayer2 = _move;
        }
        if (movePlayer1 != 0 && movePlayer2 != 0) {
            determineWinner();
        }
    }

    // Fonction de détermination du gagnant et distribution des récompenses
    function determineWinner() private {
        if (movePlayer1 == movePlayer2) {
            payable(player1).transfer(betAmountPlayer1);
            payable(player2).transfer(betAmountPlayer2);
        } else if (movePlayer1 == 1 && movePlayer2 == 2) {
            payable(player2).transfer(betAmountPlayer1 + betAmountPlayer2);
        } else if (movePlayer1 == 2 && movePlayer2 == 1) {
            payable(player1).transfer(betAmountPlayer1 + betAmountPlayer2);
        } else if (movePlayer1 == 1 && movePlayer2 == 0) {
            payable(player1).transfer(betAmountPlayer1 + betAmountPlayer2);
        } else if (movePlayer1 == 0 && movePlayer2 == 1) {
            payable(player2).transfer(betAmountPlayer1 + betAmountPlayer2);
        } else if (movePlayer1 == 2 && movePlayer2 == 0) {
            payable(player2).transfer(betAmountPlayer1 + betAmountPlayer2);
        } else if (movePlayer1 == 0 && movePlayer2 == 2) {
            payable(player1).transfer(betAmountPlayer1 + betAmountPlayer2);
        }
        // Réinitialisation de l'état du jeu
        resetGame();
    }

    // Fonction de réinitialisation du jeu
    function resetGame() private {
        player1 = address(0);
        player2 = address(0);
        hashedMovePlayer1 = 0;
        hashedMovePlayer2 = 0;
        betAmountPlayer1 = 0;
        betAmountPlayer2 = 0;
        revealDeadline = 0;
        movePlayer1 = 0;
        movePlayer2 = 0;
    }
}
