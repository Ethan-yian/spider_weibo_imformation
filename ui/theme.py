from tkinter import ttk

class ModernTheme:
    """现代主题样式"""
    # 修改为粉色系颜色
    BG_COLOR = "#ffe4e1"  # 背景颜色，淡粉色
    FG_COLOR = "#333333"  # 前景颜色，深灰色
    ACCENT_COLOR = "#ff69b4"  # 强调颜色，亮粉色
    SUCCESS_COLOR = "#ffb6c1"  # 成功颜色，浅粉色
    WARNING_COLOR = "#ffc0cb"  # 警告颜色，稍深的浅粉色
    ERROR_COLOR = "#ff1493"  # 错误颜色，玫红色

    TITLE_FONT = ("Helvetica", 12, "bold")
    NORMAL_FONT = ("Helvetica", 10)

    @classmethod
    def setup(cls, root):
        style = ttk.Style()

        # 设置主题
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")

        # 配置样式
        style.configure("Title.TLabel",
                        font=cls.TITLE_FONT,
                        foreground=cls.FG_COLOR,
                        background=cls.BG_COLOR)

        style.configure("Modern.TButton",
                        padding=5,
                        font=cls.NORMAL_FONT,
                        background=cls.BG_COLOR,
                        foreground=cls.FG_COLOR)

        style.configure("Success.TButton",
                        background=cls.SUCCESS_COLOR,
                        padding=5,
                        font=cls.NORMAL_FONT,
                        foreground=cls.FG_COLOR)

        style.configure("Warning.TButton",
                        background=cls.WARNING_COLOR,
                        padding=5,
                        font=cls.NORMAL_FONT,
                        foreground=cls.FG_COLOR)

        style.configure("Modern.TEntry",
                        padding=5,
                        font=cls.NORMAL_FONT,
                        background=cls.BG_COLOR,
                        foreground=cls.FG_COLOR)

        style.configure("Modern.TCombobox",
                        padding=5,
                        font=cls.NORMAL_FONT,
                        background=cls.BG_COLOR,
                        foreground=cls.FG_COLOR)

        style.configure("Modern.TLabelframe",
                        font=cls.TITLE_FONT,
                        background=cls.BG_COLOR,
                        foreground=cls.FG_COLOR)

        style.configure("Modern.TLabelframe.Label",
                        font=cls.TITLE_FONT,
                        foreground=cls.ACCENT_COLOR,
                        background=cls.BG_COLOR)