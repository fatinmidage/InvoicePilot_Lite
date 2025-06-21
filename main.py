#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InvoicePilot Lite - 自动读取PDF发票并提取金额信息进行文件重命名的工具
自动处理当前目录下的所有PDF发票文件
"""

import pdfplumber
import re
import os
import sys
from pathlib import Path
from typing import Optional, Tuple


class InvoiceProcessor:
    """发票处理器类"""
    
    def __init__(self):
        # 金额匹配模式，支持多种格式
        self.amount_patterns = [
            r'金额[：:]\s*¥?\s*([0-9,]+\.?[0-9]*)',  # 金额：¥100.00
            r'小写[：:]\s*¥?\s*([0-9,]+\.?[0-9]*)',  # 小写：¥100.00
            r'合计[：:]\s*¥?\s*([0-9,]+\.?[0-9]*)',  # 合计：¥100.00
            r'总计[：:]\s*¥?\s*([0-9,]+\.?[0-9]*)',  # 总计：¥100.00
            r'￥\s*([0-9,]+\.?[0-9]*)',  # ￥100.00
            r'¥\s*([0-9,]+\.?[0-9]*)',  # ¥100.00
            r'([0-9,]+\.?[0-9]*)\s*元',  # 100.00元
        ]
    
    def get_current_directory(self) -> Path:
        """
        获取当前工作目录，适配嵌入式Python环境
        
        Returns:
            当前工作目录的Path对象
        """
        # 如果是嵌入式Python，使用脚本所在目录
        if getattr(sys, 'frozen', False):
            # 打包后的可执行文件
            current_dir = Path(sys.executable).parent
        else:
            # 开发环境，使用脚本所在目录
            current_dir = Path(__file__).parent
        
        return current_dir
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        从PDF文件中提取文本内容
        
        Args:
            pdf_path: PDF文件路径
            
        Returns:
            提取的文本内容
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text
        except Exception as e:
            print(f"读取PDF文件时出错: {e}")
            return ""
    
    def extract_amount(self, text: str) -> Optional[float]:
        """
        从文本中提取金额
        
        Args:
            text: 要分析的文本
            
        Returns:
            提取到的金额，如果未找到则返回None
        """
        # 清理文本，移除多余空格
        text = re.sub(r'\s+', ' ', text.strip())
        
        for pattern in self.amount_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # 取最后一个匹配的金额（通常是最准确的）
                amount_str = matches[-1]
                # 移除逗号并转换为浮点数
                amount_str = amount_str.replace(',', '')
                try:
                    amount = float(amount_str)
                    if amount > 0:
                        return amount
                except ValueError:
                    continue
        
        return None
    
    def process_invoice(self, pdf_path: Path) -> Tuple[bool, str]:
        """
        处理单个发票文件
        
        Args:
            pdf_path: PDF文件路径
            
        Returns:
            (成功标志, 消息)
        """
        if not pdf_path.exists():
            return False, f"文件不存在: {pdf_path}"
        
        if not pdf_path.suffix.lower() == '.pdf':
            return False, f"不是PDF文件: {pdf_path}"
        
        print(f"正在处理: {pdf_path.name}")
        
        # 提取文本
        text = self.extract_text_from_pdf(str(pdf_path))
        if not text:
            return False, f"无法从PDF中提取文本: {pdf_path.name}"
        
        # 提取金额
        amount = self.extract_amount(text)
        if amount is None:
            return False, f"无法从PDF中提取金额: {pdf_path.name}"
        
        # 生成新文件名
        new_filename = f"{amount:.2f}元_发票.pdf"
        output_path = pdf_path.parent / new_filename
        
        # 检查目标文件是否已存在
        if output_path.exists():
            counter = 1
            while output_path.exists():
                new_filename = f"{amount:.2f}元_发票_{counter}.pdf"
                output_path = pdf_path.parent / new_filename
                counter += 1
        
        try:
            # 重命名文件
            pdf_path.rename(output_path)
            return True, f"成功重命名: {pdf_path.name} -> {output_path.name}"
        except Exception as e:
            return False, f"重命名文件时出错: {e}"
    
    def process_current_directory(self) -> None:
        """
        处理当前目录中的所有PDF发票文件
        """
        current_dir = self.get_current_directory()
        
        print(f"正在扫描目录: {current_dir}")
        print("=" * 60)
        
        # 查找所有PDF文件
        pdf_files = list(current_dir.glob("*.pdf"))
        
        if not pdf_files:
            print("当前目录中未找到PDF文件")
            print("请确保PDF发票文件位于程序同一目录下")
            return
        
        print(f"找到 {len(pdf_files)} 个PDF文件:")
        for pdf_file in pdf_files:
            print(f"  - {pdf_file.name}")
        print("=" * 60)
        
        success_count = 0
        failed_count = 0
        
        for pdf_file in pdf_files:
            success, message = self.process_invoice(pdf_file)
            if success:
                success_count += 1
                print(f"✓ {message}")
            else:
                failed_count += 1
                print(f"✗ {message}")
            print("-" * 40)
        
        print("=" * 60)
        print(f"处理完成: 成功 {success_count} 个，失败 {failed_count} 个")
        
        if success_count > 0:
            print(f"已重命名的文件保存在: {current_dir}")
        
        # 等待用户按键退出（嵌入式环境）
        if getattr(sys, 'frozen', False):
            input("\n按回车键退出...")
    
    def show_help(self):
        """显示帮助信息"""
        print("InvoicePilot Lite - PDF发票自动重命名工具")
        print("=" * 50)
        print("功能: 自动读取当前目录下的PDF发票，提取金额信息并重命名文件")
        print("使用方法: 将程序放在包含PDF发票的目录中，双击运行即可")
        print("重命名格式: 金额元_发票.pdf (例如: 100.00元_发票.pdf)")
        print("=" * 50)


def main():
    """主函数"""
    processor = InvoiceProcessor()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help', '/?', '-?']:
            processor.show_help()
            return
    
    # 自动处理当前目录
    processor.process_current_directory()


if __name__ == "__main__":
    main()
