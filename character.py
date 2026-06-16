# Các vai trong game. Mỗi class chỉ giữ trạng thái + hành động riêng,
# còn luật chơi để bên engine.py xử lý.

class Character:
    role = "Character"

    def __init__(self):
        self.is_alive = True
        self.is_protected = False
        self.lover = None   # người được Cupid ghép đôi

    def reset_night(self):
        self.is_protected = False


class Villager(Character):
    role = "Villager"


class Werewolf(Character):
    role = "Werewolf"


class Seer(Character):
    role = "Seer"

    def see(self, target):
        if target.role == "Werewolf":
            return "Sói (xấu)"
        return "Người tốt"


class Protector(Character):
    role = "Protector"

    def protect(self, target):
        target.is_protected = True


class Witch(Character):
    role = "Witch"

    def __init__(self):
        super().__init__()
        self.has_heal = True
        self.has_poison = True

    def use_heal(self):
        if self.has_heal:
            self.has_heal = False
            return True
        return False

    def use_poison(self):
        if self.has_poison:
            self.has_poison = False
            return True
        return False


class Hunter(Character):
    role = "Hunter"


class Cupid(Character):
    role = "Cupid"

    def link(self, p1, p2):
        p1.lover = p2
        p2.lover = p1