from character import *
from util import *

def main():
    raw_roles = start()
    players = setup_game_objects(raw_roles)
    day_count = 1

    print("\n" + "-"*30)
    print("Role (Quản trò xem):")
    for name, char_name in raw_roles.items():
        print(f"{name}: {char_name}")
    print("="*30 + "\nGAME BẮT ĐẦU!")

    while True:
        print(f"\n>>> ĐÊM THỨ {day_count}")
        for p in players.values():
            p.reset_status()

        died_tonight = []
        wolf_target_name = None

        # 0. CUPID (Chỉ đêm 1)
        if day_count == 1:
            cupids = [p for p in players.values() if p.role == 'Cupid']
            if cupids:
                print(f"[Quản trò] Gọi Cupid dậy.")
                p1 = get_target("Người thứ 1 được ghép đôi: ", players)
                p2 = get_target("Người thứ 2 được ghép đôi: ", players)
                if p1 and p2 and p1 != p2:
                    cupids[0].link(players[p1], players[p2])
                    print(f"-> Đã ghép đôi {p1} và {p2}.")

        # 1. BẢO VỆ
        protectors = [p for p in players.values() if p.role == 'Protecter' and p.is_alive]
        if protectors:
            print(f"[Quản trò] Gọi Bảo vệ.")
            target = get_target("Bảo vệ ai? ", players)
            if target: players[target].is_protected = True

        # 2. SÓI
        wolves = [p for p in players.values() if p.role == 'Werewolf' and p.is_alive]
        if wolves:
            print(f"[Quản trò] Gọi Sói.")
            wolf_target_name = get_target("Sói cắn ai? ", players)
        
        # 3. PHÙ THỦY
        witches = [p for p in players.values() if p.role == 'Witch' and p.is_alive]
        if witches:
            witch = witches[0]
            print(f"[Quản trò] Gọi Phù thủy (Heal={witch.has_heal}, Psn={witch.has_poison}).")
            
            if wolf_target_name:
                print(f"-> {wolf_target_name} bị cắn.")
                if witch.has_heal:
                    if input("Cứu? (y/n): ").lower() == 'y':
                        witch.rescue(players[wolf_target_name])
                        wolf_target_name = None 
            
            if witch.has_poison:
                if input("Dùng độc? (y/n): ").lower() == 'y':
                    t = get_target("Đầu độc ai? ", players)
                    if t: 
                        witch.kill(players[t])
                        # Xử lý cái chết ngay lập tức cho thuốc độc
                        handle_death(t, players, died_tonight)

        # 4. TIÊN TRI
        seers = [p for p in players.values() if p.role == 'Seer' and p.is_alive]
        if seers:
            print(f"[Quản trò] Gọi Tiên tri.")
            t = get_target("Soi ai? ", players)
            if t: print(f"-> {t} là {seers[0].see(players[t])}")

        # --- TỔNG KẾT ĐÊM ---
        if wolf_target_name:
            target_obj = players[wolf_target_name]
            if target_obj.is_protected:
                print(f"(Debug) {wolf_target_name} được bảo vệ.")
            else:
                # Xử lý cái chết do Sói cắn
                handle_death(wolf_target_name, players, died_tonight)

        # --- BUỔI SÁNG ---
        print(f"\n>>> NGÀY THỨ {day_count}")
        if not died_tonight:
            print("Đêm qua bình yên.")
        else:
            print("Người chết đêm qua:", ", ".join(died_tonight))

        if check_win(players): break

        print("\nNgười còn sống:", ", ".join([f"{n}[{c.role}]" for n,c in players.items() if c.is_alive]))

        # VOTE
        print("\n[VOTE TREO CỔ]")
        voted_name = get_target("Ai bị treo cổ? ", players)
        
        if voted_name:
            # Xử lý cái chết do Vote
            handle_death(voted_name, players, []) # List rỗng vì ko cần track died_tonight nữa
        
        if check_win(players): break
        
        day_count += 1
    
    # End Game
    st = check_win(players)
    if st == 1: print("\n>>> PHE DÂN THẮNG!")
    elif st == 2: print("\n>>> PHE SÓI THẮNG!")

if __name__ == "__main__":
    main()