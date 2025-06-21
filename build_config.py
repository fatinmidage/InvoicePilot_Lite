#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller 打包配置文件
用于将 InvoicePilot Lite 打包成独立的可执行文件
"""

import PyInstaller.__main__
import sys
import os

def build_executable():
    """构建可执行文件"""
    
    # 打包参数
    args = [
        'main.py',                    # 主程序文件
        '--onefile',                  # 打包成单个文件
        '--name=InvoicePilot',        # 可执行文件名称
        '--windowed',                 # Windows下隐藏控制台窗口（可选）
        '--clean',                    # 清理临时文件
        '--distpath=./dist',          # 输出目录
        '--workpath=./build',         # 工作目录
        '--specpath=./build',         # spec文件目录
        '--add-data=README.md;.',     # 包含README文件（可选）
        '--icon=icon.ico',            # 图标文件（如果有的话）
    ]
    
    # 移除不存在的文件参数
    if not os.path.exists('icon.ico'):
        args = [arg for arg in args if not arg.startswith('--icon')]
    
    # 执行打包
    PyInstaller.__main__.run(args)
    
    print("打包完成！")
    print("可执行文件位置: ./dist/InvoicePilot")

if __name__ == "__main__":
    try:
        build_executable()
    except ImportError:
        print("请先安装 PyInstaller:")
        print("pip install pyinstaller")
    except Exception as e:
        print(f"打包过程中出现错误: {e}") 