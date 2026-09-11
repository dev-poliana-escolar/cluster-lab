import requests
import os

NODES = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003"
]

FILE = "arquivo.txt"


def split_file(data):
    size = len(data)
    part_size = (size + 2) // 3

    return [
        data[:part_size],
        data[part_size:part_size * 2],
        data[part_size * 2:]
    ]


with open(FILE, "rb") as file:
    data = file.read()

parts = split_file(data)

for i, part in enumerate(parts):
    filename = f"parte_{i + 1}.bin"

    response = requests.post(
        f"{NODES[i]}/store",
        data=part,
        headers={"X-Filename": filename}
    )

    print(f"Node {i + 1}: {response.json()}")

print("Arquivo distribuído pelos três nós!")