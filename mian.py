import os
import tkinter as tk
from ui.base import WeiboSearchUI


def check_project_structure():
    """检查并创建必要的项目结构"""
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 确保 weibo 目录存在
    weibo_dir = os.path.join(current_dir, 'weibo')
    os.makedirs(weibo_dir, exist_ok=True)

    # 确保 spiders 目录存在
    spiders_dir = os.path.join(weibo_dir, 'spiders')
    os.makedirs(spiders_dir, exist_ok=True)


def main():
    # 检查项目结构
    check_project_structure()

    root = tk.Tk()
    app = WeiboSearchUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()