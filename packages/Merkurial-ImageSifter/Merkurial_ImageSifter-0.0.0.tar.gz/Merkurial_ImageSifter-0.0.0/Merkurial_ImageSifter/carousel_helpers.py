from tkinter import Label


class TkSpacer(Label):
    def __init__(self, master, pady=5):
        self.master = master
        self.pady = pady
        super().__init__(master=self.master, text=" ")
        self.config(pady=self.pady)


    def place(self, row, column, columnspan=1, rowspan=1):
        self.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan)
