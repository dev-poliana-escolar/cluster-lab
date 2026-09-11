import requests

NODES = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003"
]

with open("arquivo_recuperado.txt", "wb") as output:

    for i, node in enumerate(NODES):
        filename = f"parte_{i + 1}.bin"

        response = requests.get(
            f"{node}/file/{filename}"
        )

        response.raise_for_status()
        output.write(response.content)

print("Arquivo reconstruído com sucesso!")