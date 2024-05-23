from model2 import ExecutorDeQueries
from model3 import Processo

executor = ExecutorDeQueries()

#métodos de leitura

def lista_de_clientes_em_json(clientes):
    
    colunas = ('codigo_cliente', 'nome', 'rg', 'cpf', 'endereco', 'fone')
    
    #transformar lista de tuplas em lista de dicionários
    clientes_json = []
    
    for c in clientes:
        c_dict = {}
        for i in range(0, 6):
            c_dict[colunas[i]] = c[i]
        clientes_json.append(c_dict)

    return clientes_json


def get_lista_clientes():
    clientes = executor.obter_lista_clientes()
    clientes_json = lista_de_clientes_em_json(clientes)
    return clientes_json


def processos_de_um_cliente_em_json(processos):
    
    processos_dict = {}
    cli_dict = {}
    #as informações do cliente estão nos tres primeiros campos da tupla de processo
    #pode-se usar a primeria tupla de processo para pegar as informações
    codigo_cli, nome, cpf = processos[0][0:3]
    cli_dict['codigo_cliente'] = codigo_cli
    cli_dict['nome'] = nome
    cli_dict['cpf'] = cpf    
    processos_dict['cliente'] = cli_dict
    processos_dict['processos'] = []    
    for processo in processos:
        proc_dict = {}
        numero_processo, tipo_processo, fase, status = processo[3:]
        proc_dict['numero_processo'] = numero_processo
        proc_dict['tipo_processo'] = tipo_processo
        proc_dict['fase'] = fase
        proc_dict['status'] = status
        processos_dict['processos'].append(proc_dict)
    return processos_dict
        
        
def get_processos_de_um_cliente(codigo_cliente):
    
    processos_do_cliente = executor.obter_processos_para_cliente_especifico(codigo_cliente)
    
    processos_json = processos_de_um_cliente_em_json(processos_do_cliente)
    
    return processos_json
    

def processo_especifico_em_json(processo_info):
    #tres primeiros registros da tupla sao informações de cliente
    #o quarto e quinto registro da tupla é o numero do processo e o tipo do processo
    #o sexto, setimo e oitavo são codigo_fase, codigo_status e observacao
    codigo_cliente, nome, cpf = processo_info[0][0:3]
    numero_processo, tipo_processo = processo_info[0][3:5]
    
    fases = []
    for p in processo_info:
        codigo_fase, codigo_status, observacao = p[5:]
        fase_dict = {
            'codigo_fase' : codigo_fase,
            'codigo_status' : codigo_status,
            'observacao' : observacao
        }
        fases.append(fase_dict)
    
    processo_json = {
        'cliente': {
                 'codigo_cliente' : codigo_cliente,
                'nome': nome,
                'cpf' : cpf            
        },
        'processo' : {
             'numero_processo' : numero_processo,
            'tipo_processo' : tipo_processo            
        },
        'fases' : fases   
    }

    return processo_json


def get_processo_especifico(numero_processo):
    #método incompleto
    processo_info = executor.obter_informacoes_de_processo_especifico(numero_processo)
    processo_info_json = processo_especifico_em_json(processo_info)
    return processo_info_json
    

def processos_em_fase_especifica_em_json(processos):

    processos_json = []

    for proc in processos:

        codigo_cliente, nome, cpf = proc[0:3]

        cliente_dict = {
            'codigo_cliente' : codigo_cliente,
            'nome' : nome,
            'cpf' : cpf
        }

        numero, tipo, fase, codigo_status, observacao = proc[3:]

        processo_dict = {
            'numero' : numero,
            'tipo' : tipo,
            'fase' : fase,
            'codigo_status' : codigo_status,
            'observacao' : observacao
        }
        
        proc_dict = {'cliente' : cliente_dict, 'processo' : processo_dict}
        
        processos_json.append(proc_dict)

    return processos_json


def get_processos_em_fase_especifica(codigo_fase):
    processos = executor.obter_processos_em_uma_dada_fase(codigo_fase)
    processos_json = processos_em_fase_especifica_em_json(processos)
    return processos_json


#métodos de ação sobre os dados

def proxima_fase(id_processo):
    
    executor.passar_processo_para_proxima_fase(id_processo)

def indeferir(id_processo):
    
    executor.cancelar_prosseguimento_do_processo(id_processo)
    
def adicionar_observacao_ao_processo(id_processo, observacao):
    
    executor.adicionar_observacao_a_fase_atual_do_processo(id_processo, observacao)
    
def novo_cliente(dados_cliente):
    
    executor.cadastrar_cliente(dados_cliente)

def obter_objeto_processo_cliente(cliente):
    
    cli_proc_obj = Processo(cliente, executor)

    return cli_proc_obj

def filtrar_codigos_de_cliente(processos):
    #esse método opera sobre a estrutura de dados retornada pelo método get_processos_em_fase_especifica
    
    """
    [{'cliente': {'codigo_cliente': 2, 'nome': 'Maria Souza', 'cpf': '23423423423'}, 
    'processo': {'numero': 2, 'tipo': 'DPVAT', 'fase': 'DOC_INICIAL', 'codigo_status': 'AGUARDANDO', 'observacao': '2024-05-15 19:10:07.047822\ncliente precisa enviar foto do rg\n'}}, 
    {'cliente': {'codigo_cliente': 3, 'nome': 'Lucia Santos', 'cpf': '34534534534'}, 
    'processo': {'numero': 3, 'tipo': 'DPVAT', 'fase': 'DOC_INICIAL', 'codigo_status': 'AGUARDANDO', 'observacao': ''}}, 
    {'cliente': {'codigo_cliente': 5, 'nome': 'Maria Josefina', 'cpf': '88888888888'}, 
    'processo': {'numero': 6, 'tipo': 'DPVAT', 'fase': 'DOC_INICIAL', 'codigo_status': 'AGUARDANDO', 'observacao': ''}}, 
    {'cliente': {'codigo_cliente': 6, 'nome': 'Larissa Dias', 'cpf': '43022574827'}, 
    'processo': {'numero': 7, 'tipo': 'DPVAT; Seguro de Vida', 'fase': 'DOC_INICIAL', 'codigo_status': 'AGUARDANDO', 'observacao': ''}}]

    """
    
    return [proc['cliente']['codigo_cliente'] for proc in processos]

def criar_lista_de_objetos_processo_cliente(codigos):
    
    #esse método cria uma lista de objetos processo-cliente a partir de uma lista de códigos
    
    return [Processo(codigo, executor) for codigo in codigos]
    