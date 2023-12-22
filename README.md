# Sarsa Tic-Tac-Toe
This project details the implementation of a Sarsa-based training algorithm for learning to play Tic-Tac-Toe.

## Concept
1. Enable autonomous learning for the model to understand Tic-Tac-Toe gameplay.
2. Test the model by pitting it against a randomly playing AI.


## Award by action
- **-1** For executing a **prohibited move**.
- **0** For making a move that **does not result in a win**.
- **5** For making a **winning** move.

## Code structure
1. `sarsa.py`- Contains the implementation of the Sarsa algorithm.
2. `sarsa_morpion.py`- Holds the code specific to the Tic-Tac-Toe game.

## Conclusion
The model demonstrates effective performance, achieving wins or draws (in situations where winning is not possible).
