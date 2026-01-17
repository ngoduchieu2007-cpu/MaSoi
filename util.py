from character import *
import random

# CẬP NHẬT MAPPING
class_map = {
    'Villager': Villager,
    'Werewolf': Werewolf,
    'Witch': Witch,
    'Seer': Seer,
    'Protecter': Protecter,
    'Hunter': Hunter,
    'Cupid': Cupid
}

def start() -> dict: 
    print('=== SETUP GAME ===')
    player_nums = int(input('Tổng số người chơi: '))
    print('Chọn Role:\n0: Villager\n1: Werewolf\n2: Witch\n3: Seer\n4: Protecter\n5: Hunter\n6: Cupid')
    role_ids = list(map(int, input('Nhập danh sách ID role (VD: 0 1 5 6): ').split()))
    
    # CẬP NHẬT ID
    role_map_name = {
        0: 'Villager', 1: 'Werewolf', 2: 'Witch', 3: 'Seer', 
        4: 'Protecter', 5: 'Hunter', 6: 'Cupid'
    }

    all_roles = []
    for r_id in role_ids:
        char_name = role_map_name[r_id]
        count = int(input(f'- Số lượng {char_name}: '))
        all_roles.extend([char_name] * count)
    
    if len(all_roles) != player_nums:
        print(f"Lỗi: Tổng role ({len(all_roles)}) không khớp số người chơi ({player_nums}).")
        assert len(all_roles) == player_nums
    
    players = []
    for i in range(player_nums):
        players.append(input(f'Tên người chơi {i+1}: '))
    
    random.shuffle(all_roles)
    player_role_dict = dict(zip(players, all_roles))
    return player_role_dict

def setup_game_objects(player_role_dict):
    players_instances = {}
    for name, role_name in player_role_dict.items():
        players_instances[name] = class_map[role_name]()
    return players_instances

def check_win(players_instances):
    wolves = 0
    villagers = 0
    
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
    while True:
        name = input(prompt)
        if name == 'skip': return None
        if name in players_instances:
            return name
        print("Tên không tồn tại. Nhập lại hoặc 'skip'.")

# Hàm hỗ trợ xử lý cái chết dây chuyền (Hunter bắn, Lover chết theo)
def handle_death(dead_name, players, dead_list):
    """
    Xử lý logic khi một người chết:
    1. Kiểm tra Lover -> Lover chết theo.
    2. Kiểm tra Hunter -> Hunter bắn thêm người.
    """
    if dead_name not in players or not players[dead_name].is_alive:
        return # Người này đã chết hoặc không tồn tại

    # Xác nhận chết
    target_obj = players[dead_name]
    target_obj.is_alive = False
    if dead_name not in dead_list:
        dead_list.append(dead_name)

    print(f"-> {dead_name} đã chết.")

    # 1. Logic Cupid (Nếu có người yêu, người yêu chết theo)
    if target_obj.lover:
        # Tìm tên người yêu (phải duyệt dict vì lover lưu object)
        lover_name = None
        for name, char in players.items():
            if char == target_obj.lover:
                lover_name = name
                break
        
        if lover_name and players[lover_name].is_alive:
            print(f"💔 VÌ TÌNH YÊU: {lover_name} chết theo {dead_name}!")
            handle_death(lover_name, players, dead_list) # Đệ quy cái chết

    # 2. Logic Hunter (Nếu là Hunter, cho phép bắn)
    if target_obj.role == 'Hunter':
        print(f"🔫 KÍCH HOẠT THỢ SĂN: {dead_name} là Thợ săn!")
        shoot_target = get_target(f"{dead_name} muốn bắn ai kéo theo? ", players)
        if shoot_target and players[shoot_target].is_alive:
            print(f"-> Thợ săn đã nổ súng vào {shoot_target}!")
            handle_death(shoot_target, players, dead_list) # Đệ quy cái chết
