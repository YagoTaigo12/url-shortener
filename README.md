#  Encurtador de URLs – Sprint 6 (Frontend MVP)

Implementação da **Interface Visual (Frontend)**, transformando o projeto em uma aplicação Fullstack. Agora, além da API segura, o sistema conta com um Dashboard responsivo para gerenciamento de URLs, login integrado e feedback visual, tudo servido através do Nginx com HTTPS.

A arquitetura evoluiu para um modelo robusto onde o **Nginx** atua simultaneamente como:

* **Web Server:** Servindo os arquivos estáticos (HTML, CSS, JS) do frontend.
* **Reverse Proxy:** Roteando chamadas de API (/api/...) para o backend FastAPI.
* **SSL Terminator:** Garantindo HTTPS em todas as pontas.

---

## Novidades da Sprint 6 (Frontend & Integração)

- **Frontend Responsivo**  
  Interface construída com **HTML5**, **Vanilla JS** e **Bootstrap 5**, focada em simplicidade e performance.

- **Dashboard de Gestão**, com funcionalidades visuais para:
  - Encurtar novas URLs  
  - Listar histórico recente  
  - Copiar links curtos (Clipboard API)  
  - Excluir URLs  

- **Integração Segura (JWT)**  
  O Frontend gerencia todo o ciclo de vida do **Token JWT**:
  - Login  
  - Armazenamento seguro  
  - Logout automático em caso de expiração  

- **Arquitetura Unificada**
  - API acessada via prefixo `/api`
  - Frontend e Backend coexistem no mesmo domínio (`shrt.cc`)

```yaml
extra_hosts:
  - "shrt.cc:10.138.11.229"
```
Esse mapeamento permite:

* Acesso ao sistema via https://shrt.cc
* Uso de um hostname real para testar HTTPS/SSL
* Comportamento semelhante a um ambiente de produção


## Cronograma do Projeto

**Semana 1:** Setup e configuração inicial (FastAPI + MySQL + Docker)
**Semana 2:** Backend base (CRUD de URLs e redirecionamento)
**Semana 3:** Autenticação JWT e Segurança
**Semana 4:** Cache com Redis
**Semana 5:** Infraestrutura (Nginx, HTTPS e domínio `shrt.cc`)
**Semana 6:** Desenvolvimento do Frontend e Integração Fullstac
**Semana 7:** Testes, documentação final e ajustes de QA

---

## Tecnologias Utilizadas

### Frontend
- HTML5 / CSS3
- JavaScript (ES6+)
- Bootstrap 5

### Backend & Infra
- Python 3.10+ / FastAPI
- Nginx (Reverse Proxy + Web Server)
- HTTPS / SSL (certificados autoassinados)
- MySQL 8
- Redis
- Docker e Docker Compose

---

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

**Importante:** Após gerar os certificados, você deve instalar o arquivo nginx/certs/shrt.cc.crt no seu sistema operacional como uma Autoridade de Certificação Raiz Confiável para evitar avisos de segurança no navegador durante o desenvolvimento.

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

## Próximas Etapas (Sprint 7)

* Testes de integração ponta a ponta
* Refinamento da documentação técnica
* Empacotamento final do MVP para distribuição