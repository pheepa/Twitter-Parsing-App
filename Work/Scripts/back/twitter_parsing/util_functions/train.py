# for train
# call this:
#     initializer = Initializer();
#     initializer.train()

import sys
import pandas as pd
import numpy as np

import json
json_file_path = sys.path[0] + "/word_to_int.json"
with open(json_file_path, 'r') as j:
     word_to_int = json.loads(j.read())

import torch
import torch.nn as nn
       
    

class Initializer():
    def __init__(self):
        
        self.word_to_int = word_to_int
        self.train_on_gpu = False

        self.vocab_size = len(word_to_int) + 1 # +1 for zero padding + our word tokens
        self.output_size = 1 # prob of positive sentiment
        self.embedding_dim = 400 
        self.hidden_dim = 256
        self.n_lstm_layers = 2
        self.batch_size = 16
        self.loaded_net = SentimentLSTM(self.vocab_size, self.output_size, self.embedding_dim, 
                                        self.hidden_dim, self.n_lstm_layers)
        
      
    def train(self):
        self.loaded_net.load_state_dict(torch.load(sys.path[0] + "/weights_1_epoch_gpu.pth", 
                                                   map_location=('cpu')))
        
class SentimentLSTM(nn.Module):
    def __init__(self, vocab_size, output_size, embedding_dim, hidden_dim, n_lstm_layers, drop_prob=0.5):
        super(SentimentLSTM, self).__init__()
        
        self.train_on_gpu = False
        self.vocab_size = vocab_size
        self.output_size = output_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.n_lstm_layers = n_lstm_layers
        self.drop_prob = drop_prob
        
        self.embedding = nn.Embedding(num_embeddings=vocab_size , embedding_dim=embedding_dim)
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=hidden_dim, 
                            num_layers=n_lstm_layers, dropout=drop_prob, batch_first=True)
        
        self.dropout = nn.Dropout(p=0.3)
        
        self.fc = nn.Linear(in_features=hidden_dim, out_features=output_size)
        self.sig = nn.Sigmoid()
        
    def forward(self, x, hidden):
            batch_size = x.size(0)



            #embed = self.embedding(x) так было до (Фил - ла пук)
            embed = self.embedding(x.long()) #так после

            lstm_out, hidden = self.lstm(embed, hidden)
            # stack up lstm outputs
            lstm_out = lstm_out.contiguous().view(-1, self.hidden_dim)

            # dropout and fully connected layer
            out = self.dropout(lstm_out)
            out = self.fc(out)

            # sigmoid function
            sig_out = self.sig(out)

            # reshape to be batch_size first
            sig_out = sig_out.view(batch_size, -1)
            sig_out = sig_out[:, -1] # get last batch of labels

            # return last sigmoid output and hidden state
            return sig_out, hidden
    
    def init_hidden(self, batch_size):
        
        # Create two new tensors with sizes n_layers x batch_size x hidden_dim,
        # initialized to zero, for hidden state and cell state of LSTM
        weight = next(self.parameters()).data
        
        if(self.train_on_gpu):
          hidden = (weight.new(self.n_lstm_layers, batch_size, self.hidden_dim).zero_().cuda(),
                   weight.new(self.n_lstm_layers, batch_size, self.hidden_dim).zero_().cuda())
        else:
          hidden = (weight.new(self.n_lstm_layers, batch_size, self.hidden_dim).zero_(),
                   weight.new(self.n_lstm_layers, batch_size, self.hidden_dim).zero_())
        
        return hidden
    
initializer = Initializer()
initializer.train()





