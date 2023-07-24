from typing import Tuple
import customtkinter


import convert


class App(customtkinter.CTk):
    OLD_DEFAULT = 'Choose old pdf file'
    NEW_DEFAULT = 'Choose new pdf file'
    DEFAULT_DIR = str(convert.RESULT_DIFF)

    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("PDF-differ")
        
        # Путь до файла
        self.old_file = self.OLD_DEFAULT
        self.new_file = self.NEW_DEFAULT
        # Путь до место сохранения
        self.save_dir = self.DEFAULT_DIR
        # Текст который будет обновляться в приложении
        self.old_text = self.text(self, self.old_file)
        self.new_text = self.text(self, self.new_file)
        self.save_dir_text = self.text(self, self.DEFAULT_DIR[len(self.DEFAULT_DIR)-30:])

        self.ui()
        width = self.old_label.winfo_width() + self.old_btn.winfo_width() + 15
        height = self.old_btn.winfo_height() * 4 + 15 * 5
        self.geometry(f'{width}x{height}')
        self.configure(background='#6761A8')
        self.resizable(False, False)

    @property
    def text(self):
        return customtkinter.StringVar

    def btn_generator(self, frame: customtkinter.CTkFrame, text: str, cmd: callable, fg_color: str | None = None):
        return customtkinter.CTkButton(
            master=frame,
            text=text,
            command=cmd,
            width=100,
            fg_color=fg_color)

    def label_generator(self, frame: any, textvar: customtkinter.StringVar):
        return customtkinter.CTkLabel(
            master=frame,
            textvariable=textvar,
            width=240,
            fg_color='#6761A8',
            text_color='white',
            corner_radius=5)

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
    
    def choose_old(self):
        filename = self.choose_file()
        if filename is None:
            return
        self.old_text.set(filename[len(filename)-30:])
        self.old_file = filename

    def choose_new(self):
        filename = self.choose_file()
        if filename is None:
            return
        self.new_text.set(filename[len(filename)-30:])
        self.new_file = filename

    def choose_save_dir(self):
        directory = self.choose_path()
        if directory:
            self.dir(directory[len(directory)-30:])

    def ui(self):
        self.old_label = self.label_generator(self, self.old_text)
        self.old_label.grid(column=0, row=0, padx=5, pady=15)
        self.old_btn = self.btn_generator(self, "Open", self.choose_old)
        self.old_btn.grid(column=1, row=0, pady=15)

        self.new_label = self.label_generator(self, textvar=self.new_text)
        self.new_label.grid(column=0, row=1)
        self.new_btn = self.btn_generator(self, "Open", self.choose_new)
        self.new_btn.grid(column=1, row=1)

        self.new_label = self.label_generator(self, textvar=self.save_dir_text)
        self.new_label.grid(column=0, row=2)
        self.new_btn = self.btn_generator(self, "Save to", self.choose_path)
        self.new_btn.grid(column=1, row=2, pady=15)

        self.select = self.btn_generator(self, "Run", self.runner, '#F26430')
        self.select.grid(column=1, row=3)
        self.update()
    
    def runner(self):
        pass

if __name__ == "__main__":
    root = App()
    root.mainloop()
