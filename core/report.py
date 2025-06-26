class FarmingReport:
    def __init__(self):
        self.attempt = 0
        self.completed_attempt = 0
        self.gold = 0
        self.exp = 0

    def update_attempt(self):
        self.attempt += 1

    def update_completed_attempt(self):
        self.completed_attempt += 1

    def update_dungeon_reward(self, gold: int, exp: int):
        self.gold += gold
        self.exp += exp

        print(f"Farming Report: Attempt {self.attempt}, {gold:,} golds, {exp:,} exp")
        print(f"Farming Report: Current total reward are {self.gold:,} golds, {self.exp:,} exp")

    def add_avg_reward(self):
        avg_gold = self.gold / self.completed_attempt
        self.gold += avg_gold

        avg_exp = self.exp / self.completed_attempt
        self.exp += avg_exp