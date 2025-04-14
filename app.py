""" Arquivo principal do APP"""

# Importis
import streamlit as st
import pandas as pd
import plotly.express as px
import data_processing as dp
import charts
import tempfile
import os  



# =============== Iniciando a aplicação

st.set_page_config(page_title="Gerador de Relatórios", layout='wide')
st.title("📊 Gerador de Relatórios Automático")
st.write("Carregue seu arquivo CSV para visualizar os dados e gerar relatorios interativos")


uploaded_file = st.file_uploader("Envie um arquivo CSV", type=['csv'])

if not uploaded_file:
    st.warning("Por favor, faça o upload de um arquivo CSV")
    st.stop()


try:
    # Carregando os dados do arquivo fornecido
    df = dp.load_data(uploaded_file)

    # Realizando as validações para garantir que o arquivo esteja apto para ser manipulado
    df = dp.validations(df)

    st.subheader("Dados Carregados")
    st.write(df)


    st.subheader("Insights")
    col1, col2, col3, col4 = st.columns(4)
    with col3:

        total_items_sold = df['Quantidade'].sum()
        

        st.metric(label="Total de itens vendidos", value=f"{total_items_sold:,}")
    with col2:
        total_biling = df["Total de Vendas"].sum()
        st.metric(label="Faturamento Total", value=f"R$ {total_biling:,.2f}")
    
    with col1:
        total_orders = len(df)
        st.metric(label="Total de pedidos", value=f"{total_orders:,}")
    with col4:
        avg_ticket = dp.get_avarage_ticket(df)
        st.metric(label="Ticket Médio", value=f"R$ {avg_ticket:,.2f}")

    col1, col2 = st.columns(2)

    with col1:

        name, quantity, total_sales = dp.get_best_profitable_product(df)

        fig_best_profitable = charts.create_pie_chart(pd.DataFrame({
            "Produto": [name, 'Outros'],
            "Total em vendas": [total_sales, df["Total de Vendas"].sum() - total_sales]
        }), f"Comparção do produto mais lucrativo {name}, com os demais.")
        
        
        st.plotly_chart(fig_best_profitable)

    with col2:
        name, quantity, total_sales = dp.get_best_selling_product(df)

        fig_best_selling_product = charts.create_pie_chart(pd.DataFrame({
            'Produto': [name, "Outros"],
            'Quantidade': [quantity, df['Quantidade'].sum() - quantity],
        }), f"Comparação do produto mais vendido {name}, como os demais.")

        st.plotly_chart(fig_best_selling_product)

    """ Insight de Crecimento diario grafico de linha """
    st.subheader('Crescimento diario das vendas.')

    

    data_range_ts = st.date_input("Selecionar o periodo", [])
    
    daily_sales = df.groupby("Data")["Total de Vendas"].sum()
    if len(data_range_ts) == 2:
        daily_sales = dp.filter_by_date(df, data_range_ts[0], data_range_ts[1], "Data")
        daily_sales.groupby("Quantidade")["Total de Vendas"].sum()
    
        

    
    fig_total_sales = px.line(
        daily_sales, 
        x=daily_sales.index, 
        y="Total de Vendas",
        title=""
    )

    st.plotly_chart(fig_total_sales)
    
    # ========================================================== 
    # ================  INSIGHT DE QUANTIDADE TOTAL VENDIDA POR PRODUTOS ===============
    dataFrame = df
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        data_range_dbp = st.date_input("Selecione o periodo entre datas que deseja filtrar", [])
        
        if len(data_range_dbp) == 2:
            dataFrame = dp.filter_by_date(dataFrame, data_range_dbp[0], data_range_dbp[1], "Data")
        
    with col2:
        selected_products = st.multiselect("Filtrar por produto", df["Produto"].unique())

        if selected_products:
            dataFrame = dataFrame[dataFrame["Produto"].isin(selected_products)]

        
    with col3:

        min_price, max_price = dataFrame["Preço Unitário"].min(), dataFrame["Preço Unitário"].max()

        if min_price == max_price:
            min_price -=1
            max_price +=1

        selected_price = st.slider(
            "Filtrar por faixa de preço",
            float(min_price),
            float(max_price),
            (float(min_price), float(max_price))
        )

        dataFrame = dataFrame[
            (dataFrame["Preço Unitário"] >= selected_price[0]) & (dataFrame["Preço Unitário"] <= selected_price[1])
        ]
        
        
    with col4:

        min_quantity = st.number_input(
            "Mostrar produtos com minimo de X quantidade vendidas.",
            min_value=1,
            max_value=int(dataFrame["Quantidade"].max()),
            value=1,
            step=1
        )

        dataFrame = dataFrame[dataFrame["Quantidade"] >= min_quantity]
        
    


    sales_distribuition = dataFrame.groupby("Produto")["Quantidade"].sum().sort_values(ascending=False)

    sales_distribuition_zf = sales_distribuition.reset_index()

    fig_sales_distribuition_by_product = px.bar(
        sales_distribuition_zf,
        x="Produto",
        y="Quantidade",
        title="Distribuição de vendas por produto.",
        color="Quantidade",
        color_continuous_scale=px.colors.sequential.Plasma,
    )
    st.plotly_chart(fig_sales_distribuition_by_product)

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        report_name = st.text_input("De um nome ao seu relatório, caso contrario seguira como 'Relatório de Vendas'.")


    
    if st.button("Gerar Relatório em PDF"):
        
        
        
        try:
            best_profitable_fig_path = dp.save_chart_as_temp_image(fig_best_profitable)
            total_sales_fig_path = dp.save_chart_as_temp_image(fig_total_sales)
            best_selling_fig_path = dp.save_chart_as_temp_image(fig_best_selling_product)
            sales_distribuition_fig_path = dp.save_chart_as_temp_image(fig_sales_distribuition_by_product)

            # Salva todos os caminhos das imagens em um array para excluir depois que forem utilizadas
            temp_files = [
                best_profitable_fig_path,
                total_sales_fig_path,
                best_selling_fig_path,
                sales_distribuition_fig_path
            ]

            total_biling = f"{total_biling:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            avg_ticket = f"{avg_ticket:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

            if len(data_range_dbp) == 0:
                data_range_dbp = ('NÃO', 'SELECIONADO')
            
            if len(data_range_ts) == 0:
                data_range_ts = ('NÃO', 'SELECIONADO')

            if not report_name:
                report_name = 'Relatório de Vendas'


            data_report = {
                'metrics': {
                    'total_orders': total_orders,
                    'total_items_sold': total_items_sold,
                    'total_biling': total_biling,
                    'avg_ticket': avg_ticket,
                },
                'graphics_path': {
                    'best_profitable': best_profitable_fig_path,
                    'total_sales': total_sales_fig_path,
                    'best_selling_product': best_selling_fig_path,
                    'sales_distribuition': sales_distribuition_fig_path
                },
                'filters_chart_distribuition_by_product': {
                    'data_range_dbp': data_range_dbp,
                    'selected_products': selected_products,
                    'min_quantity': min_quantity,
                    'min_price': min_price,
                    'max_price': max_price
                },
                'filters_chart_total_sales': {
                    'data_range_ts': data_range_ts
                }

            }

            
            
            dp.generate_pdf(data_report, report_name)

            st.success('Relatório gerado com sucesso, esta na pasata Documentos/relatorios/')
            
            
        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar o relatório: {e}")

        finally:
            # Exclui as imagens temporárias
            for file in temp_files:
                if file:
                    os.remove(file)

        

except ValueError as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

    