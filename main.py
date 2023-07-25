import os
import tempfile

from ui import UI
import convert



class App(UI):
    OLD_DEFAULT = 'Choose old pdf file'
    NEW_DEFAULT = 'Choose new pdf file'
    DEFAULT_DIR = str(convert.RESULT_DIFF)

    def __init__(self):
        super().__init__()
        self.title("PDF-differ")

    def choose_old(self):
        filename = self.choose_file()
        if filename is None:
            return
        self.old_text.set(self.text_manager(filename))
        self.old_file = filename

    def choose_new(self):
        filename = self.choose_file()
        if filename is None:
            return
        self.new_text.set(self.text_manager(filename))
        self.new_file = filename

    def choose_save_dir(self):
        directory = self.choose_path()
        if directory is None:
            return
        self.save_dir_text.set(self.text_manager(directory))
        self.save_dir = directory

    def perform_check_files(self):
        if self.old_file == self.OLD_DEFAULT:
            return self.err_msg("Error", "Not choose old pdf file")
        if self.new_file == self.NEW_DEFAULT:
            return self.err_msg("Error", "Not choose new pdf file")
    
    def get_save_folder(self):
        if self.save_dir == self.DEFAULT_DIR:
            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)
        else:
            if not os.path.exists(self.save_dir):
                return self.err_msg("Error", "Save dir doesn't exist")
        return self.save_dir

    def runner(self):
        self.perform_check_files()
        folder = self.get_save_folder()
        old_tmp = tempfile.mkdtemp()
        new_tmp = tempfile.mkdtemp()
        convert.convert(self.old_file, old_tmp)
        convert.convert(self.new_file, new_tmp)
        convert.diff_all(old_tmp, new_tmp, folder)


if __name__ == "__main__":
    root = App()
    root.mainloop()
