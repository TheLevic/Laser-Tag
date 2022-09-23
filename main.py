#from curses import window
from tkinter import *
from PIL import ImageTk, Image

# function for centering the window
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

background_color = "#332B2B"
foreground_color = "white"

splash = Tk()
splash.geometry("500x500")

# Hide the title bar
splash.overrideredirect(True)

image = Image.open('logo.jpeg')
resize_image = image.resize((500,500))

logo = ImageTk.PhotoImage(resize_image)

# creating the display box
label1 = Label(image=logo)
label1.image = logo
label1.pack()

#centers splash window
center(splash)

# main function - driver
def main_window(): 
    # destroys the splash screen
    splash.destroy()
    
    # Creating the window for the player entry screen
    createGame = Tk();
    createGame.title("Photon Lasertag")
    createGame.resizable(True, True);
    createGame.configure(bg = background_color);

    #Creating the rows and columns
    Label(createGame, text="Please enter players below", bg = background_color, fg = foreground_color).grid(row=0,column=0, columnspan=2);
    #Row
    for row in range(1, 16):
        #Columns
        for column in range(0,2):
            entry = Entry(createGame, width = 30, bg = background_color, fg = foreground_color);
            entry.grid(row=row, column=column);
    
    #Create submit button
    def press():
        print("Hello");

    Button(createGame, text="Play Game", command=press, bg=background_color, fg=foreground_color).grid(row=18, column=0, columnspan=2);
    
    # Centers main window
    center(createGame)
        
        



# after 4 seconds the main function is called    
splash.after(4000, main_window)

mainloop()
