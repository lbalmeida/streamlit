import streamlit as st
import os
import locale
import services.dbcon as dbcon
import tools.tools as tools
import pandas as pd


bar = st.sidebar
bar.title('Busca por CPF')

cpf = bar.text_input('CPF(somente números):', max_chars=11)

permanencia = None
apoio = None
nada_consta = None
mobilidade = None
moradia = None

if cpf:
    if tools.validar_cpf(cpf):
        buscas = ''
#        dados = {'Sistema': ['Permanência', 'Apoio', 'Nada Consta', 'Mobilidade', 'Moradia']}
        permanencia = dbcon.pesquisa_permanencia(cpf)
        if permanencia:
            buscas = buscas + 'Permanência: :green[Encontrado]\n\n'
        else:
            buscas = buscas + 'Permanência: :red[Não encontrado]\n\n'

        apoio = dbcon.pesquisa_apoio(cpf)
        if apoio:
            buscas = buscas + 'Apoio: :green[Encontrado]\n\n'
        else:
            buscas = buscas + 'Apoio: :red[Não encontrado]\n\n'

        nada_consta = dbcon.pesquisa_nada_consta(cpf)
        if nada_consta:
            buscas = buscas + 'Nada Consta: :green[Encontrado]\n\n'
        else:
            buscas = buscas + 'Nada Consta: :red[Não encontrado]\n\n'

        mobilidade = dbcon.pesquisa_mobilidade(cpf)
        if mobilidade:
            buscas = buscas + 'Mobilidade: :green[Encontrado]\n\n'
        else:
            buscas = buscas + 'Mobilidade: :red[Não encontrado]\n\n'

        moradia = dbcon.pesquisa_moradia(cpf)
        if moradia:
            buscas = buscas + 'Moradia: :green[Encontrado]\n\n'
        else:
            buscas = buscas + 'Moradia: :red[Não encontrado]\n\n'

        bar.info(f'{buscas}')

        if permanencia or apoio or nada_consta or mobilidade:
            arquivo = f'fotos\{cpf}.jpg'
            if os.path.isfile(arquivo):
                bar.image(arquivo)
            else:
                bar.image('fotos\John Doe.jpg')
        else:
            bar.info(f':green[CPF não encontrado!]')
    else:
        bar.info(f':red[CPF inválido!]')

else:
    bar.info('Informe um CPF')

if permanencia:
    ultimo_movimento = f'{permanencia[0].upper()}'
    data_movimento = '{:%d/%m/%Y}'.format(permanencia[12])

    with st.expander(f'{permanencia[2]} - :green[Auxílio Permanência]', expanded=True):
        container = st.container()

        a, b = container.columns(2)
        a.info(f'Inscrição: :green[{permanencia[1]}]')

        if ultimo_movimento in ['INCLUSÃO', 'ALTERAÇÃO']:
            b.info(f':green[{ultimo_movimento}] - :green[{data_movimento}]')
        else:
            b.info(f':red[{ultimo_movimento}] - :green[{data_movimento}]')

        a, b = container.columns(2)
        a.info(f'Matrícula: :green[{permanencia[3]}]')
        b.info(f'E-Mail: :blue[{permanencia[5]}]')

if apoio:
    status = f'{apoio[11].upper()}'

    with st.expander(f'{apoio[3]} - :green[Bolsa de Apoio Acadêmico]', expanded=True):
        container = st.container()

        a, b = container.columns(2)
        a.info(f'Código: :green[{apoio[1]}]')

        if status == 'ATIVA':
            b.info(f':green[{status}]')
        else:
            b.info(f':red[{status}]')

        a, b = container.columns(2)
        a.info(f'Matrícula: :green[{apoio[2]}]')
        b.info(f'E-Mail: :blue[{apoio[4]}]')

if nada_consta:
    with st.expander(f'{nada_consta[1]} - :green[Nada Consta]', expanded=True):
        container = st.container()

        a, b = container.columns(2)
        a.info(f'Matrícula: :green[{nada_consta[0]}]')
        b.info(f'Tipo de Bolsa: :green[{nada_consta[3]}]')

        st.info(f'Referência: :green[{nada_consta[5]}]')

        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            valor = locale.currency(nada_consta[4], grouping=True, symbol=True)
        except:
            valor = nada_consta[4]

        if valor:        
            st.info(f'Valor: :green[{valor}]')

        if nada_consta[6]:
            st.info(f'Observação: :green[{nada_consta[6]}]')

if mobilidade:
    with st.expander(f'{mobilidade[0]} - :green[Mobilidade]', expanded=True):
        container = st.container()

        a, b, c = container.columns(3)
        a.info(f'Bicicleta: :green[{mobilidade[1]}]')
        b.info(f'Matrícula: :green[{mobilidade[4]}]')
        c.info('Retirada: :green[{:%d/%m/%Y}]'.format(mobilidade[2]))

        a, b = container.columns(2)
        a.info(f'Situação: :green[{mobilidade[5]}]')
        b.info('Data Situação: :green[{:%d/%m/%Y}]'.format(mobilidade[6]))

        if mobilidade[3]:
            st.info(f'Devolução: :green[{mobilidade[3]}]')
        else:
            st.info(f'Devolução:')

        if mobilidade[8]:
            st.info(f'Observação: :green[{mobilidade[8]}]')
        else:
            st.info(f'Observação:')

if moradia:
    with st.expander(f'{moradia[2]} - :green[Moradia]', expanded=True):
        container = st.container()

        a, b = container.columns(2)
        a.info(f'Matrícula: :green[{moradia[1]}]')

        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        valor = locale.currency(moradia[6], grouping=True, symbol=True)
        b.info(f'Valor: :green[{valor}]')
