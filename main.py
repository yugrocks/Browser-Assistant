from get_instance import Browser
import commands
from time import sleep
import VINI_voice
from predict_intent import PredictIntent
from playsound import Playsound
from ui_box import ui_box
import threading

a=Browser('firefox')#testing
with open("link.txt") as link:
    a.getPage(link.read())
commands.initialize_commands(a)
ip = PredictIntent()
prompt = ui_box()

def start_rolling():
    while(True):
        prompt.ready()
        #b=input("tell me what to do")
        b=VINI_voice.listen_for(3)
        prompt.busy()
        intent = ip.predict_intent(b)
        print(intent)
        if intent[0] in commands.commands:
            Playsound().start() #Beep sound
            commands.commands[intent[0]](b)

threading.Thread(target = start_rolling).start()
prompt.root.mainloop()
