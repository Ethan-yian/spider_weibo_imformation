from tkinter import ttk


class ModernTheme:
    """现代主题样式"""
    BG_COLOR = "#f0f0f0"
    FG_COLOR = "#333333"
    ACCENT_COLOR = "#007acc"
    SUCCESS_COLOR = "#28a745"
    WARNING_COLOR = "#ffc107"
    ERROR_COLOR = "#dc3545"

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
                        foreground=cls.FG_COLOR)

        style.configure("Modern.TButton",
                        padding=5,
                        font=cls.NORMAL_FONT)

        style.configure("Success.TButton",
                        background=cls.SUCCESS_COLOR,
                        padding=5,
                        font=cls.NORMAL_FONT)

        style.configure("Warning.TButton",
                        background=cls.WARNING_COLOR,
                        padding=5,
                        font=cls.NORMAL_FONT)

        style.configure("Modern.TEntry",
                        padding=5,
                        font=cls.NORMAL_FONT)

        style.configure("Modern.TCombobox",
                        padding=5,
                        font=cls.NORMAL_FONT)

        style.configure("Modern.TLabelframe",
                        font=cls.TITLE_FONT)

        style.configure("Modern.TLabelframe.Label",
                        font=cls.TITLE_FONT,
                        foreground=cls.ACCENT_COLOR)