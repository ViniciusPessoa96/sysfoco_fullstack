import sqlite3
import datetime

class ExecutorDeQueries():
    
    def __init__(self):
        self.__db_cur = None
        self.__db_con = None
        self.conectar_ao_banco()

    @property    
    def db_con(self):
        return self.__db_con
    
    @property
    def db_cur(self):
        return self.__db_cur 

    def conectar_ao_banco(self):        
        con = sqlite3.connect('db_sysfoco.db', check_same_thread=False)
        cursor = con.cursor()
        self.__db_con = con
        self.__db_cur = cursor
            
    def criar_registro_do_cliente(self, codigo_cliente, nome, rg, cpf, endereco, telefone):
        
        self.db_cur.execute('INSERT INTO cliente VALUES (?, ?, ?, ?, ?, ?)',
                    (codigo_cliente, nome, rg, cpf, endereco, telefone))
        
        self.db_con.commit()

    def gerar_numero_de_processo(self):
        
        query = self.db_cur.execute('SELECT numero_processo FROM processo')
        result = query.fetchall()    
        numero_processo = max([x[0] for x in result]) + 1
        return numero_processo

    def criar_registro_do_processo(self, codigo_cliente, tipo_processo):
        
        numero_processo = self.gerar_numero_de_processo()
            
        self.db_cur.execute('INSERT INTO processo VALUES(?,?,?)',
                    (numero_processo, codigo_cliente, tipo_processo))

        self.db_con.commit()

        return numero_processo

    def definir_fase_para_processo(self, id_processo, codigo_fase, data_inicio):
        
        if type(data_inicio) == str:    
            data_inicio = datetime.datetime.fromisoformat(data_inicio)
        #data_finalizacao = data_inicio + datetime.timedelta(days=15)
        
        self.db_cur.execute('INSERT INTO fase_do_processo VALUES (?,?,?,?,?,?)',
                    (id_processo, codigo_fase, data_inicio, '', 'AGUARDANDO', ''))
        
        self.db_con.commit()

    def criar_processo_vinculado_ao_cliente(self, codigo_cliente, tipo_processo, data_inicio):
        
        numero_processo = self.criar_registro_do_processo(codigo_cliente, tipo_processo)
        self.definir_fase_para_processo(numero_processo, 'DOC_INICIAL', data_inicio)
        
    def gerar_codigo_de_cliente(self):
        
        query = self.db_cur.execute('SELECT codigo_cliente FROM cliente')
        results = query.fetchall()
        codigo_cliente = max([x[0] for x in results]) + 1
        return codigo_cliente
    
    def registrar_documentos_enviados_pelo_cliente(self, codigo_cliente, documentos):
        
        for doc in documentos:
            self.db_cur.execute('INSERT INTO documentos VALUES (?,?)', 
                                (codigo_cliente, doc))

    def cadastrar_cliente(self, dados_cliente):
        
    # dados_cliente deve ser um dicionário

        if not bool(dados_cliente.get('codigo_cliente')):
            dados_cliente['codigo_cliente'] = self.gerar_codigo_de_cliente()
        
        self.criar_registro_do_cliente(dados_cliente['codigo_cliente'], 
                                dados_cliente['nome'], 
                                dados_cliente['rg'],
                                dados_cliente['cpf'], 
                                dados_cliente['endereco'], 
                                dados_cliente['fone'])

        self.criar_processo_vinculado_ao_cliente(dados_cliente['codigo_cliente'], 
                                                        dados_cliente['tipo_processo'],
                                                        dados_cliente['data_inicio'])
        
        
        if bool(dados_cliente.get('documentos')):
                self.registrar_documentos_enviados_pelo_cliente(
                    dados_cliente['codigo_cliente'], dados_cliente['documentos'])

    def obter_lista_clientes(self):
        
        query = self.db_cur.execute('SELECT codigo_cliente, nome, rg, cpf, endereco, fone FROM cliente')
        results = query.fetchall()
        return results
    
    def obter_dados_de_um_cliente(self, codigo_cliente):
        query = self.db_cur.execute('SELECT codigo_cliente, nome, rg, cpf, endereco, fone FROM cliente WHERE codigo_cliente = ?', 
                                    (codigo_cliente,))
        results = query.fetchall()
        return results[0]
    
    def obter_processos_para_cliente_especifico(self, codigo_cliente):
            
        query = self.db_cur.execute('SELECT c.codigo_cliente, c.nome, c.cpf, p.numero_processo, p.tipo_processo, \
            f.codigo_fase, f.codigo_status FROM cliente c JOIN processo p ON c.codigo_cliente = p.codigo_cliente \
            JOIN fase_do_processo f ON p.numero_processo = f.numero_processo WHERE c.codigo_cliente = ? AND f.codigo_status IN ("AGUARDANDO", "INDEFERIDO")', 
            (codigo_cliente,))
                
        results = query.fetchall()
                
        return results
        
    def obter_informacoes_de_processo_especifico(self, numero_processo):
        
        query = self.db_cur.execute('SELECT c.codigo_cliente, c.nome, c.cpf, p.numero_processo, p.tipo_processo, \
            f.codigo_fase, f.data_inicio, f.codigo_status, f.observacao FROM cliente c JOIN processo p ON c.codigo_cliente = p.codigo_cliente \
            JOIN fase_do_processo f ON p.numero_processo = f.numero_processo WHERE p.numero_processo = ?', (numero_processo,))
        
        results = query.fetchall()
        
        return results

    def obter_fases_do_processo(self, numero_processo):
        
        info = self.obter_informacoes_de_processo_especifico(numero_processo)
        
        return info
    
    def recuperar_id_de_processo_do_cliente(self, codigo_cliente):
        
        query = self.db_cur.execute('SELECT numero_processo from processo WHERE codigo_cliente = ?', (codigo_cliente,))
        result = query.fetchone()
        
        return result[0]


    def recuperar_fase_atual_do_processo(self, id_processo):
        
        query = self.db_cur.execute('SELECT codigo_fase FROM fase_do_processo WHERE numero_processo = ? AND codigo_status = ?', 
                    (id_processo, 'AGUARDANDO'))
        result = query.fetchone()
        
        return result[0]

    def get_proxima_fase(self,codigo_fase):
        
        proxima_fase = None
        
        if codigo_fase == 'DOC_INICIAL':
            proxima_fase = 'ANALISE'
        elif codigo_fase == 'ANALISE':
            proxima_fase = 'PROC_INTERN'
        elif codigo_fase == 'PROC_INTERN':
            proxima_fase = 'PERICIA'
        elif codigo_fase == 'PERICIA':
            proxima_fase = 'SEGURADORA'
        elif codigo_fase == 'SEGURADORA':
            proxima_fase = 'RECEBIMENTO'
            
        return proxima_fase
        
    
    def passar_processo_para_proxima_fase(self, id_processo):

        #id_processo = self.recuperar_id_de_processo_do_cliente(codigo_cliente)
        
        data_inicio = datetime.datetime.now()
        #data_finalizacao = data_inicio + datetime.timedelta(days=15)
        
        fase_atual = self.recuperar_fase_atual_do_processo(id_processo)
        
        #altera registro da fase atual do processo
        self.db_cur.execute('UPDATE fase_do_processo SET codigo_status = ? WHERE numero_processo = ?', 
                    ('APROVADO', id_processo))
        
        self.db_con.commit()
        
        #cria registro da nova fase do processo
        nova_fase = self.get_proxima_fase(fase_atual)
        self.definir_fase_para_processo(id_processo, nova_fase, data_inicio)

    def obter_processos_em_uma_dada_fase(self, codigo_fase):
        
        query = self.db_cur.execute('SELECT c.codigo_cliente, c.nome, c.cpf, p.numero_processo, p.tipo_processo, \
            f.codigo_fase, f.codigo_status, f.observacao FROM cliente c JOIN processo p ON c.codigo_cliente = p.codigo_cliente \
            JOIN fase_do_processo f ON p.numero_processo = f.numero_processo WHERE f.codigo_fase = ? AND f.codigo_status = "AGUARDANDO"', (codigo_fase,))
        
        results = query.fetchall()
        
        return results
    
    def cancelar_prosseguimento_do_processo(self, numero_processo):
        
        query = self.db_cur.execute(
            'UPDATE fase_do_processo SET codigo_status = "INDEFERIDO" WHERE codigo_status = "AGUARDANDO" AND numero_processo = ?', 
            (numero_processo,))
        self.db_con.commit()
        
    def recuperar_observacoes_escritas_ate_agora(self, numero_processo, fase_processo):
        
        query = self.db_cur.execute('SELECT observacao FROM fase_do_processo \
            WHERE numero_processo = ? AND codigo_fase = ?', 
            (numero_processo, fase_processo))
        
        result = query.fetchall()
        
        return result[0][0] #retornando apenas o texto, ao invés de uma lista de tuplas
    
    def formatar_texto_de_observacao(self, texto_obs):
        
        data_observacao = str(datetime.datetime.now())
        texto_final = data_observacao + '\n' + texto_obs + '\n'        
        return texto_final
        
        
    def adicionar_observacao_a_fase_atual_do_processo(self, numero_processo, nova_observacao):
        
        fase_atual = self.recuperar_fase_atual_do_processo(numero_processo)
        
        observacoes_existentes = self.recuperar_observacoes_escritas_ate_agora(numero_processo, fase_atual)
        
        observacoes_atualizadas = observacoes_existentes + self.formatar_texto_de_observacao(nova_observacao)
        
        self.db_cur.execute('UPDATE fase_do_processo SET observacao = ? \
            WHERE numero_processo = ? AND codigo_fase = ?',
            (observacoes_atualizadas, numero_processo, fase_atual))
        
        self.db_con.commit()
        
    def obter_nome_completo_da_fase(self, codigo_fase):
        
        query = self.db_cur.execute('SELECT descricao_fase FROM fases WHERE codigo_fase = ?', (codigo_fase,))
        result = query.fetchone()[0]
        
        return result
    
    def obter_documentos_do_cliente(self, codigo_cliente):
        
        query = self.db_cur.execute('SELECT nome_documento FROM documentos WHERE codigo_cliente = ?', (codigo_cliente,))
        result = query.fetchall()
        
        return result