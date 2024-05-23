import sqlite3
import datetime


db_con  = sqlite3.connect('db_sysfoco.db')
db_cur = db_con.cursor()


def criar_registro_do_cliente(codigo_cliente, nome, rg, cpf, endereco, telefone, connection):
    
    db_cur.execute('INSERT INTO cliente VALUES (?, ?, ?, ?, ?, ?)',
                (codigo_cliente, nome, rg, cpf, endereco, telefone))
    
    db_con.commit()

def gerar_numero_de_processo(connection):
    
    query = db_cur.execute('SELECT numero_processo FROM processo')
    result = query.fetchall()    
    numero_processo = len(result) + 1
    return numero_processo

def criar_processo_vinculado_ao_cliente(codigo_cliente, tipo_processo, connection):
    
    numero_processo = gerar_numero_de_processo()
        
    db_cur.execute('INSERT INTO processo VALUES(?,?,?)',
                   (numero_processo, codigo_cliente, tipo_processo))

    db_con.commit()

    return numero_processo

def definir_fase_para_processo(id_processo, codigo_fase, connection):
    
    data_inicio = datetime.datetime.now()
    data_finalizacao = data_inicio + datetime.timedelta(days=15)
    
    db_cur.execute('INSERT INTO fase_do_processo VALUES (?,?,?,?,?,?)',
                   (id_processo, codigo_fase, data_inicio, data_finalizacao, 'AGUARDANDO', ''))
    
    db_con.commit()

def cadastrar_cliente(dados_cliente, connection):
        
    # dados_cliente deve ser um dicionário
    
    criar_registro_do_cliente(dados_cliente['codigo_cliente'], 
                              dados_cliente['nome'], 
                              dados_cliente['rg'],
                              dados_cliente['cpf'], 
                              dados_cliente['endereco'], 
                              dados_cliente['fone'],
                              connection)
    
    id_processo = criar_processo_vinculado_ao_cliente(dados_cliente['codigo_cliente'], 
                                                      dados_cliente['tipo_processo'],
                                                      connection)
    
    definir_fase_para_processo(id_processo, 'DOC_INICIAL', connection)


def recuperar_id_de_processo_do_cliente(codigo_cliente):
    
    query = db_cur.execute('SELECT numero_processo from processo WHERE codigo_cliente = ?', (codigo_cliente,))
    result = query.fetchone()
    
    return result[0]


def recuperar_fase_atual_do_processo(id_processo):
    
    query = db_cur('SELECT codigo_fase FROM fase_do_processo WHERE numero_processo = ? AND codigo_status = ?', 
                   (id_processo, 'AGUARDANDO'))
    result = query.fetchone()
    
    return result[0]

def get_proxima_fase(codigo_fase):
    
    proxima_fase = None
    
    if codigo_fase == 'DOC_INICIAL':
        proxima_fase = 'ANALISE'
    elif codigo_fase == 'ANALISE':
        proxima_fase = 'PROC_INTERN'
    elif codigo_fase == 'PERICIA':
        proxima_fase = 'SEGURADORA'
    elif codigo_fase == 'SEGURADORA':
        proxima_fase = 'RECEBIMENTO'
        
    return proxima_fase
    
    
def passar_cliente_para_proxima_fase(codigo_cliente):

    id_processo = recuperar_id_de_processo_do_cliente(codigo_cliente)
    
    data_inicio = datetime.datetime.now()
    data_finalizacao = data_inicio + datetime.timedelta(days=15)
    
    fase_atual = recuperar_fase_atual_do_processo(id_processo)
    
    #altera registro da fase atual do processo
    db_cur.execute('UPDATE fase_do_processo SET codigo_status = ? WHERE numero_processo = ?', 
                   ('APROVADO', id_processo))
    
    #cria registro da nova fase do processo
    nova_fase = get_proxima_fase(fase_atual)
    definir_fase_para_processo(id_processo, fase_atual)
    

def obter_lista_clientes():
    
    query = db_cur.execute('SELECT codigo_cliente, nome, rg, cpf, endereco, fone FROM cliente')
    results = query.fetchall()
    return results


def obter_lista_de_clientes_e_processos_associados():
    
    query = db_cur.execute('SELECT c.codigo_cliente, c.nome, c.rg, c.cpf, c.endereco, c.fone, p.numero_processo, p.tipo_processo \
        FROM cliente c JOIN processo p ON c.codigo_cliente = p.codigo_cliente')
    
    results = query.fetchall()
    
    return results


def obter_processos_para_cliente_especifico(codigo_cliente):
        
    query = db_cur.execute('SELECT c.codigo_cliente, c.nome, c.cpf, p.numero_processo, p.tipo_processo, \
        f.codigo_fase, f.codigo_status FROM cliente c JOIN processo p ON c.codigo_cliente = p.codigo_cliente \
        JOIN fase_do_processo f ON p.numero_processo = f.numero_processo')
    
    results = query.fetchall()
    
    return results


def obter_processos_em_uma_dada_fase(codigo_fase):
    
    query = db_cur.execute('SELECT c.codigo_cliente, c.nome, c.cpf, p.numero_processo, p.tipo_processo, \
        f.codigo_fase, f.codigo_status FROM cliente c JOIN processo p ON c.codigo_cliente = p.codigo_cliente \
        JOIN fase_do_processo f ON p.numero_processo = f.numero_processo WHERE f.codigo_fase = ? AND f.codigo_status = "AGUARDANDO"', (codigo_fase,))
    
    results = query.fetchall()
    
    return results
    

def obter_informacoes_de_processo_especifico(numero_processo):
    
    query = db_cur.execute('SELECT c.codigo_cliente, c.nome, c.cpf, p.numero_processo, p.tipo_processo, \
        f.codigo_fase, f.codigo_status, f.observacao FROM cliente c JOIN processo p ON c.codigo_cliente = p.codigo_cliente \
        JOIN fase_do_processo f ON p.numero_processo = f.numero_processo WHERE p.numero_processo = ?', (numero_processo,))
    
    results = query.fetchall()
    
    return results


def adicionar_observacao_a_um_processo(numero_processo):
    pass

def cancelar_prosseguimento_do_processo(numero_processo):
    pass

db_con.commit()

db_con.close()