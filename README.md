# 2026-ppi-luandah-nobre

Repositório da disciplina de Programação para Internet (PPI) — 2026.

## Projetos

- **src/tutorial/** — Tutorial oficial do Flask (blog Jardim de Flores 🌸)
- **src/receitas-app/** — App CRUD de receitas culinárias 🍳
- **src/blog-news/** — Blog de notícias com Flask + MySQL 📰

---

## Projeto Semestral: Blog News 📰

### Descrição

Plataforma de publicação de notícias onde usuários podem se cadastrar, criar matérias com imagens, editar e excluir suas publicações. O sistema utiliza autenticação com email/senha e persistência em banco de dados MySQL.

### Funcionalidades

- Cadastro e login de usuários (email + senha com hash)
- Criar notícias com título, conteúdo e imagem
- Listar todas as notícias (feed público)
- Editar e excluir notícias (apenas o autor)
- Interface responsiva

### Stack

- **Backend:** Python + Flask
- **Banco de dados:** MySQL 8.0
- **Frontend:** Jinja2 + CSS3
- **CI:** GitHub Actions com flake8

### Como rodar

```bash
cd src/blog-news
pip install -r requirements.txt
cp .env.example .env
# edite o .env com suas credenciais MySQL
flask --app blog_news run --debug
```

---

## Outros projetos

### Tutorial Flask
```bash
cd src/tutorial
pip install -e .
flask --app flaskr init-db
flask --app flaskr run --debug
```

### App de Receitas
```bash
cd src/receitas-app
pip install -e .
flask --app receitas init-db
flask --app receitas run --debug
```
