import os
from PIL import ImageTk, Image
import imghdr
from natsort import natsorted


class ImagesClass:
    def __init__(self, master, images_group_path: str, image_dims: int):
        self.master=master
        self.images_list = []
        self.images_locs_list = []

        self.image_group_path = images_group_path

        self.images_label_grid_kwargs = {
            "row": 0, "column": 1, "columnspan": 1
        }
        self.file_path = "file_path"
        self.image_label = None
        self.images_number_label = None

        self.total_number_images = 0
        self.current_image_number = 0

        self.current_image_path = ""

        self.current_image = None
        self.current_image_name = ""
        self.image_dim = image_dims

    def order_images(self):
        self.images_locs_list = natsorted(self.images_locs_list)

    def pull_image_files(self):
        self.images_locs_list = [
            os.path.join(self.image_group_path, img)
            for img in os.listdir(self.image_group_path)
            if imghdr.what(os.path.join(self.image_group_path, img))
        ]

        if len(self.images_locs_list) == 0:
            return False

        self.total_number_images = len(self.images_locs_list)
        self.order_images()

    def create_image_list(self):
        for image_loc in self.images_locs_list:
            try:
                image = ImageTk.PhotoImage(Image.open(image_loc).resize((self.image_dim, self.image_dim)))
                self.images_list.append(image)
            except OSError as err:
                if "truncated" in err:
                    os.remove(image_loc)


    def get_starting_image_data(self):
        if len(self.images_locs_list) == 0:
            return False
        self.current_image_number = len(self.images_locs_list) - (len(self.images_locs_list) // 3)
        self.current_image_path = self.images_locs_list[self.current_image_number]
        self.current_image = self.images_list[self.current_image_number]
        self.current_image_name = os.path.split(self.current_image_path)[-1]
        return True

    def get_image_data(self):
        self.pull_image_files()
        self.create_image_list()

        if self.get_starting_image_data():
            return (self.current_image_name, self.current_image_path, self.current_image, self.current_image_number,
                    self.images_list, self.images_locs_list, self.total_number_images)
        return False

    def get(self):
        return self

