import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from character import *
from util import *

# --- LOGIC XỬ LÝ CÁI CHẾT (Đã sửa lại để tương thích GUI) ---
def gui_handle_death(dead_name, players, app_log_func, dead_list=None):
    if dead_name not in players or not players[dead_name].is_alive:
        return

    target_obj = players[dead_name]
    target_obj.is_alive = False
    
    if dead_list is not None and dead_name not in dead_list:
        dead_list.append(dead_name)

    app_log_func(f"☠️ {dead_name} đã chết.")

    # 1. Logic Cupid (Người yêu chết theo)
    if target_obj.lover:
        lover_name = None
        for name, char in players.items():
            if char == target_obj.lover:
                lover_name = name
                break
        
        if lover_name and players[lover_name].is_alive:
            app_log_func(f"💔 {lover_name} chết theo tình yêu!")
            gui_handle_death(lover_name, players, app_log_func, dead_list)

    # 2. Logic Hunter (Thợ săn bắn)
    if target_obj.role == 'Hunter':
        # Trong GUI, ta hiện popup để quản trò nhập tên người bị bắn
        shoot_target = simpledialog.askstring("Thợ săn", f"{dead_name} là Hunter! Bắn ai? (Để trống nếu không bắn)")
        if shoot_target and shoot_target in players and players[shoot_target].is_alive:
            app_log_func(f"🔫 Hunter {dead_name} đã bắn {shoot_target}!")
            gui_handle_death(shoot_target, players, app_log_func, dead_list)

