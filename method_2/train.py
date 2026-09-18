import numpy as np
import ast
import torch
from torch import nn, optim, load, tensor
from torch.utils.data import Dataset, DataLoader
from cube import Cube
from model import NeuralNetwork


class Data(Dataset):
    def __init__(self, X):
        self.X = X
        self.len = len(self.X)
       
    def __getitem__(self, index):
        return self.X[index]
   
    def __len__(self):
        return self.len
   
batch_size = 5

X_train = load("method_2/data.pt")

input_dim = 244
hidden_dim = 256
output_dim = 29
       
model = NeuralNetwork(input_dim, hidden_dim, output_dim)

learning_rate = 1e-3

loss_fn = nn.CrossEntropyLoss()

optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

num_epochs = 1
loss_values = []
moves = list(Cube.MOVES.keys())

for epoch in range(num_epochs):
    print(epoch)
    for X in X_train:
        optimizer.zero_grad()
        cube = Cube(X[0:8], X[8:16], X[16:28], X[28:40])
        X_vec = cube.to_tensor().float()
        pred = model(X_vec)

        pred_min = output_dim + 1

        for m in moves:
            cube.move(m)
            if cube.is_resolved():
                pred_min = 0
                break
            X_vec_moved = cube.to_tensor().float()
            pred_list_moved = model(X_vec_moved).detach().numpy()
            pred_int_moved = np.argmax(pred_list_moved)
            pred_min = min(pred_int_moved, pred_min)
            cube.antimove(m)

        y = tensor([int(i == pred_min + 1) for i in range(output_dim)]).float()

        loss = loss_fn(pred, y)
        loss_values.append(loss.item())
        loss.backward()
        optimizer.step()

torch.save(model.state_dict(), "method_2/model.pth")

print("Training Complete")
