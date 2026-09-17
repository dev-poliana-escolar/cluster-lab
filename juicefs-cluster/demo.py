#!/usr/bin/env python3

import subprocess


NODES = {
    "1": "juicefs-node1",
    "2": "juicefs-node2",
    "3": "juicefs-node3",
}


def docker_exec(node, command):
    result = subprocess.run(
        ["sudo", "docker", "exec", node, "sh", "-c", command],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"\nErro no {node}:")
        print(result.stderr)
        return None

    return result.stdout.strip()


print("=" * 50)
print("       CLUSTER - JUICEFS")
print("=" * 50)

print("\nNós disponíveis:")
print("1 - Node 1")
print("2 - Node 2")
print("3 - Node 3")

node = input("\nQual nó vai criar o arquivo? [1/2/3]: ").strip()

if node not in NODES:
    print("Nó inválido.")
    exit(1)

filename = input("Nome do arquivo: ").strip()
message = input("Mensagem: ")

creator = NODES[node]
path = f"/mnt/juicefs/{filename}"

print(f"\n[1] Criando arquivo no {creator}...")

command = f"printf '%s\\n' {message!r} > {path!r}"
docker_exec(creator, command)

print(f"[OK] Arquivo criado em {creator}.")

print("\n[2] Lendo o arquivo pelos outros nós...")

for number, container in NODES.items():
    if number == node:
        continue

    print(f"\nNode {number}:")
    content = docker_exec(container, f"cat {path!r}")

    if content is not None:
        print(f"  {content}")

print("\n" + "=" * 50)
print("FIM.")
print("=" * 50)

