import mysql.connector

"""
host = "localhost"
usuario = "root"
senha = "admin"
DB = "market_mail"
"""

def conectarDB (host, usuario, senha, DB): 
    connection=mysql.connector.connect( 
        host = host, 
        user = usuario, 
        password = senha, 
        database = DB
    )
    return connection


def insert_user(nome, email, senha, acoes_escolhidas, conn):
    connection = conn
    cursor = connection.cursor()
    sql = '''INSERT INTO usuarios (nome, email, telefone, cnpj)
    VALUES (%s, %s, %s, %s)'''
    data = (
        nome,
        email,
        senha,
        acoes_escolhidas
        )
    cursor.execute(sql, data)
    connection.commit()
    iduser = cursor.lastrowid
    cursor.close()
    connection.close()
    print("Usuário cadastrado com ID", iduser)


def update_user(nome, email, senha, acoes_escolhidas, id, conn): 
    connection = conn 
    cursor = connection.cursor() 
    sql = '''UPDATE usuarios
    SET nome=%s,
    email=%s,
    senha=%s,
    acoes_escolhidas=%s
    WHERE id=%s'''
    data = ( 
        nome,
        email,
        senha,
        acoes_escolhidas,
        id
    )
    cursor.execute(sql,data)
    connection.commit()
    iduser = cursor.lastrowid
    cursor.close()
    connection.close()
    print("Usuário de id", iduser, "atualizado.") 


def delete_user(id, conn): 
    connection = conn
    cursor = connection.cursor()
    sql = '''DELETE FROM usuarios
    WHERE ID = %s'''
    data = (id,)
    cursor.execute(sql,data)
    connection.commit()
    iduser = cursor.lastrowid
    cursor.close()
    connection.close()
    print("Usuário de id", iduser, "removido.")