from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.core.window import Window
import lib.db as db

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


        #create a cursor
        c = conn.cursor()

        values = (self.root.get_screen('mainScreen').ids.entry1.text, int(self.root.get_screen('mainScreen').ids.entry2.text))
        db.commitToDatabase(values);

        #output that the command successfully executed
        self.root.get_screen('mainScreen').ids.testBox.text = f'{self.root.get_screen("mainScreen").ids.entry1.text, self.root.get_screen("mainScreen").ids.entry2.text} added'

        #commit change to database
        conn.commit()

        #close connection to database
        conn.close()

        values = (self.root.get_screen('mainScreen').ids.entry1.text,)
        db.commitToDatabase(values)
        # list to append the values to
        values_2 = []
        #output that the command successfully executed
        self.root.get_screen('mainScreen').ids.testBox.text = f'{self.root.get_screen("mainScreen").ids.entry1.text} added'
        # print(self.root.get_screen("mainScreen").ids.entry1.text)
        for i in range(2):
            # first get the string of what it is we want to eval
            test_string = f'self.root.get_screen("mainScreen").ids.entry{i}.text'
            # print(test_string)
            # append the actaul text value of that test_string into the list
            values_2.append(eval(test_string))
        # to show that this works print the first value added into the list, which would be the first entry we get
        print(values_2[0])

    def showRecords(self):
        records = db.getAllDbValues();
        word = ''
		#loop through the returned records from our database
        for record in records:
            word = f'{word}\n{record[0]} {record[1]}'
            self.root.get_screen('mainScreen').ids.testBox.text = f'{word}'
    
    def on_start(self):
        Clock.schedule_once(self.change_screen, 3)

    def change_screen(self, dt):
        sm.current = "mainScreen"


if __name__ == '__main__':
    mainApp().run()
