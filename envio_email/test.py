import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave API do SendGrid da variável de ambiente
chave_api_sendgrid = os.getenv('SENDGRID_API_KEY')

# Verificar se a chave foi carregada corretamente
if not chave_api_sendgrid:
    raise ValueError("A chave API do SendGrid não foi encontrada. Verifique o arquivo .env.")

# Criar o cliente SendGrid
sg = SendGridAPIClient(chave_api_sendgrid)

# Definir os dados do e-mail
mensagem = Mail(
    from_email="rodrigoaraujo2700@gmail.com",
    to_emails=["rodrigoaraujo2700@gmail.com", "rafaelluckner3@gmail.com"],
    subject="Email enviado no SendGrid via Python",
    html_content="""<p>Bom dia!</p><p>Segue novo gráfico formulado.</p>"""
)

# Enviar o e-mail e tratar possíveis erros
try:
    resposta = sg.send(mensagem)
    print(f"E-mail enviado com sucesso! Status Code: {resposta.status_code}")
except Exception as e:
    print(f"Erro ao enviar o e-mail: {e}")