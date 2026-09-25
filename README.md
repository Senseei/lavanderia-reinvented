# Lavanderia Reinvented

Sistema web de lavanderia self-service: o usuário escolhe uma unidade, seleciona lavadoras e secadoras, monta um carrinho, aplica cupons de desconto e paga com saldo da carteira ou cartão (pagamentos simulados).

Este foi meu primeiro aplicativo web. Esta versão é a reescrita dele seguindo **Clean Architecture**, com um **container de injeção de dependências próprio**, inspirado no Spring.

## Funcionalidades

- Cadastro e login de usuários (todo usuário novo começa com R$ 2.000,00 de saldo)
- Listagem de unidades e de suas lavadoras e secadoras
- Escolha do ciclo (tempo e preço) de cada máquina
- Carrinho por usuário, guardado na sessão
- Cupons de desconto (percentual ou valor fixo), com validade e uso único por usuário
- Cadastro e remoção de cartões de crédito e débito
- Pagamento com saldo da carteira, crédito ou débito; as máquinas pagas ficam bloqueadas

## Como rodar

**Requisitos:** Python 3.10 ou superior.

```bash
# 1. Crie e ative um ambiente virtual
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Suba a aplicação (a partir da raiz do projeto)
flask --app app run
```

Acesse http://127.0.0.1:5000. Para recarregar a aplicação automaticamente a cada alteração no código, use `flask --app app run --debug`.

### Banco de dados

O banco é um SQLite (`database.db`) criado automaticamente na primeira execução, a partir de `infrastructure/db/sqlite3/schema.sql`. Ele já vem com uma unidade, suas máquinas e os ciclos disponíveis.

- O arquivo é criado na pasta de onde o comando foi executado, por isso rode sempre a partir da raiz do projeto.
- Para recomeçar do zero, apague `database.db` e suba a aplicação de novo.

### Criando um cupom de desconto

Não há tela de administração de cupons. Para testar, insira um direto no banco (com a aplicação já executada ao menos uma vez):

```bash
python3 -c "
import sqlite3
db = sqlite3.connect('database.db')
db.execute(\"INSERT INTO tickets (code, discount, expires_at, type) VALUES ('DESC10', 10, strftime('%s', 'now', '+30 days'), 'PERCENTAGE')\")
db.commit()
"
```

`type` pode ser `PERCENTAGE` (o `discount` é uma porcentagem) ou `FLAT` (o `discount` é um valor em reais). Depois, use o código `DESC10` na tela de pagamento.

## Arquitetura

As dependências apontam sempre para dentro: `infrastructure → presentation → application → domain`. O domínio não depende de nada.

| Camada | Pasta | Responsabilidade |
|---|---|---|
| **Domain** | `domain/` | Entidades e regras puras (`User`, `Machine`, `Ticket`, `Card`...). |
| **Application** | `application/` | Serviços com as regras de negócio e as interfaces dos repositórios. Recebem e devolvem **entidades**, nunca DTOs. |
| **Presentation** | `presentation/` | Controllers, DTOs e WebServices. O WebService é o orquestrador: chama os serviços e converte entidades em DTOs. Nada aqui depende do Flask. |
| **Infrastructure** | `infrastructure/` | Tudo que é específico de framework: rotas Flask, templates, sessão, repositórios SQLite. |

Fluxo de uma requisição:

```
Router (Flask) → Controller → WebService → Service → Repository (SQLite)
                                  ↑
                     entidades viram DTOs aqui
```

### Injeção de dependências (`di/`)

Um container simples no estilo do Spring, escrito do zero:

- **`@component`** marca uma classe para ser gerenciada pelo container (como o `@Component` do Spring).
- **`scan(...)`** importa todos os módulos dos pacotes informados, para que os decorators sejam executados.
- **`Container`** monta cada classe lendo os type hints do construtor (injeção via construtor). Quando o tipo pedido é uma interface, como `UnitRepository`, o container injeta a implementação registrada (`UnitRepositoryImpl`). Todo componente é singleton, e dependências ausentes, ambíguas ou circulares geram erros claros.

```python
@component
class UnitService:
    def __init__(self, repository: UnitRepository):  # recebe UnitRepositoryImpl
        self._repository = repository
```

O container é criado uma única vez em `app.py`, e as rotas pedem a ele seus controllers:

```python
container = Container.from_packages("application", "presentation", "infrastructure")
```

## Estrutura

```
├── app.py              # ponto de entrada: cria o app Flask e o container
├── di/                 # container de injeção de dependências
├── domain/             # entidades e enums
├── application/        # serviços, interfaces de repositório, erros
├── presentation/       # controllers, web services e DTOs, por funcionalidade
└── infrastructure/
    ├── db/sqlite3/     # schema, conexão e repositórios
    └── flask/          # rotas, templates, arquivos estáticos, sessão do carrinho
```

## Tecnologias

- Python e Flask
- Flask-Session (sessões em arquivo)
- SQLite
