#Biblioteca abaixo:

chave_api_sendgrid = "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"

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

conta_sendgrid = SendGridAPIClient(chave_api_sendgrid)

email = Mail(from_email="rodrigoaraujo2700@gmail.com", 
             to_emails=["rodrigoaraujo2700@gmail.com", "rafaelluckner3@gmail.com"], 
             subject="Email enviado no sendgrid via python", 
             html_content="<p>Bom dia!</p><p>Segue novo gráfico formuládo</p>")

resposta = conta_sendgrid.send(email)
print(resposta.status_code)
