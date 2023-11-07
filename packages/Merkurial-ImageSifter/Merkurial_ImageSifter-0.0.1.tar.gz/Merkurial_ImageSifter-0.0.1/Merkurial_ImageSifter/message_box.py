from tkinter import Toplevel, Button, Label, Tk


class MessageBox:
    # box_bg = "#DFD3D1"
    box_bg = "pink"
    box_fg = "black"
    message_bg = "green"
    message_fg = "red"
    box_width = 600
    box_height = 400
    box_font_size = 15
    button_height = 10
    button_width = 50
    button_bg = "purple"
    button_fg = "white"
    font = "Helvetica"

    def __init__(self, master: Tk, message: str, title: str):
        self.response = None
        self.master = master
        # self.box_width = self.master.winfo_width()

        self.box = Toplevel(self.master, bg=self.box_bg)
        self.box.geometry(f"{self.box_width}x{self.box_height}")
        self.box.title(title)

        self.current_box_height = self.box_height
        self.current_box_width = self.box.winfo_width()

        self.message = message
        self.message_label = Label(master=self.box, text=self.message, font=(self.font, self.box_font_size),
                                   bg=self.message_bg, fg=self.message_fg, justify="left", anchor="center"
                                   )

        self.current_message_box_width = self.message_label.winfo_width()

        self.yes_button = Button(master=self.box, text="Yes", command=self.handle_yes, font=(self.font, 20),
                                 bg=self.button_bg, fg=self.button_fg
                                 )

        self.no_button = Button(master=self.box, text="No", command=self.handle_no, font=(self.font, 20),
                                bg=self.button_bg, fg=self.button_fg
                                )

        # self.message_label.config(wraplength=self.box_width, padx=10, pady=10)
        self.message_label.pack()
        self.yes_button.pack(side="left", expand=True)
        self.no_button.pack(side="right", expand=True)
        self.center_box()

    def generate_items(self):
        self.message_label = Label(master=self.box, text=self.message, font=(self.font, 20), bg=self.message_bg,
                                   fg=self.message_fg
                                   )

        self.yes_button = Button(master=self.box, text="Yes", command=self.handle_yes, font=(self.font, 7),
                                 bg=self.button_bg, fg=self.button_fg
                                 )



        self.no_button = Button(master=self.box, text="No", command=self.handle_no, font=(self.font, 7),
                                bg=self.button_bg, fg=self.button_fg
                                )

    # def configure_items(self):
    #     self.message_label.config(height=self.box_height // 25, width=self.box_width // 11, wraplength=self.box_width)

    def display_items(self):
        self.message_label.grid(row=0, column=0, rowspan=1, columnspan=2, sticky="nsew")
        self.yes_button.grid(row=1, column=0, columnspan=1, sticky="nsew")
        self.no_button.grid(row=1, column=1, columnspan=1, sticky="nsew")

    def center_box(self):
        x = self.master.winfo_x() + self.master.winfo_width()//2 - self.box.winfo_width()//2
        # y = self.master.winfo_y() + self.master.winfo_height()//2 - self.box.winfo_height()//2
        self.box.geometry(f"{self.box_width}x{self.box_height}+{x}+{self.box_height+300}")

    def handle_yes(self):
        self.response = True
        self.box.destroy()
        print("Response changed to True")

    def handle_no(self):
        self.response = False
        self.box.destroy()
        print("Response changed to False")

    def get_response(self):
        while self.response is None:
            self.box.update()
        return self.response
