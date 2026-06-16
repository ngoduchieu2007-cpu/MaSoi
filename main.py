# Ban choi tren terminal.
# Chay: python main.py

from util import setup_roles, build_players, ask_name
from engine import GameEngine, ONGOING, VILLAGE_WIN


class ConsoleIO:
    def log(self, msg):
        print(msg)

    def ask_hunter(self, name):
        ans = input(f"{name} la Tho san, ban ai? (Enter de bo qua): ").strip()
        return ans or None


def night_phase(engine):
    players = engine.players
    engine.start_night()
    print(f"\n>>> ĐÊM {engine.day}")

    # cupid chi dem 1
    cupids = engine.alive("Cupid")
    if engine.day == 1 and cupids:
        print("[Quản trò] Gọi Cupid.")
        p1 = ask_name("Ghép đôi - người 1: ", players)
        p2 = ask_name("Ghép đôi - người 2: ", players)
        if p1 and p2 and p1 != p2:
            cupids[0].link(players[p1], players[p2])
            print(f"Đã ghép đôi {p1} và {p2}.")

    # bao ve
    if engine.alive("Protector"):
        print("[Quản trò] Gọi Bảo vệ.")
        t = ask_name("Bảo vệ ai? ", players)
        if t:
            players[t].is_protected = True

    # soi
    if engine.alive("Werewolf"):
        print("[Quản trò] Gọi Sói.")
        engine.wolf_target = ask_name("Sói cắn ai? ", players)

    # phu thuy
    witches = engine.alive("Witch")
    if witches:
        witch = witches[0]
        print(f"[Quản trò] Gọi Phù thuỷ (cứu={witch.has_heal}, độc={witch.has_poison}).")
        if engine.wolf_target:
            print(f"-> Đêm nay {engine.wolf_target} bị cắn.")
            if witch.has_heal and input("Cứu? (y/n): ").lower() == "y":
                if witch.use_heal():
                    engine.wolf_target = None
        if witch.has_poison and input("Dùng độc? (y/n): ").lower() == "y":
            t = ask_name("Đầu độc ai? ", players)
            if t and witch.use_poison():
                engine.resolve_death(t)

    # tien tri
    seers = engine.alive("Seer")
    if seers:
        print("[Quản trò] Gọi Tiên tri.")
        t = ask_name("Soi ai? ", players)
        if t:
            print(f"-> {t} là: {seers[0].see(players[t])}")

    engine.resolve_night()


def day_phase(engine):
    print(f"\n>>> NGÀY {engine.day}")
    alive = [f"{n}[{c.role}]" for n, c in engine.players.items() if c.is_alive]
    print("Người còn sống:", ", ".join(alive))

    t = ask_name("Ai bị treo cổ? ", engine.players)
    if t:
        engine.resolve_death(t)


def main():
    players = build_players(setup_roles())
    engine = GameEngine(players, ConsoleIO())

    print("\n--- VAI (chỉ quản trò xem) ---")
    for name, c in players.items():
        print(f"{name}: {c.role}")
    print("=== GAME BẮT ĐẦU ===")

    while True:
        night_phase(engine)
        if engine.check_win() != ONGOING:
            break
        day_phase(engine)
        if engine.check_win() != ONGOING:
            break
        engine.day += 1

    if engine.check_win() == VILLAGE_WIN:
        print("\n>>> PHE DÂN THẮNG!")
    else:
        print("\n>>> PHE SÓI THẮNG!")


if __name__ == "__main__":
    main()