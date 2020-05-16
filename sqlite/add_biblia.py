import re
import json
import sqlite3
from textwrap import dedent
from typing import List

nome_arquivo = input('Nome do arquivo: ')
sigla_versao = input("Sigla da versão: ").upper()

versos: List[dict] = []

with open(nome_arquivo, encoding='utf-8') as f:
    linhas = f.read().split('\n')
    for linha in linhas:
        liv, cap, ver, texto = re.findall(
            r'{{(\w+):(\d+):(\d+)}}(.+)', linha)[0]
        versos.append({
            'liv': liv,
            'cap': cap,
            'ver': ver,
            'texto': texto
        })

siglas = [
    'gn', 'ex', 'lv', 'nm', 'dt', 'js', 'jz', 'rt', '1sm', '2sm', '1rs', '2rs', '1cr', '2cr', 'ed',
    'ne', 'et', 'jó', 'sl', 'pv', 'ec', 'ct', 'is', 'jr', 'lm', 'ez', 'dn', 'os', 'jl', 'am',
    'ob', 'jn', 'mq', 'na', 'hc', 'sf', 'ag', 'zc', 'ml', 'mt', 'mc', 'lc', 'jo', 'at',
    'rm', '1co', '2co', 'gl', 'ef', 'fp', 'cl', '1ts', '2ts', '1tm', '2tm', 'tt', 'fm', '1pe',
    '2pe', '1jo', '2jo', '3jo', 'hb', 'tg', 'jd', 'ap'
]


connection = sqlite3.connect('biblia.db')
cursor = connection.cursor()
cursor.execute("INSERT INTO versoes(sigla) VALUES('%s')" % sigla_versao)
cursor.execute("SELECT id FROM versoes ORDER BY id DESC LIMIT 1")
id_versao, = cursor.fetchone()

sql = dedent(f"""
    INSERT INTO versos (
        id_versao, id_livro, capitulo, versiculo, texto
    ) VALUES ({id_versao}, %s, %s, %s, '%s')
""")

try:
    for verso in versos:
        vars = (
            siglas.index(verso['liv'].lower())+1,
            verso['cap'],
            verso['ver'],
            verso['texto'],
        )
        cursor.execute(sql % vars)

    connection.commit()
finally:
    connection.close()
