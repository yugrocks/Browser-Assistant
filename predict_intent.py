import numpy as np
from model import model
import pickle

class PredictIntent:
    
    def __init__(self):
        with open("vocab.pkl", 'rb') as data0:
            data = pickle.load(data0) #data is a set
        self.intents = {'forward':0,'backward':1,'type':2, 'reload':3, 'down':4,
                        'up':5, 'stop_scroll':6,'next_input':7,
                        'previous_input':8, 'submit':9, 'click':10,'search':11,
                        'quit':12, 'erase':13,
                        'change_tab':14, 'open_new_tab':15, 'close_tab':16
                       }
        self.indexes = {self.intents[word]:word for word in self.intents}
        self.words = list(data)
        self.words.sort()
        self.input_size = len(self.words)
        data = None
        self.model = self.load_model()
        
    def get_index_of(self, word):
        try:
            return self.words.index(word)
        except:
            return -1
    
    def load_model(self):
        model2 = model()
        return model2
        
    def encode_sent(self, sentence):
        sent = np.zeros((1, self.input_size))
        for _ in sentence.split():
            indx = self.get_index_of(_)
            if indx != -1:
                sent[0][indx] = 1
        return sent

    def decode_intent(self, y_pred):
        index = y_pred.argmax()
        return self.indexes[index]
    
    def predict_intent(self, sentence):
             y_pred = self.model.predict(self.encode_sent(sentence))
             if y_pred.max() > 0.8:
                 return self.decode_intent(y_pred), y_pred.max()
             else:
                 return "other", 0.00
