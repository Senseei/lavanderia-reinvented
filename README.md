# lavanderia

Bem-vindo(a)!

Este foi meu primeiro aplicativo web, feito inicialmente de maneira simples, agora reestruturado para seguir a **Clean Architecture** e as boas práticas de desenvolvimento.

## O que mudou?

O projeto foi refatorado para adotar a Clean Architecture, separando responsabilidades em camadas bem definidas:

- **Domain**: Entidades e regras de negócio puras.
- **Application**: Casos de uso e serviços com as regras de negócio; retornam entidades, nunca DTOs.
- **Presentation**: Controllers, DTOs e WebServices (orquestradores que convertem entidades em DTOs). Fluxo: `Router → Controller → WebService → Service → Repository`.
- **Infrastructure**: Frameworks externos (rotas Flask, banco SQLite, etc).

## Benefícios

- Código desacoplado e testável
- Facilidade para manutenção e evolução
- Separação clara de responsabilidades

## Tecnologias

- Linguagem: Python
- Framework: Flask
- Arquitetura: Clean Architecture
- Organização: Modular, por camadas

## O que faz?

É um sistema de lavanderia self-service, com cadastro de usuários, locais, máquinas, produtos, compra de serviços e simulação de pagamentos.