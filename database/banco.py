import sqlite3

# Nome do banco de dados
DB_NAME = "puppet_master.db"

def conectar():
    """Estabelece conexão com o banco SQLite"""
    return sqlite3.connect(DB_NAME)

