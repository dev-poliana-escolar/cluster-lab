# storj-cluster-prototype

# Sumário
1. [O que é o Storj?](#o-que-é-o-storj)
2. [O que foi desenvolvido aqui?](#o-que-foi-desenvolvido-aqui)
3. [Como executar?](#como-executar)

## O que é o Storj?
Storj é uma plataforma de armazenamento em nuvem descentralizada que fornece soluções de armazenamento seguras, privadas e eficientes usando a tecnologia blockchain para criar uma rede distribuída de nós de armazenamento em todo o mundo. Muito comum em criptomoedas.

## O que foi desenvolvido aqui?
Apenas **um protótipo** que simula como o Storj funciona.\
Segue abaixo o que não foi implementado:

1. **Criptografia:** O arquivo seria criptografado antes de sair do cliente. 
    > No Storj, o armazenamento é projetado para que os nós não tenham acesso ao conteúdo original.
2. **Erasure coding/redundância**: haveria divisão em vários segmentos com redundância, permitindo recuperar o arquivo mesmo se alguns nós ficarem indisponíveis.
    > Isto é, o arquivo não seria simplesmente partido em partes 1, 2 e 3, como fiz.
3. **Identidade e autenticação dos nós:** Cada *storage node* precisaria ter uma identidade própria e mecanismos para provar que é um nó autorizado.

Entre outras coisas, visto que a arquitetura foi simplificada **para fins acadêmicos**.\
O protótipo **não implementa a rede Storj real** e não utiliza a infraestrutura pública do Storj.\
Essa é a documentação oficial: [Storj Docs](https://storj.dev/)

## Como executar?

1. Abra um terminal e execute o comando:
    ```bash
    docker compose up --build
    ```
    > Você deve ver que foram criadas e iniciadas **três** containers `Flask`

2. Abra outro terminal, entre na pasta client:\
Você pode ver que ela já tem um arquivo de exemplo denominado `arquivo.txt, portando:
    ```bash
    cd client #para entrar na pasta
    python upload.py 
    ```
    Para recuperar:
    ```bash
    python download.py
    ```

3. Caso queira ver a saúde de cada nó, basta:
    ```bash
    curl http://localhost:5001/health
    curl http://localhost:5002/health
    curl http://localhost:5003/health
    ```

    Cada nó deve retornar seu status como `online`.\
    Os nós são identificados no Docker como:
    ```
    storj-node1
    storj-node2
    storj-node3
    ```
    > Os três nós deste projeto são executados como containers Docker na mesma máquina. Portanto, representam três nós lógicos para fins de demonstração, e não três máquinas físicas independentes.