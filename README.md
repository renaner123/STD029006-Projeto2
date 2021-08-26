## ## Projeto prático 2: Replicação primário e secundários

<!--ts-->
   * [Projeto proposto](#Projeto-proposto-e-solução)
   * [Funcionalidades implementadas](#Funcionalidades-implementadas)  
   * [Executando o projeto](#Executando-o-projeto)
   * [Consumindo o serviço com o curl](#Consumindo-o-serviço-com-o-curl)
   * [Documentação](#Documentação)
<!--te-->


## Projeto proposto

Projeto consiste em demonstrar o funcionamento de um processo de commit em duas fases (2PC) de forma simplificada e não usual. A descrição do que foi solicitado encontra-se no [arquivo](projeto2.pdf)


## Funcionalidades implementadas

- [x] Carregar lista de réplicas
- [x] Apagar lista de réplicas
- [x] Obter lista de réplicas
- [x] Obter lista de contas
- [x] Enviar ação
- [x] Enviar decisão
- [x] Obter histórico de ações processadas
- [x] Carregar semente
## Executando o projeto

No arquivo docker-compose.yml estão sendo instanciados os serviços de 3 réplicas, onde a replica1 usara a porta 5001, replica2 porta 5002 e a replica3 a porta 5003. Ambos os containeres deverão receber também um nome para ser usado na rede. Exemplo de um comando para executar uma replica econtrase logo abaixo.

```docker
command: python app.py 5001 replica1
```

Para iniciar as replicas, basta estar no diretório raiz e usar o comando:

```docker
docker-compose up
```

Com os containers rodando, pode-se efetuar alguns exemplos descritos abaixo.

## Consumindo o serviço com o curl

Carregar réplicas
```shell
curl -X POST http://127.0.0.1:5001/replicas -H "Content-Type: application/json" -d '{"replicas" : [{"id" : "replica 1","endpoint" : "http://localhost:5001"},{"id" : "replica 2","endpoint" : "http://localhost:5002"}]}'
```

Enviar uma ação de débito para conta 1234 com valor 15
```shell
curl -X POST http://127.0.0.1:5001/acoes -H "Content-Type: application/json" -d '{"id" : "7c40d404-481c-47fd-98c4-50d307fcee47","operacao" : "debito","conta" : 1234,"valor" : 15.00}'
```

Enviar uma ação de credito para conta 1234 com valor 50
```shell
curl -X POST http://127.0.0.1:5001/acoes -H "Content-Type: application/json" -d '{"id" : "7c40d404-481c-47fd-98c4-50d307fcee47","operacao" : "credito","conta" : 1234,"valor" : 50.00}'
```

Listar as contas salvas em memória
```shel
curl http://127.0.0.1:5001/contas
```

Listar replicas carregadas
```shel
curl http://localhost:5001/replicas
```

Deletar as réplicas carregadas
```shell
curl -X DELETE http://localhost:5001/replicas
```

Listar histórico de ações processadas
```shel
curl http://localhost:5001/historico
```

Semente do gerador de números pseudo aleatórios
```shell
curl -X POST http://127.0.0.1:5001/replicas -H "Content-Type: application/json" -d '{"seed": 123456}'
```


## Documentação

[Essa API foi documentada](https://projeto2std.docs.apiary.io/) de acordo com a especificação API Blueprint e a mesma pode ser visualizada com o [Apiary](https://apiary.io/). O código fonte dessa documentação também está disponível no arquivo [apiary.apib](apiary.apib) nesse repositório.
