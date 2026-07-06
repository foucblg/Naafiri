from model import NeuralNetwork
from cube import cube_resolved
from torch import argmax, load

model = NeuralNetwork(244, 256, 30)
model.load_state_dict(load("method_2/model.pth"))
model.eval()

data = cube_resolved.to_tensor().float()
output = model(data)
prediction = argmax(output)
print(prediction)