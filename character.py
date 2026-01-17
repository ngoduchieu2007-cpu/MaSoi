class General_Character:
    def __init__(self):
        self.is_alive = True
        self.is_protected = False
        self.role = None
        self.lover = None # Thêm thuộc tính người yêu (cho Cupid)

    def reset_status(self):
        self.is_protected = False

class Villager(General_Character):
    def __init__(self):
        super().__init__() 
        self.role = 'Villager'

class Werewolf(General_Character):
    def __init__(self):
        super().__init__()
        self.role = 'Werewolf'

class Witch(General_Character):
    def __init__(self):
        super().__init__()
        self.role = 'Witch'
        self.has_heal = True
        self.has_poison = True

    def kill(self, target: General_Character):
        if self.has_poison:
            target.is_alive = False
            self.has_poison = False
            return True
        return False
    
    def rescue(self, target: General_Character):
        if self.has_heal:
            target.is_alive = True
            self.has_heal = False
            return True
        return False

class Seer(General_Character):
    def __init__(self):
        super().__init__() 
        self.role = 'Seer'

    def see(self, target: General_Character):
        return "Là Sói (Bad)" if target.role == 'Werewolf' else "Người tốt (Good)"

class Protecter(General_Character):
    def __init__(self):
        super().__init__()
        self.role = 'Protecter'
    
    def protect(self, target: General_Character):
        target.is_protected = True

# --- NEW ROLES ---

class Hunter(General_Character):
    def __init__(self):
        super().__init__()
        self.role = 'Hunter'
        self.has_shot = False # Tránh bắn 2 lần nếu được hồi sinh (optional)

class Cupid(General_Character):
    def __init__(self):
        super().__init__()
        self.role = 'Cupid'
        self.has_linked = False # Cupid chỉ ghép đôi 1 lần đầu game

    def link(self, p1: General_Character, p2: General_Character):
        # Ghép đôi 2 chiều
        p1.lover = p2
        p2.lover = p1
        self.has_linked = True