from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.core.window import Window

Window.fullscreen = False
Window.size = (800, 800)

class splashScreen(Screen):
    pass

class mainScreen(Screen):
    def onPress(self):
        print("Hello");

class mainApp(App):
    global sm
    sm = ScreenManager()
    
    def build(self):
        sm.add_widget(Builder.load_file("splashScreen.kv"))
        sm.add_widget(Builder.load_file("mainScreen.kv"))
        return sm
    
    def on_start(self):
        Clock.schedule_once(self.change_screen, 3)
    
    def change_screen(self, dt):
        sm.current = "mainScreen"

    

if __name__ == '__main__':
    mainApp().run()