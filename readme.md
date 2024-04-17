
# Big Two ML AI

Experimenting with using machine learning to create an AI to play Big Two


## Features

### Game logic
- [x] For a given a hand, find all possible playable combinations
- [x] For a given hand and last played cards, find all possible playable combinations
- [ ] Start a game with the player with the 3♦ (and ensure they use that card when they start)
- [ ] Implement basic turn-based play loop
- [ ] Declare win state

### Machine learning
- [ ] Decide which package to use (PyTorch/Tensorflow/other)
- [ ] Figure out best way to pass game state to model
    - one input per card in deck, with values of:
        - 0: unknown where card is
        - 1: card in own hand
        - 2: card played
- [ ] Figure out best way to calculate reward
    - use hand size?
    - give points for win?
    - give points based on final rank?
- [ ] Figure out how to get the model to interact with the game
- [ ] Build model
    - how many layers?
    - what algorithms?
- [ ] Train model (reinforcement learning: Q-learning)

### 'Levels' of AI (?)
- [ ] Save checkpoints during training and store weights so various 'difficulties' can be chosen

### Visualisation/implementation
- [ ] Build a visual representation of the game
- [ ] Build a single-player version of the game where the other players are controlled by AI
- [ ] Display suggested plays from the fully-trained AI model