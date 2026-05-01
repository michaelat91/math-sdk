"""Game configuration for 333 — define game identity, dimensions, symbols, paytable, reels, and bet modes."""

from src.config.config import Config
from src.config.distributions import Distribution
from src.config.config import BetMode


class GameConfig(Config):
    """Configuration class for 333."""

    def __init__(self):
        super().__init__()
        # ── Game Identity ──────────────────────────────────────────
        self.game_id = "333"
        self.provider_numer = 0
        self.working_name = "333"
        self.wincap = 5000          # TODO: set max win cap multiplier
        self.win_type = "lines"  # TODO: "lines", "ways", "cluster", "scatter"
        self.rtp = 0.97          # TODO: set target RTP
        self.construct_paths()

        # ── Game Dimensions ────────────────────────────────────────
        self.num_reels = 5                                  # TODO: set number of reels
        self.num_rows = [3] * self.num_reels                # TODO: set rows per reel

        # ── Symbols & Paytable ─────────────────────────────────────
        self.paytable = {
            "3": [0, 0, 50, 200, 1000],  # High value symbol
            "A": [0, 0, 25, 100, 500],
            "K": [0, 0, 20, 80, 400],
            "Q": [0, 0, 15, 60, 300],
            "J": [0, 0, 10, 40, 200],
            "10": [0, 0, 8, 30, 150],
            "9": [0, 0, 6, 20, 100],
            "8": [0, 0, 5, 15, 75],
            "7": [0, 0, 4, 10, 50],
            "6": [0, 0, 3, 8, 40],
            "5": [0, 0, 2, 6, 30],
            "4": [0, 0, 1, 4, 20],
            "2": [0, 0, 0.5, 2, 10],
            "1": [0, 0, 0.2, 1, 5],
        }

        self.include_padding = True
        self.special_symbols = {"wild": ["3"], "scatter": [], "multiplier": []}

        # ── Freespin / Feature Triggers ────────────────────────────
        self.freespin_triggers = {self.basegame_type: {}, self.freegame_type: {}}
        self.anticipation_triggers = {self.basegame_type: 0, self.freegame_type: 0}

        # ── Reels ──────────────────────────────────────────────────
        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv"}
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(str.join("/", [self.reels_path, f]))

        # ── Bet Modes ──────────────────────────────────────────────
        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.001,
                        win_criteria=self.wincap,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {},
                            "force_wincap": True,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="freegame",
                        quota=0.1,
                        conditions={
                            "reel_weights": {
                                self.basegame_type: {"BR0": 1},
                                self.freegame_type: {"FR0": 1},
                            },
                            "scatter_triggers": {},
                            "force_wincap": False,
                            "force_freegame": True,
                        },
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.4,
                        win_criteria=0.0,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.5,
                        conditions={
                            "reel_weights": {self.basegame_type: {"BR0": 1}},
                            "force_wincap": False,
                            "force_freegame": False,
                        },
                    ),
                ],
            ),
        ]
