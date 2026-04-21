#!/bin/bash
# skill-tracker Mac 启动脚本
# 双击此文件即可启动服务并打开浏览器

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "✅ skill-tracker 服务启动中..."
echo "👉 浏览器即将打开 http://localhost:7788/viewer.html"
echo "   (关闭此窗口或按 Ctrl+C 停止服务)"
echo ""

python3 serve.py
