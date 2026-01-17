from character import *
import random

# Mapping string sang class
class_map = {
    'Villager': Villager,
    'Werewolf': Werewolf,
    'Witch': Witch,
    'Seer': Seer,
    'Protecter': Protecter
}

def start() -> dict: 
    print('=== SETUP GAME ===')
    player_nums = int(input('Tổng số người chơi: '))
    print('Chọn Role:\n0: Villager\n1: Werewolf\n2: Witch\n3: Seer\n4: Protecter')
    role_ids = list(map(int, input('Nhập danh sách ID role có trong game (VD: 0 1 2): ').split()))
    
    role_map_name = {0: 'Villager', 1: 'Werewolf', 2: 'Witch', 3: 'Seer', 4: 'Protecter'}

    all_roles = []
    for r_id in role_ids:
        char_name = role_map_name[r_id]
        count = int(input(f'- Số lượng {char_name}: '))
        all_roles.extend([char_name] * count)
    
    if len(all_roles) != player_nums:
        print(f"Lỗi: Tổng role ({len(all_roles)}) không khớp số người chơi ({player_nums}). Nhập lại phần role còn thiếu/thừa.")
        # Trong thực tế nên loop để nhập lại, ở đây assert để dừng
        assert len(all_roles) == player_nums
    
    players = []
    for i in range(player_nums):
        players.append(input(f'Tên người chơi {i+1}: '))
    
    random.shuffle(all_roles)
    player_role_dict = dict(zip(players, all_roles))
    return player_role_dict

def setup_game_objects(player_role_dict):
    """Chuyển dict {Tên: 'Role'} thành dict {Tên: Object}"""
    players_instances = {}
    for name, role_name in player_role_dict.items():
        players_instances[name] = class_map[role_name]()
    return players_instances

def check_win(players_instances):
    """
    Return: 
    0: Chưa ai thắng
    1: Phe Dân thắng (Hết sói)
    2: Phe Sói thắng (Số sói >= Số dân)
    """
    wolves = 0
    villagers = 0 # Bao gồm cả dân và các role có chức năng khác
    
    for name, char in players_instances.items():
        if char.is_alive:
            if char.role == 'Werewolf':
                wolves += 1
            else:
                villagers += 1
    
    if wolves == 0:
        return 1
    if wolves >= villagers:
        return 2
    return 0

def get_target(prompt, players_instances):
    """Hàm hỗ trợ nhập tên cho chuẩn"""
    while True:
        name = input(prompt)
        if name == 'skip': return None # Bỏ qua hành động
        if name in players_instances:
            return name
        print("Tên không tồn tại. Nhập lại hoặc 'skip' để bỏ qua.")