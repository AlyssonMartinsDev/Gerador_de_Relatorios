import pandas as pd
from plotly.graph_objects import Figure
import os
import tempfile





def load_data(file_path):
    """ Carrega os dados do arquivo.csv"""
    return pd.read_csv(file_path)


COLUMN_MAPPING = {
    "Data": ["Data", "data", "Data de Venda", "Dia"],
    "Produto": ["Produto", "Item", "Mercadoria", "produto"],
    "Quantidade": ["Quantidade", "Qtd", "Qtd Vendida", "quantidade"],
    "Preço Unitário": ["Preço Unitário", "Valor Unitário", "Preço", "preco_unitario"],
    "Total de Vendas": ["Total de Vendas", "Valor Total", "Total", "Total Venda", "total venda"]
}


def normalize_column_names(df: pd.DataFrame):

    """ 
        Essa funçã e resposavel por verificar se as colunas necessarias estao presentes e normalizar o nome das colunas caso esteja
        params: df -> aqui recebemos o frame de dados carregado
        return: df -> frame de dados com as colunas normalizadas
    """
    column_corrections = {}

    
    # Normaliza os nomes das colunas que vieram
    for standard_name, possible_names in COLUMN_MAPPING.items():
        for file_column in df.columns:
            if file_column in possible_names:
                column_corrections[file_column ] = standard_name
    
    # Renomeia as colunas
    df.rename(columns=column_corrections, inplace=True)


    # Verifica se as colunas necessárias estão presentes após a normalização
    missing_columns = [col for col in COLUMN_MAPPING.keys() if col not in df.columns]

    if missing_columns:
        raise ValueError(f"O arquivo CSV está faltando as seguintes colunas obrigatórias: {', '.join(missing_columns)}")

    
    return df

def validations(df: pd.DataFrame):
    """"
        Realizando as validações necessarias para o dataframe e garantir que ele esteja pronto para o processamento"
    """
    # normaliza e verifica se as colunas necessarias estão presentes
    df = normalize_column_names(df=df)

    # estamos garantindo que o o tipos de dados estao no formato correto
    df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce')
    df['Preço Unitário'] = pd.to_numeric(df['Preço Unitário'], errors='coerce')
    df['Total de Vendas'] = pd.to_numeric(df["Total de Vendas"], errors='coerce')
    df['Data'] = pd.to_datetime(df['Data'], errors="raise")

    # Garantindo valores padroes para as colunas
    df.fillna({
        'Quantidade': 0,
        'Preço Unitário': 0,
        'Total de Vendas': 0
    }, inplace=True)

    # Removendo dados duplicados
    df.drop_duplicates(inplace=True)

    # Verificando se ha valores fora do esperado caso nao atenda ao requisito o dado nao e exibido
    df = df[df['Quantidade'] > 0]

    # Verificando a consistencia dos dados
    df['Vendas_validas'] = df['Preço Unitário'] * df['Quantidade'] == df['Total de Vendas']

    if not df['Vendas_validas'].all():
        raise ValueError("A consistência dos dados está comprometida. O total de vendas não corresponde ao valor calculado.")
    return df



    df.describe()

    return df

def get_best_selling_product(data: pd.Series) -> tuple:
    """
        função analisa o data frame e retor o produto mais vedido, valor total em vendas, quantidade vendida e relação a outro produtos

        :param df -> DataFrame para a analise
        :return -> Tupla com o produto mais vendido e o valor total de vendas
    """
   
    products_and_total_sales = data.groupby("Produto").agg(
        {
            "Quantidade": "sum",
            "Total de Vendas": "sum"
        }
    ) # Agrupando os dados por produto e calculando o total de vendas

    # Extraindo o nome do produto mais vendido
    best_selling_product = products_and_total_sales["Quantidade"].idxmax()

    # Extraindo a quantidade de vendas desse produto
    best_selling_quantity = products_and_total_sales.loc[best_selling_product, "Quantidade"]

    # Extraindo o total das vendas desse produto
    best_selling_total_sales = products_and_total_sales.loc[best_selling_product, "Total de Vendas"]



    return (best_selling_product, best_selling_quantity, best_selling_total_sales)
    
def get_best_profitable_product(df:pd.DataFrame):

    """
        Essa função e responsavel por identificar o produto mais lucrativo, o valor total de vendas, a quantidade vendida
        :param -> DataFrame para a analise
        :return -> Tupla com o produto mais lucrativo e o valor total de vendas
    """


    data = df.groupby("Produto")["Total de Vendas"].sum()
    
    best_profitable_product = data.idxmax()
    best_profitable_total_sales = data.max()
    best_profitable_quantity = df.loc[df['Produto'] == best_profitable_product, 'Quantidade'].sum()

    return (best_profitable_product, best_profitable_quantity, best_profitable_total_sales)

