from sysfoco import app
from flask import render_template
import views_api
import controller

@app.route('/')
def inicio():
    
    return render_template('index.html')

@app.route('/clientes')
def clientes():
    
    lista_de_clientes = views_api.lista_clientes()
    lista_de_codigos = [x.get('codigo_cliente') for x in lista_de_clientes]
    
    clientes_obj = controller.criar_lista_de_objetos_processo_cliente(lista_de_codigos)

    #breakpoint()

    return render_template('clientes.html', lista_de_clientes=clientes_obj)
  
@app.route('/clientes_por_fase/<fase>')
def clientes_por_fase(fase):
  
  processos = None
  
  if fase == 'documentacao_inicial':
    processos = views_api.documentacao_inicial()
  elif fase == 'analise':
    processos = views_api.analise()
  elif fase == 'processos_internos':
    processos = views_api.processos_internos()
  elif fase == 'pericia':
    processos = views_api.pericia()
  elif fase == 'seguradora':
    processos = views_api.seguradora()
  elif fase == 'recebimento':
    processos = views_api.recebimento()
    
  lista_de_codigos = controller.filtrar_codigos_de_cliente(processos)
  lista_de_objetos_processo_cliente = controller.criar_lista_de_objetos_processo_cliente(lista_de_codigos)
    
  return render_template('clientes_por_fase.html', processos=lista_de_objetos_processo_cliente, fase=fase)
  