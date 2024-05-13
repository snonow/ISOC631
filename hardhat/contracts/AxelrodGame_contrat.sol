// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract AxelrodGame_contrat {
    address private player1;
    address private player2;
    uint256 private constant FINNEY = 1e15; // 1 finney en wei
    uint256 private constant betMin = FINNEY; // Mise minimale = 1 finney     
    uint256 private constant revealTimeout=600;
    uint256 private initialBet;

    enum Move {Cooperate, Defect}
    struct Player {
        bytes32 moveHash;
        bool revealed;
        uint256 bet;
    }

    mapping(address => Player) private players;

    event GameStarted(address player1, address player2, uint256 bet);
    event MoveSubmitted(address player);
    event GameEnded(address winner, uint256 winnings);
    constructor() payable {}

    function register() external payable {
        require(player1 == address(0) || player2 == address(0), "Game is full");
        require(msg.value >= betMin, "Insufficient bet");
        
        if (player1 == address(0)) {
            player1 = msg.sender;
            initialBet = msg.value;
        } else {
            player2 = msg.sender;
            initialBet = players[player1].bet;
            require(msg.value >= initialBet, "Bet must be equal or higher than initial player's bet");
        }

        players[msg.sender].bet = msg.value;
        if (player1 != address(0) && player2 != address(0)) {
            emit GameStarted(player1, player2, initialBet);
        }
    }

    function submitMove(bytes32 _moveHash) external {
        require(players[msg.sender].moveHash == bytes32(0), "Move already submitted");
        players[msg.sender].moveHash = _moveHash;
        emit MoveSubmitted(msg.sender);
    }

    function revealMove(string memory _password)  external {
        Player storage player = players[msg.sender];
        require(player.moveHash != bytes32(0), "Move not submitted");
        require(!player.revealed, "Move already revealed");
        require(keccak256(abi.encodePacked(_password)) == player.moveHash, "Invalid password");
        player.revealed = true;
        
    }

    function getOutcome() external {
        
        if (players[player1].revealed && players[player2].revealed) {
           
            Player storage player1Data = players[player1];
            Player storage player2Data = players[player2];

            bytes32 player1MoveHash = player1Data.moveHash;
            bytes32 player2MoveHash = player2Data.moveHash;

            require(player1MoveHash != bytes32(0) && player2MoveHash != bytes32(0), "Moves not submitted");

            Move player1Move = Move(uint8(uint256(keccak256(abi.encodePacked(player1MoveHash, address(this)))) % 2));
            Move player2Move = Move(uint8(uint256(keccak256(abi.encodePacked(player2MoveHash, address(this)))) % 2));

            if (player1Move == Move.Cooperate && player2Move == Move.Cooperate) {
                payOut(player1, player2, initialBet, initialBet);
            } else if (player1Move == Move.Cooperate && player2Move == Move.Defect) {
                payOut(player2, player1, initialBet * 2, 0);
            } else if (player1Move == Move.Defect && player2Move == Move.Cooperate) {
                payOut(player1, player2,  initialBet * 2,0);
            } else {
                payOut(address(0), address(0), 0, 0); // Both defect, no winner
            }

        }
    }

    function payOut(address _winner, address _loser, uint256 _winnerAmount, uint256 _loserAmount) private {
        if (_winner != address(0)) {
            payable(_winner).transfer(_winnerAmount);
            emit GameEnded(_winner, _winnerAmount);
        }
        if (_loser != address(0)) {
            payable(_loser).transfer(_loserAmount);
            emit GameEnded(_loser, _loserAmount);
        }
        resetGame();
    }

    function resetGame() private {
        player1 = address(0);
        player2 = address(0);
        initialBet = 0;
        delete players[player1];
        delete players[player2];
    }

    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }
    function whoAmI() public view returns (uint8) {
        if (msg.sender == player1) {
            return 1;
        } else if (msg.sender == player2) {
            return 2;
        } else {
            return 0;
        }
    }

    function bothPlayed() public view returns (bool) {
        return (players[player1].moveHash != bytes32(0) && players[player2].moveHash != bytes32(0));
    }

    function bothRevealed() public view returns (bool) {
        return (players[player1].revealed && players[player2].revealed);
    }

    function revealTimeLeft() public view returns (uint256) {
        if (players[player1].moveHash == bytes32(0) || players[player2].moveHash == bytes32(0)) {
            return revealTimeout; // Le timer n'a pas encore démarré
        } else {
            uint256 timeElapsed = block.timestamp - revealTimeout; // Temps écoulé depuis le début de la révélation
            if (timeElapsed < 0) {
                return revealTimeout + timeElapsed; // Temps restant avant la fin de la révélation
            } else {
                return 0; // La phase de révélation est terminée
            }
        }
    }

   function avoir_movehash(string memory _password) external pure returns (bytes32) {
  
    
        // Calculer le hachage SHA256 de la chaîne concaténée
        bytes32 moveHash = keccak256(abi.encodePacked(_password));

        return moveHash;
    }
}
