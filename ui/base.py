import tkinter as tk
from tkinter import ttk, messagebox
from twisted.internet import reactor
import queue
import os

from .theme import ModernTheme
from .crawler_panel import CrawlerPanel
from .converter_panel import ConverterPanel
from .utils import get_current_time


class WeiboSearchUI:
    def __init__(self, root):
        self.root = root
        self.root.title('微博关键词数据爬取')

        # 设置窗口大小和位置
        window_width = 900
        window_height = 750
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # 应用现代主题
        ModernTheme.setup(root)

        # 创建消息队列
        self.log_queue = queue.Queue()

        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建面板
        self.create_panels()

        # 创建状态栏
        self.create_status_bar()

        # 设置窗口关闭处理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 启动日志更新
        self.update_log()

    def create_panels(self):
        # 创建左右分隔面板
        left_panel = ttk.Frame(self.main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        right_panel = ttk.Frame(self.main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # 创建爬虫控制面板
        self.crawler_panel = CrawlerPanel(left_panel, self.log_queue)

        # 创建转换工具面板
        self.converter_panel = ConverterPanel(right_panel, self.log_queue)

    def create_status_bar(self):
        """创建状态栏"""
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(self.root, textvariable=self.status_var,
                                 relief=tk.SUNKEN, padding=(5, 2))
        status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def update_log(self):
        """更新日志显示"""
        while True:
            try:
                message = self.log_queue.get_nowait()
                if not message.startswith('libpng warning'):
                    self.crawler_panel.update_log(f"[{get_current_time()}] {message}")
            except queue.Empty:
                break
        self.root.after(100, self.update_log)

    def on_closing(self):
        """窗口关闭处理"""
        if messagebox.askokcancel("确认", "确定要退出吗？，..._〆(°▽°*)"):
            if reactor.running:
                reactor.callFromThread(reactor.stop)
            self.root.destroy()