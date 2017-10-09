from speech_recognition import Recognizer,Microphone

recognizer = Recognizer()
audio = None


def listen():
    global audio
    with Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print(recognizer.energy_threshold)
        print(recognizer.get_energy)
        audio = recognizer.listen(source)
    try:
        print(audio)
        # return recognizer.recognize_sphinx(audio)
        return recognizer.recognize_google(audio)
    except:
        return ""


def listen_for(time):
    global audio
    with Microphone() as source:
        # recognizer.adjust_for_ambient_noise(source)
        print(recognizer.energy_threshold)
        print(recognizer.get_energy)
        audio = recognizer.record(source,duration=time)
    # audio = recognizer.listen(source,timeout=1)
    try:
        # return recognizer.recognize_sphinx(audio)
        return recognizer.recognize_google(audio)
    except :
        return ""