def filter_by_date (df: pd.DataFrame, start_date, end_date, column:str):
    """
        A função e resposavel por filtrar os dados para uma data especifica
        :param -> DataFrame para a analise
        :param -> Data para a filtragem
        :return -> DataFrame filtrado
    """

    df[column] = df[column].dt.date
    df = df[(df[column] >= start_date) & (df[column] <= end_date)]

    
    return df

def get_avarage_ticket(df: pd.DataFrame):
    """
        Essa função e responsavel por obter o ticket medio do produto
        :param -> DataFrame para a analise
        :return -> Ticket medio do produto
    """

    total_revenue  = df["Total de Vendas"].sum()
    total_orders = len(df)

    avarage_ticket = total_revenue / total_orders

    return avarage_ticket
    
def generate_pdf(data_report: dict, report_name: str = "relatorio.pdf"):
    import pdfkit
    from platformdirs import user_documents_dir
    from pathlib import Path
    import platform


    

    products = ''
    if data_report["filters_chart_distribuition_by_product"]["selected_products"] != []:
        for product in data_report["filters_chart_distribuition_by_product"]["selected_products"]:
            products += f'{product} '
    else:
        products = 'Todos os produtos'

    data = {
        **data_report["metrics"],
        **data_report["graphics_path"],
        **data_report["filters_chart_distribuition_by_product"],
        **data_report["filters_chart_total_sales"],
        "products": products
    }

    html = """
    <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Relatório de Vendas</title>
            <style>
                body {{ max-width: 750px; font-family: 'Times New Roman', Times, serif; }}
                .container {{ display: flex; flex-direction: column; align-items: center; }}
                .content-insights {{ display: flex; justify-content: space-between; }}
                .content-insights div {{ margin: 0 10px; }}
                .pie-charts {{ display: flex; justify-content: space-between; }}
                .pie-charts img, .chart img {{ max-width: 100%; height: auto; }}
                .filters-dp {{ display: flex; font-size: 10pt; }}
                .chart {{ margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Relatório de Vendas</h1>

                <h2>Insights</h2>
                <div class="content-insights">
                    <div>
                        <h4>Total de Pedidos</h4>
                        <p>{total_orders}</p>
                    </div>
                    <div>
                        <h4>Total de Itens Vendidos</h4>
                        <p>{total_items_sold}</p>
                    </div>
                    <div>
                        <h4>Faturamento Total</h4>
                        <p>R$ {total_biling}</p>
                    </div>
                    <div>
                        <h4>Ticket Médio</h4>
                        <p>R$ {avg_ticket}</p>
                    </div>
                </div>

                <h2>Gráficos de Produto</h2>
                <div class="pie-charts">
                    <div>
                        <h4>Mais Lucrativo</h4>
                        <img src="{best_profitable}" alt="Mais Lucrativo">
                    </div>
                    <div>
                        <h4>Mais Vendido</h4>
                        <img src="{best_selling_product}" alt="Mais Vendido">
                    </div>
                </div>

                <h2>Vendas Totais</h2>
                <div class="chart">
                    <img src="{total_sales}" alt="Vendas Totais">
                </div>

                <h2>Distribuição por Produto</h2>
                <div class="filters-dp">
                    <p><strong>De:</strong> {data_range_dbp[0]} até {data_range_dbp[1]}</p>
                    <p><strong>Produto(s):</strong>{products}</p>
                    <p><strong>Faixa de preço:</strong> R$ {min_price} até R$ {max_price}</p>
                    <p><strong>Quantidade mínima vendida:</strong> {min_quantity}</p>
                </div>
                <div class="chart">
                    <img src="{sales_distribuition}" alt="Distribuição por Produto">
                </div>
            </div>
        </body>
        </html>

    """.format(**data)

    system = platform.system()

    if system == "Windows":
        wkhtmltopdf_path = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
    elif system == "Linux":
        wkhtmltopdf_path = "/usr/bin/wkhtmltopdf"
    else:
        print("Sistema nao suportado")

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    options = {
        'encoding': 'UTF-8',
        'enable-local-file-access': None,  # Necessário para imagens locais
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }

    documents_path = Path(user_documents_dir()) / "relatorios"
    documents_path.mkdir(parents=True, exist_ok=True)

    full_path = f"{documents_path}/{report_name}"
    
    pdfkit.from_string(html, full_path, options=options, configuration=config)

def save_chart_as_temp_image(fig: Figure) -> str:

    """
        Função responsavel por salvar uma imagem temporariamente no sistema e retornar o caminho/nome dela
        :param -> Figura para a imagem
        :return -> Caminho para a imagem
    """

    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)

    fig.write_image(temp_file.name)

    temp_file.close()

    return temp_file.name