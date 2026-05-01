"""Game-specific state overrides for 333."""

from game_executables import GameExecutables


class GameStateOverride(GameExecutables):
    """
    Override or extend universal state.py functions for 333.
    e.g: Custom book properties to reset, special symbol assignments, etc.
    """

    def reset_book(self):
        """Reset game specific properties."""
        super().reset_book()
