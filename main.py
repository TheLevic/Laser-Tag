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
sm = ScreenManager()


class splashScreen(Screen):
    pass


class mainScreen(Screen):
    def myFunc(self):
        print("entering")


class mainApp(App):
    def build(self):
        sm.add_widget(Builder.load_file("kv/splashScreen.kv"))
        sm.add_widget(Builder.load_file("kv/mainScreen.kv"))
        return sm

    def submit(self):
        values = (self.root.get_screen('mainScreen').ids.entry1.text,)
        db.commitToDatabase(values);

        #output that the command successfully executed
        self.root.get_screen('mainScreen').ids.testBox.text = f'{self.root.get_screen("mainScreen").ids.entry1.text} added'

    def showRecords(self):
        records = db.getAllDbValues();
        word = ''
		#loop through the returned records from our database
        for record in records:
            word = f'{word}\n{record[0]}'
            self.root.get_screen('mainScreen').ids.testBox.text = f'{word}'
    
    def on_start(self):
        Clock.schedule_once(self.change_screen, 3)

    def change_screen(self, dt):
        sm.current = "mainScreen"


if __name__ == '__main__':
    mainApp().run()