# --- GIAO DIỆN CHÍNH ---
class WerewolfApp:
    def __init__(self, root, players):
        self.root = root
        self.root.title("Ma Sói Manager - Quản Trò")
        self.players = players
        self.day_count = 1
        self.died_tonight = []
        self.wolf_target = None
        
        # Chia layout: Bên trái (Danh sách), Bên phải (Hành động), Dưới (Log)
        self.frame_left = tk.Frame(root, width=200)
        self.frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.frame_right = tk.Frame(root)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 1. Danh sách người chơi
        tk.Label(self.frame_left, text="DANH SÁCH NGƯỜI CHƠI", font=("Arial", 12, "bold")).pack()
        self.player_list_frame = tk.Frame(self.frame_left)
        self.player_list_frame.pack(fill=tk.BOTH, expand=True)
        self.player_buttons = {} # Lưu các button để update màu
        self.refresh_player_list()

        # 2. Khu vực điều khiển (Action)
        tk.Label(self.frame_right, text="BẢNG ĐIỀU KHIỂN", font=("Arial", 12, "bold")).pack()
        
        # Các nút chức năng Đêm
        self.grp_night = tk.LabelFrame(self.frame_right, text="Hành Động Đêm")
        self.grp_night.pack(fill=tk.X, pady=5)
        
        tk.Button(self.grp_night, text="Bắt đầu Đêm (Reset Giáp)", command=self.action_start_night, bg="#ddd").pack(fill=tk.X, pady=2)
        tk.Button(self.grp_night, text="Cupid Ghép Đôi (Đêm 1)", command=self.action_cupid).pack(fill=tk.X, pady=2)
        tk.Button(self.grp_night, text="Bảo vệ (Protector)", command=self.action_protect).pack(fill=tk.X, pady=2)
        tk.Button(self.grp_night, text="Sói Cắn (Werewolf)", command=self.action_wolf, bg="#ffcccc").pack(fill=tk.X, pady=2)
        tk.Button(self.grp_night, text="Phù Thủy (Witch)", command=self.action_witch).pack(fill=tk.X, pady=2)
        tk.Button(self.grp_night, text="Tiên Tri (Seer)", command=self.action_seer).pack(fill=tk.X, pady=2)
        tk.Button(self.grp_night, text="Xử lý Sói Cắn (Kết thúc Đêm)", command=self.action_resolve_night, bg="#ff9999").pack(fill=tk.X, pady=2)

        # Các nút chức năng Ngày
        self.grp_day = tk.LabelFrame(self.frame_right, text="Hành Động Ngày")
        self.grp_day.pack(fill=tk.X, pady=5)
        tk.Button(self.grp_day, text="Treo Cổ (Vote)", command=self.action_vote, bg="#ffcc99").pack(fill=tk.X, pady=2)
        tk.Button(self.grp_day, text="Kiểm tra Thắng/Thua", command=self.check_game_end).pack(fill=tk.X, pady=2)

        # 3. Log
        self.log_area = scrolledtext.ScrolledText(root, height=10, state='disabled')
        self.log_area.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        self.log(f"Game bắt đầu! Số lượng người chơi: {len(self.players)}")

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def refresh_player_list(self):
        # Xóa list cũ
        for widget in self.player_list_frame.winfo_children():
            widget.destroy()
        
        # Vẽ lại list
        for name, char in self.players.items():
            status_color = "green" if char.is_alive else "gray"
            role_text = f"{name} [{char.role}]"
            if not char.is_alive: role_text += " (DEAD)"
            if char.is_protected: role_text += " [🛡️]"
            if char.lover: 
                lover_name = [n for n, c in self.players.items() if c == char.lover][0]
                role_text += f" [❤️ {lover_name}]"

            lbl = tk.Label(self.player_list_frame, text=role_text, fg=status_color, font=("Arial", 10))
            lbl.pack(anchor="w")

    # --- ACTION HANDLERS ---
    
    def get_alive_player_input(self, title, prompt):
        name = simpledialog.askstring(title, prompt)
        if not name: return None
        if name not in self.players:
            messagebox.showerror("Lỗi", "Tên không tồn tại!")
            return None
        return name

    def action_start_night(self):
        self.died_tonight = []
        self.wolf_target = None
        for p in self.players.values():
            p.reset_status()
        self.refresh_player_list()
        self.log(f"\n>>> BẮT ĐẦU ĐÊM THỨ {self.day_count}")
        messagebox.showinfo("Thông báo", "Đã reset trạng thái bảo vệ. Hãy gọi các chức năng theo thứ tự.")

    def action_cupid(self):
        if self.day_count > 1:
            messagebox.showwarning("Lỗi", "Cupid chỉ ghép đôi đêm 1!")
            return
        p1 = self.get_alive_player_input("Cupid", "Người thứ 1:")
        p2 = self.get_alive_player_input("Cupid", "Người thứ 2:")
        if p1 and p2:
            self.players[p1].role_class = 'Cupid_Target' # Hacky check
            # Tìm object cupid để gọi hàm link (nếu cần đúng logic class)
            cupids = [p for p in self.players.values() if p.role == 'Cupid']
            if cupids:
                cupids[0].link(self.players[p1], self.players[p2])
                self.log(f"💘 Cupid đã ghép đôi {p1} và {p2}")
                self.refresh_player_list()

    def action_protect(self):
        target = self.get_alive_player_input("Bảo vệ", "Bảo vệ muốn bảo vệ ai?")
        if target:
            self.players[target].is_protected = True
            self.log(f"🛡️ {target} đã được bảo vệ.")
            self.refresh_player_list()

    def action_wolf(self):
        target = self.get_alive_player_input("Sói", "Sói thống nhất cắn ai?")
        if target:
            self.wolf_target = target
            self.log(f"🐺 Sói chọn cắn {target}.")

    def action_witch(self):
        # Logic hiển thị thông tin witch
        witches = [p for p in self.players.values() if p.role == 'Witch' and p.is_alive]
        if not witches:
            messagebox.showinfo("Witch", "Không có phù thủy hoặc đã chết.")
            return
        
        witch = witches[0]
        msg = f"Tình trạng thuốc: Cứu={witch.has_heal}, Độc={witch.has_poison}.\n"
        if self.wolf_target:
            msg += f"Đêm nay {self.wolf_target} bị cắn."
        else:
            msg += "Đêm nay chưa ai bị cắn."
        
        choice = messagebox.askyesno("Phù thủy", msg + "\nBạn có muốn dùng thuốc (Cứu/Giết) không?")
        if choice:
            # Simple logic: Hỏi cứu trước
            if self.wolf_target and witch.has_heal:
                if messagebox.askyesno("Cứu", f"Cứu {self.wolf_target}?"):
                    witch.rescue(self.players[self.wolf_target])
                    self.log(f"✨ Phù thủy dùng bình cứu {self.wolf_target}.")
                    self.wolf_target = None # Sói cắn thất bại
            
            # Hỏi giết
            if witch.has_poison:
                if messagebox.askyesno("Độc", "Dùng bình độc không?"):
                    target = self.get_alive_player_input("Độc", "Đầu độc ai?")
                    if target:
                        witch.kill(self.players[target])
                        gui_handle_death(target, self.players, self.log, self.died_tonight)

    def action_seer(self):
        target = self.get_alive_player_input("Tiên tri", "Muốn soi ai?")
        if target:
            seers = [p for p in self.players.values() if p.role == 'Seer']
            if seers:
                res = seers[0].see(self.players[target])
                messagebox.showinfo("Kết quả soi", f"{target} là: {res}")
                self.log(f"👁️ Tiên tri đã soi {target}.")

    def action_resolve_night(self):
        if self.wolf_target:
            target_obj = self.players[self.wolf_target]
            if target_obj.is_protected:
                self.log(f"🛡️ {self.wolf_target} bị sói cắn nhưng ĐƯỢC BẢO VỆ.")
            else:
                gui_handle_death(self.wolf_target, self.players, self.log, self.died_tonight)
        
        self.day_count += 1
        self.refresh_player_list()
        self.log(f"--- TRỜI SÁNG (Ngày {self.day_count}) ---")
        if not self.died_tonight:
            self.log("Đêm qua bình yên.")
        self.check_game_end()

    def action_vote(self):
        target = self.get_alive_player_input("Treo cổ", "Ai bị cả làng vote chết?")
        if target:
            gui_handle_death(target, self.players, self.log, [])
            self.refresh_player_list()
            self.check_game_end()

    def check_game_end(self):
        st = check_win(self.players)
        if st == 1:
            messagebox.showinfo("GAME OVER", "PHE DÂN THẮNG!")
        elif st == 2:
            messagebox.showinfo("GAME OVER", "PHE SÓI THẮNG!")

# --- MAIN ---
if __name__ == "__main__":
    # 1. Setup bằng terminal (giữ nguyên logic cũ cho nhanh)
    try:
        raw_roles = start() # Hàm từ util.py
        players = setup_game_objects(raw_roles) # Hàm từ util.py

        # 2. Khởi tạo GUI
        root = tk.Tk()
        app = WerewolfApp(root, players)
        root.mainloop()
    except Exception as e:
        print(f"Có lỗi xảy ra hoặc bạn đã huỷ setup: {e}")