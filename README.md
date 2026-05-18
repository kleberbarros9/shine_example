# Shiny Dashboard Example (Python)

Dashboard estatístico desenvolvido com Shiny for Python.

O projeto contém:

- Reatividade
- Cards
- Slider
- Dropdown
- Radio buttons
- Tabelas interativas
- Gráficos estatísticos com matplotlib
- Navegação com múltiplas páginas

---

# Instalação

## Clonar o repositório

```bash
git clone https://github.com/kleberbarros9/shine_example.git
```

## Entrar na pasta

```bash
cd shine_example
```

## Criar ambiente virtual

```bash
python3 -m venv shiny_env
```

## Ativar ambiente virtual

Linux:

```bash
source shiny_env/bin/activate
```

Windows:

```bash
shiny_env\Scripts\activate
```

## Instalar dependências

```bash
pip install shiny pandas numpy matplotlib
```

---

# Executar o projeto

```bash
shiny run app.py --reload
```

---

# Acesso HTTP

Após executar, abrir no navegador:

```text
http://127.0.0.1:8000
```

ou

```text
http://localhost:8000
```

---

# Estrutura do projeto

```text
shine_example/
│
├── app.py
├── README.md
└── .gitignore
```

---

# Tecnologias

- Python
- Shiny for Python
- Pandas
- NumPy
- Matplotlib
