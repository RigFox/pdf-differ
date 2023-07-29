from typing import Optional, Tuple, Union, Any
import customtkinter
from tkinter.messagebox import showerror, showinfo
from pathlib import Path


HOME_DIR = Path(__file__).parent


class UI:
    OLD_DEFAULT = ''
    NEW_DEFAULT = ''
    DEFAULT_DIR = ''

    def __init__(self) -> None:
        self.fg_color = '#518048'
        self.text_color = '#F2E8CF'
        self.label_fg_color = '#6A994E'
        self.btn_choose_fg_color = '#386641'
        self.btn_choose_border_color = '#335D3B'
        self.btn_run_fg_color = '#BC4749'
        self.btn_run_border_color = '#C2585A'

    @property
    def text(self):
        return customtkinter.StringVar

    def btn_generator(self,
                      frame: customtkinter.CTkFrame,
                      text: str,
                      cmd: callable,
                      fg_color: str | None = None,
                      border_color: str | None = None):
        if fg_color is None:
            fg_color = self.btn_choose_fg_color
        if border_color is None:
            border_color = self.btn_choose_border_color

        return customtkinter.CTkButton(
            master=frame,
            text=text,
            command=cmd,
            width=100,
            fg_color=fg_color,
            border_color=border_color,
            border_width=2,
            text_color=self.text_color)

    def label_generator(self, frame: any, textvar: customtkinter.StringVar):
        return customtkinter.CTkLabel(
            master=frame,
            textvariable=textvar,
            width=240,
            fg_color=self.label_fg_color,
            text_color=self.text_color,
            corner_radius=10)

    def choose_file(self) -> str | None:
        filetype = (("PDF-file", "*.pdf"),)
        filename = customtkinter.filedialog.askopenfilename(
            title="Open File",
            initialdir=HOME_DIR,
            filetypes=filetype)
        return filename
    
    def choose_path(self) -> str | None:
        directory = customtkinter.filedialog.askdirectory(
            title="Open Directory",
            initialdir=HOME_DIR)
        return directory
    
    def text_manager(self, text: str) -> str:
        if len(text) > 30:
            return text[len(text)-30:]
        return text

    def err_msg(self, title: str, text: str):
        return showerror(title, text)
    
    def info_msg(self, title: str, text: str):
        return showinfo(title, text)


class MainUI(customtkinter.CTk, UI):

    def __init__(self):
        UI.__init__(self)
        super().__init__()

    def ui(self):
        self.old_label = self.label_generator(
            frame=self,
            textvar=self.old_text)
        self.old_label.grid(
            column=0,
            row=0,
            padx=5,
            pady=15)
        self.old_btn = self.btn_generator(
            frame=self,
            text="Open",
            cmd=self.choose_old)
        self.old_btn.grid(
            column=1,
            row=0,
            pady=15)

        self.new_label = self.label_generator(
            frame=self,
            textvar=self.new_text)
        self.new_label.grid(
            column=0,
            row=1)
        self.new_btn = self.btn_generator(
            frame=self,
            text="Open",
            cmd=self.choose_new)
        self.new_btn.grid(
            column=1,
            row=1)

        self.new_label = self.label_generator(
            frame=self,
            textvar=self.save_dir_text)
        self.new_label.grid(
            column=0,
            row=2)
        self.save_dir_btn = self.btn_generator(
            frame=self,
            text="Save to",
            cmd=self.choose_save_dir)
        self.save_dir_btn.grid(
            column=1,
            row=2,
            pady=15)
        self.settings_btn = self.btn_generator(
            frame=self,
            text="Settings",
            cmd=self.run_settings,
            fg_color=self.btn_choose_fg_color,
            border_color=self.btn_run_border_color)
        self.settings_btn.grid(
            column=0,
            row=3)

        self.select = self.btn_generator(
            frame=self,
            text="Run",
            cmd=self.runner,
            fg_color=self.btn_run_fg_color,
            border_color=self.btn_run_border_color)
        self.select.grid(
            column=1,
            row=3)
        self.set_window_size()

    def set_window_size(self):
        self.update()
        width = self.old_label.winfo_width() + self.old_btn.winfo_width() + 15
        height = self.old_btn.winfo_height() * 4 + 15 * 5
        self.geometry(f'{width}x{height}')
        self.resizable(False, False)


class SettingsUI(customtkinter.CTkToplevel, UI):
    def __init__(self, *args, master, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        UI.__init__(self)
        super().__init__(*args, fg_color=fg_color, **kwargs)
        self.master = master

    def ui(self):
        self.label = self.classic_label_generator(
            frame=self,
            text='Set old pdf file as default')
        self.label.grid(column=0, row=0, pady=(10, 0), padx=5)
        self.label_old = self.label_generator(
            frame=self,
            textvar=self.default_old_text)
        self.label_old.grid(column=0, row=1, padx=5)
        self.old_btn = self.btn_generator(
            frame=self,
            text="Open",
            cmd=self.choose_default_old_file)
        self.old_btn.grid(column=1, row=1)
        self.save_btn = self.btn_generator(
            frame=self,
            text="Save",
            cmd=self.save,
            fg_color=self.btn_run_fg_color,
            border_color=self.btn_run_border_color)
        self.save_btn.grid(column=1, row=2, pady=(15, 0))
        self.set_window_size()

    def classic_label_generator(self, frame, text):
        return customtkinter.CTkLabel(
            master=frame,
            text=text,
            width=240,
            corner_radius=10)
    
    def get_height(self):
        return self.label_old.winfo_height() + \
               self.old_btn.winfo_height() + \
               self.label.winfo_height() + \
               self.save_btn.winfo_height() + \
               10

    def get_width(self):
        return self.label_old.winfo_width() + \
               self.old_btn.winfo_width() + \
               5 * 4

    def set_window_size(self):
        self.update()
        width = self.get_width()
        height = self.get_height()
        self.geometry(f'{width}x{height}')
        self.resizable(False, False)
