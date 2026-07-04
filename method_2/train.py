import numpy as np
import ast
import torch
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
from method_2.cube import Cube
from model import NeuralNetwork


class Data(Dataset):
    def __init__(self, X):
        self.X = torch.from_numpy(X.astype(np.float32))
        self.len = self.X.shape[0]
       
    def __getitem__(self, index):
        return self.X[index]
   
    def __len__(self):
        return self.len
   
batch_size = 64

x_train = []

with open("method_2/data.txt", encoding="utf-8") as file:
    for line in file:
        clean_line = line.strip()
        if not clean_line:
            continue
        cube = ast.literal_eval(line)
        x_train.append(cube)

X_train = np.array(x_train, dtype=np.float32)

train_data = Data(X_train)
train_dataloader = DataLoader(dataset=train_data, batch_size=batch_size, shuffle=True)


input_dim = 246
hidden_dim = 256
output_dim = 30
       
model = NeuralNetwork(input_dim, hidden_dim, output_dim)

learning_rate = 1e-3

loss_fn = nn.CrossEntropyLoss()

optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

num_epochs = 1 # 100
# loss_values = []
moves = list(Cube.MOVES.keys())

for epoch in range(num_epochs):
    for X in train_dataloader:
        optimizer.zero_grad()
        cube = Cube(X[0:8],X[8:16],X[16:28],X[28:40])
        X_vec = cube.to_vector()
        pred = model(X_vec)

        for m in moves:
            cube.move(m)
            







        # loss = loss_fn(pred, y)
        # loss_values.append(loss.item())
        # loss.backward()
        # optimizer.step()

torch.save(model.state_dict(), "model.pth")

print("Training Complete")

"""
Training Complete
"""