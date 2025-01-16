import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import platform
import ctypes
import subprocess

# Biến toàn cục
app_process = None  # Biến lưu trữ tiến trình Flask

# Đường dẫn đến thư mục chứa main.py
directory_path = None

def start_flask_server():
    global app_process

    if app_process is None or app_process.poll() is not None:  # Nếu chưa có tiến trình hoặc tiến trình đã kết thúc
        if directory_path is None:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục chứa main.py trước!")
            return

        main_py_path = os.path.join(directory_path, "main.py")
        if not os.path.exists(main_py_path):
            messagebox.showerror("Lỗi", f"Không tìm thấy main.py trong thư mục {directory_path}")
            return
        try:
            # Chạy main.py bằng subprocess
            app_process = subprocess.Popen(
                [sys.executable, main_py_path],
                cwd=directory_path,  # Đặt thư mục làm việc là thư mục chứa main.py
                stdout=subprocess.PIPE,  # Ghi lại stdout
                stderr=subprocess.PIPE
            )
            messagebox.showinfo("Thông báo", "Máy chủ Flask đã khởi động tại 127.0.0.1:<port là 5000 hoặc là port bạn cấu hình ở trên app.run trên main.py của bạn>.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể khởi động Flask server: {str(e)}")
    else:
        messagebox.showinfo("Thông báo", "Máy chủ Flask đang chạy.")
def stop_flask_server():
    global app_process

    if app_process:
        try:
            # Kiểm tra nếu tiến trình đang chạy
            if app_process.poll() is None:
                app_process.terminate()  # Yêu cầu tiến trình dừng
                try:
                    app_process.wait(timeout=5)  # Đợi tiến trình kết thúc trong 5 giây
                except subprocess.TimeoutExpired:
                    app_process.kill()  # Buộc dừng nếu không phản hồi
                    app_process.wait()  # Thu dọn tiến trình sau khi kill
            messagebox.showinfo("Thông báo", "Máy chủ Flask đã dừng.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi dừng máy chủ Flask: {str(e)}")
        finally:
            app_process = None  # Đặt lại biến tiến trình
    else:
        messagebox.showinfo("Thông báo", "Máy chủ Flask chưa chạy.")
def choose_directory():
    global directory_path
    directory_path = filedialog.askdirectory()
    if directory_path:
        folder_label.config(text=f"Đã chọn thư mục: {directory_path}")

def open_instructions1():
    fixed_path = os.path.abspath('flaskconfig.html')
    if os.path.exists(fixed_path):
        webbrowser.open(f'file://{fixed_path}')
    else:
        messagebox.showerror("Lỗi", "Không tìm thấy file flaskconfig.html tại đường dẫn cố định.")
def open_instructions():
    fixed_path = os.path.abspath('index.html')
    if os.path.exists(fixed_path):
        webbrowser.open(f'file://{fixed_path}')
    else:
        messagebox.showerror("Lỗi", "Không tìm thấy file index.html tại đường dẫn cố định.")
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def is_root():
    return os.geteuid() == 0

def run_as_admin():
    system = platform.system()
    if system == "Windows":
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            sys.exit()
    elif system in ["Linux", "Darwin"]:
        if not is_root():
            print("Chạy lại ứng dụng với quyền root.")
            os.system(f'sudo {sys.executable} {__file__}')
            sys.exit()

run_as_admin()
def open_instructions2():
    fixed_path = os.path.abspath('virtualhost.html')
    if os.path.exists(fixed_path):
        webbrowser.open(f'file://{fixed_path}')
    else:
        messagebox.showerror("Lỗi", "Không tìm thấy file index.html tại đường dẫn cố định.")
# Giao diện Tkinter
root = tk.Tk()
root.title("Bobby webserver for flask")

# Nhãn hiển thị thư mục chứa main.py
folder_label = tk.Label(root, text="Chưa chọn thư mục chứa main.py", width=50)
folder_label.pack(pady=10)

# Nút chọn thư mục chứa main.py
choose_button = tk.Button(root, text="Chọn thư mục chứa main.py", command=choose_directory)
choose_button.pack(pady=5)

# Nút khởi động máy chủ Flask
start_button = tk.Button(root, text="Bật máy chủ", command=start_flask_server)
start_button.pack(pady=5)

# Nút tắt máy chủ Flask
stop_button = tk.Button(root, text="Tắt máy chủ", command=stop_flask_server)
stop_button.pack(pady=5)

# Nút mở trang HTML hướng dẫn đưa web lên mạng
instructions_button = tk.Button(root, text="Hướng dẫn đưa web lên mạng", command=open_instructions)
instructions_button.pack(pady=5)

instructions_button1 = tk.Button(root, text="Cách cấu hình môi trường cho flask server", command=open_instructions1)
instructions_button1.pack(pady=5)
instructions_button2 = tk.Button(root, text="Cách cấu hình virtualhost cho flask server", command=open_instructions2)
instructions_button2.pack(pady=5)
# Chạy giao diện Tkinter
root.mainloop()
print("Cảm ơn đã dùng dịch vụ webserverbobby")