import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from datetime import datetime
import os
import re
import ast
from weibo.spiders.search import SearchSpider


class CrawlerPanel:
    def __init__(self, parent, log_queue):
        self.parent = parent
        self.log_queue = log_queue

        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.settings_path = os.path.join(current_dir, 'weibo', 'settings.py')

        # 定义类型映射
        self.weibo_types = {
            0: '搜索全部微博',
            1: '搜索全部原创微博',
            2: '热门微博',
            3: '关注人微博',
            4: '认证用户微博',
            5: '媒体微博'
        }

        self.contain_types = {
            0: '不筛选，获取全部微博',
            1: '搜索包含图片的微博',
            2: '包含视频的微博',
            3: '包含音乐的微博'
        }

        self.create_widgets()
        self.load_settings_from_file()

    def create_widgets(self):
        # 基本设置框架
        basic_frame = ttk.LabelFrame(self.parent, text="基本设置", style="Modern.TLabelframe")
        basic_frame.pack(fill=tk.X, pady=(0, 10))

        # 关键词设置
        keyword_frame = ttk.Frame(basic_frame)
        keyword_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(keyword_frame, text="关键词:").pack(side=tk.LEFT)
        self.keyword_var = tk.StringVar()
        self.keyword_entry = ttk.Entry(keyword_frame, textvariable=self.keyword_var,
                                       style="Modern.TEntry")
        self.keyword_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(keyword_frame, text="导入文件",
                   command=self.load_keyword_file,
                   style="Modern.TButton").pack(side=tk.RIGHT)

        # 微博类型
        type_frame = ttk.Frame(basic_frame)
        type_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(type_frame, text="微博类型:").pack(side=tk.LEFT)
        self.weibo_type_var = tk.IntVar()
        self.weibo_type_combo = ttk.Combobox(type_frame,
                                             values=[f"{k}: {v}" for k, v in self.weibo_types.items()],
                                             style="Modern.TCombobox")
        self.weibo_type_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 内容类型
        content_frame = ttk.Frame(basic_frame)
        content_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(content_frame, text="内容类型:").pack(side=tk.LEFT)
        self.contain_type_var = tk.IntVar()
        self.contain_type_combo = ttk.Combobox(content_frame,
                                               values=[f"{k}: {v}" for k, v in self.contain_types.items()],
                                               style="Modern.TCombobox")
        self.contain_type_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 高级设置框架
        advanced_frame = ttk.LabelFrame(self.parent, text="高级设置", style="Modern.TLabelframe")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))

        # 地区设置
        region_frame = ttk.Frame(advanced_frame)
        region_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(region_frame, text="地区:").pack(side=tk.LEFT)
        self.region_var = tk.StringVar(value="全部")
        self.region_entry = ttk.Entry(region_frame, textvariable=self.region_var,
                                      style="Modern.TEntry")
        self.region_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 日期范围
        date_frame = ttk.Frame(advanced_frame)
        date_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(date_frame, text="起始日期:").pack(side=tk.LEFT)
        self.start_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.start_date_entry = ttk.Entry(date_frame, textvariable=self.start_date_var,
                                          width=12, style="Modern.TEntry")
        self.start_date_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(date_frame, text="结束日期:").pack(side=tk.LEFT)
        self.end_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.end_date_entry = ttk.Entry(date_frame, textvariable=self.end_date_var,
                                        width=12, style="Modern.TEntry")
        self.end_date_entry.pack(side=tk.LEFT, padx=5)

        # Cookie设置
        cookie_frame = ttk.Frame(advanced_frame)
        cookie_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(cookie_frame, text="Cookie:").pack(side=tk.LEFT)
        self.cookie_var = tk.StringVar()
        self.cookie_entry = ttk.Entry(cookie_frame, textvariable=self.cookie_var,
                                      style="Modern.TEntry")
        self.cookie_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # 其他设置
        other_frame = ttk.Frame(advanced_frame)
        other_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(other_frame, text="下载延迟(秒):").pack(side=tk.LEFT)
        self.delay_var = tk.StringVar(value="10")
        self.delay_spin = ttk.Spinbox(other_frame, from_=1, to=60,
                                      textvariable=self.delay_var, width=5)
        self.delay_spin.pack(side=tk.LEFT, padx=5)

        # 存储选项
        storage_frame = ttk.Frame(advanced_frame)
        storage_frame.pack(fill=tk.X, padx=10, pady=5)
        self.save_images_var = tk.BooleanVar()
        self.save_videos_var = tk.BooleanVar()
        ttk.Checkbutton(storage_frame, text="保存图片",
                        variable=self.save_images_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(storage_frame, text="保存视频",
                        variable=self.save_videos_var).pack(side=tk.LEFT, padx=5)

        # 控制按钮
        control_frame = ttk.Frame(self.parent)
        control_frame.pack(fill=tk.X, pady=10)

        self.start_button = ttk.Button(control_frame, text="开始爬取",
                                       command=self.start_crawler,
                                       style="Success.TButton")
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(control_frame, text="停止",
                                      command=self.stop_crawler,
                                      state='disabled',
                                      style="Warning.TButton")
        self.stop_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="保存设置",
                   command=self.save_settings,
                   style="Modern.TButton").pack(side=tk.LEFT, padx=5)

        # 进度条
        self.progress = ttk.Progressbar(self.parent, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)

        # 日志区域
        self.log_text = scrolledtext.ScrolledText(self.parent, height=15,
                                                  font=("Helvetica", 10))
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)

    def load_keyword_file(self):
        """从文件加载关键词"""
        file_name = filedialog.askopenfilename(
            title="选择关键词文件",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    keywords = f.read().strip()
                self.keyword_var.set(keywords)
                self.log_queue.put(f"已从文件加载关键词: {file_name}")
            except Exception as e:
                messagebox.showerror("错误", f"读取文件失败: {str(e)}")

    def load_settings_from_file(self):
        """从 settings.py 文件加载配置"""
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 关键词列表
            keyword_match = re.search(r'KEYWORD_LIST\s*=\s*(\[[^\]]*\]|\'[^\']*\'|\"[^\"]*\")', content)
            if keyword_match:
                keywords = ast.literal_eval(keyword_match.group(1))
                if isinstance(keywords, list):
                    self.keyword_var.set(','.join(keywords))
                else:
                    self.keyword_var.set(keywords)

            # 微博类型
            weibo_type_match = re.search(r'WEIBO_TYPE\s*=\s*(\d+)', content)
            if weibo_type_match:
                type_value = int(weibo_type_match.group(1))
                self.weibo_type_var.set(type_value)
                for i, item in enumerate(self.weibo_type_combo['values']):
                    if item.startswith(f"{type_value}:"):
                        self.weibo_type_combo.current(i)
                        break

            # 内容类型
            contain_type_match = re.search(r'CONTAIN_TYPE\s*=\s*(\d+)', content)
            if contain_type_match:
                type_value = int(contain_type_match.group(1))
                self.contain_type_var.set(type_value)
                for i, item in enumerate(self.contain_type_combo['values']):
                    if item.startswith(f"{type_value}:"):
                        self.contain_type_combo.current(i)
                        break

            # 地区
            region_match = re.search(r'REGION\s*=\s*(\[[^\]]*\])', content)
            if region_match:
                regions = ast.literal_eval(region_match.group(1))
                self.region_var.set(regions[0] if regions else '全部')

            # 日期范围
            start_date_match = re.search(r'START_DATE\s*=\s*\'([^\']+)\'', content)
            if start_date_match:
                self.start_date_var.set(start_date_match.group(1))

            end_date_match = re.search(r'END_DATE\s*=\s*\'([^\']+)\'', content)
            if end_date_match:
                self.end_date_var.set(end_date_match.group(1))

            # 下载延迟
            delay_match = re.search(r'DOWNLOAD_DELAY\s*=\s*(\d+)', content)
            if delay_match:
                self.delay_var.set(delay_match.group(1))

            # Cookie
            cookie_match = re.search(r'\'cookie\':\s*\'([^\']+)\'', content)
            if cookie_match:
                self.cookie_var.set(cookie_match.group(1))

            # 管道设置
            self.save_images_var.set('MyImagesPipeline' in content and \
                                     not content.split('MyImagesPipeline')[0].rstrip().endswith('#'))
            self.save_videos_var.set('MyVideoPipeline' in content and \
                                     not content.split('MyVideoPipeline')[0].rstrip().endswith('#'))

            self.log_queue.put("成功加载配置文件")

        except Exception as e:
            self.log_queue.put(f"加载配置文件失败: {str(e)}")
            messagebox.showerror("错误", f"加载配置文件失败: {str(e)}")

    def save_settings(self):
        """保存设置到 settings.py 文件"""
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]

                # 更新关键词列表
                if line.startswith('KEYWORD_LIST'):
                    keywords = [k.strip() for k in self.keyword_var.get().split(',')]
                    new_lines.append(f"KEYWORD_LIST = {repr(keywords)}\n")

                # 更新微博类型
                elif line.startswith('WEIBO_TYPE'):
                    type_value = int(self.weibo_type_combo.get().split(':')[0])
                    new_lines.append(f"WEIBO_TYPE = {type_value}\n")

                # 更新内容类型
                elif line.startswith('CONTAIN_TYPE'):
                    type_value = int(self.contain_type_combo.get().split(':')[0])
                    new_lines.append(f"CONTAIN_TYPE = {type_value}\n")

                # 更新地区
                elif line.startswith('REGION'):
                    regions = [self.region_var.get() or '全部']
                    new_lines.append(f"REGION = {repr(regions)}\n")

                # 更新日期
                elif line.startswith('START_DATE'):
                    new_lines.append(f"START_DATE = '{self.start_date_var.get()}'\n")
                elif line.startswith('END_DATE'):
                    new_lines.append(f"END_DATE = '{self.end_date_var.get()}'\n")

                # 更新下载延迟
                elif line.startswith('DOWNLOAD_DELAY'):
                    new_lines.append(f"DOWNLOAD_DELAY = {self.delay_var.get()}\n")

                # 更新 Cookie
                elif "'cookie'" in line:
                    new_lines.append(f"    'cookie': '{self.cookie_var.get()}'\n")

                # 更新管道设置
                elif line.startswith('ITEM_PIPELINES'):
                    new_lines.append('ITEM_PIPELINES = {\n')
                    new_lines.append("    'weibo.pipelines.DuplicatesPipeline': 300,\n")
                    new_lines.append("    'weibo.pipelines.CsvPipeline': 301,\n")

                    if self.save_images_var.get():
                        new_lines.append("    'weibo.pipelines.MyImagesPipeline': 304,\n")
                    else:
                        new_lines.append("    # 'weibo.pipelines.MyImagesPipeline': 304,\n")

                    if self.save_videos_var.get():
                        new_lines.append("    'weibo.pipelines.MyVideoPipeline': 305\n")
                    else:
                        new_lines.append("    # 'weibo.pipelines.MyVideoPipeline': 305\n")

                    new_lines.append("}\n")
                    while i < len(lines) and '}' not in lines[i]:
                        i += 1
                else:
                    new_lines.append(line)
                i += 1

            # 写入文件
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

            self.log_queue.put("设置已保存到 settings.py")
            messagebox.showinfo("成功", "设置已保存")

        except Exception as e:
            self.log_queue.put(f"保存设置失败: {str(e)}")
            messagebox.showerror("错误", f"保存设置失败: {str(e)}")

    def validate_inputs(self):
        """验证输入"""
        if not self.keyword_var.get().strip():
            messagebox.showerror("错误", "请输入关键词")
            return False

        if not self.cookie_var.get().strip():
            messagebox.showerror("错误", "请输入Cookie")
            return False

        try:
            datetime.strptime(self.start_date_var.get(), '%Y-%m-%d')
            datetime.strptime(self.end_date_var.get(), '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("错误", "日期格式错误，请使用 YYYY-MM-DD 格式")
            return False

        return True

    def start_crawler(self):
        """启动爬虫"""
        if not self.validate_inputs():
            return

        self.save_settings()  # 先保存设置

        self.start_button.state(['disabled'])
        self.stop_button.state(['!disabled'])
        self.progress.start()

        self.log_queue.put("开始爬取...")

        # 在新线程中启动爬虫
        threading.Thread(target=self.crawler_thread, daemon=True).start()

    def crawler_thread(self):
        """爬虫线程"""
        try:
            settings = get_project_settings()
            runner = CrawlerRunner(settings)
            deferred = runner.crawl(SearchSpider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run(installSignalHandlers=False)
            self.parent.after(0, self.crawler_finished)
        except Exception as e:
            self.log_queue.put(f"错误: {str(e)}")
            self.parent.after(0, self.crawler_finished)

    def stop_crawler(self):
        """停止爬虫"""
        if reactor.running:
            reactor.callFromThread(reactor.stop)
        self.crawler_finished()
        self.log_queue.put("爬虫已停止")

    def crawler_finished(self):
        """爬虫完成时的处理"""
        self.start_button.state(['!disabled'])
        self.stop_button.state(['disabled'])
        self.progress.stop()
        self.log_queue.put("爬虫任务已完成")

    def update_log(self, message):
        """更新日志显示"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)