import streamlit as st
import os
import locale
import services.dbcon as dbcon


bar = st.sidebar
bar.title('Busca por CPF')

cpf = bar.text_input('CPF(somente números):', max_chars=11)

permanencia = None
apoio = None
nada_consta = None
mobilidade = None
moradia = None

if cpf:
    permanencia = dbcon.pesquisa_permanencia(cpf)
    apoio = dbcon.pesquisa_apoio(cpf)
    nada_consta = dbcon.pesquisa_nada_consta(cpf)
    mobilidade = dbcon.pesquisa_mobilidade(cpf)
    moradia = dbcon.pesquisa_moradia(cpf)

    if permanencia or apoio or nada_consta or mobilidade:
        arquivo = f'fotos\{cpf}.jpg'
        if os.path.isfile(arquivo):
            bar.image(arquivo)
        else:
            bar.image('fotos\John Doe.jpg')
    else:
        bar.error('Informe um CPF correto!')


if permanencia:
    ultimo_movimento = f'{permanencia[0].upper()}'
    data_movimento = '{:%d/%m/%Y}'.format(permanencia[12])

    with st.expander(f'Auxílio Permanência - {permanencia[2]}', expanded=True):
        container = st.container()

        a, b = container.columns(2)
        a.info(f'Inscrição: {permanencia[1]}')

        if ultimo_movimento in ['INCLUSÃO', 'ALTERAÇÃO']:
            b.success(f'{ultimo_movimento} - {data_movimento}')
        else:
            b.error(f'{ultimo_movimento} - {data_movimento}')

        a, b = container.columns(2)
        a.info(f'Matrícula: {permanencia[3]}')
        b.info(f'E-Mail: {permanencia[5]}')

if apoio:
    status = f'{apoio[11].upper()}'

    with st.expander(f'Bolsa de Apoio Acadêmico - {apoio[3]}', expanded=True):
        container = st.container()

        a, b = container.columns(2)
        a.info(f'Código: {apoio[1]}')

        if status == 'ATIVA':
            b.info(f':green[{status}]')
        else:
            b.info(f':red[{status}]')

        a, b = container.columns(2)
        a.info(f'Matrícula: {apoio[2]}')
        b.info(f'E-Mail: {apoio[4]}')

if nada_consta:
    with st.expander('Nada Consta', expanded=True):
        container = st.container()

        a, b = container.columns(2)
        a.info(f'Matrícula: {nada_consta[0]}')
        b.info(f'Tipo de Bolsa: {nada_consta[3]}')

        st.info(f'Nome: {nada_consta[1]}')
        st.info(f'Referência: {nada_consta[5]}')

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        valor = locale.currency(nada_consta[4], grouping=True, symbol=True)
        st.info(f'Valor: {valor}')

        if nada_consta[6] or nada_consta[8]:
            st.info(f'Observação: {nada_consta[6]} - {nada_consta[8]}')

if mobilidade:
    with st.expander(f'Mobilidade - {mobilidade[0]}', expanded=True):
        container = st.container()

        a, b, c = container.columns(3)
        a.info(f'Bicicleta: {mobilidade[1]}')
        b.info(f'Matrícula: {mobilidade[4]}')
        c.info('Retirada: {:%d/%m/%Y}'.format(mobilidade[2]))

        a, b = container.columns(2)
        a.info(f'Situação: {mobilidade[5]}')
        b.info('Data Situação: {:%d/%m/%Y}'.format(mobilidade[6]))

        st.info(f'Devolução: {mobilidade[3]}')
        st.info(f'Observação: {mobilidade[8]}')

if moradia:
    with st.expander(f'Moradia - {moradia[2]}', expanded=True):
        container = st.container()

        a, b = container.columns(2)
        a.info(f'Matrícula: {moradia[1]}')

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        valor = locale.currency(moradia[6], grouping=True, symbol=True)
        b.info(f'Valor: {valor}')
