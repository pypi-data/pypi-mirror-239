import _tkinter
import os
from tkinter import Button, Label, Tk
import PIL
from PIL import ImageTk, Image
from FileUtils.paths import Dir
from buttons import UpdateButton
from message_box import MessageBox
import json
import re
import shutil


class ImageViewer:
    def __init__(self, root_dir: str, category_dict: dict):
        self.root = None
        self.root_dir = root_dir

        self.category_dict = category_dict
        self.current_categories_dict = {}

        self.images_dir = None
        self.image_number = 0
        self.images_list = []
        self.image_locs = []

        self.image_carousel = Label
        self.image_row_number_display = Label
        self.file_count = 0
        self.is_updating = True
        self.left_button = Button
        self.right_button = Button
        self.total_columns = 7

        self.image_row = 0
        self.button_row = 0
        self.img_number_row = 1
        self.img_name_row = 2
        self.spacer_row = 3
        self.info_row_start = 4
        self.cat_rows_start = 5

        self.current_cats_objects = []
        self.current_file_name = ""
        self.current_group_path = ""
        self.current_full_file_path = ""
        self.current_group_json_path = ""
        self.parent_path = ""
        self.current_group_files = []
        self.UPDATED_FILE_PATH = os.path.join(self.root_dir, "fixed.txt")

        self.largest_row_num = 0
        self.walker = os.walk(self.root_dir)

        self.message_box = None

    def get_file(self):
        num_files = len(self.current_group_files)
        if num_files == 0:
            return False, 0, False
        else:
            try:
                with open(self.UPDATED_FILE_PATH, "r") as fixed:
                    for line in fixed.readlines():
                        line = line.strip()
                        if line.strip() == self.current_group_path.strip():
                            return False, num_files, False

            except FileNotFoundError:
                with open(self.UPDATED_FILE_PATH, "w+"):
                    pass

            file_num = num_files // 3
            return self.current_group_files[file_num], num_files, False

    def cleanup(self):
        self.image_number = 0
        self.current_categories_dict = {}
        self.image_carousel = Label
        self.image_row_number_display = Label
        self.images_list = []
        self.image_locs = []

        self.current_cats_objects = []
        self.current_file_name = ""
        self.current_group_path = ""
        self.current_full_file_path = ""
        self.current_group_json_path = ""
        self.parent_path = ""
        self.current_group_files = []


    def generate_images(self):
        try:
            self.image_carousel = Label(self.root, image=self.images_list[self.image_number])
        except _tkinter.TclError:
            self.root.destroy()
            return False
        self.image_row_number_display = Label(self.root, text=f"{self.image_number} of {len(self.images_list)}",
                                              font="Helvetica, 20")

        self.image_carousel.grid(row=self.image_row, column=1, columnspan=5)
        self.generate_side_buttons()
        self.image_row_number_display.grid(row=self.img_number_row, column=1, columnspan=5)

        return self

    def create_images(self):
        self.images_dir = self.current_group_path
        self.get_images()
        self.image_number = self.image_locs.index(self.current_full_file_path)
        return self.generate_images()

    def get_images(self):
        def num_sort(test_string):
            return list(map(int, re.findall(r'\d+', test_string)))[0]
        all_images = [img for img in os.listdir(self.images_dir) if img != "meta.json"]
        all_images.sort(key=num_sort)

        for image in all_images:
            full_path = os.path.join(self.images_dir, image)
            try:
                image = ImageTk.PhotoImage(Image.open(full_path).resize((700, 700)))
            except PIL.UnidentifiedImageError:
                pass
            self.image_locs.append(full_path)
            self.images_list.append(image)

    def update_image(self):
        self.display_current_file_name(self.current_file_name)
        self.image_carousel = Label(self.root, image=self.images_list[self.image_number])
        self.image_carousel.config(image=self.images_list[self.image_number])
        self.image_carousel.grid(row=self.image_row, column=1, columnspan=5)

    def update_image_text(self):
        self.image_row_number_display = Label(self.root, text=f"{self.image_number} of {len(self.images_list)}",
                                              font="Helvetica, 20")

        self.image_row_number_display.config(text=f"{str(self.image_number + 1)} of {str(len(self.images_list))}")

        self.image_row_number_display.grid(row=self.img_number_row, column=1, columnspan=5)

        current_file_loc = self.image_locs[self.image_number]
        self.current_file_name = os.path.split(current_file_loc)[-1]

    def update_image_data(self):
        self.update_image()
        self.update_image_text()

    def go_left(self):
        self.image_number -= 1
        if self.image_number < 0:
            self.image_number = len(self.images_list) - 1

        self.update_image_data()

    def go_right(self):
        self.image_number += 1
        if self.image_number > len(self.images_list) - 1:
            self.image_number = 0
        self.update_image_data()

    def generate_text_items(self):
        self.root.title(os.path.split(self.images_dir)[-1])
        self.image_carousel = Label(self.root, image=self.images_list[self.image_number])
        self.image_row_number_display = Label(self.root, text=f"Image {self.image_number} of {len(self.images_list)}",
                                              font="Helvetica, 20")

    def display_current_file_name(self, filename: str):
        current_file_name = Label(self.root, text=filename)
        current_file_name.config(font="Helvetica, 15")
        current_file_name.grid(row=self.img_name_row, rowspan=1, column=1, columnspan=5)

    def display_space(self, row_num: int,  column_num: int):
        spacer = Label(self.root, text=" ")
        spacer.config(pady=20)
        spacer.grid(row=row_num, column=column_num, columnspan=self.total_columns - 1)

    def get_category_options(self):
        category_options = []
        for cat_num in self.category_dict.keys():
            for cat in self.category_dict[cat_num]:
                options = self.category_dict[cat_num][cat]
                category_options.append(options)

        return category_options

    def display_current_categories(self):
        current_categories = []
        for cat_int, group_cat_num in enumerate(self.current_categories_dict.keys()):
            category = self.current_categories_dict[group_cat_num]
            current_categories.append(category)
            text = f"{cat_int + 1}: {category}"
            num_label = Label(self.root, text=text)
            self.current_cats_objects.append(num_label)

            num_label.config(width=20)
            num_label.grid(row=3, column=cat_int + 1, columnspan=1)
        return current_categories

    def display_all_possible_categories(self):

        btn_width = 20
        category_options = self.get_category_options()
        starting_row = 4

        def handle_update_category(this_option_text: str, this_category_int: int, this_option_int: int):
            self.current_categories_dict[str(this_category_int)] = this_option_text
            for cat_object in self.current_cats_objects:
                cat_object.destroy()
            self.current_cats_objects = []
            self.display_current_categories()

        for options_int, options in enumerate(category_options):
            for option_int, option in enumerate(options):

                row_num = starting_row + option_int
                if row_num > self.largest_row_num:
                    self.largest_row_num = row_num

                update_button = UpdateButton(self.root, option, option_int + 1, options_int + 1,
                                             handle_update_category)
                update_button.config(width=btn_width, borderwidth=1, pady=10)
                update_button.grid(row=starting_row + option_int, column=options_int + 1)
        self.display_space(self.largest_row_num+1, 0)

    def confirm_update(self, new_group_path):
        message = f"From:\n\n{self.current_group_path}\n\nTo:\n\n{new_group_path}"
        message = f"Are You Sure You Want To Update The Directory\n\n{message}"
        box = MessageBox(master=self.root, message=message, title="Confirm Update")
        self.message_box = box
        response = box.get_response()
        self.message_box = None
        print("Message Response: ", response)
        return response


    def update_group_data(self):
        image_group_dir = os.path.split(self.images_dir)[-1]
        if len(self.current_categories_dict.keys()) > 0:
            category_list = [
                self.current_categories_dict[cat_string_num] for cat_string_num in self.current_categories_dict.keys()
            ]
            if len(category_list) > 0:
                old_group_path = self.current_group_path
                new_group_path = os.path.join(self.root_dir, *category_list, image_group_dir)
                if self.confirm_update(new_group_path):
                    print("Passed Validation")
                    # if self.current_group_path != new_group_path:
                    with open(self.current_group_json_path) as group_json_file:
                        json_file = json.load(group_json_file)

                    json_file["Categories"] = self.current_categories_dict
                    json_file["Directory"] = new_group_path

                    try:
                        with open(self.current_group_json_path, "w+", encoding="utf-8") as group_json_file:
                            json.dump(json_file, group_json_file, indent=4)
                        try:
                            shutil.move(old_group_path, new_group_path)
                        except shutil.Error:
                            print("Directory Already Exists")
                            with open(self.UPDATED_FILE_PATH, "a+", newline="\n") as fixed:
                                fixed.write(old_group_path + "\n")
                            return

                        if not os.path.isdir(new_group_path):
                            print("The Folder Path Has Now Been Created For You :)")

                        match = False
                        with open(self.UPDATED_FILE_PATH, "r+") as fixed:
                            for line in fixed.readlines():
                                line = line.strip()
                                if line == old_group_path:
                                    match = True
                                    contents = fixed.read()

                        if match is True:
                            contents = contents.replace(old_group_path, new_group_path)
                            with open(self.UPDATED_FILE_PATH, "w+", newline="\n") as fixed:
                                fixed.write(contents)
                        else:
                            with open(self.UPDATED_FILE_PATH, "a+", newline="\n") as fixed:
                                fixed.write(new_group_path + "\n")

                        print(f"Successfully Moved Folder To :) {new_group_path}")

                    except Exception as err:
                        print("err: ", err)
                        print(f"Move To: {new_group_path} Was Unsuccessful :(")
                        pass
                else:
                    print("Update Cancelled :|")
                    return False
            return False
        else:
            return False

    def display_action_buttons(self):
        def handle_next():
            self.root.destroy()
            self.cleanup()

        def handle_finish():
            self.is_updating = False
            if self.message_box:
                self.message_box.response = False
                self.cleanup()

            else:
                self.root.destroy()
            # exit(0)

        def handle_update():
            self.update_group_data()
            handle_next()

        btn_width = 20
        next_button = Button(self.root, text="Next", command=handle_next)
        next_button.config(width=btn_width, height=2)
        next_button.grid(row=self.largest_row_num + 3, column=1, columnspan=1)

        update_button = Button(self.root, text="Update", command=handle_update)
        update_button.config(width=btn_width, height=2)
        update_button.grid(row=self.largest_row_num + 3, column=3, columnspan=1)

        finish_updating_button = Button(self.root, text="Finish", command=handle_finish)
        finish_updating_button.config(width=btn_width, height=2)
        finish_updating_button.grid(row=self.largest_row_num + 3, column=5, columnspan=1)

    def generate_side_buttons(self):
        width = 3
        height = 29
        self.left_button = Button(self.root, text="<", bg="purple", fg="white",
                                  command=self.go_left)

        self.right_button = Button(self.root, text=">", bg="purple", fg="white",
                                   command=self.go_right)

        self.left_button.config(width=width, height=height, font="Helvetica, 15")
        self.right_button.config(width=width, height=height, font="Helvetica, 15")
        self.left_button.grid(row=self.button_row, column=1)
        self.right_button.grid(row=self.button_row, column=5)

    def populate_category_dict(self):
        self.current_group_json_path = os.path.join(self.current_group_path, "meta.json")
        with open(self.current_group_json_path, "r") as json_file_data:
            json_data = json.load(json_file_data)
        return json_data["Categories"], self.current_group_json_path

    def create_text(self):
        self.generate_text_items()
        self.display_space(self.spacer_row, 0)
        self.display_current_file_name(self.current_file_name)

    def show_category_info(self):
        self.display_current_categories()
        self.display_all_possible_categories()

    def generate_starting_data(self):
        self.current_categories_dict, self.current_group_json_path = self.populate_category_dict()
        self.current_full_file_path = os.path.join(self.current_group_path, self.current_file_name)

    def next_step(self):
        self.current_group_path, _, self.current_group_files = next(self.walker)
        if len(self.current_group_files) > 2:
            return True
        else:
            return False

    def image_sifter(self):
        if Dir(self.root_dir).check_is_dir():
            while self.is_updating:

                self.root = Tk()
                self.root.geometry("1000x1200+1000+0")
                if self.next_step():
                    self.current_file_name, num_files, all_done = self.get_file()
                    if self.current_file_name:
                        self.file_count += num_files
                        self.generate_starting_data()
                        print("Current Working Group Dir: ", self.current_group_path)
                        if self.create_images():
                            self.create_text()
                            self.show_category_info()
                            self.display_action_buttons()
                            if not self.is_updating:
                                self.root.destroy()
                                break
                            else:
                                self.root.update_idletasks()
                                self.root.update()
                        else:
                            self.cleanup()

                    else:
                        self.root.destroy()
                else:
                    self.root.destroy()
                self.root.mainloop()


