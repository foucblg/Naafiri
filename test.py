import ast

import matplotlib.pyplot as plt
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


def confusion_matrix(y_true, y_pred, num_classes):
    matrix = np.zeros((num_classes, num_classes), dtype=np.int64)

    for true_label, pred_label in zip(y_true, y_pred):
        matrix[true_label, pred_label] += 1

    return matrix


def plot_confusion_matrix(matrix, output_path="confusion_matrix.png"):
    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(matrix, interpolation="nearest", cmap="Blues")
    ax.figure.colorbar(im, ax=ax)

    num_classes = matrix.shape[0]
    labels = list(range(num_classes))

    ax.set(
        xticks=np.arange(num_classes),
        yticks=np.arange(num_classes),
        xticklabels=labels,
        yticklabels=labels,
        xlabel="Classe prédite",
        ylabel="Classe réelle",
        title="Matrice de confusion",
    )
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    threshold = matrix.max() / 2 if matrix.max() > 0 else 0
    for i in range(num_classes):
        for j in range(num_classes):
            value = matrix[i, j]
            if value > 0:
                ax.text(
                    j,
                    i,
                    str(value),
                    ha="center",
                    va="center",
                    color="white" if value > threshold else "black",
                    fontsize=7,
                )

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"Matrice de confusion sauvegardée dans `{output_path}`")
    plt.close(fig)


def evaluate(X_test, y_test):
    correct = 0
    total = len(X_test)
    total_error = 0
    y_pred = []

    for x, y in zip(X_test, y_test):
        pred, _ = predict(x)
        y_pred.append(pred)

        if pred == y:
            correct += 1

        total_error += abs(pred - y)

    y_pred = np.array(y_pred)
    num_classes = max(y_test.max(), y_pred.max()) + 1
    matrix = confusion_matrix(y_test, y_pred, num_classes)

    accuracy = correct / total
    mean_error = total_error / total

    print("Accuracy :", accuracy)
    print("Mean absolute error :", mean_error)
    print(f"Classe prédite la plus fréquente : {np.bincount(y_pred).argmax()}")
    plot_confusion_matrix(matrix)


evaluate(X_test, y_test)