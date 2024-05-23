let globalFasesDict = null
let serverUrl = 'http://localhost:5002/'

function criarElementoHTMLDeDocumento(link, nome) {

  const htmlString = `<a href="${link}"> <div>
    <i><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark" viewBox="0 0 16 16">
      <path d="M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h5.5zm-3 0A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4.5z"/>
    </svg></i>
    <span>${nome}</span>
  </div>
</a>`

  var div = document.createElement('div');
  div.innerHTML = htmlString.trim();

  // Change this to div.childNodes to support multiple top-level nodes.
  return div.firstChild;
}

function getServerUrl(endpoint) {
  return serverUrl + endpoint
}

function xor(val1, val2) {
  return (val1 || val2) && !(val1 && val2)
}


$(exampleModalLong).on('show.bs.modal', (event) => {

  const obterDadosDoElementoQueDisparouAModal = (event) => {
    const triggerElement = $(event.relatedTarget)
    const tableRow = triggerElement.parent().parent()
    const dataElements = tableRow.find('td')
    const tableHeader = tableRow.find('th')[0]
    dataElements.push(tableHeader)
    return { 'tableRow': tableRow, 'dataElements': dataElements }
  }

  const criarDicionarioCliente = (dataElements) => {
    const clientDict = {}
    for (let element of dataElements) {
      if (element.className != '') {
        clientDict[element.className] = element.textContent
      }
    }
    return clientDict
  }

  const alterarInformacoesExibidasNaModal = (tableRow, dicionarioCliente) => {

    //selecionando e alterando o elemento de codigo
    document.getElementById('codigo_cliente').value = dicionarioCliente['codigo']
    //selecionando e alterando o elemento de nome
    document.getElementById('nome_cliente').value = dicionarioCliente['nome']
    //selecionando e alterando o elemento de rg
    document.getElementById('rg_cliente').value = dicionarioCliente['rg']
    //selecionando e alterando o elemento de cpf
    document.getElementById('cpf_cliente').value = dicionarioCliente['cpf']
    //selecionando e alterando o elemento de endereco
    document.getElementById('endereco_cliente').value = dicionarioCliente['endereco']
    //selecionando e alterando o elemento de fone
    document.getElementById('fone_cliente').value = dicionarioCliente['fone']


    //modificando as checkboxes de tipos de seguro

    const marcarOpcaoDeSeguro = (seguro) => {

      switch (seguro) {
        case 'Seguro de Vida':
          document.getElementById('seguro_de_vida').setAttribute('checked', 'checked')
          break
        case 'DPVAT':
          document.getElementById('DPVAT').setAttribute('checked', 'checked')
          break
        case 'Acidente de Trabalho':
          document.getElementById('acidente_de_trabalho').setAttribute('checked', 'checked')
          break
        case 'Terceiro':
          document.getElementById('terceiro').setAttribute('checked', 'checked')
          break
      }
    }

    const seguros = dicionarioCliente['tipos']

    if (seguros.includes(';')) {
      const segurosArr = seguros.split('; ')
      for (let seguro of segurosArr) {
        marcarOpcaoDeSeguro(seguro)
      }
    } else {
      marcarOpcaoDeSeguro(seguros)
    }

    //documentos do cliente

    const renderizarElementosDeDocumentos = (tableRow, iconGrid) => {
      const tdDocumentos = tableRow.find('.td_documentos')[0]
      const documentos = tdDocumentos.getElementsByClassName('documento_individual')
      dicionarioCliente['documentos_enviados'] = []

      for (let doc of documentos){
        let nome = doc.textContent
        let link = ""
        dicionarioCliente['documentos_enviados'].push(nome)
        const docHtml = criarElementoHTMLDeDocumento(link, nome)
        iconGrid.appendChild(docHtml)
      }

    }

    const iconGrid = document.getElementsByClassName('icon-grid')[0]
    
    renderizarElementosDeDocumentos(tableRow, iconGrid)
    
    const btnDocumentosCliente = document.getElementById('btn_documentos_cliente')

    btnDocumentosCliente.onclick = () => {
      let iconGridDisplay = iconGrid.style.display

      if (iconGridDisplay == 'none'){
        iconGrid.style.display = 'block'
      } else {
        iconGrid.style.display = 'none'
      }

    }

    const construirFasesDict = (tableRow) => {

      const tdFases = tableRow.find('.td_fases')[0]
      const entries = tdFases.getElementsByClassName('fase_dict_entry')
      const fasesDict = {}

      for (let entry of entries) {
        const faseCodigo = entry.getElementsByClassName('fase_dict_codigo')[0].innerHTML
        const faseNome = entry.getElementsByClassName('fase_dict_nome_por_extenso')[0].innerHTML
        const faseObservacoes = entry.getElementsByClassName('fase_dict_observacoes')[0].innerHTML
        fasesDict[faseCodigo] = {}
        fasesDict[faseCodigo]['nome_por_extenso'] = faseNome
        fasesDict[faseCodigo]['observacoes'] = faseObservacoes
      }

      return fasesDict
    }

    const fasesDict = construirFasesDict(tableRow)
    globalFasesDict = fasesDict

    const selectOptionsFases = document.getElementById('select_options_fases')
    selectOptionsFases.textContent = ''

    for (let fase of Object.keys(fasesDict)) {
      const optionElement = document.createElement('option')
      optionElement.innerHTML = fasesDict[fase]['nome_por_extenso']
      selectOptionsFases.appendChild(optionElement)
    }

    selectOptionsFases.value = dicionarioCliente['fase_atual']


    const obterCodigoPeloNomePorExtenso = (nomePorExtenso) => {

      let codigo = null

      switch (nomePorExtenso) {
        case 'Documentação inicial':
          codigo = 'DOC_INICIAL'
          break
        case 'Análise':
          codigo = 'ANALISE'
          break
        case 'Processos internos':
          codigo = 'PROC_INTERN'
          break
        case 'Perícia':
          codigo = 'PERICIA'
          break
        case 'Seguradora':
          codigo = 'SEGURADORA'
          break
      }

      return codigo
    }

    const exibirHistoricoDaFase = () => {
      //const opcoes = document.getElementById('select_options_fases')
      const faseSelecionada = selectOptionsFases.value
      const historico = document.getElementById('historicoTextArea1')

      historico.textContent = globalFasesDict[obterCodigoPeloNomePorExtenso(faseSelecionada)]['observacoes']
    }

    exibirHistoricoDaFase()

    const habilitarOuDesabilitarEdicaoDeHistorico = () => {
      const faseSelecionada = selectOptionsFases.value
      const historicoEdicao = document.getElementById('historicoTextArea2')
      if (faseSelecionada != dicionarioCliente['fase_atual']) {
        historicoEdicao.setAttribute('readonly', 'readonly')
      } else {
        historicoEdicao.removeAttribute('readonly')
      }
    }

    selectOptionsFases.onchange = () => {
      //type code here
      exibirHistoricoDaFase()
      habilitarOuDesabilitarEdicaoDeHistorico()
    }
  }

  const dataDict = obterDadosDoElementoQueDisparouAModal(event)
  const dataElements = dataDict['dataElements']
  const tableRow = dataDict['tableRow']
  const dicionarioCliente = criarDicionarioCliente(dataElements)
  alterarInformacoesExibidasNaModal(tableRow, dicionarioCliente)


  const btnSalvarAlteracoes = document.getElementById('btn-salvar-alteracoes')

  btnSalvarAlteracoes.onclick = () => {
    const historicoEdicao = document.getElementById('historicoTextArea2')
    const opcaoDeFinalizacao = document.getElementById('opcao_de_finalizacao_de_fase')
    const valorFoiDigitadoNoCampo = (historicoEdicao.value != "")
    const opcaoDeFinalizacaoSelecionada = (opcaoDeFinalizacao.checked)

    const adicionarObservacaoNoHistorico = () => {
      const textoDigitado = historicoEdicao.value
      let idProcesso = dicionarioCliente['numero_processo']  
      fetch(getServerUrl(`api/processo/${idProcesso}/adicionar_observacao`), {
        "method": "POST", // *GET, POST, PUT, DELETE, etc.
        "mode": "cors", // no-cors, *cors, same-origin
        "cache": "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        "credentials": "same-origin", // include, *same-origin, omit
        "headers": {
          "Content-Type": "application/json",
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        "redirect": "follow", // manual, *follow, error
        "referrerPolicy": "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        "body": JSON.stringify({ observacao: textoDigitado }), // body data type must match "Content-Type" header
      }).then((data) => {
        console.log(data)
        location.reload()
    })}

    const finalizarFaseDoProcesso = () => {
      const textoDigitado = historicoEdicao.value
      let idProcesso = dicionarioCliente['numero_processo']  
      fetch(getServerUrl(`api/processo/${idProcesso}/proxima_fase`), {
        "method": "POST", // *GET, POST, PUT, DELETE, etc.
        "mode": "cors", // no-cors, *cors, same-origin
        "cache": "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        "credentials": "same-origin", // include, *same-origin, omit
        "headers": {
          "Content-Type": "application/json",
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        "redirect": "follow", // manual, *follow, error
        "referrerPolicy": "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        "body": JSON.stringify({ proxima_fase: "sim" }), // body data type must match "Content-Type" header
      }).then((data) => {
        console.log(data)
        location.reload()
      })      
    }

    const adicionarObservacaoEFinalizarFase = () => {
      const textoDigitado = historicoEdicao.value
      let idProcesso = dicionarioCliente['numero_processo']  
      fetch(getServerUrl(`api/processo/${idProcesso}/adicionar_observacao`), {
        "method": "POST", // *GET, POST, PUT, DELETE, etc.
        "mode": "cors", // no-cors, *cors, same-origin
        "cache": "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        "credentials": "same-origin", // include, *same-origin, omit
        "headers": {
          "Content-Type": "application/json",
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        "redirect": "follow", // manual, *follow, error
        "referrerPolicy": "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        "body": JSON.stringify({ observacao: textoDigitado }), // body data type must match "Content-Type" header
      }).then((data) => {
        //console.log(data)
        fetch(getServerUrl(`api/processo/${idProcesso}/proxima_fase`), {
          "method": "POST", // *GET, POST, PUT, DELETE, etc.
          "mode": "cors", // no-cors, *cors, same-origin
          "cache": "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
          "credentials": "same-origin", // include, *same-origin, omit
          "headers": {
            "Content-Type": "application/json",
            // 'Content-Type': 'application/x-www-form-urlencoded',
          },
          "redirect": "follow", // manual, *follow, error
          "referrerPolicy": "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
          "body": JSON.stringify({ proxima_fase: "sim" }), // body data type must match "Content-Type" header
        }).then((data) => {
          //console.log(data)
          location.reload()
        })
    })      
    }

    if (xor(valorFoiDigitadoNoCampo, opcaoDeFinalizacaoSelecionada)) {

      console.log('xor')

      if (valorFoiDigitadoNoCampo) {
        //type code here fetch api
        adicionarObservacaoNoHistorico()
      }
      else {
        //type code here
        finalizarFaseDoProcesso()
      }
    } else {
      //type code here

      console.log('not xor')
      adicionarObservacaoEFinalizarFase()
    }
    }
  }
)


const btnCadastro = document.getElementById('cadastro')

btnCadastro.addEventListener('click', () => {
  const form = document.getElementById('formulario')
  form.submit()
})
