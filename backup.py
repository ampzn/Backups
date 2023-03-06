import os
import shutil
import hashlib
import pickle
import datetime
import prettytable


class Backup:
    
    def __init__(self, source_dir, dest_drive_letter):
        self.src_dir = source_dir
        self.dest_drive_letter = dest_drive_letter
        self.dest_drive = f"{self.dest_drive_letter}:\\"
        self.timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
        self.backup_folder = os.path.join(
            self.dest_drive, "Backup", datetime.date.today().isoformat())
        self.backup_file = os.path.join(self.backup_folder, "backup.pkl")
        self.files = {}

        try:
            with open(self.backup_file, "rb") as f:
                self.files, self.last_backup = pickle.load(f)
        except FileNotFoundError:
            self.files = {}
            self.last_backup = None


    def backup(self):
        self._update_files()

        if self.last_backup is not None:
            print(f"Creating incremental backup since {self.last_backup}...")
            self._backup_incremental()
        else:
            print("Creating full backup...")
            self._backup_full()

        with open(self.backup_file, "wb") as f:
            pickle.dump((self.files, datetime.datetime.now()), f)

        print("Backup completed successfully.")

    def _update_files(self):
        for root, dirs, files in os.walk(self.src_dir):
            for name in files:
                path = os.path.join(root, name)
                with open(path, "rb") as f:
                    checksum = hashlib.md5(f.read()).hexdigest()
                self.files[path] = checksum

    def _backup_full(self):
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder)
        for path in self.files:
            try:
                dest_path = os.path.join(self.backup_folder, os.path.relpath(path, self.src_dir))
                shutil.copy2(path, dest_path)
            except Exception as e:
                print(f"Failed to copy {path}. Error: {str(e)}")


    def _backup_incremental(self):
        logs_dir = os.path.join(self.backup_folder, "logs")
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        for path, checksum in self.files.items():
            dest_path = path.replace(self.src_dir, logs_dir)
            if os.path.exists(path) and (not os.path.exists(dest_path) or self.files[path] != self._get_checksum(dest_path)):
                shutil.copy2(path, dest_path)


    def _get_checksum(self, path):
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

if __name__ == "__main__":
    source_dir = input("Enter the source directory: ")
    dest_drive = input("Enter the destination drive path: ")
    backup = Backup(source_dir, dest_drive)

    def print_backup_data():
        with open(backup.backup_file, "rb") as f:
            backup_data = pickle.load(f)

        files_table = prettytable.PrettyTable()
        files_table.field_names = ["File Path", "Checksum"]

        for file_path, checksum in backup_data[0].items():
            files_table.add_row([file_path, checksum])

        print("Last backup:", backup_data[1])
        print("Backup directory:", backup.backup_folder)

        print("Files:")
        print(files_table)

    backup.backup()
    print_backup_data()

    """ def clear_backup_file():
        with open(backup.backup_file, "wb") as f:
            pickle.dump((), f) """
