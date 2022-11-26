from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.core.window import Window
import lib.db as db
from lib.Player import Player

Window.fullscreen = False
Window.size = (800, 800)
sm = ScreenManager()
switchScreens = False
createdNest = True


class splashScreen(Screen):
    pass


class playActionDisplay(Screen):
    pass


class mainScreen(Screen):
    pass


class keyboardInput(Screen):
    def __init__(self, **kwargs):
        super(keyboardInput, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.switchScreens = False
    
    def _keyboard_closed(self):
        pass

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'f5':
            self.switchScreens = not self.switchScreens
            if self.switchScreens is False:
                sm.current = "mainScreen"
            if self.switchScreens is True:
                global switchScreens
                switchScreens = True
                sm.current = "playActionDisplay"
            
        # Return True to accept the key.
        return True


class mainApp(App):
    def __init__(self):
        super(mainApp, self).__init__()
        self.players_list = []
        self.greenPlayers = [] 
        self.redPlayers = []
        self.redDict = {}
        self.greenDict = {}

    def build(self):
        sm.add_widget(Builder.load_file("kv/splashScreen.kv"))
        sm.add_widget(Builder.load_file("kv/mainScreen.kv"))
        sm.add_widget(Builder.load_file("kv/playActionDisplay.kv"))
        sm.add_widget(Builder.load_file("kv/keyboardInput.kv"))
        return sm

    def loopThroughDict(self, team_dict, team_list):
        if team_dict:
            for idx in team_dict:
                values = (team_dict[idx]['player_name'], team_dict[idx]['player_id'])
                db.commitToDatabase(values)
                team_list.append(Player(team_dict[idx]['player_name'], team_dict[idx]['player_id']))
                #self.root.get_screen('mainScreen').ids.testBox.text = f"{team_dict[idx]['player_name']} " \
                #                                                      f"{team_dict[idx]['player_id']} added"

    def createNestedDict(self):
        # create red and green team nested dictionary
        for i in range(15):
            red_name_string = f'self.root.get_screen("mainScreen").ids.red_name_entry{i}.text'
            red_id_string = f'self.root.get_screen("mainScreen").ids.red_id_entry{i}.text'
            green_name_string = f'self.root.get_screen("mainScreen").ids.green_name_entry{i}.text'
            green_id_string = f'self.root.get_screen("mainScreen").ids.green_id_entry{i}.text'
            if eval(red_name_string) == "" and eval(green_name_string) == "":
                break
            if eval(red_name_string) != "":
                red_sub_dict = {f'red_{i}': {'player_name': eval(red_name_string), 'player_id': eval(red_id_string)}}
                self.redDict.update(red_sub_dict)
            if eval(green_name_string) != "":
                green_sub_dict = {f'green_{i}': {'player_name': eval(green_name_string), 'player_id': eval(green_id_string)}}
                self.greenDict.update(green_sub_dict)
        self.loopThroughDict(self.redDict, self.redPlayers)
        self.loopThroughDict(self.greenDict, self.greenPlayers)
        for player in self.redPlayers:
            player.color = "Red"
            self.players_list.append(player)
        for player in self.greenPlayers:
            player.color = "Green"
            self.players_list.append(player)

    def submit(self):
        self.createNestedDict()
        for player in self.players_list:
            print(f"{player.name} is a member of the {player.color} team")

        # print("The red players are: ")
        # for i in range(len(self.players_list)):
        #     if self.players_list[i].color == "Red":
        #         print(self.players_list[i].name)
        #
        # print("The green players are: ")
        # for i in range(len(self.players_list)):
        #     if self.players_list[i].color == "Green":
        #         print(self.players_list[i].name)

        # update names in play action screen
        self.updateNames()

        # Starts the countdown timer
        self.updateTimer()

        # Automatically move to playaction screen
        sm.current = "playActionDisplay"

    def f5StartGame(self, dt):
        global switchScreens
        global createdNest
        if switchScreens is True:
            self.updateTimer()
            self.updateNames()

            if createdNest is True:
                self.createNestedDict()

    def showRecords(self):
        records = db.getAllDbValues()
        word = ''
        # loop through the returned records from our database
        for record in records:
            word = f'{word}\n{record[0]} {record[1]}'
            #self.root.get_screen('mainScreen').ids.testBox.text = f'{word}'

    def removeRecords(self):
        print('Database cleared')
        db.clearDB()

    # Countdown timer functionality.
    def updateTimer(self):
        self.clockNumber = NumericProperty()
        self.clockNumber = 60

        def decrementClock(interval):
            if self.clockNumber>0:
                self.clockNumber -= 1
                self.clockNumber = int(self.clockNumber)
                self.root.get_screen('playActionDisplay').ids.countdownTimer.text = "Timer:" f'{self.clockNumber}'
        Clock.schedule_interval(decrementClock, 1)
        
    # updates the names in the play action screen
    def updateNames(self):
        redNames = ''
        greenNames = ''
        for i in range(len(self.redPlayers)):
            redNames = f'{redNames}\n{self.redPlayers[i].name}'
        for i in range(len(self.greenPlayers)):
            greenNames = f'{greenNames}\n{self.greenPlayers[i].name}'
        self.root.get_screen('playActionDisplay').ids.redPlayerNames.text = f'{redNames}'
        self.root.get_screen('playActionDisplay').ids.greenPlayerNames.text = f'{greenNames}'

    def on_start(self):
        Clock.schedule_once(self.change_screen, 3)
        Clock.schedule_interval(self.f5StartGame, 1)

    def change_screen(self, dt):
        sm.current = "mainScreen"

    
if __name__ == '__main__':
    mainApp().run()
