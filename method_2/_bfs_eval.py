import time
import torch
from cube import Cube, cube_resolved
from model import NeuralNetwork

MAX_DEPTH = 6
SAMPLES_PER_DEPTH = 300


def build_oracle(max_depth):
    moves = list(Cube.MOVES.keys())
    start = cube_resolved.copy()
    start_key = tuple(start.to_one_list())
    dist = {start_key: 0}
    frontier = [start]
    for d in range(1, max_depth + 1):
        next_frontier = []
        for c in frontier:
            for m in moves:
                nc = c.copy()
                nc.move(m)
                key = tuple(nc.to_one_list())
                if key not in dist:
                    dist[key] = d
                    next_frontier.append(nc)
        frontier = next_frontier
        print(f"  profondeur {d}: {len(frontier):>8} nouveaux etats, {len(dist):>9} au total")
    return dist


print(f"Construction de l'oracle BFS jusqu'a profondeur {MAX_DEPTH}...")
t0 = time.perf_counter()
oracle = build_oracle(MAX_DEPTH)
print(f"Oracle construit en {time.perf_counter() - t0:.1f}s ({len(oracle)} etats)\n")

model = NeuralNetwork(244, 256, 29)
model.load_state_dict(torch.load("model.pth"))
model.eval()

print(f"{'depth':>5} | {'label!=vrai':>11} | {'acc / label':>11} | {'acc / vrai':>10}")
print("-" * 48)
for depth in range(1, MAX_DEPTH + 1):
    mismatch = 0
    acc_label = 0
    acc_true = 0
    for _ in range(SAMPLES_PER_DEPTH):
        c = cube_resolved.copy()
        c.shuffle(depth)
        key = tuple(c.to_one_list())
        true_d = oracle[key]
        if true_d != depth:
            mismatch += 1
        pred = torch.argmax(model(c.to_tensor().float())).item()
        if pred == depth:
            acc_label += 1
        if pred == true_d:
            acc_true += 1
    n = SAMPLES_PER_DEPTH
    print(f"{depth:>5} | {mismatch/n:>10.1%} | {acc_label/n:>10.1%} | {acc_true/n:>9.1%}")
