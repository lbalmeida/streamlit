import pyodbc


def pesquisa_permanencia(cpf):
    try:
        driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
        filepath = r'R:\Dados\Bolsas-Dados.accdb'
        password = 'BolsaUenf2021'

        conn = pyodbc.connect(driver=driver, dbq=filepath, autocommit=True, PWD=password)

        cursor = conn.cursor()
        query = "" \
            "SELECT " \
            "       Folha.[Tipo de Movimento], " \
            "       [Item Folha].Aluno, " \
            "       [Cadastro de Alunos].Nome, " \
            "       [Cadastro de Alunos].Matrícula, " \
            "       [Cadastro de Alunos].CPF, " \
            "       [Cadastro de Alunos].Email, " \
            "       [Cadastro de Alunos].Telefone, " \
            "       [Cadastro de Alunos].Celular, " \
            "       [Cadastro de Alunos].Celular2, " \
            "       [Cadastro de Alunos].Agencia, " \
            "       [Cadastro de Alunos].Conta, " \
            "       [Tabela de Cursos].Duração, " \
            "       [Item Folha].[Data de Início], " \
            "       [Item Folha].Vencimento, " \
            "       Folha.[Código Folha], " \
            "       [Item Folha].Abatimentos " \
            "  FROM (Folha " \
            " INNER JOIN ([Item Folha] " \
            " INNER JOIN [Cadastro de Alunos] ON [Item Folha].Aluno = [Cadastro de Alunos].Inscrição) ON Folha.[Código Folha] = [Item Folha].[Código Folha])  " \
            " INNER JOIN [Tabela de Cursos] ON [Cadastro de Alunos].Curso = [Tabela de Cursos].Nome " \
            f" WHERE [Cadastro de Alunos].CPF = '{cpf}' " \
            " ORDER BY [Item Folha].Aluno, [Item Folha].[Data de Início] DESC " \

        cursor.execute(query)

        row = cursor.fetchone()

#        if row:
#            print('')
#            print('---------------------------------')
#            print('Auxílio Permanência')
#            print(f'Último Movimento: {row[0].upper()}')
#            print(f'Inscrição: {row[1]}')
#            print(f'Nome: {row[2]}')
#            print(f'Matrícula: {row[3]}')
#            print(f'CPF: {row[4]}')
#            print(f'E-Mail: {row[5]}')
#            print("Data: {:%d/%m/%Y}".format(row[12]))
#            print(f'Foto: {cpf}.jpg')

        conn.close()

        return row

    except pyodbc.Error as e:
        print("Error in connection", e)


def pesquisa_apoio(cpf):
    try:
        driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
        filepath = r'Q:\Dados\BAA-Dados.accdb'
        password = 'BolsaUenf2021'

        conn = pyodbc.connect(driver=driver, dbq=filepath, autocommit=True, PWD=password)

        cursor = conn.cursor()
        query = "" \
            "SELECT " \
            "       [cadastroSolicitaçãoBolsas].cpfaluno, " \
            "       cadbolsas.codbolsista, "\
            "       alunos.matricula, " \
            "       cadbolsas.bolsista, " \
            "       alunos.email, " \
            "       alunos.[ddd tel aluno], alunos.telefone, " \
            "       alunos.[ddd cel aluno], alunos.celular, " \
            "       cadbolsas.inicio, " \
            "       cadbolsas.vencimentodabolsa, " \
            "       cadbolsas.[situaçãodabolsa], " \
            "       cadbolsas.[motivo exclusão] " \
            "  FROM alunos " \
            " INNER JOIN ([cadastroSolicitaçãoBolsas] " \
            " INNER JOIN cadbolsas ON [cadastroSolicitaçãoBolsas].[numeroInscrição] = cadbolsas.codbolsista) ON alunos.CPF = [cadastroSolicitaçãoBolsas].cpfaluno " \
            f" WHERE [cadastroSolicitaçãoBolsas].cpfaluno = '{cpf}' " \
            " ORDER BY [cadastroSolicitaçãoBolsas].cpfaluno, cadbolsas.codbolsista DESC"

        cursor.execute(query)

        row = cursor.fetchone()

