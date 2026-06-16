# Xu ly luat choi, tach roi khoi giao dien.
# main.py (terminal) va gui_game.py (tkinter) dung chung file nay.
# io la doi tuong co 2 ham: io.log(msg) va io.ask_hunter(name).

ONGOING = 0
VILLAGE_WIN = 1
WOLF_WIN = 2


class GameEngine:
    def __init__(self, players, io):
        self.players = players
        self.io = io
        self.day = 1
        self.wolf_target = None
        self.died_tonight = []

    def alive(self, role=None):
        return [c for c in self.players.values()
                if c.is_alive and (role is None or c.role == role)]

    def name_of(self, char):
        for name, c in self.players.items():
            if c is char:
                return name
        return None

    def resolve_death(self, name):
        char = self.players.get(name)
        if char is None or not char.is_alive:
            return

        char.is_alive = False
        if name not in self.died_tonight:
            self.died_tonight.append(name)
        self.io.log(f"{name} đã chết.")

        # nguoi yeu chet theo
        if char.lover and char.lover.is_alive:
            lover_name = self.name_of(char.lover)
            self.io.log(f"{lover_name} chết theo người yêu.")
            self.resolve_death(lover_name)

        # tho san ban kem 1 phat
        if char.role == "Hunter":
            shot = self.io.ask_hunter(name)
            if shot and shot in self.players and self.players[shot].is_alive:
                self.io.log(f"Thợ săn {name} bắn {shot}.")
                self.resolve_death(shot)

    def start_night(self):
        self.wolf_target = None
        self.died_tonight = []
        for c in self.players.values():
            c.reset_night()

    def resolve_night(self):
        target = self.wolf_target
        if target:
            if self.players[target].is_protected:
                self.io.log(f"{target} bị cắn nhưng được bảo vệ.")
            else:
                self.resolve_death(target)

        if not self.died_tonight:
            self.io.log("Đêm qua bình yên.")

    def check_win(self):
        wolves = len(self.alive("Werewolf"))
        others = len(self.alive()) - wolves
        if wolves == 0:
            return VILLAGE_WIN
        if wolves >= others:
            return WOLF_WIN
        return ONGOING