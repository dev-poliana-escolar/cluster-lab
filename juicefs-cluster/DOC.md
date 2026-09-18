# Cluster JuiceFS

## O que é o JuiceFS?
É um sistema de arquivo distribuído que divide o armazenamento entre dois serviços. Um para guardar o dado, outro para os metadados desse dado em um banco (Redis, MySql etc).

1. **O que é um cluster?**\
É um agrupamento de múltiplos nós de computação (node1, node2, node3) que acessam e compartilham de forma simultânea o mesmo sistema de arquivos. No ecossistema do JuiceFS, o cluster se consolida porque todas essas instâncias independentes conversam com os mesmos motores centrais: o MinIO (dados) e o Redis (metadados).

---

## SUMÁRIO
1. [Estrutura deste projeto](#estrutura-deste-projeto)
2. [Como executar?](#como-executar)
3. [Erros conhecidos](#erros-conhecidos)

---

## Estrutura deste projeto:
```text
└── juicefs-cluster
    ├── data
    │   ├── minio
    │   ├── node1
    │   ├── node2
    │   └── node3
    ├── demo.py
    ├── docker-compose.yaml
    ├── DOC.md
    └── README
```
---

## Como executar?
1. Na raiz do projeto, entre na pasta `juicefs-cluster`
    ```bash
    cd juicefs-cluster
    ```

2. Suba o container do `minio` e do `redis`:
    ```bash
    sudo docker compose up -d minio redis 
    #ou
    docker compose up -d minio redis
    ```

    - Crie um bucket chamado **juicefs** no `minio`: http://localhost:9001/browser

- Para verificar que o Redis está saudável:
    ```bash
    sudo docker exec juicefs-redis redis-cli ping
    ```
    > Deve retornar `PONG`
3. Formatar o *filesystem* do JuiceFS: \
    A formatação serve para interligar os motores independentes (minio e redis) 
    ```bash
    sudo docker run --rm \
    --network juicefs-cluster_juicefs \
    juicedata/mount:ce-v1.3.1 \
    juicefs format \
    --storage s3 \
    --bucket http://minio:9000/juicefs \
    --access-key=minioadmin \
    --secret-key=minioadmin \
    redis://redis:6379/1 \
    meucluster
    ```
    >**ATENÇÃO**: se formatou com sucesso, deve ser executado esta única vez!

    No terminal deve aparecer:
    ```text
    .....
    2026/09/17 21:43:36.101626 juicefs[1] <INFO>: Volume is formatted as {
        "Name": "meucluster",
    .....[Estrutura deste projeto](#estrutura-deste-projeto)
    ```

4. Inicie os container dos nós:
    ```bash
    sudo mkdir -p data/node1 data/node2 data/node3 #crie as pastas
    ```

    Depois:
    ```
    ```bash
    sudo docker compose up -d node1 node2 node3
    #ou
    sudo docker compose up -d
    ```

    - Os cinco serviços devem estar funcionando, verifique:
        ```bash
        sudo docker compose ps
        ```
        > minio \
        redis \
        node1 \
        node2 \
        node3

5. Crie um arquivo rápido:
    - Dê a permissão de execução do script:
        ```bash
        chmod +x demo.py
        ```      
    - Execute-o
        ```bash
        ./demo.py
        ```  
    
    O programa solicita:
    1. qual nó criará o arquivo;
    2. o nome do arquivo;
    3. o conteúdo do arquivo.
   > O propósito é demonstrar que os três nós conseguem acessar o mesmo filesystem.

   Outro método:
   ```bash
   sudo docker exec juicefs-node2 sh -c \ 'echo "arquivo compartilhado" > /mnt/juicefs/arquivo.txt' #cria o arquivo com conteúdo no node2

   sudo docker exec juicefs-node1 cat /mnt/juicefs/arquivo.txt #node 1, para ler

   sudo docker exec juicefs-node3 sh -c \ 'echo "arquivo modificado pelo Node 3" > /mnt/juicefs/arquivo.txt' # node 3 , para modificar
   ```

### Erros conhecidos:
| Erro | Descrição | Solução encontrada |
| :-- | :-- | :-- |
| `database is not formatted` | Redis não tem o metadata do JuiceFS | **Primeira vez no projeto**: executar `juicefs format`. Se já foi formatado, verificar se o Redis perdeu os dados
| `FATAL: Load metadata: dial tcp ...:6379: i/o timeout` | Container não consegue acessar Redis pela rede Docker | Verificar rede; no meu caso, aconteceu no Codespace. Rodar localmente resolveu
