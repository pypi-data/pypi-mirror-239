from tkinter import Button, Frame, Label


class UpdateButton(Button):
    def __init__(self, master, text, number, category_number, command, font="Helvetica, 10"):
        super().__init__(master=master)
        self.master = master
        self.text = text
        self.number = number
        self.category_number = category_number
        self.command = command
        self.make()
        self.image_row = 0
        self.image_column = 0
        self.image_column_span = 5
        self.font = font

    def action(self):
        self.command(self.text, self.category_number)

    def make(self):
        self.config(text=self.text, command=self.action)


class CarouselButtons:
    def __init__(self, master, current_image_number: int = 0, total_images_number: int = 0,
                 button_width: int = 3, button_height: int = 29):
        self.master = master
        self.current_image_number = current_image_number
        self.total_images_number = total_images_number

        self.left_button = Button(self.master, text="<", bg="purple", fg="white",
                                  command=self._go_left)

        self.right_button = Button(self.master, text=">", bg="purple", fg="white",
                                   command=self._go_right)

        self.button_width = button_width
        self.button_height = button_height

        self.left_button.config(width=self.button_width, height=self.button_height, font="Helvetica, 15")
        self.right_button.config(width=self.button_width, height=self.button_height, font="Helvetica, 15")

    def get_buttons(self):
        return self.left_button, self.right_button

    def _go_left(self):
        current = self.current_image_number - 1
        if current < 1:
            self.current_image_number = self.total_images_number
        else:
            self.current_image_number = current

    def _go_right(self):
        current = self.current_image_number + 1
        if current > self.total_images_number:
            self.current_image_number = 1
        else:
            self.current_image_number = current

    def provide_current_image_number(self, current_image_index: int):
        self.current_image_number = current_image_index

    def __str__(self):
        return self.current_image_number

    def __repr__(self):
        return self.current_image_number


class ActionButtons:
    def __init__(self, master, row, handle_next, handle_finish, handle_update):
        self.master = master
        self.is_done = False
        self.actions_frame = Frame(master=self.master)
        self.handle_next = handle_next
        self.handle_finish = handle_finish
        self.handle_update = handle_update
        self.row = row

    def display_action_buttons(self):
        btn_width = 20
        filler = Label(self.actions_frame)
        filler.grid(row=4, column=0)

        next_button = Button(self.actions_frame, text="Next", command=self.handle_next)
        next_button.config(width=btn_width, height=2)
        next_button.grid(row=0, column=1, columnspan=1)

        update_button = Button(self.actions_frame, text="Update", command=self.handle_update)
        update_button.config(width=btn_width, height=2)
        update_button.grid(row=0, column=3, columnspan=1)

        finish_updating_button = Button(self.actions_frame, text="Finish", command=self.handle_finish)
        finish_updating_button.config(width=btn_width, height=2)
        finish_updating_button.grid(row=0, column=5, columnspan=1)
        filler2 = Label(self.actions_frame)
        filler2.grid(row=0, column=6)
        self.actions_frame.grid(row=self.row, column=0, columnspan=10)