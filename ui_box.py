import tkinter as tk


class ui_box:
    root = tk.Tk()
    widthpixels=130
    heightpixels=25
    root.geometry('{}x{}'.format(widthpixels, heightpixels))
    root.configure(background="green")
    label = tk.Label(root,text='Listening',width=10,anchor=tk.W,bg='green', fg = "white",font='Mincho 10')
    label.pack()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    
    def ready(self):
        self.root.lift()
        self.root.configure(background = "green")
        self.label.config(text='Listening!')
        self.label.config(bg = "green")
        self.root.attributes("-topmost", True)
    
    def busy(self):
        self.root.configure(background = "red")
        self.label.config(text='analysing...')
        self.label.config(bg = "red")
        self.root.lift()
        self.root.attributes("-topmost", True)

