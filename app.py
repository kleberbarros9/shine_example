from shiny import App, ui, render, reactive
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =========================================================
# DADOS SIMULADOS
# =========================================================

np.random.seed(123)

df = pd.DataFrame({
    "grupo": np.repeat(["Controle", "Tratamento A", "Tratamento B"], 100),
    "idade": np.random.randint(18, 70, 300),
    "sexo": np.random.choice(["Masculino", "Feminino"], 300),
    "valor": np.concatenate([
        np.random.normal(50, 10, 100),
        np.random.normal(60, 12, 100),
        np.random.normal(70, 15, 100)
    ])
})

df["valor"] = df["valor"].round(2)


# =========================================================
# INTERFACE
# =========================================================

app_ui = ui.page_navbar(

    ui.nav_panel(
        "Dashboard",

        ui.layout_sidebar(

            ui.sidebar(
                ui.h4("Filtros"),

                ui.input_slider(
                    "idade",
                    "Faixa de idade",
                    min=18,
                    max=69,
                    value=[25, 60]
                ),

                ui.input_select(
                    "grupo",
                    "Grupo",
                    choices=["Todos", "Controle", "Tratamento A", "Tratamento B"],
                    selected="Todos"
                ),

                ui.input_radio_buttons(
                    "grafico",
                    "Tipo de gráfico",
                    choices={
                        "hist": "Histograma",
                        "box": "Boxplot"
                    },
                    selected="hist"
                )
            ),

            ui.layout_columns(
                ui.value_box(
                    "Número de observações",
                    ui.output_text("n_obs"),
                    showcase="📊"
                ),
                ui.value_box(
                    "Média",
                    ui.output_text("media"),
                    showcase="📈"
                ),
                ui.value_box(
                    "Desvio-padrão",
                    ui.output_text("desvio"),
                    showcase="📉"
                )
            ),

            ui.card(
                ui.card_header("Gráfico estatístico"),
                ui.output_plot("grafico_estatistico")
            ),

            ui.card(
                ui.card_header("Tabela filtrada"),
                ui.output_data_frame("tabela")
            )
        )
    ),

    ui.nav_panel(
        "Resumo",

        ui.layout_sidebar(

            ui.sidebar(
                ui.h4("Opções"),

                ui.input_select(
                    "variavel_resumo",
                    "Variável de agrupamento",
                    choices={
                        "grupo": "Grupo",
                        "sexo": "Sexo"
                    },
                    selected="grupo"
                ),

                ui.input_radio_buttons(
                    "estatistica",
                    "Estatística",
                    choices={
                        "mean": "Média",
                        "median": "Mediana",
                        "std": "Desvio-padrão"
                    },
                    selected="mean"
                )
            ),

            ui.card(
                ui.card_header("Resumo estatístico"),
                ui.output_data_frame("tabela_resumo")
            ),

            ui.card(
                ui.card_header("Gráfico do resumo"),
                ui.output_plot("grafico_resumo")
            )
        )
    ),

    title="Dashboard Estatístico em Shiny Python"
)


# =========================================================
# SERVIDOR
# =========================================================

def server(input, output, session):

    @reactive.calc
    def dados_filtrados():
        dados = df.copy()

        idade_min, idade_max = input.idade()

        dados = dados[
            (dados["idade"] >= idade_min) &
            (dados["idade"] <= idade_max)
        ]

        if input.grupo() != "Todos":
            dados = dados[dados["grupo"] == input.grupo()]

        return dados

    @output
    @render.text
    def n_obs():
        return str(len(dados_filtrados()))

    @output
    @render.text
    def media():
        return f"{dados_filtrados()['valor'].mean():.2f}"

    @output
    @render.text
    def desvio():
        return f"{dados_filtrados()['valor'].std():.2f}"

    @output
    @render.plot
    def grafico_estatistico():
        dados = dados_filtrados()

        fig, ax = plt.subplots(figsize=(7, 4))

        if input.grafico() == "hist":
            ax.hist(dados["valor"], bins=20, edgecolor="black")
            ax.set_title("Histograma dos valores")
            ax.set_xlabel("Valor")
            ax.set_ylabel("Frequência")

        else:
            dados.boxplot(column="valor", by="grupo", ax=ax)
            ax.set_title("Boxplot por grupo")
            ax.set_xlabel("Grupo")
            ax.set_ylabel("Valor")
            fig.suptitle("")

        return fig

    @output
    @render.data_frame
    def tabela():
        return render.DataGrid(
            dados_filtrados(),
            filters=True,
            selection_mode="rows"
        )

    @reactive.calc
    def resumo():
        var = input.variavel_resumo()
        estat = input.estatistica()

        if estat == "mean":
            tab = df.groupby(var)["valor"].mean()
        elif estat == "median":
            tab = df.groupby(var)["valor"].median()
        else:
            tab = df.groupby(var)["valor"].std()

        return tab.reset_index().rename(columns={"valor": "estatistica"})

    @output
    @render.data_frame
    def tabela_resumo():
        return render.DataGrid(
            resumo().round(2),
            filters=True
        )

    @output
    @render.plot
    def grafico_resumo():
        dados = resumo()

        fig, ax = plt.subplots(figsize=(7, 4))

        ax.bar(dados.iloc[:, 0], dados["estatistica"])
        ax.set_title("Resumo estatístico")
        ax.set_xlabel(input.variavel_resumo())
        ax.set_ylabel(input.estatistica())

        return fig


app = App(app_ui, server)