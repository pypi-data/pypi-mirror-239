import os
from tkinter import Label, Frame, Canvas
from file_handlers import ImagesClass
from buttons import CarouselButtons
from carousel_text import CarouselText


class Carousel:
    def __init__(self, master, row: int, carousel_width: int = 200, image_width: int = 700):
        # Basics
        self.image_group_path = ""
        self.image_group_name = ""
        self.image_data = None
        self.width = carousel_width
        self.image_width = image_width
        self.row = row

        # Widgets
        self.master = master
        self.carousel_frame = Frame(self.master, bg="black")
        self.carousel_frame.config(width=self.width)
        self.picture_frame = Canvas(self.carousel_frame, bg="black")

        # Image Data
        self.images_list = []
        self.images_locs_list = []

        self.current_image_index = 0
        self.total_number_images = 0
        self.current_image_label = None
        self.image_row_number_display = ""
        self.current_image_name = "Empty"

        # self.start()
        self.buttons = CarouselButtons(self.carousel_frame, self.current_image_index)
        self.left_button, self.right_button = self.buttons.get_buttons()
        button_width = (self.width - self.image_width) // 2
        self.left_button.config(width=button_width)
        self.right_button.config(width=button_width)

        self.images_number_label = None
        self.image_name_label = None

        # Current Image In Use
        self.current_image = None
        self.current_image_path = None

        # Other
        self.images_label_grid_kwargs = {
            "row": 0, "column": 1, "columnspan": 1
        }

        self.is_looking = False

        self.carousel_text = CarouselText(self.carousel_frame)

    def generate_current_image(self):
        self.current_image = self.images_list[self.current_image_index]
        self.current_image_label = Label(self.picture_frame, image=self.current_image)
        self.current_image_label.grid(row=0, column=0)


    def clean(self):
        # Current Image In Use
        self.current_image = None
        self.current_image_path = None
        self.current_image_index = 0
        self.total_number_images = 0
        self.current_image_label = None
        self.image_row_number_display = ""
        self.current_image_name = "Empty"
        self.image_data = None

        self.images_list = []
        self.images_locs_list = []
        self.image_group_name = ""

    def provide_group_path(self, image_group_path: str | None = None):
        self.clean()
        if not os.path.isdir(image_group_path):
            raise NotADirectoryError(f"{image_group_path} is not a directory")

        self.image_group_path = image_group_path
        self.image_group_name = os.path.split(self.image_group_path)[-1]
        self.master.title(self.image_group_name)

        if self.pull_all_images_data():
            self.current_image_index = len(self.images_locs_list) - (len(self.images_locs_list) // 3)
            # Give Button Number of Images
            self.buttons.total_images_number = self.total_number_images

            # Update Button Number To Make Sure It Is Inline With Carousel
            self.buttons.current_image_number = self.current_image_index + 1

            self.current_image_path = self.images_locs_list[self.current_image_index]
            self.current_image = self.images_list[self.current_image_index]

            self.generate_current_image()

            self.carousel_text.get_text(self.current_image_name, self.buttons.current_image_number,
                                        self.total_number_images)

            if self.current_image:
                return (self.current_image_name, self.current_image_path, self.current_image,
                        self.current_image_index, self.images_list, self.images_locs_list,
                        self.total_number_images)
        return False

    def pull_all_images_data(self):
        self.image_data = ImagesClass(self.picture_frame, self.image_group_path, self.image_width)
        image_data = self.image_data.get_image_data()
        if image_data:
            (self.current_image_name, self.current_image_path, self.current_image, self.current_image_index,
             self.images_list, self.images_locs_list, self.total_number_images) = image_data


            return True
        else:
            return False

    def generate_carousel(self):
        self.left_button.grid(row=0, column=0)
        self.picture_frame.grid(row=0, column=1, sticky="news")
        self.right_button.grid(row=0, column=2)
        self.carousel_frame.grid(row=self.row, column=1, columnspan=8)
        self.carousel_text.border_frame.grid(row=1, column=0, columnspan=8, sticky="news")
        # self.carousel_text.container.grid_columnconfigure(1, weight=1)

        current_image_number = self.current_image_index + 1 if self.total_number_images > 0 else 0
        current_number_images = self.total_number_images + 1 if self.total_number_images > 0 else 0
        self.carousel_text.get_text(self.current_image_name, current_image_number, current_number_images)

    def generate(self):
        self.generate_carousel()

    def update_image(self):
        if self.buttons.current_image_number != self.current_image_index + 1:
            # Update The Index To The Proper Position
            self.current_image_index = self.buttons.current_image_number - 1

            # Update Image And Accompanying Text
            self.current_image_path = self.images_locs_list[self.current_image_index]

            self.current_image_name = os.path.split(self.current_image_path)[-1]

            self.carousel_text.get_text(self.current_image_name, self.buttons.current_image_number,
                                        self.total_number_images)

            # Update Current Image To That Of The Index The Buttons Provided
            self.current_image = self.images_list[self.current_image_index]
            self.current_image_label.configure(image=self.current_image)