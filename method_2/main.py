from model import NeuralNetwork
from cube import cube_resolved
from torch import argmax, load

model = NeuralNetwork(244, 256, 29)
model.load_state_dict(load("method_2/model.pth"))
model.eval()
cube = cube_resolved.copy()
cube.shuffle(1)
data = cube.to_tensor().float()
output = model(data)
print(output)
prediction = argmax(output)
print(prediction)