class General_Character:
    def __init__(self):
        self.is_alive = True
        self.is_protected = False # Trạng thái được bảo vệ trong đêm
        self.role = None

    def reset_status(self):
        """Reset các trạng thái tạm thời khi bắt đầu đêm mới"""
        self.is_protected = False

class Villager(General_Character):
    def __init__(self):
        super().__init__() 
        self.role = 'Villager'

class Werewolf(General_Character):
    def __init__(self):
        super().__init__()
        self.role = 'Werewolf'
    
    # Sói thống nhất vote giết, hành động thực hiện ở main xử lý logic chung
    
class Witch(General_Character):
    def __init__(self):
        super().__init__()
        self.role = 'Witch'
        self.has_heal = True  # Bình cứu
        self.has_poison = True # Bình độc

    def kill(self, target: General_Character):
        if self.has_poison:
            target.is_alive = False
            self.has_poison = False
            return True
        return False
    
    def rescue(self, target: General_Character):
        if self.has_heal:
            target.is_alive = True # Sửa lỗi: Cứu target chứ không phải self
            self.has_heal = False
            return True
        return False

class Seer(General_Character):
    def __init__(self):
        super().__init__() 
        self.role = 'Seer'

    def see(self, target: General_Character):
        # Trả về chuỗi để in ra màn hình dễ hơn
        return "Là Sói (Bad)" if target.role == 'Werewolf' else "Người tốt (Good)"

class Protecter(General_Character):
    def __init__(self):
        super().__init__()
        self.role = 'Protecter'
    
    def protect(self, target: General_Character):
        target.is_protected = True