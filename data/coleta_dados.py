import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta


def baixar_dados(ticker, start_date, end_date):
    data = yf.download(
        tickers=ticker,
        start=start_date,
        end = end_date,
        interval="5m"
        # start: Data de início no formato YYYY-MM-DD.
        # interval: Frequência dos dados (opções: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
    )
    try:
        dados = yf.download(ticker, start=start_date, end=end_date, interval="1d")
        data.iloc[-1,3] = dados.iloc[-1, 3]
        return data
    except:
        return data
    
    

def buscar_dados_diarios():
    dfs = []  
    now = datetime.now()
    if now.weekday() == 5:  # Sábado
        now = now - timedelta(days=1)  # Retrocede para sexta
    elif now.weekday() == 6:  # Domingo
        now = now - timedelta(days=2)  # Retrocede para sexta

    end_day = now.day
    end_date = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    if now.weekday() == 0: now = now - timedelta(days=2) # Retrocede para sexta
    date_previous = now - timedelta(days=1)
    start_day = date_previous.day    
    start_date = date_previous.strftime("%Y-%m-%d")

    brasil_tickers =  ['ABEV3.SA', 'ALPA4.SA',  'ASAI3.SA', 'AZUL4.SA', 'B3SA3.SA', 'BBAS3.SA', 'BBDC3.SA', 'BBDC4.SA', 'BBSE3.SA', 'BEEF3.SA', 'BPAC11.SA','BRAP4.SA',
                       'BRFS3.SA', 'BRKM5.SA',  'CASH3.SA', 'CCRO3.SA', 'CMIG4.SA', 'CPFE3.SA', 'CRFB3.SA', 'CSAN3.SA', 'CVCB3.SA', 'CYRE3.SA', 'DXCO3.SA', 'ECOR3.SA',
                       'EGIE3.SA', 'ELET3.SA',  'ELET6.SA', 'EMBR3.SA', 'ENEV3.SA', 'ENGI11.SA','EQTL3.SA', 'EZTC3.SA', 'GGBR4.SA', 'GOAU4.SA', 'GOLL4.SA', 'HAPV3.SA',
                       'IGTI11.SA','IRBR3.SA',  'ITSA4.SA', 'ITUB4.SA', 'JBSS3.SA', 'JHSF3.SA', 'KLBN11.SA','LREN3.SA', 'MGLU3.SA', 'MRFG3.SA', 'MRVE3.SA', 'MULT3.SA',
                       'NTCO3.SA', 'HYPE3.SA',  'PETR3.SA', 'PETR4.SA', 'POSI3.SA', 'PRIO3.SA', 'QUAL3.SA', 'RADL3.SA' ,'RAIL3.SA', 'RENT3.SA', 'SANB11.SA','SBSP3.SA',
                       'SAPR4.SA', 'SAPR11.SA', 'SUZB3.SA', 'TAEE11.SA','TRPL4.SA', 'TOTS3.SA', 'UGPA3.SA', 'USIM5.SA','VALE3.SA', 'BRBI11.SA', 'RAIZ4.SA', 'RANI3.SA',
                       'KLBN3.SA', 'KLBN4.SA', 'KLBN11.SA']

    count = 0
    for acao in brasil_tickers:
        dados_diarios = baixar_dados(acao, start_date, end_date)
        dados_diarios['variacao'] = dados_diarios['Close'].pct_change()     
        dados_diarios['variacao'] = dados_diarios['variacao'].apply(lambda x: round(x * 100, 4))
        dados_diarios['variacao'] = (1 + dados_diarios['variacao']).cumprod() - 1
        dados_diarios = dados_diarios.loc[:, ['Close', 'Volume', 'variacao']]
        dados_diarios['acao'] = acao.replace('.SA', '')  # Adiciona a coluna com o nome da ação
        dados_diarios = dados_diarios.reset_index()
        count = count +1
        try:
            print(f"Coletados Dados Diarios da Ação {dados_diarios['acao'][0]}")
        except:
            return 
        print(f'Total de ações: {count}')
        
        dfs.append(dados_diarios)

    
    # união dos dfs
    resultado = pd.concat(dfs, ignore_index=True)
    resultado['Datetime'] = pd.to_datetime(resultado['Datetime'])
    resultado['day'] = resultado['Datetime'].dt.day

    # dados do dia anterior
    dados_start_day = resultado.loc[resultado['day'] == start_day, :]
    dados_start_day.to_csv('df_day_before.csv', index=False)

    # dados ultimo dia
    dados_end_day = resultado.loc[resultado['day'] == end_day, :]
    dados_end_day.to_csv('df_day.csv', index=False)
    

buscar_dados_diarios()

