from tkinter import Frame, Label, LEFT, W
from buttons import UpdateButton
from carousel_helpers import TkSpacer



class CarouselText:
    def __init__(self, master, font="Helvetica, 12"):
        self.master = master
        self.bg = "grey"
        self.border_frame = Frame(self.master, background=self.bg)
        self.font = font

        self.container = Frame(self.border_frame, background=self.bg)
        self.container.config(borderwidth=2)

        self.image_name = "Empty"
        self.image_counts = ""
        self.current_image_number = 0
        self.total_images = 0

        self.name_label = None
        self.counts_label = None

    def generate_text(self):
        if self.name_label is None or self.counts_label is None:
            self.name_label = Label(self.container, text=self.image_name, bg=self.bg, anchor=W, font=self.font)
            self.counts_label = Label(self.container, text=self.image_counts, bg=self.bg, anchor=W, font=self.font)

            self.name_label.config(justify=LEFT)
            self.counts_label.config(justify=LEFT)

            self.name_label.grid(row=1, column=0, columnspan=8, sticky=W)
            self.counts_label.grid(row=0, column=0, columnspan=8)


        else:
            self.name_label.configure(text=self.image_name)
            self.counts_label.configure(text=self.image_counts)

    def get_text(self, image_name: str, current_image_number: str | int, total_images: str | int):
        self.image_name = image_name
        self.current_image_number = current_image_number
        self.total_images = total_images
        self.image_counts = f"Image {self.current_image_number} | {self.total_images}"
        self.container.pack()
        self.generate_text()


class OptionsDisplay:
    def __init__(self, master, row, font="Helvetica, 10"):
        self.master = master
        self.options_frame = None
        self.current_categories_frame = None
        self.all_categories_frame = None

        self.saved_category_labels_for_updating = []

        self.font = font

        self.all_categories_dict = {}

        self.current_categories_dict = {}

        self.saved_categories_for_updating = []

        self.current_categories = []

        self.category_options = None

        self.largest_row_num = 0
        self.row = row
        self.all_categories_row_num = 0

        self.item_width = 20

    def display_all(self):
        self.display_current_categories()
        self.display_all_possible_categories()


    def clean(self):
        self.current_categories_dict = {}
        self.all_categories_dict = {}
        self.saved_categories_for_updating = []
        self.category_options = []
        self.options_frame = Frame(self.master)
        self.current_categories_frame = Frame(self.options_frame)
        self.all_categories_frame = Frame(self.options_frame)
        self.current_categories_frame.config(pady=10)
        self.all_categories_frame.config(pady=10)

    def populate(self, current_categories_dict: dict, all_categories_dict: dict):
        self.clean()
        self.current_categories_dict = current_categories_dict
        self.all_categories_dict = all_categories_dict
        self.saved_categories_for_updating = [self.current_categories_dict[cat_num]
                                              for cat_num in self.current_categories_dict.keys()]
        self.get_all_category_options()
        self.options_frame.grid(row=self.row, column=0, columnspan=10)
        self.display_all()
        return self.saved_categories_for_updating, self.current_categories_dict

    def get_all_category_options(self):
        self.category_options = []
        for cat_num in self.all_categories_dict.keys():
            for cat in self.all_categories_dict[cat_num]:
                options = self.all_categories_dict[cat_num][cat]
                self.category_options.append(options)

    def display_current_categories(self):
        for cat_int, group_cat_num in enumerate(self.current_categories_dict.keys()):
            category = self.current_categories_dict[group_cat_num]
            self.current_categories.append(category)
            text = f"{cat_int + 1}: {category}"
            num_label = Label(self.current_categories_frame, text=text)
            num_label.config(width=23, justify="center", font=self.font)

            num_label.grid(row=0, column=cat_int, columnspan=1)

            self.all_categories_row_num += 1
            self.saved_category_labels_for_updating.append(num_label)

        self.current_categories_frame.grid(row=0, column=0, columnspan=10)



    def handle_update_category(self, this_option_text: str, this_category_int: int):
        new_category = f"{this_category_int}: {this_option_text}"
        self.current_categories_dict[str(this_category_int)] = this_option_text
        for cat_object in self.saved_category_labels_for_updating:
            label_text = cat_object.cget("text").strip()
            if str(this_category_int) == label_text[0]:
                self.current_categories_dict[str(this_category_int)] = this_option_text
                cat_object.configure(text=new_category)
                break

    def display_all_possible_categories(self):
        starting_row = 0
        self.largest_row_num = self.all_categories_row_num
        for options_int, options in enumerate(self.category_options):
            for option_int, option in enumerate(options):
                row_num = starting_row + option_int
                if row_num > self.largest_row_num:
                    self.largest_row_num = row_num
                update_button = UpdateButton(self.all_categories_frame, option, option_int + 1, options_int + 1,
                                             self.handle_update_category)

                update_button.config(width=self.item_width, borderwidth=1, pady=10)

                update_button.grid(row=starting_row + option_int, column=options_int + 1)
        self.all_categories_frame.grid(row=1, column=0, columnspan=10)
        spacer = TkSpacer(self.options_frame, pady=10)
        spacer.grid(row=2, column=0, columnspan=10)




