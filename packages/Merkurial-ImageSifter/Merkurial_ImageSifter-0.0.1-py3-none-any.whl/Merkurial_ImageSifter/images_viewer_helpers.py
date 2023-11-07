import os
import json
import shutil
from image_sifter.message_box import MessageBox


class ImageViewerFileHandler:
    def __init__(self, master = None):
        self.master = master
        self.message_box = None


    @staticmethod
    def check_for_matching_file(full_group_path: str, updated_file_path: str):
        try:
            with open(updated_file_path, "r") as fixed:
                for line in fixed.readlines():
                    line = line.strip()
                    if line.strip() == full_group_path.strip():
                        return True

        except FileNotFoundError:
            with open(updated_file_path, "w+"):
                pass

        return False

    # @staticmethod
    def get_file(self, current_group_files: list, full_group_path: str, updated_file_path: str):
        num_files = len(current_group_files)
        if num_files == 0:
            return False, 0, False
        else:

            if self.check_for_matching_file(full_group_path, updated_file_path):
                return False, num_files, False

            file_num = num_files // 3
            return current_group_files[file_num], num_files, False

    def confirm_update(self, current_group_path, new_group_path):
        message = f"From:\n\n{current_group_path}\n\nTo:\n\n{new_group_path}"
        message = f"Are You Sure You Want To Update The Directory\n\n{message}"
        box = MessageBox(master=self.master, message=message, title="Confirm Update")
        self.message_box = box
        response = box.get_response()
        self.message_box = None
        return response

    @staticmethod
    def read_json_file(current_group_json_path) -> dict:
        with open(current_group_json_path, "r+") as group_json_file:
            json_file = json.load(group_json_file)

        return json_file

    @staticmethod
    def dump_json_file(current_group_json_path, json_file):
        with open(current_group_json_path, "w+", encoding="utf-8") as group_json_file:
            print("Writing Json File")
            json.dump(json_file, group_json_file, indent=4)

        return True

    @staticmethod
    def fixed_file_update(updated_file_path, old_group_path):
        with open(updated_file_path, "a+", newline="\n") as fixed:
            fixed.write(old_group_path + "\n")
        return


    @staticmethod
    def add_updated_item_to_file(updated_file_path: str, new_group_path: str):
        with open(updated_file_path, "a+", newline="\n") as fixed:
            fixed.write(new_group_path + "\n")

    # @staticmethod
    def update_fixed_file(self, updated_file_path, old_group_path, new_group_path):
        match = False
        with open(updated_file_path, "r+") as fixed:
            # print("Reading Updated File Path")
            for line in fixed.readlines():
                line = line.strip()
                if line == old_group_path:
                    match = True
                    contents = fixed.read()

        if match:
            contents = contents.replace(old_group_path, new_group_path)

            with open(updated_file_path, "w+", newline="\n") as fixed:
                fixed.write(contents)
        else:
            self.add_updated_item_to_file(updated_file_path, new_group_path)


    @staticmethod
    def move_folder(old_path: str, new_path: str):
        try:
            print("Trying To Move Folder")
            shutil.move(old_path, new_path)

            if not os.path.isdir(new_path):
                print("The Folder Path Has Now Been Created For You :)")
            return True

        except shutil.Error:

            return False


    def update_group_data(self, root_dir, old_group_path: str, current_categories_dict: dict, current_group_json_path):
        group_name = os.path.split(old_group_path)[-1]
        new_group_path = os.path.join(root_dir, *current_categories_dict.values(),
                                      group_name)

        if self.confirm_update(old_group_path, new_group_path):

            json_file = self.read_json_file(current_group_json_path)
            print("JSON FILE: ", json_file)
            json_file["Categories"] = current_categories_dict
            json_file["Directory"] = new_group_path

            self.dump_json_file(current_group_json_path, json_file)
            if self.move_folder(old_group_path, new_group_path):
                print(f"Successfully Moved Folder To :) {new_group_path}")
                return new_group_path

        else:
            print("Update Cancelled :|")
            return False

    @staticmethod
    def populate_category_dict(current_group_path: str):
        current_group_json_path = os.path.join(current_group_path, "meta.json")
        with open(current_group_json_path, "r") as json_file_data:
            json_data = json.load(json_file_data)
        return json_data["Categories"], current_group_json_path
