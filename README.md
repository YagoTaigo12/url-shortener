#  Encurtador de URLs – Sprint 4

Implementação do **sistema de cache com Redis** para otimizar a velocidade de redirecionamento, **complementando a segurança** de acesso via JWT. As funcionalidades de **criação e gestão de URLs curtas** agora exigem autenticação e contam com um sistema de failover para garantir a disponibilidade.

---
# Novidades da Sprint 4 (Cache Redis)

* **Otimização de Redirecionamento:** A rota GET /{short_code} agora consulta o cache Redis primeiro, antes de buscar no MySQL. Isso reduz drasticamente a latência e a carga do banco para leituras frequentes.

* **Failover Automático:** Se o serviço Redis estiver indisponível, a aplicação automaticamente recorre ao MySQL para garantir que o redirecionamento continue funcionando (padrão fail-soft).

* **Invalidação Assíncrona:** A atualização e a exclusão de URLs são realizadas em Background Tasks (FastAPI) para não bloquear a resposta HTTP enquanto o cache é atualizado.


## 📅 Cronograma do Projeto

**Semana 1:** Setup e configuração inicial do ambiente (estrutura, containers, integração FastAPI + MySQL + Docker Compose).
**Semana 2:** Implementação do backend base – CRUD de URLs, geração de códigos curtos e redirecionamento.
**Semana 3:** **Implementação completa da autenticação JWT** e persistência de usuários no banco de dados. (LDAP adiado para v2.0)
**Semana 4:** Implementação de cache Redis.
**Semana 5:** Configuração do Nginx e HTTPS.
**Semana 6:** Desenvolvimento do frontend.
**Semana 7:** Testes, documentação e ajustes finais do MVP.

---

## 🛠️ Tecnologias Utilizadas

* Python 3.10+
* FastAPI
* Passlib / Python-JOSE (JWT/Hashing)
* SQLAlchemy 2.0
* MySQL 8
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

###  Subir o ambiente com Docker Compose

```bash
docker-compose up --build
```

O Docker realiza:

* Criação da rede e containers
* Inicialização do MySQL
* Espera automática via healthcheck
* Execução do backend FastAPI no contêiner principal

---

## Acesso à Aplicação

* **API:** [http://localhost:8000](http://localhost:8000)
* **Documentação Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)

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

* Banco **MySQL** inicializa com base `url_shortener`
* **Redis** disponível para cachin
* API **FastAPI** disponível em `http://localhost:8000`
* Documentação interativa em `http://localhost:8000/docs`
* Sistema pronto para autenticação, CRUD e redirecionamento OTIMIZADO por cache

---

## Próximas Etapas (Sprint 5)

* Configuração do Nginx e HTTPS.
