import customtkinter
from tkinter.messagebox import showerror

class UI(customtkinter.CTk):
    OLD_DEFAULT = ''
    NEW_DEFAULT = ''
    DEFAULT_DIR = ''

    def __init__(self):
        self.fg_color = '#518048'
        self.text_color = '#F2E8CF'
        self.label_fg_color = '#6A994E'
        self.btn_choose_fg_color = '#386641'
        self.btn_choose_border_color = '#335D3B'

        super().__init__(self.fg_color)

        # Path to the files
        self.old_file = self.OLD_DEFAULT
        self.new_file = self.NEW_DEFAULT
        # Path to save directory
        self.save_dir = self.DEFAULT_DIR
        # Text who updates in labels
        self.old_text = self.text(self, self.text_manager(self.old_file))
        self.new_text = self.text(self, self.text_manager(self.new_file))
        self.save_dir_text = self.text(self, self.text_manager(self.DEFAULT_DIR))


        self.btn_run_fg_color = '#BC4749'
        self.btn_run_border_color = '#C2585A'

        self.ui()
        width = self.old_label.winfo_width() + self.old_btn.winfo_width() + 15
        height = self.old_btn.winfo_height() * 4 + 15 * 5
        self.geometry(f'{width}x{height}')
        self.resizable(False, False)

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
            initialdir='/',
            filetypes=filetype)
        return filename
    
    def choose_path(self) -> str | None:
        directory = customtkinter.filedialog.askdirectory(
            title="Open Directory",
            initialdir="/")
        return directory
    
    def text_manager(self, text: str) -> str:
        if len(text) > 30:
            return text[len(text)-30:]
        return text

    def err_msg(self, title: str, text: str):
        return showerror(title, text)

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
        self.new_btn = self.btn_generator(
            frame=self,
            text="Save to",
            cmd=self.choose_save_dir)
        self.new_btn.grid(
            column=1,
            row=2,
            pady=15)

        self.select = self.btn_generator(
            frame=self,
            text="Run",
            cmd=self.runner,
            fg_color=self.btn_run_fg_color,
            border_color=self.btn_run_border_color)
        self.select.grid(
            column=1,
            row=3)
        self.update()