#        if row:
#            print('')
#            print('---------------------------------')
#            print('Bolsa de Apoio Acadêmico')
#            print(f'Status da Bolsa: {row[11].upper()}')
#            print(f'Inscrição: {row[1]}')
#            print(f'Nome: {row[3]}')
#            print(f'Matrícula: {row[2]}')
#            print(f'CPF: {row[0]}')
#            print(f'E-Mail: {row[4]}')
#            print(f'Foto: {cpf}.jpg')

        conn.close()

    except pyodbc.Error as e:
        print("Error in connection", e)

    return row

def pesquisa_nada_consta(cpf):
    try:
        driver = '{Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)}'
        filepath = r'S:\Meu Drive\Nada Consta\LISTA DE CONSTA GERAL- BOLSISTAS UENF- 2017.xlsx'

        conn = pyodbc.connect(driver=driver, dbq=filepath, readonly=0, autocommit=True)

        cursor = conn.cursor()

        for worksheet in cursor.tables():
            table_name = worksheet[2]

        query = "SELECT * FROM [{}]".format(table_name)
        cursor.execute(query)

        for row in cursor:
            cpf_formatado = row[2]
            if cpf_formatado:
                if cpf_formatado[0].isnumeric():
                    cpf_formatado = cpf_formatado.replace(' ', '')
                    cpf_formatado = cpf_formatado.replace('.', '')
                    cpf_formatado = cpf_formatado.replace('-', '')

                    if cpf_formatado == cpf:
                        return row

    except pyodbc.Error as e:
        print("Error in connection", e)

def pesquisa_mobilidade(cpf):
    try:
        driver = '{Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)}'
        filepath = r'S:\Meu Drive\Mobilidade - Bicicletas\Controle de bicicletas - Verificar.xlsx'

        conn = pyodbc.connect(driver=driver, dbq=filepath, readonly=0, autocommit=True)

        cursor = conn.cursor()

        for worksheet in cursor.tables():
            table_name = worksheet[2]

        query = "SELECT * FROM [{}]".format(table_name)
        cursor.execute(query)

        for row in cursor:
            cpf_formatado = row[7]
            if cpf_formatado:
                if cpf_formatado[0].isnumeric():
                    cpf_formatado = cpf_formatado.replace(' ', '')
                    cpf_formatado = cpf_formatado.replace('.', '')
                    cpf_formatado = cpf_formatado.replace('-', '')

                    if cpf_formatado == cpf:
                        return row

    except pyodbc.Error as e:
        print("Error in connection", e)

def pesquisa_moradia(cpf):
    try:
        driver = '{Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)}'
        filepath = r'S:\Meu Drive\Moradia\Pagamentos Auxilios Moradia - busca por CPF.xlsx'

        conn = pyodbc.connect(driver=driver, dbq=filepath, readonly=0, autocommit=True)

        cursor = conn.cursor()

        for worksheet in cursor.tables():
            table_name = worksheet[2]
        query = "SELECT * FROM [{}]".format(table_name)
        cursor.execute(query)

        for row in cursor:
            cpf_formatado = row[3]
            if cpf_formatado:
                if cpf_formatado[0].isnumeric():
                    cpf_formatado = cpf_formatado.replace(' ', '')
                    cpf_formatado = cpf_formatado.replace('.', '')
                    cpf_formatado = cpf_formatado.replace('-', '')

                    if cpf_formatado == cpf:
                        return row

    except pyodbc.Error as e:
        print("Error in connection", e)


if __name__ == '__main__':
    print(pesquisa_permanencia('12079226762'))
    print(pesquisa_apoio('08697038626'))
    print(pesquisa_nada_consta('05700382784'))
    print(pesquisa_mobilidade('08333147690'))
    print(pesquisa_moradia('17839931707'))
