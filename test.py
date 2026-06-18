import ast
import numpy as np
import torch
from model import NeuralNetwork

X_test = []
y_test = []

with open("test.txt", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue

        cube, label = ast.literal_eval(line)

        X_test.append(cube)
        y_test.append(label)

X_test = np.array(X_test, dtype=np.float32)
y_test = np.array(y_test, dtype=np.int64)


model = NeuralNetwork(40, 256, 30)
model.load_state_dict(torch.load("model.pth"))
model.eval()

def predict(cube_state):
    x = torch.tensor(cube_state, dtype=torch.float32)
    x = x.unsqueeze(0)  # batch size = 1

    with torch.no_grad():
        output = model(x)

    probs = torch.softmax(output, dim=1)
    predicted_class = torch.argmax(probs).item()

    return predicted_class, probs.squeeze().numpy()


def evaluate(X_test, y_test):
    correct = 0
    total = len(X_test)
    total_error = 0

    for x, y in zip(X_test, y_test):

        pred, _ = predict(x)

        # accuracy
        if pred == y:
            correct += 1

        # erreur absolue
        total_error += abs(pred - y)

    accuracy = correct / total
    mean_error = total_error / total

    print("Accuracy :", accuracy)
    print("Mean absolute error :", mean_error)

evaluate(X_test, y_test)