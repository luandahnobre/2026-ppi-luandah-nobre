# 2026-ppi-luandah-nobre

Repositório da disciplina de Programação para Internet (PPI) — 2026.

## Projetos

- **src/tutorial/** — Tutorial oficial do Flask (blog Jardim de Flores 🌸)
- **src/receitas-app/** — App CRUD de receitas culinárias 🍳

## Como rodar o tutorial

```bash
cd src/tutorial
pip install -e .
flask --app flaskr init-db
flask --app flaskr run --debug
```

## Como rodar o app de receitas

```bash
cd src/receitas-app
pip install -e .
flask --app receitas init-db
flask --app receitas run --debug
```
