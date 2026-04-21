"""
skill-tracker 本地服务器
双击运行，或命令行执行：python serve.py
然后用浏览器打开：http://localhost:7788
"""
import http.server
import socketserver
import os
import threading
import time
import webbrowser

PORT = 7788
DIR = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def log_message(self, format, *args):
        pass  # 静默日志

def open_browser():
    time.sleep(0.8)
    webbrowser.open(f"http://localhost:{PORT}/viewer.html")

print(f"✅ skill-tracker 服务已启动")
print(f"👉 正在打开：http://localhost:{PORT}/viewer.html")
print(f"   (按 Ctrl+C 停止服务)")

threading.Thread(target=open_browser, daemon=True).start()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
