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



# class Window(Tk):
#     def __init__(self):
#         super().__init__()
#
#     def inside(self):
#
#         self.mainloop()
