from curses import window
from tkinter import *
from PIL import ImageTk, Image

background_color = "#332B2B"

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
    Label(createGame, text="Please enter players below", bg = background_color, fg="white").grid(row=0,column=0, columnspan=2);
    #Row
    for row in range(1, 16):
        #Columns
        for column in range(0,2):
            entry = Entry(createGame, width = 30, bg = background_color, fg="white");
            entry.grid(row=row, column=column);
    
    #Create submit button
    def press():
        print("Hello");

    Button(createGame, text="Play Game", command=press).grid(row=18, column=0, columnspan=2);
        
        



# after 4 seconds the main function is called    
splash.after(4000, main_window)

mainloop()
