from itsdangerous import URLSafeTimedSerializer
from flask import Flask, request, url_for, redirect, render_template_string
from flask_mail import Mail, Message

emails_confirmados = [] # <- substituir por banco de dados

def generate_confirmation_token(email, secret_key):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt='email-confirm-salt')


def confirm_token(token, secret_key, expiration=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(
            token,
            salt='email-confirm-salt',
            max_age=expiration
        )
    except:
        return False
    return email


app = Flask(__name__)

# Configurações do servidor de e-mail (exemplo com Gmail)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '00116679@aluno.uniso.br'
app.config['MAIL_PASSWORD'] = '52830611837'

mail = Mail(app)

def send_confirmation_email(user_email, secret_key):
    token = generate_confirmation_token(user_email, secret_key)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = f'<p>Por favor, clique no link para confirmar seu e-mail:</p><a href="{confirm_url}">{confirm_url}</a>'
    
    msg = Message('Confirme seu email', sender='00116679@aluno.uniso.br', recipients=[user_email])
    msg.html = html
    mail.send(msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form['email']
        token = generate_confirmation_token(user_email, app.config['SECRET_KEY'])
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = f'<p>Por favor, clique no link para confirmar seu e-mail:</p><a href="{confirm_url}">{confirm_url}</a>'
        
        # Envia o e-mail
        msg = Message('Confirme seu email', sender='00116679@aluno.uniso.br', recipients=[user_email])
        msg.html = html
        mail.send(msg)
        
        return '<h1>Um e-mail de confirmação foi enviado para você. Verifique sua caixa de entrada.</h1>'
    
    return render_template_string('''
        <form method="post">
            <label>Insira seu e-mail:</label>
            <input type="email" name="email" required>
            <button type="submit">Enviar</button>
        </form>
    ''')


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token, app.config['SECRET_KEY'])
    except:
        return '<h1>O link de confirmação é inválido ou expirou.</h1>'
    
    emails_confirmados.append(email) # problema: emails_confirmados é sempre vazio

    # marcar o e-mail como confirmado no banco de dados
    return f'<h1>Email {email} confirmado com sucesso!</h1>'