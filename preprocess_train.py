import csv
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
from keras.models import model_from_json
import pickle


with open("training_data.txt") as data0:
    data = np.array(list(csv.reader(data0)))

intents = {
                'forward':0,'backward':1,'type':2, 'reload':3, 'down':4,'up':5, 'stop_scroll':6,'next_input':7,
                'previous_input':8, 'submit':9, 'click':10,'search':11, 'quit':12, 'erase':13,
                'change_tab':14, 'open_new_tab':15, 'close_tab':16
                }

words = []
for _ in data[:, 0]:
    words.extend(_.split())
words = list(set(words))
words.sort()
X = data[:, 0]
Y = data[:, 1] #differentiate X and Y

#parameters
input_size = len(words)
nb_intents = 17 #output size
data_size = X.shape[0]


data = None

def get_index_of(word):
    try:
        return words.index(word)
    except:
        return -1

def get_training_data():
    y = np.zeros((data_size, nb_intents))
    
    for i in range(data_size):
        index = intents[Y[i].strip()]
        y[i][index] = 1
    
    x = np.zeros((data_size, input_size))
    for i in range(data_size):
        for word in X[i].split():
            index = get_index_of(word)
            if index != -1:
                x[i][index] = 1
    
    return (x,y)
        
X, Y = get_training_data()

#shufle them
randomize = np.arange(X.shape[0])
np.random.shuffle(randomize)
X = X[randomize]
Y = Y[randomize]

X_train = X[0:, :]
Y_train = Y[0:, :]
X_test = X[169:, :]
Y_test = Y[169:, :]

def make_model():
    model = Sequential()
    # Adding the input layer and the first hidden layer
    model.add(Dense(output_dim = 5, init = 'uniform', activation = 'relu', input_dim = input_size))
    # Add Output layer
    model.add(Dense(output_dim = nb_intents, init = 'uniform', activation = 'softmax',
                                kernel_regularizer=regularizers.l2(0.2)))
    # Compile it
    model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
    return model

def train_nn():
    model = make_model()
    history = model.fit(X_train,Y_train, batch_size=162,validation_data=(X_test, Y_test), epochs=9000,verbose=1, 
                        #validation_split=0.1
                        )
    return history, model
    
history, model = train_nn()


#save the model and the weights
model.save_weights("weights.hdf5",overwrite=True)

#saving the model itself in json format:
model_json = model.to_json()
with open("model.json", "w") as model_file:
    model_file.write(model_json)
print("Model has been saved.")

    
def encode_sent(sentence):
    sent = np.zeros((1, input_size))
    for _ in sentence.split():
        indx = get_index_of(_)
        if indx != -1:
            sent[0][indx] = 1
    return sent
    
def load_model():
    try:
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        model.load_weights("weights.hdf5")
        print("Model successfully loaded from disk.")
        
        #compile again
        model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
        return model
    except:
        print("""Model not found. Please train the CNN by running the script 
cnn_train.py. Note that the training and test samples should be properly 
set up in the dataset directory.""")
        return None

y_pred = model.predict(encode_sent("quit"))


weights0 = {}
def pickle_weights():
    layers = model.layers
    for i in range(len(layers)):
        layer = layers[i]
        weights0["W"+str(i)] = np.copy(layer.get_weights()[0])
        weights0['b'+str(i)] = np.copy(layer.get_weights()[1])
    with open('weights.pkl','wb') as file:
        pickle.dump(weights0, file)
        
pickle_weights()
