from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.core.window import Window

import psycopg2

Window.fullscreen = False
Window.size = (800, 800)

class splashScreen(Screen):
    pass

class mainScreen(Screen):
    def on_enter(self):
        self.myFunc()

    def myFunc(self):
        print("entering")

class mainApp(App):
    global sm
    sm = ScreenManager()

    def build(self):
        sm.add_widget(Builder.load_file("splashScreen.kv"))
        sm.add_widget(Builder.load_file("mainScreen.kv"))
        return sm

        #connect the database
        conn = psycopg2.connect(
            host = "ec2-34-234-240-121.compute-1.amazonaws.com",
            database = "d3pvstjgsdbmjp",
            user = "rmbmdpagnloizn",
            password = "c371c84f18d0b18a39d271bce2a695c6f4a2dbe4974d036cac1a86a2f5f4d076",
            port = "5432",
        )

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
        conn = psycopg2.connect(
            host = "ec2-34-234-240-121.compute-1.amazonaws.com",
            database = "d3pvstjgsdbmjp",
            user = "rmbmdpagnloizn",
            password = "c371c84f18d0b18a39d271bce2a695c6f4a2dbe4974d036cac1a86a2f5f4d076",
            port = "5432",
        )

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
        conn = psycopg2.connect(
			host = "ec2-34-234-240-121.compute-1.amazonaws.com",
            database = "d3pvstjgsdbmjp",
            user = "rmbmdpagnloizn",
            password = "c371c84f18d0b18a39d271bce2a695c6f4a2dbe4974d036cac1a86a2f5f4d076",
            port = "5432",
		)
        
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