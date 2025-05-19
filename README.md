# lavanderia

Bem-vindo(a)!

Este foi meu primeiro aplicativo web, feito inicialmente de maneira simples, agora reestruturado para seguir a **Clean Architecture** e as boas práticas de desenvolvimento.

## O que mudou?

O projeto foi refatorado para adotar a Clean Architecture, separando responsabilidades em camadas bem definidas:

- **Domain**: Entidades e regras de negócio puras.
- **Use Cases (Application)**: Casos de uso da aplicação, orquestrando as regras de negócio.
- **Interface Adapters**: Adaptadores para entrada (controllers, views) e saída (repositórios, gateways).
- **Frameworks & Drivers**: Frameworks externos (Flask, banco de dados, etc).

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