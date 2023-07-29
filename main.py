import os
import json
import tempfile
from typing import Tuple

from ui import MainUI, SettingsUI
import convert


class App(MainUI):
    OLD_DEFAULT = 'Choose old pdf file'
    NEW_DEFAULT = 'Choose new pdf file'
    DEFAULT_DIR = str(convert.RESULT_DIFF)
    CONFIG_FILE = 'config.json'

    def __init__(self):
        super().__init__()
        # Path to the files
        self.old_file = self.OLD_DEFAULT
        self.new_file = self.NEW_DEFAULT
        # Path to save directory
        self.save_dir = self.DEFAULT_DIR
        # Set texts on labels

        self.old_text = self.text(self, self.text_manager(self.old_file))
        self.new_text = self.text(self, self.text_manager(self.new_file))
        self.save_dir_text = self.text(self, self.text_manager(self.DEFAULT_DIR))
        self.ui()

        with open(self.CONFIG_FILE, 'r') as f:
            self.config = json.load(f)

        self.title("PDF-differ")
        self.set_default()

    def set_default(self):
        old = self.config.get('old_default', '')
        if old  == '':
            old = self.OLD_DEFAULT
        self.old_file = old
        self.old_text.set(self.text_manager(old))

    def choose_old(self):
        filename = self.choose_file()
        if filename == '':
            return
        self.old_text.set(self.text_manager(filename))
        self.old_file = filename

    def choose_new(self):
        filename = self.choose_file()
        if filename == '':
            return
        self.new_text.set(self.text_manager(filename))
        self.new_file = filename

    def choose_save_dir(self):
        directory = self.choose_path()
        if directory == '':
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
    
    def deactivate_btn(self):
        self.old_btn._state = 'disabled'
        self.new_btn._state = 'disabled'
        self.select._state = 'disabled'
        self.settings_btn._state = 'disabled'

    def activate_btn(self):
        self.old_btn._state = 'active'
        self.new_btn._state = 'active'
        self.select._state = 'active'
        self.settings_btn._state = 'active'

    def run_settings(self):
        if not self.settings_runner:
            Settings(master=self)
            self.deactivate_btn()

    def runner(self):
        self.perform_check_files()
        folder = self.get_save_folder()
        old_tmp = tempfile.mkdtemp()
        new_tmp = tempfile.mkdtemp()
        convert.convert(self.old_file, old_tmp)
        convert.convert(self.new_file, new_tmp)
        convert.diff_all(old_tmp, new_tmp, folder)
        self.info_msg("Success", "Diff files has been created")


class Settings(SettingsUI):
    def __init__(self, *args, master: App, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, master=master, fg_color=fg_color, **kwargs)
        self.master = master
        self.title('PDF-differ settings')
        self.default_old_text = self.set_default_old_text()
        self.default_old = self.master.old_file
        self.ui()


    def destroy(self):
        self.master.set_default()
        self.master.activate_btn()
        return super().destroy()

    def set_default_old_text(self):
        if self.master.old_file == self.master.OLD_DEFAULT:
            text = "/"
        else:
            text = self.master.old_file
        return self.master.text(self, self.master.text_manager(text))

    def update_config(self):
        with open(self.master.CONFIG_FILE, 'w') as f:
            json.dump(self.master.config, f, indent=4)

    def choose_default_old_file(self):
        filename = self.choose_file()
        if filename == '':
            return
        if filename != self.master.config.get('old_default', ''):
            self.default_old_text.set(self.text_manager(filename))
            self.default_old = filename

    def save(self):
        if self.default_old != self.master.OLD_DEFAULT:
            if self.default_old != self.master.config.get('old_default', ''):
                self.master.config['old_default'] = self.default_old
        self.update_config()
        self.destroy()


if __name__ == "__main__":
    root = App()
    root.mainloop()
