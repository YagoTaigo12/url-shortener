#  Encurtador de URLs – Sprint 5

Implementação do **Proxy Reverso Nginx e HTTPS/SSL e suporte ao domínio customizado shrt.cc**, garantindo que toda a comunicação com a API e futuros frontends seja criptografada e usando um domínio único para acesso durante o desenvolvimento.

A aplicação agora segue os padrões de arquitetura de produção: proxy reverso dedicado, SSL obrigatório, isolamento do backend e uso de certificados auto-assinados criados localmente.
---

# Novidades da Sprint 5 (Nginx, HTTPS e Domínio shrt.cc)

* **Camada de Segurança (HTTPS):** Toda a aplicação agora é servida via HTTPS (porta 443), utilizando certificados SSL auto-assinados para o ambiente local.
* **Proxy Reverso:** O Nginx atua como ponto de entrada único, roteando o tráfego externo para o container FastAPI (backend).
* **Redirecionamento Automático:** Todo o tráfego HTTP (porta 80) é automaticamente redirecionado para HTTPS (porta 443), forçando o acesso seguro.
* **Arquitetura de Produção:** O acesso direto ao FastAPI na porta 8000 foi desabilitado externamente, sendo acessível apenas pelo Nginx (melhor prática de segurança e infraestrutura).
* **Script de Setup de Certificados:** Adição de um script auxiliar (nginx/setup_certs.sh) para simplificar a geração dos certificados SSL auto-assinados necessários para o Nginx
* **Novo domínio local: shrt.cc:** A aplicação agora suporta o acesso pelo domínio customizado shrt.cc. Este domínio é resolvido internamente pelo Docker através do extra_hosts: 

```yaml
extra_hosts:
  - "shrt.cc:10.138.11.229"
```
Esse mapeamento permite:

* Acesso ao sistema via https://shrt.cc
* Uso de um hostname real para testar HTTPS/SSL
* Comportamento semelhante a um ambiente de produção


## Cronograma do Projeto

**Semana 1:** Setup e configuração inicial do ambiente (estrutura, containers, integração FastAPI + MySQL + Docker Compose).
**Semana 2:** Implementação do backend base – CRUD de URLs, geração de códigos curtos e redirecionamento.
**Semana 3:** Implementação completa da autenticação JWT e persistência de usuários no banco de dados. (LDAP adiado para v2.0)
**Semana 4:** Implementação de cache Redis.
**Semana 5:** Configuração do Nginx, HTTPS e domínio.
**Semana 6:** Desenvolvimento do frontend.
**Semana 7:** Testes, documentação e ajustes finais do MVP.

---

## Tecnologias Utilizadas

* Python 3.10+
* FastAPI
* **Nginx**
* **HTTPS/SSL (Certificados auto-assinados para shrt.cc)**
* Passlib / Python-JOSE (JWT/Hashing)
* SQLAlchemy 2.0
* MySQL 8
* Redis (Cache)
* Alembic (migrações)
* Docker + Docker Compose
* Uvicorn (ASGI)
* Healthcheck de serviço (aguarda MySQL antes de iniciar a API)

---

## Setup do Projeto

### Clonar o repositório

```bash
git clone https://github.com/seu-usuario/url-shortener.git
cd url-shortener
```

### Preparação dos Certificados SSL

* Antes de subir a aplicação, é **obrigatório** gerar os certificados SSL auto-assinados para o Nginx.

# Navega para a pasta do Nginx
cd nginx 

# Torna o script executável
chmod +x setup_certs.sh

# Executa o script para gerar shrt.cc.key e shrt.cc.crt em nginx/certs
./setup_certs.sh

# Volta para a raiz do projeto
cd ..

**Importante:** Após gerar os certificados, você deve instalar o arquivo nginx/certs/localhost.crt no seu sistema operacional como uma Autoridade de Certificação Raiz Confiável para evitar avisos de segurança no navegador durante o desenvolvimento.

###  Subir o ambiente com Docker Compose

```bash
docker-compose up --build
```

O Docker realiza:

* Criação da rede e containers
* Inicialização do MySQL
* Espera automática via healthcheck
* Execução do backend FastAPI no contêiner principal
* **Inicialização do Nginx, que passa a ser o ponto de entrada**

---

## Acesso à Aplicação

**Via domínio customizado**
* **API:** [https://shrt.cc](https://shrt.cc)
* **Documentação Swagger:** [https://shrt.cc/docs](https://shrt.cc/docs)

**Também disponível via localhost**
* https://localhost
* https://localhost/docs

---

## Endpoints Principais

| Método                      | Rota                             | Descrição |
| :-------------------------- | :------------------------------- | :-------- |
| `POST /urls/`               | Cria uma URL curta               |           |
| `GET /urls/`                | Lista as URLs cadastradas        |           |
| `DELETE /urls/{short_code}` | Remove uma URL pelo código curto |           |
| `GET /{short_code}`         | Redireciona para a URL original  |           |

---

##  Resultado Esperado

Após rodar:

```bash
docker-compose up --build
```
* Os serviços MySQL e Redis estarão rodando.
* A API FastAPI estará rodando internamente na porta 8000.
* O Nginx estará roteando o tráfego.
* A API e documentação interativa estarão acessíveis via https://shrt.cc

---

## Próximas Etapas (Sprint 6)

* Desenvolvimento do frontend – construção de uma interface simples em HTML e Bootstrap integrada à API para encurtamento e gerenciamento de URLs.