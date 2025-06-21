@echo off
chcp 65001 >nul
title InvoicePilot Lite - PDF发票自动重命名工具

echo.
echo ================================================
echo    InvoicePilot Lite - PDF发票自动重命名工具
echo ================================================
echo.

echo 正在启动程序...
echo 请确保PDF发票文件位于当前目录中
echo.

python main.py

echo.
echo 程序执行完毕，按任意键退出...
pause >nul 