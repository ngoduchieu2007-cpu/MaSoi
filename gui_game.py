# Ban giao dien tkinter. Dung chung engine voi main.py.
# Chay: python gui_game.py

import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

from util import setup_roles, build_players
from engine import GameEngine, VILLAGE_WIN, WOLF_WIN


class TkIO:
    def __init__(self):
        self.log_func = None

    def log(self, msg):
        if self.log_func:
            self.log_func(msg)

    def ask_hunter(self, name):
        return simpledialog.askstring(
            "Thợ săn", f"{name} là Thợ săn! Bắn ai? (để trống nếu không bắn)")


class WerewolfApp:
    def __init__(self, root, players):
        self.root = root
        self.root.title("Ma Sói Manager - Quản Trò")

        self.io = TkIO()
        self.engine = GameEngine(players, self.io)

        self.frame_left = tk.Frame(root, width=220)
        self.frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.frame_right = tk.Frame(root)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.frame_left, text="DANH SÁCH NGƯỜI CHƠI",
                 font=("Arial", 12, "bold")).pack()
        self.player_list_frame = tk.Frame(self.frame_left)
        self.player_list_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.frame_right, text="BẢNG ĐIỀU KHIỂN",
                 font=("Arial", 12, "bold")).pack()

        grp_night = tk.LabelFrame(self.frame_right, text="Hành Động Đêm")
        grp_night.pack(fill=tk.X, pady=5)
        tk.Button(grp_night, text="Bắt đầu Đêm (Reset Giáp)",
                  command=self.action_start_night, bg="#dddddd").pack(fill=tk.X, pady=2)
        tk.Button(grp_night, text="Cupid Ghép Đôi (Đêm 1)",
                  command=self.action_cupid).pack(fill=tk.X, pady=2)
        tk.Button(grp_night, text="Bảo vệ (Protector)",
                  command=self.action_protect).pack(fill=tk.X, pady=2)
        tk.Button(grp_night, text="Sói Cắn (Werewolf)",
                  command=self.action_wolf, bg="#ffcccc").pack(fill=tk.X, pady=2)
        tk.Button(grp_night, text="Phù Thuỷ (Witch)",
                  command=self.action_witch).pack(fill=tk.X, pady=2)
        tk.Button(grp_night, text="Tiên Tri (Seer)",
                  command=self.action_seer).pack(fill=tk.X, pady=2)
        tk.Button(grp_night, text="Kết thúc Đêm (Xử lý Sói)",
                  command=self.action_resolve_night, bg="#ff9999").pack(fill=tk.X, pady=2)

        grp_day = tk.LabelFrame(self.frame_right, text="Hành Động Ngày")
        grp_day.pack(fill=tk.X, pady=5)
        tk.Button(grp_day, text="Treo Cổ (Vote)",
                  command=self.action_vote, bg="#ffcc99").pack(fill=tk.X, pady=2)
        tk.Button(grp_day, text="Kiểm tra Thắng/Thua",
                  command=self.check_game_end).pack(fill=tk.X, pady=2)

        self.log_area = scrolledtext.ScrolledText(root, height=10, state="disabled")
        self.log_area.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.io.log_func = self.log
        self.refresh_player_list()
        self.log(f"Game bắt đầu! Số người chơi: {len(self.engine.players)}")

    def log(self, msg):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")

    def refresh_player_list(self):
        for w in self.player_list_frame.winfo_children():
            w.destroy()
        for name, char in self.engine.players.items():
            text = f"{name} [{char.role}]"
            if not char.is_alive:
                text += " (DEAD)"
            if char.is_protected:
                text += " [bảo vệ]"
            if char.lover:
                text += f" [yêu {self.engine.name_of(char.lover)}]"
            color = "green" if char.is_alive else "gray"
            tk.Label(self.player_list_frame, text=text, fg=color,
                     font=("Arial", 10)).pack(anchor="w")

    def ask_alive(self, title, prompt):
        name = simpledialog.askstring(title, prompt)
        if not name:
            return None
        if name not in self.engine.players:
            messagebox.showerror("Lỗi", "Tên không tồn tại!")
            return None
        if not self.engine.players[name].is_alive:
            messagebox.showerror("Lỗi", f"{name} đã chết!")
            return None
        return name

    def action_start_night(self):
        self.engine.start_night()
        self.refresh_player_list()
        self.log(f"\n>>> BẮT ĐẦU ĐÊM {self.engine.day}")
        messagebox.showinfo("Thông báo", "Đã reset giáp. Gọi các vai theo thứ tự.")

    def action_cupid(self):
        if self.engine.day > 1:
            messagebox.showwarning("Lỗi", "Cupid chỉ ghép đôi đêm 1!")
            return
        cupids = self.engine.alive("Cupid")
        if not cupids:
            messagebox.showinfo("Cupid", "Không có Cupid còn sống.")
            return
        p1 = self.ask_alive("Cupid", "Người thứ 1:")
        p2 = self.ask_alive("Cupid", "Người thứ 2:")
        if p1 and p2 and p1 != p2:
            cupids[0].link(self.engine.players[p1], self.engine.players[p2])
            self.log(f"Cupid ghép đôi {p1} và {p2}.")
            self.refresh_player_list()

    def action_protect(self):
        t = self.ask_alive("Bảo vệ", "Bảo vệ ai?")
        if t:
            self.engine.players[t].is_protected = True
            self.log(f"{t} đã được bảo vệ.")
            self.refresh_player_list()

    def action_wolf(self):
        t = self.ask_alive("Sói", "Sói thống nhất cắn ai?")
        if t:
            self.engine.wolf_target = t
            self.log(f"Sói chọn cắn {t}.")

    def action_witch(self):
        witches = self.engine.alive("Witch")
        if not witches:
            messagebox.showinfo("Phù thuỷ", "Không có Phù thuỷ còn sống.")
            return
        witch = witches[0]

        if self.engine.wolf_target and witch.has_heal:
            if messagebox.askyesno("Cứu", f"{self.engine.wolf_target} bị cắn. Cứu?"):
                if witch.use_heal():
                    self.log(f"Phù thuỷ cứu {self.engine.wolf_target}.")
                    self.engine.wolf_target = None

        if witch.has_poison and messagebox.askyesno("Độc", "Dùng bình độc?"):
            t = self.ask_alive("Độc", "Đầu độc ai?")
            if t and witch.use_poison():
                self.engine.resolve_death(t)
        self.refresh_player_list()
        self.check_game_end()

    def action_seer(self):
        t = self.ask_alive("Tiên tri", "Soi ai?")
        if t:
            seers = self.engine.alive("Seer")
            if seers:
                res = seers[0].see(self.engine.players[t])
                messagebox.showinfo("Kết quả soi", f"{t} là: {res}")
                self.log(f"Tiên tri đã soi {t}.")

    def action_resolve_night(self):
        self.engine.resolve_night()
        self.refresh_player_list()
        self.log(f"--- TRỜI SÁNG (Ngày {self.engine.day}) ---")
        self.engine.day += 1
        self.check_game_end()

    def action_vote(self):
        t = self.ask_alive("Treo cổ", "Ai bị cả làng vote chết?")
        if t:
            self.engine.died_tonight = []
            self.engine.resolve_death(t)
            self.refresh_player_list()
            self.check_game_end()

    def check_game_end(self):
        st = self.engine.check_win()
        if st == VILLAGE_WIN:
            messagebox.showinfo("GAME OVER", "PHE DÂN THẮNG!")
        elif st == WOLF_WIN:
            messagebox.showinfo("GAME OVER", "PHE SÓI THẮNG!")


if __name__ == "__main__":
    try:
        players = build_players(setup_roles())
        root = tk.Tk()
        WerewolfApp(root, players)
        root.mainloop()
    except Exception as e:
        print(f"Có lỗi xảy ra hoặc bạn đã huỷ setup: {e}")