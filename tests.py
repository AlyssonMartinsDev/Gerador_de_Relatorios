import plotly.express as px
import plotly.io as pio



fig = px.bar(x=["A", "B", "C"], y=[10, 20, 30], title="Teste de gráfico")

# Testar salvar imagem
pio.write_image(fig, "grafico_teste.png")
print("Imagem salva com sucesso!")