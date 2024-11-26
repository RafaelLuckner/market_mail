import pytest
import pandas as pd
from data.coleta_dados import baixar_dados
from frontend.confirmacao_email import generate_confirmation_token, confirm_token, app

"""
teste coleta_dados.py:
verificar se a função baixar_dados retorna um DataFrame com
as colunas esperadas para um ticker válido e um período razoável
"""

def test_baixar_dados_basico():
    data = baixar_dados("AAPL", "2023-11-01", "2023-11-30")
    assert isinstance(data, pd.DataFrame)
    assert "Close" in data.columns

"""
testes confirmacao_email.py:
Verificar se a geração e validação do token funcionam
corretamente e se o endereço retorna status code 200
"""

def test_gerar_e_validar_token():
    email = "teste@email.com"
    token = generate_confirmation_token(email, "secret_key")
    recovered_email = confirm_token(token, "secret_key")
    assert recovered_email == email

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    rv = client.get('/register')
    assert rv.status_code == 200