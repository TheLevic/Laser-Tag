from tkinter import *
from PIL import ImageTk, Image
root = Tk()
root.geometry("500x500")

# Hide the title bar
root.overrideredirect(True)

image = Image.open('logo.jpeg')
resize_image = image.resize((500,500))

logo = ImageTk.PhotoImage(resize_image)

# creating the display box
label1 = Label(image=logo)
label1.image = logo
label1.pack()

# main function - driver
def main_window(): 
    # destroys the splash screen
    root.destroy()
    
    #add your code below this comment

# after 4 seconds the main function is called    
root.after(4000, main_window)

mainloop()
