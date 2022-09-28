from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.core.window import Window
import lib.db as db

import psycopg2

Window.fullscreen = False
Window.size = (800, 800)

class splashScreen(Screen):
    pass

class mainScreen(Screen):
    def myFunc(self):
        print("entering")

class mainApp(App):
    global sm
    sm = ScreenManager()

    def build(self):
        sm.add_widget(Builder.load_file("kv/splashScreen.kv"))
        sm.add_widget(Builder.load_file("kv/mainScreen.kv"))
        return sm

        #connect the database
        conn = db.connectToDatabase();

        #create a cursor
        c = conn.cursor()

        #create a table
        #c.execute("""CREATE TABLE if not exists temp (name TEXT);""")

        #commit changes
        #conn.commit()

        #close connection to database
        conn.close()

        return Builder.load_file(mainScreen.kv)

    def submit(self):
        conn = db.connectToDatabase();

        #create a cursor
        c = conn.cursor()

        #command used to insert name into database
        sql_command = "INSERT INTO temp (name) VALUES (%s)"
        values = (self.root.get_screen('mainScreen').ids.entry1.text,)

        #execute command
        c.execute(sql_command, values)

        #output that the command successfully executed
        self.root.get_screen('mainScreen').ids.testBox.text = f'{self.root.get_screen("mainScreen").ids.entry1.text} added'

        #commit change to database
        conn.commit()

        #close connection to database
        conn.close()

    def showRecords(self):
        conn = db.connectToDatabase();
        
		#create a cursor
        c = conn.cursor()
		
		#retreive records from database
        c.execute("SELECT * FROM temp")
        records = c.fetchall()

        word = ''
		#loop through records in database
        for record in records:
            word = f'{word}\n{record[0]}'
            self.root.get_screen('mainScreen').ids.testBox.text = f'{word}'

		#commit changes to database
        conn.commit()

		#close connection to database
        conn.close()
    
    def on_start(self):
        Clock.schedule_once(self.change_screen, 3)
    
    def change_screen(self, dt):
        sm.current = "mainScreen"
        
if __name__ == '__main__':
    mainApp().run()