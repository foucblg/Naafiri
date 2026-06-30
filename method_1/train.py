import numpy as np
import ast
import torch
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
from model import NeuralNetwork


class Data(Dataset):
    def __init__(self, X, y):
        self.X = torch.from_numpy(X.astype(np.float32))
        self.y = torch.from_numpy(y).long()
        self.len = self.X.shape[0]
       
    def __getitem__(self, index):
        return self.X[index], self.y[index]
   
    def __len__(self):
        return self.len
   
batch_size = 64

X_train, y_train = [], []

with open("data.txt", encoding="utf-8") as file:
    for line in file:
        clean_line = line.strip()
        if not clean_line:
            continue
        # transforme "[[...],0]" -> Python object
        cube, label = ast.literal_eval(line)
        X_train.append(cube)
        y_train.append(label)

X_train = np.array(X_train, dtype=np.float32)
y_train = np.array(y_train, dtype=np.int64)

train_data = Data(X_train, y_train)
train_dataloader = DataLoader(dataset=train_data, batch_size=batch_size, shuffle=True)


input_dim = 244
hidden_dim = 256
output_dim = 30
       
model = NeuralNetwork(input_dim, hidden_dim, output_dim)

learning_rate = 1e-3

loss_fn = nn.CrossEntropyLoss()

optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

num_epochs = 100
loss_values = []


for epoch in range(num_epochs):
    for X, y in train_dataloader:
        # zero the parameter gradients
        optimizer.zero_grad()
       
        # forward + backward + optimize
        pred = model(X)
        loss = loss_fn(pred, y)
        loss_values.append(loss.item())
        loss.backward()
        optimizer.step()

torch.save(model.state_dict(), "model.pth")

print("Training Complete")

"""
Training Complete
"""