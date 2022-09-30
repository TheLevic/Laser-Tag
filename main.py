from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.core.window import Window
import lib.db as db
import lib.Player as Player

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
        values = (self.root.get_screen('mainScreen').ids.name_entry0.text,)
        db.commitToDatabase(values)
        # list to append the values to
        kv_dict = {}
        # output that the command successfully executed
        self.root.get_screen(
            'mainScreen').ids.testBox.text = f'{self.root.get_screen("mainScreen").ids.name_entry0.text} added'
        for i in range(15):
            # first get the string of what it is we want to eval
            name_string = f'self.root.get_screen("mainScreen").ids.name_entry{i}.text'
            id_string = f'self.root.get_screen("mainScreen").ids.id_entry{i}.text'
            # print(name_string)
            # append the actual text value of that name_string into the list
            if eval(name_string) == "":
                break
            sub_dict = {i: {'player_name': eval(name_string), 'player_id': eval(id_string)}}
            kv_dict.update(sub_dict)
        print(kv_dict)

        
    def showRecords(self):
        records = db.getAllDbValues();
        word = ''
        # loop through the returned records from our database
        for record in records:
            word = f'{word}\n{record[0]} {record[1]}'
            self.root.get_screen('mainScreen').ids.testBox.text = f'{word}'

    def on_start(self):
        Clock.schedule_once(self.change_screen, 3)

    def change_screen(self, dt):
        sm.current = "mainScreen"


if __name__ == '__main__':
    mainApp().run()
