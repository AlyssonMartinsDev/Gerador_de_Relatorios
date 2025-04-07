import plotly.express as px
import  pandas as pd 


def create_single_product_pie_chart(best_selling_product, quantity_selling, total_selling ):
    """
        Gera um grafico de pizza destacando  o produto com maior venda.

        :param df -> DataFrame contendo os dados das vendas 
        :return -> Objeto grafico Plotly
    """



    data = pd.DataFrame({
        'Categoria': [best_selling_product, 'Outros'],
        'Quantidade': [quantity_selling, total_selling]
    }) # criando o dataframe com os dados para o grafico de pizza 


    fig = px.pie(
        data_frame=data, 
        names='Categoria',
        values='Quantidade',
        title=f'{best_selling_product}: {quantity_selling / total_selling.sum():.2%}', # Definindo o titulo 
        color_discrete_sequence=[ px.colors.qualitative.Set3[0], px.colors.qualitative.Set3[1]], # Definindo as cores
    )
    

    return fig

def create_pie_chart(data: pd.DataFrame, title: str):
    
    """
        Cria um grafico de pizza com dois dados

    """

    
    label_column, value_column = data.columns

    
    fig = px.pie(
        data_frame=data,
        names=label_column,
        values=value_column,
        title=title,
        color_discrete_sequence=px.colors.qualitative.Set3[:3],
    )

    return fig



