import subprocess
import tkinter.ttk as ttk
import tkinter.messagebox
import time
import tkinter
import tkinter as tk


def distribute_integer(total, n):
    # 初始化列表，存放分配后的整数
    distribution = [0] * n
    # 计算平均值
    average = total // n
    # 计算剩余的部分
    remainder = total % n
    # 将平均值分配到每个位置
    for i in range(n):
        distribution[i] = average
    # 将剩余部分加到某个位置，直到剩余部分为零
    i = 0
    while remainder > 0:
        distribution[i] += 1
        remainder -= 1
        i += 1
    return distribution


def ShowInstallerWindow(InstallerLibList):
    app = Installer(InstallerLibList)
    app.mainloop()


class Installer(tk.Tk):
    def __init__(self, InstallerLibList: list = []):
        super().__init__()
        self.window_real_width = 440
        self.window_real_height = 180
        self.InstallerLibList = InstallerLibList
        self.installCount = 0
        if len(self.InstallerLibList) > 0:
            self.Progress_Add = distribute_integer(
                100, len(self.InstallerLibList))
        else:
            return
        self.libCount = 0
        with open('./LICENSE/EULA', 'r', encoding='utf-8') as license_file:
            self.LICENSE = license_file.read()
        #
        self.window_width = 420
        self.window_height = 160
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        x = (self.screen_width - self.window_real_width) / 2
        y = (self.screen_height - self.window_real_height) / 2
        self.geometry("%dx%d+%d+%d" %
                      (self.window_real_width, self.window_real_height, x, y))
        self.resizable(False, False)
        self.title('Structure Studio Installer')
        self.iconbitmap('./img/appIcon_2_64.ico')
        self.attributes('-topmost', True)
        # self.attributes("-alpha", 0.8)
        self.attributes("-transparent", "purple")
        self.overrideredirect(True)
        #
        style = ttk.Style()
        style.theme_use('vista')
        #
        self.image_big = tk.PhotoImage(
            file="./img/installer/window_2_180_5.png")
        self.Background_big = ttk.Label(self, image=self.image_big,
                                        text='', border=0, padding=0, background='purple')
        self.Background_big.place(x=0, y=0, width=self.window_real_width,
                                  height=self.window_real_height)
        #
        self.image = tk.PhotoImage(file="./img/installer/mcEarth_2_100.png")
        self.Background = ttk.Label(self, image=self.image,
                                    text='', border=0, padding=0, background='#dfdfdf')
        self.Background.place(x=16, y=24, width=self.window_width -
                              9, height=self.window_height-28 - 20)
        #
        self.DownLoadLabel = ttk.Label(
            self, text='start to download ...', background='#dfdfdf')
        self.DownLoadLabel.place(x=16, y=self.window_height-20-9,
                                 height=20, width=self.window_width - 9)
        #
        self.Count = 0
        self.progressbarOne = ttk.Progressbar(self)
        self.progressbarOne.place(x=16, y=self.window_height - 9,
                                  height=20, width=self.window_width - 9)
        self.progressbarOne['maximum'] = 100
        self.progressbarOne['value'] = 0

        # close button
        self.close_imag = tk.PhotoImage(
            file="./img/installer/big_close_2__.png")
        self.closeButton = tk.Button(
            self, text='', image=self.close_imag, background='#c6c6c6', relief=tk.GROOVE, command=self.close)
        self.closeButton.place(x=self.window_real_width -
                               20, y=6, height=16, width=16)
        # hide button
        self.hide_imag = tk.PhotoImage(
            file="./img/installer/small_black_2.png")
        self.hideButton = tk.Button(
            self, text='', image=self.hide_imag, background='#c6c6c6', relief=tk.GROOVE, command=self.small)
        self.hideButton.place(x=self.window_real_width -
                              36, y=6, height=16, width=16)
        # title label
        self.titleLabel = tk.Label(
            self, text='Structure Studio Installer', border=0, background='#c6c6c6', foreground='#888')
        self.titleLabel.place(x=9, y=6, height=16)
        # start
        self.Background_big.bind("<ButtonPress-1>", self.start_move)
        self.Background_big.bind("<ButtonRelease-1>", self.stop_move)
        self.Background_big.bind("<B1-Motion>", self.do_move)
        #
        self.titleLabel.bind("<ButtonPress-1>", self.start_move)
        self.titleLabel.bind("<ButtonRelease-1>", self.stop_move)
        self.titleLabel.bind("<B1-Motion>", self.do_move)
        # info
        self.MakeInfo()
        # after loop
        self.after(0, self.update_progress)

    def MakeInfo(self):
        '''
        info面板
        '''
        self.InfoPanel = tk.Label(
            self.Background, text='', background='#dfdfdf')
        self.InfoPanel.place(x=110, y=0, width=320, height=110)
        #
        self.title_X = tk.Label(
            self.InfoPanel, text='Structure Studio', font=('System', 22), background='#dfdfdf')
        self.title_X.place(x=0, y=0)
        a = tk.Text(self.InfoPanel,
                    border=0, background='#dfdfdf', font=('', 9), foreground='#555')
        a.insert(
            'insert', '   Structure Studio是一个用于编辑和模拟Minecraft结构(NBT)的工具，本软件使用开源协议，本软件与Mojang AB无关。用户协议\n\n\n     (c)Copyright 2023 Pure.XK | XinYuanIT')
        a.place(x=0, y=30, width=300)
        a.configure(state='disabled')
        a.tag_add("link", "1.75", "1.79")
        a.tag_config("link", foreground="blue",
                     underline=True)
        a.tag_bind("link", "<Button-1>", self.callback)

    def callback(self, event):
        import webbrowser
        webbrowser.open_new("https://www.baidu.com")

    def close(self):
        ifclose = tk.messagebox.askokcancel(
            'Stop download', 'Download is running, do you want to close it?')
        if ifclose:
            self.quit()

    def small(self):
        self.geometry('0x0')

    def update_progress(self):
        if self.Count < 100:
            self.Count += self.Progress_Add[self.libCount]
            self.progressbarOne['value'] = self.Count
            self.DownLoadLabel.config(
                text='Download '+str(self.Count)+f'% install : {self.InstallerLibList[self.libCount]}')
            self.installLib(self.InstallerLibList[self.libCount])
            self.libCount += 1
            self.after(100, self.update_progress)
        else:
            self.DownLoadLabel.config(text='Download done ...')
            # exit()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def installLib(self, libName):
        try:
            self.installCount += 1
            # 使用 subprocess 调用命令行执行 pip 安装
            subprocess.check_call(['pip', 'install', libName])
            self.installCount = 0
        except subprocess.CalledProcessError as e:
            ifclose = tk.messagebox.askokcancel(
                'install Error', f"Failed to install lib <{libName}>\n\tError: {e}")
            if ifclose:
                self.quit()
            else:
                self.quit()


useLib = [
    'minecraft_launcher_lib',
    'pywin32',
    'IPython',
    'PyQt5',
    'numpy',
    'psutil',
    'vtk',
    'nbtlib',
    'win32mica',
    'qtconsole',
]
InstallLib = []

ShowInstallerWindow(['a', 'b', 'c'])
