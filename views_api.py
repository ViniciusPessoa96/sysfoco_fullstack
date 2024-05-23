from sysfoco import app
import controller
from flask import redirect, url_for, request
import os

@app.route('/login', methods=['POST', ])
def login():
    pass

@app.route('/api/novo_cliente', methods=['POST',])
def novo_cliente():

    dados_cliente = {}
    dados_formulario = request.form
    dados_cliente['codigo_cliente'] = dados_formulario['codigo']
    dados_cliente['nome'] = dados_formulario['nome']
    dados_cliente['rg'] = dados_formulario['rg']
    dados_cliente['cpf'] = dados_formulario['cpf']
    dados_cliente['endereco'] = dados_formulario['endereco']
    dados_cliente['fone'] = dados_formulario['fone']
    dados_cliente['tipo_processo'] = ('; ').join(dados_formulario.getlist('tiposeguro'))
    dados_cliente['data_inicio'] = dados_formulario['data_inicio']
    #dados_cliente['documentos'] = dados_formulario['documentos']
    dados_cliente['documentos'] = []
    documentos = request.files.getlist('documentos')
    
    for doc in documentos:
        dados_cliente['documentos'].append(doc.filename)
        doc.save(os.path.join(app.config['UPLOAD_FOLDER'], doc.filename))
        
    controller.novo_cliente(dados_cliente)
    return redirect(url_for('clientes'))
    
@app.route('/api/clientes')
def lista_clientes():
    clientes = controller.get_lista_clientes()
    return clientes

@app.route('/api/cliente/<int:codigo_cliente>')
def processos_do_cliente(codigo_cliente):
    processos = controller.get_processos_de_um_cliente(codigo_cliente)
    return processos

@app.route('/api/processo/<int:processo_id>')
def processo_cliente(processo_id):
    processo_info = controller.get_processo_especifico(processo_id)
    return processo_info

@app.route('/api/processo/<int:processo_id>/proxima_fase', methods=['POST',])
def passar_processo_para_proxima_fase(processo_id):
    
    if request.json['proxima_fase'] == 'sim':
        controller.proxima_fase(processo_id)
    
    return {'mensagem' : 'o processo foi movido para a próxima fase'}

@app.route('/api/processo/<int:processo_id>/cancelar', methods=['POST',])
def cancelar_processo(processo_id):
    
    if request.json['fazer_cancelamento'] == 'sim':
        controller.indeferir(processo_id)
    
    return {'mensagem' : 'o processo foi cancelado'}

@app.route('/api/processo/<int:processo_id>/adicionar_observacao', methods=['POST',])
def adicionar_observacao(processo_id):

    #breakpoint()

    observacao = request.json['observacao']
    controller.adicionar_observacao_ao_processo(processo_id, observacao)
    return {'mensagem' : 'observacao adicionada'}

@app.route('/api/processos/documentacao_inicial')
def documentacao_inicial():
    processos = controller.get_processos_em_fase_especifica('DOC_INICIAL')
    return processos

@app.route('/api/processos/analise')
def analise():
    processos = controller.get_processos_em_fase_especifica('ANALISE')
    return processos

@app.route('/api/processos/processos_internos')
def processos_internos():
    processos = controller.get_processos_em_fase_especifica('PROC_INTERN')
    return processos

@app.route('/api/processos/pericia')
def pericia():
    processos = controller.get_processos_em_fase_especifica('PERICIA')
    return processos

@app.route('/api/processos/seguradora')
def seguradora():
    processos = controller.get_processos_em_fase_especifica('SEGURADORA')
    return processos

@app.route('/api/processos/recebimento')
def recebimento():
    processos = controller.get_processos_em_fase_especifica('RECEBIMENTO')
    return processos

