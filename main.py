from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.core.window import Window
import lib.db as db
from lib.Player import Player
import lib.server 
from threading import Thread
import re
import os
import psutil

Window.fullscreen = False
Window.size = (800, 800)
sm = ScreenManager()
switchScreens = False
createdNest = True
updateTimer = True
pid = ""


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
        self.server = lib.server.Server()
        self.players_list = []
        self.greenPlayers = [] 
        self.redPlayers = []
        self.players_dict = {}
        self.displayString = []
        self.redScore =0
        self.greenScore =0
        self.pid = ""

    def build(self):
        sm.add_widget(Builder.load_file("kv/splashScreen.kv"))
        sm.add_widget(Builder.load_file("kv/mainScreen.kv"))
        sm.add_widget(Builder.load_file("kv/playActionDisplay.kv"))
        sm.add_widget(Builder.load_file("kv/keyboardInput.kv"))
        return sm

    def insertNames(self):
        for i in range(15):
            #loop through red players
            id = eval(f'self.root.get_screen("mainScreen").ids.red_id_entry{i}.text')
            if(id != ''):
                name = db.getName(id)
                regex = re.compile('[^a-zA-Z]')
                name = regex.sub('', str(name))
                exec(f'self.root.get_screen("mainScreen").ids.red_name_entry{i}.text = str(name)')
            #loop through green players
            id = eval(f'self.root.get_screen("mainScreen").ids.green_id_entry{i}.text')
            if(id != ''):
                name = db.getName(id)
                regex = re.compile('[^a-zA-Z]')
                name = regex.sub('', str(name))
                exec(f'self.root.get_screen("mainScreen").ids.green_name_entry{i}.text = str(name)')

    def get_players(self):
        # create red and green team nested dictionary
        #db.clearDB()
        for i in range(15):
            red_name_string = f'self.root.get_screen("mainScreen").ids.red_name_entry{i}.text'
            red_id_string = f'self.root.get_screen("mainScreen").ids.red_id_entry{i}.text'
            green_name_string = f'self.root.get_screen("mainScreen").ids.green_name_entry{i}.text'
            green_id_string = f'self.root.get_screen("mainScreen").ids.green_id_entry{i}.text'
            if eval(red_name_string) == "" and eval(green_name_string) == "":
                break
            if eval(red_name_string) != "":
                self.redPlayers.append(Player(eval(red_name_string), eval(red_id_string)))
            if eval(green_name_string) != "":
                self.greenPlayers.append(Player(eval(green_name_string), eval(green_id_string)))
        for player in self.redPlayers:
            player.color = "Red"
            self.players_dict.update({player.uid: player})
            self.players_list.append(player)
        for player in self.greenPlayers:
            player.color = "Green"
            self.players_dict.update({player.uid: player})
            self.players_list.append(player)

        for player in self.players_list:
            values = (player.name, player.uid)
            db.commitToDatabase(values)
        global createdNest
        createdNest = False

    def submit(self):
        self.get_players()
        self.updateTimer()
        # Automatically move to playaction screen
        sm.current = "playActionDisplay"
         #Start the server as a thread
        self.serverThread = Thread(target=self.server.runServer,args=(self.players_dict,self.displayString,));
        self.serverThread.start();


        global pid
        pid = os.getpid()


    def f5StartGame(self, dt):
        global switchScreens
        global createdNest
        global updateTimer
        if switchScreens is True:
            self.updateNames(dt)
            if updateTimer is True:
                self.updateTimer()
                

            if createdNest is True:
                self.get_players()

    def showRecords(self):
        records = db.getAllDbValues()
        word = ''
        # loop through the returned records from our database
        for record in records:
            word = f'{word}\n{record[0]} {record[1]}'
            #self.root.get_screen('mainScreen').ids.testBox.text = f'{word}'

    def removeRecords(self):
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
        Clock.schedule_interval(self.checkTimer, 1); 
        global updateTimer
        updateTimer = False
        
    #Checking if timer is at 0 to end the game
    def checkTimer(self, dt):
        if self.clockNumber == 0:
            self.server.GameIsOn = False;

    # updates the names in the play action screen
    def updateNames(self,dt):
        if len(self.displayString) > 6:
            self.displayString.pop(0)
        redNames = ''
        greenNames = ''
        for i in range(len(self.redPlayers)):
            redNames = f'{redNames}\n{self.redPlayers[i].name + " " + str(self.redPlayers[i].numHits *100)}'
        for i in range(len(self.greenPlayers)):
            greenNames = f'{greenNames}\n{self.greenPlayers[i].name+ " " + str(self.greenPlayers[i].numHits*100)}'
        self.root.get_screen('playActionDisplay').ids.redPlayerNames.text = f'{redNames}'
        self.root.get_screen('playActionDisplay').ids.greenPlayerNames.text = f'{greenNames}'
        
        displaynames =''
        for i in range (len(self.displayString)):
            displaynames += f'{self.displayString[i]}\n'
        self.root.get_screen('playActionDisplay').ids.playerActions.text = displaynames

    def on_start(self):
        Clock.schedule_interval(self.updateNames,1);
        Clock.schedule_once(self.change_screen, 3)
        Clock.schedule_interval(self.f5StartGame, 1)
        Clock.schedule_interval(self.updateTeamscores,1);

    def change_screen(self, dt):
        sm.current = "mainScreen"

    # updates teams scores in the play action screen
    def updateTeamscores(self,dt):
        redScore = 0
        greenScore = 0
        for i in range(len(self.redPlayers)):
            redScore += self.redPlayers[i].numHits 
        for i in range(len(self.greenPlayers)):
            greenScore += self.greenPlayers[i].numHits 
        self.root.get_screen('playActionDisplay').ids.redScore.text = "Score:" f'{redScore * 100}'
        self.root.get_screen('playActionDisplay').ids.greenScore.text = "Score:" f'{greenScore * 100}'


if __name__ == '__main__':
    app = mainApp()
    app.run()
    app.server.GameIsOn = False;
    p = psutil.Process(int(pid))
    p.terminate()

