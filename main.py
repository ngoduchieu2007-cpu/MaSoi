from character import *
from util import *

def main():
    # 1. Setup
    raw_roles = start()
    players = setup_game_objects(raw_roles)
    day_count = 1

    print("\n" + "-"*30)
    print("\nRole của các người chơi:\n")
    for name, char_name in raw_roles.items():
        print(name,':', char_name)

    print("\n" + "="*30)
    print("GAME BẮT ĐẦU!")
    print("="*30)

    while True:
        # --- ĐÊM ---
        print(f"\n>>> ĐÊM THỨ {day_count}")
        
        # Reset trạng thái bảo vệ đầu đêm
        for p in players.values():
            p.reset_status()

        # Danh sách người chết tạm thời trong đêm (để xử lý logic bảo vệ/cứu)
        died_tonight = []
        wolf_target_name = None

        # 1. Bảo vệ gọi (Protector)
        protectors = [p for p in players.values() if p.role == 'Protecter' and p.is_alive]
        if protectors:
            print(f"[Quản trò] Gọi Bảo vệ dậy.")
            target_name = get_target("Bảo vệ ai? ", players)
            if target_name:
                players[target_name].is_protected = True

        # 2. Sói gọi (Werewolf)
        wolves = [p for p in players.values() if p.role == 'Werewolf' and p.is_alive]
        if wolves:
            print(f"[Quản trò] Gọi Sói dậy.")
            wolf_target_name = get_target("Sói thống nhất cắn ai? ", players)
        
        # 3. Phù thủy (Witch)
        witches = [p for p in players.values() if p.role == 'Witch' and p.is_alive]
        if witches:
            witch = witches[0] # Giả sử 1 phù thủy
            print(f"[Quản trò] Gọi Phù thủy dậy.")
            print(f"Status: Heal={witch.has_heal}, Poison={witch.has_poison}")
            
            # Thông báo người bị cắn
            if wolf_target_name:
                print(f"-> Đêm nay {wolf_target_name} bị cắn.")
                if witch.has_heal:
                    choice = input("Dùng bình cứu không? (y/n): ")
                    if choice.lower() == 'y':
                        # Nếu cứu, xóa mục tiêu của sói (coi như không chết)
                        witch.rescue(players[wolf_target_name]) # Trừ bình
                        wolf_target_name = None 
            
            # Hỏi dùng độc
            if witch.has_poison:
                choice = input("Dùng bình độc không? (y/n): ")
                if choice.lower() == 'y':
                    poison_target = get_target("Đầu độc ai? ", players)
                    if poison_target:
                        witch.kill(players[poison_target])
                        died_tonight.append(poison_target)

        # 4. Tiên tri (Seer)
        seers = [p for p in players.values() if p.role == 'Seer' and p.is_alive]
        if seers:
            print(f"[Quản trò] Gọi Tiên tri dậy.")
            check_name = get_target("Soi ai? ", players)
            if check_name:
                result = seers[0].see(players[check_name])
                print(f"-> Kết quả: {check_name} là {result}")

        # --- XỬ LÝ KẾT QUẢ ĐÊM ---
        # Kiểm tra mục tiêu của sói có chết không (Do bảo vệ)
        if wolf_target_name:
            target_obj = players[wolf_target_name]
            if target_obj.is_protected:
                print(f"(Debug) {wolf_target_name} được bảo vệ, không chết.")
            else:
                target_obj.is_alive = False
                died_tonight.append(wolf_target_name)

        # --- BUỔI SÁNG ---
        print(f"\n>>> NGÀY THỨ {day_count}")
        
        # Công bố người chết
        if not died_tonight:
            print("Đêm qua là một đêm bình yên. Không ai chết.")
        else:
            print("Đêm qua, những người sau đã chết:", ", ".join(died_tonight))

        # Kiểm tra thắng thua sau đêm
        status = check_win(players)
        if status == 1:
            print("PHE DÂN THẮNG!"); break
        elif status == 2:
            print("PHE SÓI THẮNG!"); break

        # Hiển thị người còn sống
        print("\nDanh sách người còn sống:")
        for name, char in players.items():
            if char.is_alive:
                print(f"- {name} [{char.role}]") # Bỏ [char.role] nếu muốn giấu role

        # Vote treo cổ
        print("\n[Thảo luận và Vote]")
        voted_name = get_target("Ai bị vote chết? (nhập 'skip' nếu hoà): ", players)
        
        if voted_name:
            players[voted_name].is_alive = False
            print(f"-> {voted_name} đã bị treo cổ.")
        
        # Kiểm tra thắng thua sau vote
        status = check_win(players)
        if status == 1:
            print("PHE DÂN THẮNG!"); break
        elif status == 2:
            print("PHE SÓI THẮNG!"); break

        day_count += 1

if __name__ == "__main__":
    main()