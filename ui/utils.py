import os
import re
import ast
from datetime import datetime
import threading
from tkinter import messagebox
import logging
import warnings

# 设置警告过滤
warnings.filterwarnings("ignore", category=UserWarning)
logging.getLogger('PIL').setLevel(logging.ERROR)

def validate_date(date_str):
    """验证日期格式"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def get_current_time():
    """获取当前时间字符串"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def run_async(func):
    """异步执行装饰器"""
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        thread.start()
        return thread
    return wrapper

def parse_settings_file(file_path):
    """解析设置文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        messagebox.showerror("错误", f"读取配置文件失败: {str(e)}")
        return None

def save_settings_file(file_path, content):
    """保存设置文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        messagebox.showerror("错误", f"保存配置文件失败: {str(e)}")
        return False