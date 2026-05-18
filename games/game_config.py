"""Game-specific configuration file for 3 the Hardway"""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "3_the_hardway"
        self.provider_number = 0
        self.working_name = "3 the Hardway"
        self.wincap = 5000.0
        self.win_type = "lines"
        self.rtp = 0.9700
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 5
        self.num_rows = [3] * self.num_reels

        # === SYMBOLS ===
        self.symbols = ["10", "J", "Q", "K", "A", "BB", "W", "S"]

        # === PAYTABLE ===
        self.paytable = {
            (5, "W"): 50, (4, "W"): 20, (3, "W"): 10,
            (5, "BB"): 120, (4, "BB"): 60, (3, "BB"): 25,
            (5, "A"): 50,  (4, "A"): 25,  (3, "A"): 12,
            (5, "K"): 40,  (4, "K"): 20,  (3, "K"): 10,
            (5, "Q"): 30,  (4, "Q"): 15,  (3, "Q"): 8,
            (5, "J"): 25,  (4, "J"): 12,  (3, "J"): 5,
            (5, "10"): 20, (4, "10"): 10, (3, "10"): 5,
        }

        # === 20 PAYLINES ===
        self.paylines = {
            1: [0,0,0,0,0],   2: [1,1,1,1,1],   3: [2,2,2,2,2],
            4: [0,1,2,1,0],   5: [2,1,0,1,2],
            6: [0,0,1,2,2],   7: [2,2,1,0,0],
            8: [1,0,1,2,1],   9: [1,2,1,0,1],
            10: [0,1,1,1,2], 11: [2,1,1,1,0],
            12: [0,1,0,1,2], 13: [2,1,2,1,0],
            14: [1,1,0,1,1], 15: [1,1,2,1,1],
            16: [0,2,1,0,2], 17: [2,0,1,2,0],
            18: [0,0,2,0,0], 19: [2,2,0,2,2],
            20: [1,0,0,0,1],
        }

        self.include_padding = True
        self.special_symbols = {"wild": ["W"], "scatter": ["S"], "multiplier": ["W"]}

        # Free Spins Triggers
        self.freespin_triggers = {
            self.basegame_type: {3: 10, 4: 15, 5: 20},
            self.freegame_type: {2: 3, 3: 5, 4: 8, 5: 12},
        }

        self.anticipation_triggers = {
            self.basegame_type: 2,
            self.freegame_type: 1,
        }

        # Reel Loading
        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv", "WCAP": "FRWCAP.csv"}
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))

        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]

        self.padding_symbol_values = {"W": {"multiplier": {2: 100, 3: 50, 4: 50, 5: 50}}}

                # === GAME CONDITIONS ===
        freegame_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR0": 1},
            },
            "scatter_triggers": {3: 50, 4: 20, 5: 5},
            "mult_values": {
                self.basegame_type: {1: 1},
                self.freegame_type: {2: 60, 3: 80, 4: 50, 5: 20, 10: 15, 20: 10, 50: 5},
            },
            "force_wincap": False,
            "force_freegame": True,
        }

        basegame_condition = {
            "reel_weights": {self.basegame_type: {"BR0": 1}},
            "mult_values": {self.basegame_type: {1: 1}},
            "force_wincap": False,
            "force_freegame": False,
        }

        wincap_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR0": 1, "WCAP": 5},
            },
            "mult_values": {
                self.basegame_type: {1: 1},
                self.freegame_type: {2: 10, 3: 20, 4: 50, 5: 60, 10: 100, 20: 90, 50: 50},
            },
            "scatter_triggers": {4: 1, 5: 2},
            "force_wincap": True,
            "force_freegame": True,
        }

        self.distributions = Distribution({
            self.basegame_type: basegame_condition,
            self.freegame_type: freegame_condition,
            "wincap": wincap_condition,
        })

        # Bet Modes
        mode_maxwins = {"base": 5000, "bonus": 5000}
        self.bet_modes = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp,
                max_win=mode_maxwins["base"],
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(criteria="wincap", quota=0.001, win_criteria=mode_maxwins["base"], conditions=wincap_condition),
                    Distribution(criteria="freegame", quota=0.1, conditions=freegame_condition),
                    Distribution(criteria="basegame", quota=0.899, conditions=basegame_condition),
                ],
            ),
        ]