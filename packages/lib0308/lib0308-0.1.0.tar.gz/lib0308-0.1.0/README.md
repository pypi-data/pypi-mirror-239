# lib0308 Library
A simple Python library to play various card games, including High-Low, and B
lackjack.
## Installation
Install the package using pip:
`pip install lib0308`
## Usage
# Add players, deal cards, etc.
```
### High-Low
```python
from lib0308.high_low import HighLow
game = HighLow()
game.start_game()
# Draw cards, compare cards, etc.
```
### Blackjack
```python
from lib0308.blackjack import Blackjack
game = Blackjack()
game.start_game()
# Add players, deal cards, hit, stand, etc.
```
## License
This project is licensed under the MIT License - see the LICENSE file for det
ails.