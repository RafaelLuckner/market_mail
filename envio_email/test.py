import os
import io
import base64
import pandas as pd
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId

from grafico_mensagem import mensagem as ms
from grafico_mensagem import grafico


# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave API do SendGrid da variável de ambiente
chave_api_sendgrid = os.getenv('SENDGRID_API_KEY')

# Verificar se a chave foi carregada corretamente
if not chave_api_sendgrid:
    raise ValueError("A chave API do SendGrid não foi encontrada. Verifique o arquivo .env.")

# Criar o cliente SendGrid
sg = SendGridAPIClient(chave_api_sendgrid)

# Carregar dados e gerar gráfico
df = pd.read_csv('../data/df_day.csv', parse_dates=['Datetime'])

lista_acoes1 = ['VALE3', 'BBSE3', 'CSAN3', 'RAIZ4', 'BRBI11', 'BBAS3', 'SAPR4', 'SAPR11', 'TRPL4', 'RANI3', 'TAEE11']
lista_acoes2 = ['RAIZ4', 'BBAS3', 'CSAN3', 'RANI3', 'TAEE11']
lista_lista_acoes = [lista_acoes1, lista_acoes2]
lista_emails = ["rafaelluckner3@gmail.com","rafaelluckner0@gmail.com"]

for lista_acoes, emails in zip(lista_lista_acoes, lista_emails):

    mens = ms(df, lista_acoes)
    print(mens)
    # Converter a string para HTML com as cores# Converter a string para HTML com as cores

    html_conteudo = mens.replace("\x1b[32m", "<span style='color:green;'>") \
                                .replace("\x1b[31m", "<span style='color:red;'>") \
                                .replace("\x1b[0m", "</span>")

    # Adicionar quebras de linha (tag <br>) após cada linha de ação
    html_conteudo = html_conteudo.replace("\n", "<br>")

    img_buffer = io.BytesIO()
    fig = grafico(df, lista_acoes[0:6], mean=False)
    fig.savefig(img_buffer, format='png', dpi=300)

    # Resetar a posição do ponteiro para o início do buffer
    img_buffer.seek(0)

    # Ler a imagem gerada e codificá-la em base64
    encoded_image = base64.b64encode(img_buffer.read()).decode()


    # Criar a mensagem com a imagem incorporada (CID)
    mensagem = Mail(
        from_email="rodrigoaraujo2700@gmail.com",
        to_emails=["rodrigoaraujo2700@gmail.com", emails],
        subject="O resultado das suas ações chegaram!",
        html_content=f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email com Gráfico</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
                color: #333;
            }}
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                background: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .email-header {{
                font-size: 20px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 20px;
            }}
            .email-body p {{
                margin: 0 0 10px;
            }}
            .email-footer {{
                margin-top: 20px;
                font-size: 12px;
                text-align: center;
                color: #555;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                Atualização das Ações
            </div>
            <div class="email-body">
                <p>Bom dia!</p>
                {html_conteudo}
            </div>
            <div class="email-footer">
                Este e-mail foi enviado automaticamente. Por favor, não responda.
            </div>
        </div>
    </body>
    </html>
    """
    )

    # Anexar a imagem ao e-mail como CID
    attachment = Attachment(
        FileContent(encoded_image),
        FileName("comparacao_de_acoes.png"),
        FileType("image/png"),
        Disposition("inline"),
        ContentId("graph_image")
    )
    mensagem.add_attachment(attachment)

    # Enviar o e-mail e tratar possíveis erros
    try:
        resposta = sg.send(mensagem)
        print(f"E-mail enviado com sucesso! Status Code: {resposta.status_code}")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")
