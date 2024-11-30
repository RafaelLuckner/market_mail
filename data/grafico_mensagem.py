import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from colorama import Fore, Style
import mplcyberpunk as mp
import matplotlib 
matplotlib.use('Agg')

def grafico(df1, lista_acoes, mean=False):
    plt.style.use("cyberpunk")
    # plt.style.use("Solarize_Light2")
    # plt.style.use("default")

    tam_geral = 12
    all_variacoes = []
    lista_legend = []

    fig, fig_acoes1 = plt.subplots(figsize = (tam_geral,tam_geral/2))

    for acao in lista_acoes:
        df_aux = df1.loc[df1['acao']==acao,:].copy()
        if df_aux.empty:
            print(f'Ação não encontrada: {acao}')
        else:
            lista_legend.append(acao)
        df_aux['variacao'] = df_aux['Close'].pct_change() 
        df_aux['variacao'] = (1 + df_aux['variacao']).cumprod() - 1
        df_aux['variacao'] = df_aux['variacao'].apply(lambda x: round(x * 100, 5))

        df_aux['variacao'] = df_aux['variacao'].fillna(0)
        fig_acoes1.plot(df_aux['Datetime'], df_aux['variacao'],label=acao)
        all_variacoes.append(df_aux[['Datetime','variacao']])

    if mean:
        # Média
        df_aux = pd.concat(all_variacoes,ignore_index=True)
        variacao_geral = df_aux.loc[:,['Datetime', 'variacao']].groupby('Datetime').mean()
        fig_acoes1.plot(variacao_geral.index, variacao_geral , color='white', linestyle='--', linewidth= 1.5)
        lista_legend = lista_legend + ['Média']

    # plt.title( )
    fig_acoes1.set_xlabel('Horário',fontsize=tam_geral )
    fig_acoes1.set_ylabel('Percentual de Variação',fontsize=tam_geral)

    y_min, y_max = fig_acoes1.get_ylim()
    margem = 0.1 * (y_max - y_min)
    fig_acoes1.set_ylim(y_min - margem, y_max + margem)

    fig_acoes = fig_acoes1.twinx()
    fig_acoes.set_ylim(fig_acoes1.get_ylim())

    fig_acoes.grid(color='white', linestyle='-', linewidth=0.2, alpha=0.5)
    fig_acoes1.grid(color='white', linestyle='-', linewidth=0.2, alpha=0.5)

    leg = fig_acoes1.legend(lista_legend, title = 'Ações', fontsize=tam_geral, title_fontsize=tam_geral, loc='lower left',             
                    bbox_to_anchor=(1.05, 0.4), borderaxespad=0.1, frameon=True)

    # Estilo da caixa
    leg.get_frame().set_color('black')  # Cor da caixa
    leg.get_frame().set_alpha(0.15)

    plt.tight_layout()
    return  fig

def mensagem(df1, lista_acoes):
    frase = ''   
    variacoes_acoes = []
    for acao in lista_acoes:
        df_test = df1.loc[df1['acao'] == acao, :].copy()
        df_test['variacao'] = df_test['Close'].pct_change()
        df_test['variacao'] = (1 + df_test['variacao']).cumprod() - 1
        df_test['variacao'] = df_test['variacao'].apply(lambda x: round(x * 100, 5))

        if df_test.empty:
            print(f"Ação {acao} não encontrada ou sem dados.")
            continue

        variacao = df_test.iloc[-1, 3]
        variacoes_acoes.append((acao, variacao, df_test))
    
    # Ordenar as ações por variação (maior para menor)
    variacoes_acoes.sort(key=lambda x: x[1], reverse=True)

    for acao, variacao, df_test in variacoes_acoes:
        
        variacao = df_test.iloc[-1,3]
        if variacao > 0:
            simbolo = f"{Fore.GREEN}\u25B2{Style.RESET_ALL}"  
        elif variacao < 0:
            simbolo = f"{Fore.RED}\u25BC{Style.RESET_ALL}"  
        else:
            simbolo = "="  
        
        if len(acao) < 6:
            result = f"{acao}:  {df_test.iloc[-1,1]:.2f} " 
        else:
            result = f"{acao}: {df_test.iloc[-1,1]:.2f} "

        if len(f"{df_test.iloc[-1,1]:.2f}") <5:
            if df_test.iloc[-1,3] > 0:
                val = f" | +{df_test.iloc[-1,3]:.2f}% {simbolo}\n"
            elif df_test.iloc[-1,3] == 0:
                val = f" |  {df_test.iloc[-1,3]:.2f}% {simbolo}\n"
            else: 
                val = f" | {df_test.iloc[-1,3]:.2f}% {simbolo}\n"

        else:
            if df_test.iloc[-1,3] > 0:
                val = f"| +{df_test.iloc[-1,3]:.2f}% {simbolo}\n"
            elif df_test.iloc[-1,3] == 0:
                val = f"|  {df_test.iloc[-1,3]:.2f}% {simbolo}\n"
            else: 
                val = f"| {df_test.iloc[-1,3]:.2f}% {simbolo}\n"

        frase = frase + result + val

    frase = "Variação das ações selecionadas:\n" + frase + f"\nAtualizado: {df1['Datetime'].iloc[-1]}"
    return frase


df = pd.read_csv('df_day.csv', parse_dates=['Datetime'])

lista_acoes = ['VALE3','BBSE3', 'CSAN3', 'RAIZ4', 'BRBI11', 'BBAS3', 'SAPR4', 'SAPR11', 'TRPL4', 'RANI3', 'TAEE11']
# lista_acoes = ['VALE3', 'SAPR4', 'BBAS3', 'TRPL4']

mens = mensagem(df, lista_acoes)
print(mens)

fig = grafico(df, lista_acoes[0:6], mean=False)
fig.savefig('comparacao_de_acoes.png', dpi=300)


