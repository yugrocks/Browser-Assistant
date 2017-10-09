from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from threading import Thread
import VINI_voice
from predict_intent import PredictIntent
import click_command_interpret
from click_command_interpret import get_the_objective
import tab_command_parser as tcp
from playsound import  Playsound

class Browser:
    up_interrupted=False
    down_interrupted=False
    links=[]
    inputs=[]
    selected_inpt=None
    
    def __init__(self,browser_name='firefox'):
        if browser_name=='firefox':
            self.browser=webdriver.Firefox()
        elif browser_name=='chrome':
            self.browser=webdriver.Chrome()
        self.ip = PredictIntent()
        self.original_style = None
  
    def back(self, command):  # simulates the click on the back button of the browser
        try:
            self.browser.back()
        except:
            print("The process  has disconnected from browser.")

    def forward(self, command):  # simulates the click on forward button
        try:
            self.browser.forward()
        except:
            print("Either The process  has disconnected from browser, or no forwarding possible")

    def quit(self, command):  # clicks the close window
        try:
            self.browser.quit()
        except:
            print("Either The process  has disconnected from browser, or no forwarding possible")

    def reload(self, command):  # clicks refresh button
        try:
            self.browser.refresh()
        except:
            print("Either The process  has disconnected from browser, or no forwarding possible")

    def scroll_down(self, command):  # scrolls down until interrupted
        self.up_interrupted=True
        self.down_interrupted=False
        def new_thread():
            try:
                while not self.down_interrupted:
                   self.browser.execute_script("window.scrollBy(0, 20);")
                   sleep(0.15)
                self.down_interrupted=False
                self.up_interrupted=False
            except:
                print("End of page reached")
        Thread(target=new_thread).start()

    def scroll_up(self, command):  # scrolls up until interrupted
        self.down_interrupted=True
        self.up_interrupted=False
        def new_thread2():
            try:
                while not self.up_interrupted:
                   self.browser.execute_script("window.scrollBy(0, -20);")
                   sleep(0.15)
                self.up_interrupted=False
                self.down_interrupted=False
            except:
                print("Beginning of page reached.")
        Thread(target=new_thread2).start()

    def stop_scrolling(self, command):  # stop
        self.up_interrupted=True
        self.down_interrupted=True

    def getPage(self,url):  # open a page
        self.url=url
        self.browser.get(url)
        self.getLinks()

    def getLinks(self): # get all  the links in a page
        self.links=self.browser.find_elements_by_tag_name('a')
        self.links.extend(self.browser.find_elements_by_tag_name('button'))
        
    def clickOn(self,element):  # clicks on an element
        element.click()

    def search(self,string):  # search google for something
        string = get_the_objective(string)
        self.getPage("https://www.google.co.in/#safe=off&q={}".format(string))

    def highlight(self, element, toNormal = False):
        def apply_style(s):
            self.browser.execute_script("arguments[0].setAttribute('style', arguments[1]);",self.selected_inpt, s)
        if toNormal:
            apply_style(self.original_style)
            return 
        self.original_style = element.get_attribute('style')
        apply_style(self.original_style+";background: yellow;")
        
     	
    def findLink(self,string):
        print("got here")
        self.getLinks()
        print(len(self.links))
        string = get_the_objective(string)
        string = string.lower()
        queries = string.split()
        scores = [0]*len(self.links)
        for i in range(len(self.links)):
            text = self.links[i].text
            for word in queries:
                if word in text.lower():
                    scores[i] += 1
            if scores[i] == len(queries):  # early stopping to save time
                break
        print("found")
        best_candidate_index = scores.index(max(scores))
        self.clickOn(self.links[best_candidate_index])
        """
        try:
            self.clickOn(self.browser.find_element_by_link_text(string))
        except:
            try:
                self.clickOn(self.browser.find_element_by_link_text(string.capitalize()))
            except:    
                for _ in self.links:
                    if _.text.lower().startswith(string):
                        self.clickOn(_)
                        break"""

    def getInputs(self):
        self.inputs=self.browser.find_elements_by_tag_name('input')
        self.inputs.extend(self.browser.find_elements_by_tag_name('textarea'))

    def input_time(self):
        self.getInputs()
        self.selected_inpt = self.inputs[0]
        self.highlight(self.selected_inpt, toNormal = False)

    def enter_text(self, string):
        non_writable_inputs = ['radio', 'checkbox', 'button', 'color',
                               'file', 'hidden', 'image', 'month', 'range']
        try:
            if self.selected_inpt is None:
                self.input_time()
                self.enter_text("")
                return
            if not self.selected_inpt.is_displayed():
                self.next_input("")
                self.enter_text("")
                return
            if not self.selected_inpt.is_displayed():
                self.next_input("")
                self.enter_text("")
                return
            if self.selected_inpt.get_attribute('type') in non_writable_inputs:
                self.next_input("")
                self.enter_text("")
                return
        except:
            self.input_time()
            self.enter_text("")
            return
        print("I am listening. Dictate the text in one go.")
        """beep sound here"""
        Playsound(True).start() #Blip sound
        b=VINI_voice.listen_for(7)
        
        #b = input("enter the text")
        intent = self.ip.predict_intent(b)
        if intent[0] == "next_input":
            Playsound().start() #Beep sound
            self.next_input("")
        elif intent[0] == "submit":
            Playsound().start() #Beep sound
            self.submit("")
        elif intent[0] == "previous_input":
            Playsound().start() #Beep sound
            self.previous_input("")
        if intent[0] == "clear":
            Playsound().start() #Beep sound
            self.clear_text("")
        else:
            try:
                self.selected_inpt.send_keys(b)
            except:
                return

    def clear_text(self, command):
        try:
            self.selected_inpt.clear()
        except:
            try:
                if self.selected_inpt is None:
                    self.input_time()
                    self.clear_text("")
                    return
                if not self.selected_inpt.is_displayed():
                    self.next_input("")
                    self.clear_text("")
                    return
                if not self.selected_inpt.is_displayed():
                    self.next_input("")
                    self.clear_text("")
                    return
                if self.selected_inpt.get_attribute('type') in non_writable_inputs:
                    self.next_input("")
                    self.enter_text("")
                    return
            except:
                self.input_time()
                self.clear_text("")
                return
    
    def next_input(self, command):
        non_writable_inputs = ['radio', 'checkbox', 'button', 'color',
                               'file', 'hidden', 'image', 'month', 'range',""]
        try:
            self.getInputs()
            try:
                self.highlight(self.selected_inpt, toNormal = True) #unhighlight the previous input
            except:
                print("")
            self.selected_inpt = self.inputs[self.inputs.index(self.selected_inpt)+1]
            if self.selected_inpt.get_attribute('type') in non_writable_inputs:
                self.next_input("")
                return
            self.highlight(self.selected_inpt, toNormal = False)
        except:
            return
        
    def previous_input(self, command):
        non_writable_inputs = ['radio', 'checkbox', 'button', 'color',
                               'file', 'hidden', 'image', 'month', 'range',""]
        if True:
            self.getInputs()
            try:
                self.highlight(self.selected_inpt, toNormal = True) #unhighlight the previous input
            except:
                print("")
            self.selected_inpt = self.inputs[self.inputs.index(self.selected_inpt)-1]
            if self.selected_inpt.get_attribute('type') in non_writable_inputs:
                self.previous_input("")
                return
            self.highlight(self.selected_inpt, toNormal = False)
        else:
            return
        
    def submit(self, command):
        try:
            self.selected_inpt.submit()
        except:
            return

    def open_new_tab(self, command):
        indx = len(self.browser.window_handles)
        try:
            self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL+ 't')
        except:
            self.browser.execute_script('''window.open("about:blank", "_blank");''')
        curWindowHndl = self.browser.current_window_handle
        self.browser.switch_to_window(self.browser.window_handles[indx])

    def close_tab(self, command):
        curWindowHndl = self.browser.current_window_handle
        print(curWindowHndl)
        self.browser.close()
        #after closing the current tab, switch to bext tab if available
        #otherwise the previous tab
        if len(self.browser.window_handles) >=1:
            #switch to the next greatest index
            indx = len(self.browser.window_handles) - 1
        self.browser.switch_to_window(self.browser.window_handles[indx])
        

    def switch_tab(self, command):
        #next/previous or n'th tab
        object = tcp.get_the_objective(command) #nothing to do with the TCP protocol though :P
        curWindowHndl = self.browser.current_window_handle
        current_indx = self.browser.window_handles.index(curWindowHndl)
        response = tcp.process_objective(object)
        if type(response) is str:
            if response == "+1":
                try:
                    self.browser.switch_to_window(self.browser.window_handles[current_indx + 1])
                except:
                    pass
            else:
                try:
                    self.browser.switch_to_window(self.browser.window_handles[current_indx - 1])
                except:
                    pass
        elif type(response) is int:
            if response < len(self.browser.window_handles):
                self.browser.switch_to_window(self.browser.window_handles[response])
            else:
                self.browser.switch_to_window(self.browser.window_handles[len(self.browser.window_handles) - 1])

