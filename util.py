# Setup game: chon vai, tao nguoi choi, nhap ten.

import random
from character import (Villager, Werewolf, Witch, Seer,
                       Protector, Hunter, Cupid)

class_map = {
    "Villager": Villager,
    "Werewolf": Werewolf,
    "Witch": Witch,
    "Seer": Seer,
    "Protector": Protector,
    "Hunter": Hunter,
    "Cupid": Cupid,
}

role_by_id = {
    0: "Villager", 1: "Werewolf", 2: "Witch", 3: "Seer",
    4: "Protector", 5: "Hunter", 6: "Cupid",
}


def setup_roles():
    print("=== SETUP GAME ===")
    n = int(input("Tổng số người chơi: "))

    print("Chọn Role:")
    for rid, rname in role_by_id.items():
        print(f"  {rid}: {rname}")
    ids = list(map(int, input("Nhập ID role (VD: 0 1 5 6): ").split()))

    roles = []
    for rid in ids:
        rname = role_by_id[rid]
        count = int(input(f"- Số lượng {rname}: "))
        roles.extend([rname] * count)

    assert len(roles) == n, f"Tổng vai ({len(roles)}) khác số người ({n})."

    names = [input(f"Tên người chơi {i + 1}: ") for i in range(n)]
    random.shuffle(roles)
    return dict(zip(names, roles))


def build_players(name_to_role):
    return {name: class_map[role]() for name, role in name_to_role.items()}


def ask_name(prompt, players):
    while True:
        name = input(prompt).strip()
        if name == "skip":
            return None
        if name in players:
            return name
        print("Tên không tồn tại. Nhập lại hoặc gõ 'skip'.")