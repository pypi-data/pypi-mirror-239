import os
from tkinter import Tk
from Paths import Dir
from carousel import Carousel
from buttons import ActionButtons
from carousel_text import OptionsDisplay
from images_viewer_helpers import ImageViewerFileHandler


class ImageViewer:
    def __init__(self, root_dir: str, category_dict: dict):
        # GLOBALS UNCHANGED
        self.main = Tk()
        self.root_dir = root_dir
        self.width = 1000
        self.height = 1200
        self.image_width = 600
        self.total_columns = 5
        self.total_rows = 4
        self.category_dict = category_dict
        self.UPDATED_FILE_PATH = os.path.join(self.root_dir, "fixed.txt")
        self.walker = os.walk(self.root_dir)
        self.files = ImageViewerFileHandler(self.main)

        self.group_count = 0
        self.file_count = 0
        self.is_updating = True
        self.is_done = False

        # Helper Classes
        self.message_box = None
        self.carousel = Carousel(self.main, row=0, image_width=self.image_width)
        self.options = None
        self.actions = ActionButtons(self.main, 5, self.handle_next, self.handle_finish, self.handle_update)

        # Group File Data
        self.parent_path = ""
        self.current_categories_dict = {}
        self.current_cats_objects = []
        self.current_file_name = ""
        self.current_group_path = None
        self.starting_group_path = None
        self.current_full_file_path = ""
        self.current_group_json_path = ""
        self.current_num_files = 0
        self.current_group_files = []
        self.current_group_name = ""

    def handle_next(self):
        self.is_done = True
        self.cleanup()

    def handle_finish(self):
        self.is_updating = False
        self.is_done = True
        if self.message_box:
            self.message_box.response = False
            self.cleanup()

        else:
            self.main.destroy()

    def handle_update(self):
        self.is_done = True
        self.update_group_data()
        self.handle_next()

    def cleanup(self):
        self.current_categories_dict = {}

    def get_file_data(self):
        self.current_group_json_path = os.path.join(self.starting_group_path, "meta.json")
        self.current_group_name = os.path.split(self.starting_group_path)[-1]

        self.current_file_name, self.current_num_files, all_done = \
            self.files.get_file(self.current_group_files, self.starting_group_path, self.UPDATED_FILE_PATH)
        if all_done:
            self.is_updating = False

    def update_group_data(self):
        self.current_group_path = self.files.update_group_data(self.root_dir,
                                                               self.starting_group_path,
                                                               self.current_categories_dict,
                                                               self.current_group_json_path)

        if self.current_group_path:
            self.files.update_fixed_file(self.UPDATED_FILE_PATH, self.starting_group_path, self.current_group_path)

    def generate_starting_data(self):
        self.current_categories_dict, self.current_group_json_path = \
            self.files.populate_category_dict(self.starting_group_path)
        self.current_full_file_path = os.path.join(self.starting_group_path, self.current_file_name)

    def next_step(self):
        try:
            self.starting_group_path, _, self.current_group_files = next(self.walker)
            if "meta.json" in self.current_group_files:
                return True
            else:
                return False
        except StopIteration:
            print("All Images Have Been Updated.")
            self.cleanup()
            self.main.destroy()
            return exit(0)

    def image_sifter(self):
        if Dir(self.root_dir).check_is_dir():
            self.carousel.generate()
            self.actions.display_action_buttons()
            while self.is_updating:
                if self.next_step():
                    self.get_file_data()
                    if self.current_file_name:
                        current_image = self.carousel.provide_group_path(self.starting_group_path)
                        if current_image:

                            self.file_count += self.current_num_files
                            self.generate_starting_data()

                            (self.current_image_name, self.current_image_path, self.current_image,
                             self.current_image_number, self.images_list, self.images_locs_list,
                             self.total_number_images) = current_image
                            # print("Main Current Group", self.starting_group_path)
                            # print("Main Current Image: ", self.current_file_name)
                            # print("Current Image Path: ", self.current_image_path)

                            self.options = OptionsDisplay(self.main, 4)

                            saved_categories, self.current_categories_dict = \
                                self.options.populate(self.current_categories_dict, self.category_dict)

                            self.is_done = False
                            while not self.is_done:
                                self.carousel.update_image()
                                self.carousel.carousel_frame.update()
                                self.carousel.carousel_frame.update_idletasks()

                        else:
                            self.cleanup()
                if not self.is_updating:
                    self.main.destroy()
                self.main.update()
                self.main.update_idletasks()
        self.main.mainloop()
