# Gerador de Relatórios

Sistema em python para a geração de relatórios automáticos com base em em dados de vendas.
Permite carregar arquivos CSV, processar dados, gerar gráficos e resumos automaticamente.

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

Consulte **[Implantação](#-implanta%C3%A7%C3%A3o)** para saber como implantar o projeto.

### 📋 Pré-requisitos

Para executar o projeto, você precisará ter o Python e o motor wkhtmlropdf instalados em sua máquina.


### 🔧 Instalação

Primeiro de tudo, precisamos instalar o Python e o wkhtmltopdf em sua máquina.

#### Instalação no Windows:

baixe o python no site oficial: https://www.python.org/downloads/
e intale normalmente

E baixe tambem o wkhtml no site ofcial: https://wkhtmltopdf.org/downloads.html e instale normalmente

#### Instalação no Linux:

Por padrão, o Python já vem instalado em muitos sistemas Linux. Se você não tiver o Python instalado, você pode instalá-lo usando o gerenciador de pacotes do seu sistema.


```
sudo apt-get install python3
```

Agora precisamos instalar o wkhtmltopdf no Linux:

```
sudo apt-get install wkhtmltopdf
```

Após a instalação dos pré-requisitos vamos prosseguir para a instalação do projeto.

#### Passo-1
Crie um novo diretório para o projeto e clone o repositório:

```
git clone https://github.com/your-username/gerador-de-relatorios.git
```

obs: caso não tenha o git instalado, instale-o primeiro.

##### Windows

Site oficial: https://git-scm.com/download/win

##### Linux

```
sudo apt-get install git
```

Ou baixe o arquivo [.zip](https://github.com/AlyssonMartinsDev/Gerador_de_Relatorios/archive/refs/heads/main.zip) do programa e extraia na pasta desejada.

Após baixar o arquivo, vá até a pasta com o cmd e execute o comando para iniciar a venv:
```
python -m venv venv
```

E ative a venv:
##### Windows
```
venv\Scripts\activate
```
##### Linux
```
source venv/bin/activate
```

Após ativar a venv , instale as dependências do projeto:

```
pip install -r requirements.txt
```

Depois de tudo instalado , você pode executar o projeto com o comando:

```
streamlit run app.py
```

E logo abriará uma janela no seu navegador!!!

## ⚙️ Executando os testes

Dentro da pasta pricipal do projeto há um arquivo chamado `MOCK_DATA.csv` para usar como dados de teste para a aplicação.

É so carregar ele e verá o programa funcionar.

Depois pode testar com seu proprio arquivo csv.

##### obs: Lembrando seu arquivo csv precisa obrigatóriamente ter as seguintes colunas : `data`, `produto`, `quantidade`, `preco_unitario`, `total venda`, com algumas variações de nome o programa consegue lidar com isso.


## 🛠️ Construído com

Ferramentas e bibliotecas utilizadas neste projeto:

- [**Python**](https://www.python.org/) — Linguagem principal usada no backend e para análise de dados  
- [**Streamlit**](https://streamlit.io/) — Framework para construção de aplicações web interativas com Python  
- [**Pandas**](https://pandas.pydata.org/) — Biblioteca para manipulação e análise de dados  
- [**Matplotlib**](https://matplotlib.org/) / [**Seaborn**](https://seaborn.pydata.org/) — Criação de gráficos e visualizações  
- [**pdfkit**](https://pypi.org/project/pdfkit/) — Biblioteca Python para converter HTML em PDF  
- [**wkhtmltopdf**](https://wkhtmltopdf.org/) — Motor de conversão utilizado pelo pdfkit para gerar arquivos PDF  

## ✒️ Autores

* **Alysson Gabriel** – *Desenvolvimento e idealização do projeto* – [AlyssonMartinsDev](https://github.com/AlyssonMartinsDev)

## 📄 Licença

Este projeto está sob a licença MIT 

