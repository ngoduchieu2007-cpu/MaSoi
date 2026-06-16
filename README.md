# Ma Sói (Werewolf)

Game Ma Sói viết bằng Python, có bản chơi trên terminal và bản giao diện (tkinter).
Dùng cho 1 người làm **quản trò** điều khiển ván chơi.

## Cách chạy

Cần Python 3.8 trở lên.

```bash
python main.py        # bản terminal
python gui_game.py    # bản giao diện
```

## Cách chơi

Game chia làm các vòng **Đêm** và **Ngày**, lặp lại đến khi một phe thắng.

**Đêm** — quản trò gọi từng vai dậy lần lượt:
- **Cupid** (chỉ đêm đầu): ghép đôi 2 người. Sau này 1 người chết thì người kia chết theo.
- **Bảo vệ**: chọn 1 người để chặn đòn cắn của Sói đêm đó.
- **Sói**: chọn 1 người để cắn.
- **Phù thuỷ**: có 1 bình cứu và 1 bình độc (mỗi bình dùng 1 lần). Có thể cứu người bị Sói cắn, hoặc đầu độc 1 người.
- **Tiên tri**: soi 1 người để biết người đó là Sói hay người tốt.

**Ngày** — cả làng thảo luận rồi vote treo cổ 1 người.

Vai đặc biệt:
- **Thợ săn**: khi chết (bị cắn, bị độc hay bị treo cổ) được bắn kèm 1 người.

## Điều kiện thắng

- **Phe Dân thắng**: khi không còn con Sói nào.
- **Phe Sói thắng**: khi số Sói nhiều hơn hoặc bằng số người còn lại.

## Các file

| File | Nội dung |
|------|----------|
| `character.py` | Các vai trong game |
| `engine.py` | Luật chơi |
| `util.py` | Phần setup (chọn vai, nhập tên) |
| `main.py` | Bản terminal |
| `gui_game.py` | Bản giao diện tkinter |