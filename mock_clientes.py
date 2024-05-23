#from model import cadastrar_cliente
from model2 import ExecutorDeQueries

executor = ExecutorDeQueries()

def definir_tipo_de_processo_para_o_cliente(cliente_dict):
    
    cliente_dict['tipo_processo'] = 'DPVAT'

def ler_dados_de_clientes_do_arquivo_de_mocks():

    arquivo = open('mocks', mode='r', encoding='utf8')
    conteudo_mocks = arquivo.readlines()
    chaves = [x.strip() for x in conteudo_mocks[0].split(',')]
    dados_cliente = []
    
    for line in conteudo_mocks[1:]:
        cliente_dict = {}
        line_values = [i.strip() for i in line.split(',')]
        for x in range(0, 6):
            cliente_dict[chaves[x]] = line_values[x]
        dados_cliente.append(cliente_dict)

    arquivo.close()
    
    for cli in dados_cliente:
        definir_tipo_de_processo_para_o_cliente(cli)

    return dados_cliente

dados_clientes = ler_dados_de_clientes_do_arquivo_de_mocks()

for cli in dados_clientes:
    executor.cadastrar_cliente(cli)

         