
# dados que eu preciso
# nome, tipos_de_seguro, data_inicio, fase_atual
# self.db_cur.execute('SELECT codigo_cliente, nome, rg, cpf, endereco, fone FROM cliente')

from datetime import datetime
from model2 import ExecutorDeQueries

class Processo():

    def __init__(self, codigo_cliente, executor):

        self.__executor = executor
        self.__codigo_cliente = codigo_cliente

        self.__nome_cliente = None       
        self.__endereco = None
        self.__fone = None
        self.__rg = None
        self.__cpf = None
        self.__numero_processo = None        
        self.__tipos_de_seguros = None
        self.__fase_atual = None
        self.__data_inicio = None
        self.__fases = None
        self.__lista_fases = []
        self.__lista_documentos = []

        self.obter_dados_do_cliente()
        self.obter_dados_do_processo()
        
    def obter_dados_do_cliente(self):
        
        dados = self.__executor.obter_dados_de_um_cliente(self.__codigo_cliente)
        
        _, nome, rg, cpf, endereco, fone = dados
        
        self.__nome_cliente = nome       
        self.__endereco = endereco
        self.__fone = fone
        self.__rg = rg
        self.__cpf = cpf

    def traduzir_codigo_da_fase(self, codigo):

        nome_por_extenso = None

        if codigo == 'DOC_INICIAL':
            nome_por_extenso = 'Documentação inicial'
        elif codigo == 'ANALISE':
            nome_por_extenso = 'Análise'
        elif codigo == 'PROC_INTERN':
            nome_por_extenso = 'Processos internos'
        elif codigo == 'SEGURADORA':
            nome_por_extenso = 'Seguradora'
        
        return nome_por_extenso

    def obter_dados_do_processo(self):
        
        dados_do_processo = self.__executor.obter_processos_para_cliente_especifico(self.__codigo_cliente)[0]
        #breakpoint()
        numero_processo = dados_do_processo[3]
        self.__tipos_de_seguros = dados_do_processo[4]
        #breakpoint()
        self.__fase_atual = self.__executor.obter_nome_completo_da_fase(dados_do_processo[5])
        
        fases = self.__executor.obter_fases_do_processo(numero_processo)
        #self.__fases = [{"fase" : f[5], "observacoes" : f[-1]} for f in fases]

        self.__numero_processo = numero_processo

        self.__fases = []

        for fase in fases:
            self.__lista_fases.append(fase[5])
            faseEntry = {}
            faseEntry['codigo'] = fase[5]
            faseEntry['nome_por_extenso'] = self.traduzir_codigo_da_fase(fase[5])
            faseEntry['observacoes'] = fase[-1]
            self.__fases.append(faseEntry)
        
        for fase in fases:
            if 'DOC_INICIAL' in fase:
                self.__data_inicio = datetime.fromisoformat(fase[6]).strftime('%d-%m-%Y')
                
        self.__lista_documentos = self.__executor.obter_documentos_do_cliente(self.__codigo_cliente)


    @property
    def nome_cliente(self):
        return self.__nome_cliente

    @property
    def codigo_cliente(self):
        return self.__codigo_cliente
    
    @property
    def endereco(self):
        return self.__endereco
    
    @property
    def fone(self):
        return self.__fone
    
    @property
    def rg(self):
        return self.__rg
    
    @property
    def cpf(self):
        return self.__cpf
    
    @property
    def tipos_de_seguros(self):
        return self.__tipos_de_seguros
    
    @property
    def fase_atual(self):
        return self.__fase_atual
    
    @property
    def data_inicio(self):
        return self.__data_inicio
    
    @property
    def fases(self):
        return self.__fases
    
    @property
    def lista_fases(self):
        return self.__lista_fases
    
    @property
    def numero_processo(self):
        return self.__numero_processo
    
    @property
    def lista_documentos(self):
        return self.__lista_documentos