import os
import torch
from torch import nn, load
from cube import Cube, move_batch, is_resolved_batch, to_vector_batch
from model import NeuralNetwork

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

data = torch.tensor(load("method_2/data.pt"), dtype=torch.long, device=device)

input_dim = 244
hidden_dim = 256
output_dim = 29

model = NeuralNetwork(input_dim, hidden_dim, output_dim).to(device)
if os.path.exists("method_2/model.pth"):
    model.load_state_dict(load("method_2/model.pth"))

learning_rate = 5e-4
batch_size = 4096

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9)

num_epochs = 2000
loss_values = []
moves = list(Cube.MOVES.keys())

for epoch in range(num_epochs):
    data = data[torch.randperm(len(data), device=device)]
    epoch_losses = []

    for start in range(0, len(data), batch_size):
        batch = data[start:start + batch_size]
        cp, co, ep, eo = batch[:, 0:8], batch[:, 8:16], batch[:, 16:28], batch[:, 28:40]

        optimizer.zero_grad()
        pred = model(to_vector_batch(cp, co, ep, eo))

        pred_min = torch.full((len(batch),), output_dim + 1, dtype=torch.long, device=device)
        with torch.no_grad():
            for m in moves:
                n_cp, n_co, n_ep, n_eo = move_batch(cp, co, ep, eo, m)
                resolved = is_resolved_batch(n_cp, n_co, n_ep, n_eo)
                dist = model(to_vector_batch(n_cp, n_co, n_ep, n_eo)).argmax(dim=1)
                pred_min = torch.minimum(pred_min, torch.where(resolved, torch.zeros_like(dist), dist))

        y = torch.clamp(pred_min + 1, max=output_dim - 1)

        loss = loss_fn(pred, y)
        loss_values.append(loss.item())
        epoch_losses.append(loss.item())
        loss.backward()
        optimizer.step()

    if epoch % 50 == 0 or epoch == num_epochs - 1:
        print(epoch, sum(epoch_losses) / len(epoch_losses))

torch.save(model.state_dict(), "method_2/model.pth")

print("Training Complete")
