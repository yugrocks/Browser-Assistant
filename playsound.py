import winsound
import threading


class Playsound(threading.Thread):

    def __init__(self, alternate = False):
        threading.Thread.__init__(self)
        self.alternate = alternate #which sound

    def run(self):
        if self.alternate:
            file = r'sounds/blip1.wav'
        else:
            file = r'sounds/s1.wav'
        try:
            winsound.PlaySound(file, winsound.SND_FILENAME)
        except:
            return
        
    
