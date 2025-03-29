import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import pandas as pd
import os
from datetime import datetime
import threading


class ConverterPanel:
    def __init__(self, parent, log_queue):
        self.parent = parent
        self.log_queue = log_queue

        # 初始化变量
        self.csv_dir = tk.StringVar()
        self.excel_dir = tk.StringVar()
        self.csv_encoding = tk.StringVar(value='utf-8')
        self.convert_progress_var = tk.DoubleVar()

        self.create_widgets()

    def create_widgets(self):
        # 创建Notebook
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 转换工具面板
        convert_frame = ttk.LabelFrame(self.notebook, text="CSV转Excel工具", padding=10)
        self.notebook.add(convert_frame, text="数据转换")

        # CSV 输入部分
        input_frame = ttk.Frame(convert_frame)
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_frame, text="CSV文件目录:").pack(side=tk.LEFT)
        csv_entry = ttk.Entry(input_frame, textvariable=self.csv_dir, width=40)
        csv_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(input_frame, text="浏览",
                   command=self.browse_csv_dir,
                   style="Modern.TButton").pack(side=tk.LEFT)

        # Excel 输出部分
        output_frame = ttk.Frame(convert_frame)
        output_frame.pack(fill=tk.X, pady=5)
        ttk.Label(output_frame, text="Excel保存位置:").pack(side=tk.LEFT)
        excel_entry = ttk.Entry(output_frame, textvariable=self.excel_dir, width=40)
        excel_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="浏览",
                   command=self.browse_excel_dir,
                   style="Modern.TButton").pack(side=tk.LEFT)

        # 编码选择
        encoding_frame = ttk.Frame(convert_frame)
        encoding_frame.pack(fill=tk.X, pady=5)
        ttk.Label(encoding_frame, text="CSV编码:").pack(side=tk.LEFT)
        encoding_combo = ttk.Combobox(encoding_frame, textvariable=self.csv_encoding,
                                      values=['utf-8', 'gbk', 'gb2312', 'ascii'],
                                      width=10)
        encoding_combo.pack(side=tk.LEFT, padx=5)

        # 转换按钮
        ttk.Button(convert_frame, text="开始转换",
                   command=self.start_conversion,
                   style="Modern.TButton").pack(pady=10)

        # 转换进度条
        self.convert_progress = ttk.Progressbar(convert_frame,
                                                variable=self.convert_progress_var,
                                                mode='determinate',
                                                length=300)
        self.convert_progress.pack(fill=tk.X, pady=5)

        # 转换状态
        self.convert_status_var = tk.StringVar(value="准备就绪")
        ttk.Label(convert_frame, textvariable=self.convert_status_var).pack()

        # 转换日志
        convert_log_frame = ttk.LabelFrame(convert_frame, text="转换日志")
        convert_log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.convert_log = scrolledtext.ScrolledText(convert_log_frame, height=10)
        self.convert_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def browse_csv_dir(self):
        """浏览CSV文件目录"""
        path = filedialog.askdirectory(title="选择CSV文件所在目录")
        if path:
            self.csv_dir.set(path)
            self.log_convert_message(f"已选择CSV目录: {path}")

    def browse_excel_dir(self):
        """浏览Excel保存目录"""
        path = filedialog.askdirectory(title="选择Excel文件保存目录")
        if path:
            self.excel_dir.set(path)
            self.log_convert_message(f"已选择Excel保存目录: {path}")

    def log_convert_message(self, message):
        """记录转换日志"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.convert_log.insert(tk.END, f"[{current_time}] {message}\n")
        self.convert_log.see(tk.END)

    def start_conversion(self):
        """开始转换CSV到Excel"""
        if not self.csv_dir.get() or not self.excel_dir.get():
            messagebox.showerror("错误", "请选择输入和输出目录！")
            return

        # 在新线程中执行转换
        self.convert_status_var.set("正在转换...")
        thread = threading.Thread(target=self.convert_files)
        thread.daemon = True
        thread.start()

    def convert_files(self):
        """执行CSV到Excel的转换"""
        try:
            csv_dir = self.csv_dir.get()
            excel_dir = self.excel_dir.get()

            # 获取所有CSV文件
            csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
            total_files = len(csv_files)

            if total_files == 0:
                self.log_convert_message("未找到CSV文件！")
                self.convert_status_var.set("未找到CSV文件")
                return

            self.convert_progress_var.set(0)

            for index, csv_file in enumerate(csv_files):
                try:
                    csv_path = os.path.join(csv_dir, csv_file)
                    excel_filename = os.path.splitext(csv_file)[0] + '.xlsx'
                    excel_path = os.path.join(excel_dir, excel_filename)

                    # 读取CSV
                    df = pd.read_csv(csv_path, encoding=self.csv_encoding.get())

                    # 保存为Excel
                    df.to_excel(excel_path, index=False)

                    progress = (index + 1) / total_files * 100
                    self.convert_progress_var.set(progress)
                    self.log_convert_message(f"已转换: {csv_file} -> {excel_filename}")

                except Exception as e:
                    self.log_convert_message(f"转换 {csv_file} 时出错: {str(e)}")

            self.convert_status_var.set("转换完成！")
            self.parent.after(0, lambda: messagebox.showinfo("完成", "所有文件转换完成！"))

        except Exception as e:
            self.convert_status_var.set("转换失败！")
            self.parent.after(0, lambda: messagebox.showerror("错误", f"转换过程中出错：{str(e)}"))