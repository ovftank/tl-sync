# tlsync

[![ClaudeAI](https://img.shields.io/badge/ClaudeAI-ovftank%2Ftl--sync-orange.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAAD40lEQVRIibWVXWgcVRTHf3dmdpPs7Gc2u8lqLDEV0tCWpqLW+IVo8hJao8T6kLZQkVYUQlpBROij9EEURAQfbBEUBQtGRUEUK12tLa3bJvEz3UrT1m6CSZM0+72zmbk+7Hazu8lKH8yBwwznnvv/33Pv+RAXXnlGIlkWAchb+Fb7V0vRrqxYlLf4rfavlqJdQ9by+H9EKVCtolKib7yHwMA+FHsdhYNIhKri2NC1qn9Jy+xKxUKVk7u7F+fWB3He/XAJxLmlm+Zdw6hOT03QcnsFgShTpCQROQGAu7sXIQRIieZvxsobWMlFhJQ4Orpo2fsyaoNjxX6kRBGAQCKK7Krbh771IYSikDp/kuyVKLbGII6N9yKQqLqb/EwMLJP69k6Cg0M03LUJmz9UEUUBk5sRLK/pm7cReHo/Lc+9iur0MP/lh0jA+/hTgILq8mJMXUbzBggMDiFUjeT4KXJXL67ylLLqkaUkceY4iUiY+rYOQkOvodQ7SI2dwh64Db2rG83tIz87RWD3MKrDhfHPNeZGjq7+jlIiogf7V+SpBPRN9+HvfxZFd5EaP43e9QBG7DKax4eVy2BrCmHlsky/c4j87FTNNBXRA0/ULATF4aKxfy/6lm6EEMhizQghAFj45hMyF8apa12PLbQOe0sryUiYZCRcTrCjROB+ZDtKgxMrk8RKp7CyacxUnPq2Dry9OxGqWhmpaSIUBStvYMQmyV2JkoyEyc/GSm1FKy/1/PTf1LV3onmbEMFWFJsdNBuKzVboLWVi5Q0yE6NkJsYwYpOY6QRWKoHMG5TQJWjlzSQTHSMTHasAsgVvx9e3G0wTKZTS9chsBmlk8Tz2JFpjsHCF5hJzn75H8ucTIAq4NXuRorvw9u7EdX8P6V/Pkp2cQPM3F8AA1ekGCbHXD6C6PNS3bcB+x3qM6auFCOTNNxjqW8Hg2LwN/8B+pLnE/MgRtMYg7kd3EA9/Rd2dndhD6xCKwtLiPFYuw+wHbyKN3OoHXVEdioJv+x7Sv59l6o2DmKk43r5Brn/8NqruxlyYYf6L91F9ATITo1jJRZr3HUJpcFDqQ//Z7MwlYodfZO7YuwjVRmDPS8S//5zsX79hb23HjC+Q+SNCevQknp4BFo9/Rur8j/gHnl8Gr9XsqrVp1zC5S3+y+O0xgCLBDZCSuZEjWKkEnp4BEj99zfWP3loVQyvLapZzUSIQpM79QOpcGClNbE0hVN2FmVgopGk6wczRw6hOT2E6mvmq/QACTVRkUeV/6sx3RTcw4zdI/3IaY2qy0GOA/LVL5IvehREsq8pFIi6+0LumM1OrPPVaEKzx0P8XFf4brY7C27AAAAAASUVORK5CYII=)](https://claude.ai/new?q=Read+https://raw.githubusercontent.com/ovftank/tl-sync/main/.github/INSTRUCTION.md%2C+I+want+to+ask+questions+about+it.)

mở terminal ở thư mục code: `ctrl+l` → gõ `cmd`

## cài đặt

### 1. cài uv

```cmd
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

tắt cmd bật lại

### 2. cài dependencies

```cmd
uv sync
```

### 3. tắt firewall

```cmd
netsh advfirewall firewall add rule name="Allow All Traffic" dir=out action=allow
netsh advfirewall firewall add rule name="Allow All Traffic" dir=in action=allow
```

---

## cấu hình bot

điền vào `app.py`:

```python
TOKEN = ""        # dòng 22
API_ID = 0        # dòng 23
API_HASH = ""     # dòng 24
```

### lấy token từ botfather

1. mở [@botfather](https://t.me/BotFather)
2. `/start` - xem danh sách lệnh
3. `/newbot` - tạo bot mới
4. **tên bot**: điền tên hiển thị (ví dụ: `VÃI CẢ BÌU`)
5. **username**: điền tên user, **phải kết thúc bằng `bot`** (ví dụ: `vaicabiu_bot`)
   - nếu bị trùng, botfather báo và phải chọn tên khác

---

### lấy api id + hash

1. vào [https://my.telegram.org](https://my.telegram.org)
2. login sđt
3. **api development tools**
4. tạo app, copy **api id**, **api hash**

---

## lấy chat id

1. thêm bot vào group/channel
2. gõ `gid`
3. bot sẽ trả về:
   - chat id
   - type (PRIVATE, GROUP, SUPERGROUP, CHANNEL, GIGAGROUP)
   - topic id (nếu reply vào topic)

---

## chạy

```bash
uv run app.py
```

truy cập web để cấu hình

---

## technical

xem [TECHNICAL.MD](TECHNICAL.MD) để hiểu về telethon event object

---

tele: [@ovftank](https://t.me/ovftank)
