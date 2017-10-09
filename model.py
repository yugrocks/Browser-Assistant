import numpy as np
import pickle

class model:
    def __init__(self):
        #Hyperparameters
        self.input_size = 108
        self.hidden_size = 5
        self.output_size = 17
        self.W1, self.b1, self.W2, self.b2 = self.load_pickled_weights()
    
    def load_pickled_weights(self):
        with open('weights.pkl' ,'rb') as file:
            weights = pickle.load(file)
        return [np.copy(weights['W0']).T,np.copy(weights['b0']),np.copy(weights['W1']).T,np.copy(weights['b1'])]
    
    def relu(self, z):
        return np.maximum(0, z)
    
    def sigmoid(self, z):
        return 1/(1 + np.exp(-z))
    
    def forward_propagate(self, X):
        Z1 = np.dot(self.W1, X.T) 
        Z1 = Z1 + self.b1.reshape(self.b1.shape[0], 1)
        A1 = self.relu(Z1) #relu for hidden
        Z2 = np.dot(self.W2, A1)
        Z2 = Z2 +self.b2.reshape(self.b2.shape[0], 1)
        A2 = self.sigmoid(Z2)#sigmoid for output
        return A2
    
    def predict(self, X):
        y_pred = self.forward_propagate(X)
        return y_pred
