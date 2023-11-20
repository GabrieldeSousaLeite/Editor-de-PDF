import os
import fitz
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import aspose.words as aw
import shutil
import glob
import sqlite3
import cv2
import numpy as np
import codecs

def editor_pdf_iniciar():

    def Read(coluna):

        banco = sqlite3.connect('configue.db')
        cursor = banco.cursor()

        cursor.execute(f"SELECT {coluna} FROM configuração WHERE id = ?", (1,))

        resultado = cursor.fetchone()

        banco.close()

        try:
            bytes_ = memoryview(resultado[0]).tobytes()
            return bytes_

        except:

            return resultado[0]
        

    def extrair_texto_pdf(nome_arquivo):
        nome_arquivo_base = os.path.splitext(os.path.basename(nome_arquivo))[0]  # Nome base do arquivo sem a extensão
        diretorio_saida = nome_arquivo_base + "_txt"  # Nome do diretório de saída
        os.makedirs(diretorio_saida, exist_ok=True)  # Cria o diretório de saída

        pdf = fitz.open(nome_arquivo)
        total_paginas = pdf.page_count

        for indice in range(total_paginas):
            pagina = pdf.load_page(indice)
            blocos = pagina.get_text("blocks")  # Obtém os blocos de texto da página

            nome_arquivo_saida = os.path.join(diretorio_saida, f'{nome_arquivo_base}_pagina_{indice+1}.txt')

            with open(nome_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida:
                for bloco in blocos:
                    linhas = bloco[4]  # Obtém as linhas de texto do bloco
                    for linha in linhas:
                        arquivo_saida.write(linha + " ")  # Escreve a linha de texto com um espaço no final
                    arquivo_saida.write("\n\n")  # Inclui linhas vazias entre os parágrafos

            print(f'Página {indice+1} de {total_paginas} do arquivo {nome_arquivo} extraída e salva em {nome_arquivo_saida}.')

        pdf.close()

    diretorio_atual = os.getcwd()  # Obtém o diretório atual onde o código está sendo executado
    padrao_arquivo_pdf = os.path.join(diretorio_atual, "*.pdf")

    # Encontrar o primeiro arquivo PDF no diretório atual
    arquivo_pdf = next(glob.iglob(padrao_arquivo_pdf), None)

    if arquivo_pdf:
        extrair_texto_pdf(arquivo_pdf)


    #-----------------------------------------------------------------------------------------

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Percorre todos os diretórios e arquivos
    for diretorio_raiz, diretorios, arquivos in os.walk(diretorio_atual):
        for arquivo in arquivos:
            # Verifica se o arquivo é um arquivo .txt
            if arquivo.endswith(".txt"):
                # Caminho completo para o arquivo
                caminho_arquivo = os.path.join(diretorio_raiz, arquivo)

                # Abre o arquivo com diferentes codecs e tenta ler
                for codec in ['utf-8', 'latin-1', 'utf-16']:
                    try:
                        with codecs.open(caminho_arquivo, "r", encoding=codec) as arquivo_txt:
                            linhas = arquivo_txt.readlines()
                        print(f"O codec {codec} funcionou para o arquivo {caminho_arquivo}")
                        break  # Se o codec funcionar, interrompe o loop
                    except UnicodeDecodeError:
                        print(f"O codec {codec} não funcionou para o arquivo {caminho_arquivo}")

                # Abre o arquivo em modo de escrita com o codec que funcionou
                with codecs.open(caminho_arquivo, "w", encoding=codec) as arquivo_txt:
                    # Processa cada linha e salva no arquivo original
                    for linha in linhas:
                        texto = linha.strip()
                        novo_texto = ''

                        for indice in range(len(texto)):
                            if indice < len(texto) - 1 and texto[indice] == ' ' and texto[indice+1] == ' ':
                                novo_texto += texto[indice]

                            if indice < len(texto) - 1 and texto[indice] != ' ':
                                novo_texto += texto[indice]

                            if not indice < len(texto) -1:
                                novo_texto += texto[indice]

                        arquivo_txt.write(novo_texto + '\n')

    #----------------------------------------------------------------------------------------
    # Obtém o diretório atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Percorre todos os diretórios e arquivos
    for diretorio_raiz, diretorios, arquivos in os.walk(diretorio_atual):
        for arquivo in arquivos:
            # Verifica se o arquivo é um arquivo .txt
            if arquivo.endswith(".txt"):
                # Caminho completo para o arquivo
                caminho_arquivo = os.path.join(diretorio_raiz, arquivo)

                # Abre o arquivo em modo de leitura
                with open(caminho_arquivo, "r", encoding='utf-8') as arquivo_txt:
                    # Lê todas as linhas do arquivo
                    linhas = arquivo_txt.readlines()

                # Abre o arquivo em modo de escrita
                with open(caminho_arquivo, "w", encoding='utf-8') as arquivo_txt:
                    # Processa cada linha e salva no arquivo original
                    for linha in linhas:
                        texto = linha.strip()
                        novo_texto = ''

                        for indice in range(len(texto)):
                            if indice < len(texto) - 1 and texto[indice] == ' ' and texto[indice+1] == ' ':
                                novo_texto += texto[indice]
                            
                            if indice < len(texto) - 1 and texto[indice] != ' ':
                                novo_texto += texto[indice]
                            
                            if not indice < len(texto) -1:
                                novo_texto += texto[indice]

                        arquivo_txt.write(novo_texto + '\n')

    #-------------------------------------------------------------------------------------------

    # Obtém o diretório do código-fonte
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Variável para armazenar o diretório com os arquivos TXT
    diretorio_txt = None

    # Percorre a árvore de diretórios a partir do diretório atual
    for diretorio, subdiretorios, arquivos in os.walk(diretorio_atual):
        # Verifica se há arquivos TXT neste diretório
        if any(arquivo.lower().endswith('.txt') for arquivo in arquivos):
            diretorio_txt = diretorio
            break

    # Verifica se o diretório foi encontrado
    if diretorio_txt:
        # Lista para armazenar os caminhos dos arquivos TXT
        caminhos_arquivos = []

        # Percorre os arquivos TXT no diretório
        for nome_arquivo in os.listdir(diretorio_txt):
            caminho_arquivo = os.path.join(diretorio_txt, nome_arquivo)

            # Verifica se é um arquivo TXT
            if os.path.isfile(caminho_arquivo) and nome_arquivo.endswith('.txt'):
                # Extrai o número do nome do arquivo usando uma expressão regular
                numero = re.findall(r'(\d+)\.txt$', nome_arquivo)
                if numero:
                    caminhos_arquivos.append((int(numero[0]), caminho_arquivo))

        # Ordena os caminhos dos arquivos com base no número extraído
        caminhos_arquivos.sort(key=lambda x: x[0])

    diretorio_atual = os.getcwd()

    f = 0

    for c in range(2):

        if c == 1:
            f = -1
                
        with open(caminhos_arquivos[f][1], 'r', encoding='utf-8') as arquivo_txt:
            linhas = arquivo_txt.readlines()
            for i in range(len(linhas)):
                linha = linhas[i].strip()

                if linha.startswith('https://'):
                    linha_atualizada = ''
                    linhas[i] = linha_atualizada
                
                if linha.startswith('<image:'):
                    linha_atualizada = ''
                    linhas[i] = linha_atualizada
                    
            # Reescreve o arquivo com as alterações
            with open(caminhos_arquivos[f][1], 'w', encoding='utf-8') as arquivo_atualizado:
                arquivo_atualizado.writelines(linhas)

    #----------------------------------------------------------------------------------------------

    def get_first_pdf_filename():
        pdf_files = glob.glob("*.pdf")
        
        if pdf_files:
            first_pdf_filename = os.path.splitext(pdf_files[0])[0]
            return first_pdf_filename
        else:
            return None

    def percorrer_diretorios(diretorio_atual, substituicoes):
        for raiz, diretorios, arquivos in os.walk(diretorio_atual):
            for arquivo in arquivos:
                if arquivo.endswith(".txt"):
                    caminho_arquivo = os.path.join(raiz, arquivo)
                    with open(caminho_arquivo, "r", encoding='utf-8') as arquivo_txt:
                        linhas = arquivo_txt.readlines()

                    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo_modificado:
                        for linha in linhas:
                            linha_modificada = linha
                            for substituicao in substituicoes:
                                string_original, string_substituta = substituicao
                                linha_modificada = linha_modificada.replace(string_original, string_substituta)
                            arquivo_modificado.write(linha_modificada)

                    print(f"As strings foram substituídas no arquivo: {caminho_arquivo}")

    nome_sem_extensao = get_first_pdf_filename()
    nome_arquivo_html = f"{nome_sem_extensao}.html"

    diretorio_atual = os.getcwd()
    link = Read('link')
    if link == None:
        link = ''

    substituicoes = [
        ("https://passedexams.com/", f"{link}"),
        ("https://www.validexamdumps.com", f"{link}"),
        ("Questions and Answers PDF", ""),
        (f'/{nome_arquivo_html}', "")
    ]

    percorrer_diretorios(diretorio_atual, substituicoes)

    #---------------------------------------------------------------------------------------

    diretorio_atual = os.getcwd()  # Obtém o diretório atual
    contador_arquivos_txt = 0

    for diretorio, subdiretorios, arquivos in os.walk(diretorio_atual):
        for arquivo in arquivos:
            if arquivo.endswith(".txt"):
                contador_arquivos_txt += 1

    for diretorio, subdiretorios, arquivos in os.walk(diretorio_atual):
        for arquivo in arquivos:
            if arquivo.endswith(".txt"):
                numero_arquivos = str(contador_arquivos_txt)
                padrao_numero_barra = r'/' + numero_arquivos + r'$'
                regex = re.compile(padrao_numero_barra)

                caminho_arquivo = os.path.join(diretorio, arquivo)
                linhas_sem_numero_barra = []

                with open(caminho_arquivo, "r", encoding='utf-8') as arquivo_txt:
                    for linha in arquivo_txt:
                        if not regex.search(linha):
                            linhas_sem_numero_barra.append(linha.strip())

                with open(caminho_arquivo, "w", encoding='utf-8') as arquivo_txt:
                    arquivo_txt.write("\n".join(linhas_sem_numero_barra))

    print("Número total de arquivos .txt:", contador_arquivos_txt)


    #----------------------------------------------------------------------------------------

    for c in range(1):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))

        # Percorre todos os diretórios e arquivos
        for diretorio_raiz, diretorios, arquivos in os.walk(diretorio_atual):
            for arquivo in arquivos:
                # Verifica se o arquivo é um arquivo .txt
                if arquivo.endswith(".txt"):
                    # Caminho completo para o arquivo
                    caminho_arquivo = os.path.join(diretorio_raiz, arquivo)

                    # Abre o arquivo em modo de leitura
                    with open(caminho_arquivo, "r", encoding='utf-8') as arquivo_txt:
                        # Lê todas as linhas do arquivo
                        linhas = arquivo_txt.readlines()

                    # Remove excesso de linhas vazias
                    linhas_filtradas = []
                    linha_vazia_anterior = False

                    for linha in linhas:
                        linha = linha.strip()

                        if linha == "":
                            if not linha_vazia_anterior:
                                linhas_filtradas.append(linha)
                            linha_vazia_anterior = True
                        else:
                            linhas_filtradas.append(linha)
                            linha_vazia_anterior = False

                    # Abre o arquivo em modo de escrita
                    with open(caminho_arquivo, "w", encoding='utf-8') as arquivo_txt:
                        arquivo_txt.write("\n".join(linhas_filtradas))
    #----------------------------------------------------------------------------------------------

    # Obtém o diretório do código-fonte
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Variável para armazenar o diretório com os arquivos TXT
    diretorio_txt = None

    # Percorre a árvore de diretórios a partir do diretório atual
    for diretorio, subdiretorios, arquivos in os.walk(diretorio_atual):
        # Verifica se há arquivos TXT neste diretório
        if any(arquivo.lower().endswith('.txt') for arquivo in arquivos):
            diretorio_txt = diretorio
            break

    # Verifica se o diretório foi encontrado
    if diretorio_txt:
        # Lista para armazenar os caminhos dos arquivos TXT
        caminhos_arquivos = []

        # Percorre os arquivos TXT no diretório
        for nome_arquivo in os.listdir(diretorio_txt):
            caminho_arquivo = os.path.join(diretorio_txt, nome_arquivo)

            # Verifica se é um arquivo TXT
            if os.path.isfile(caminho_arquivo) and nome_arquivo.endswith('.txt'):
                # Extrai o número do nome do arquivo usando uma expressão regular
                numero = re.findall(r'(\d+)\.txt$', nome_arquivo)
                if numero:
                    caminhos_arquivos.append((int(numero[0]), caminho_arquivo))

        # Ordena os caminhos dos arquivos com base no número extraído
        caminhos_arquivos.sort(key=lambda x: x[0])

    else:
        print('Nenhum diretório com arquivos TXT foi encontrado.')


    ocorrencias = 0

    for numero, caminho_arquivo_txt in caminhos_arquivos:
                
        with open(caminho_arquivo_txt, 'r', encoding='utf-8') as arquivo_txt:
            linhas = arquivo_txt.readlines()
            for i in range(len(linhas)):
                linha = linhas[i].strip()
                
                if linha.startswith('Question:'):
                    ocorrencias += 1
                    linha_atualizada = 'Question: {}'.format(ocorrencias)
                    linhas[i] = linha_atualizada + '\n'
                
                if linha.endswith('Case Study'):
                    ocorrencias += 1
                    linha_anterior = linhas[i - 1].strip()
                    linha_em_branco = 'Question: {}'.format(ocorrencias)

                    linhas[i - 1] = linha_em_branco + '\n'
                    linhas[i] = '\n' + linha
                    
            # Reescreve o arquivo com as alterações
            with open(caminho_arquivo_txt, 'w', encoding='utf-8') as arquivo_atualizado:
                arquivo_atualizado.writelines(linhas)

    print('Total de ocorrências:', ocorrencias)

    #---------------------------------------------------------------------------------------------

    # Obtém o diretório atual do script
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Cria o diretório 'PDF paginas' se não existir
    diretorio_paginas = os.path.join(diretorio_atual, 'PDF paginas')
    if not os.path.exists(diretorio_paginas):
        os.makedirs(diretorio_paginas)

    # Localiza o PDF no diretório atual
    pdf_nome = [arquivo for arquivo in os.listdir(diretorio_atual) if arquivo.endswith('.pdf')]

    if len(pdf_nome) > 0:
        pdf_nome = pdf_nome[0]  # Assume o primeiro PDF encontrado
        caminho_pdf = os.path.join(diretorio_atual, pdf_nome)

        # Abre o PDF
        documento = fitz.open(caminho_pdf)

        # Salva as páginas do PDF como arquivos PDF individuais no diretório 'PDF paginas'
        for num_pagina, pagina in enumerate(documento):
            novo_documento = fitz.open()
            novo_documento.insert_pdf(documento, from_page=num_pagina, to_page=num_pagina)
            nome_pagina = f'pagina_{num_pagina + 1}.pdf'  # Nome da página
            caminho_pagina = os.path.join(diretorio_paginas, nome_pagina)
            novo_documento.save(caminho_pagina)
            novo_documento.close()

            print(f'Página {nome_pagina} salva com sucesso!')

        documento.close()
    else:
        print('Nenhum arquivo PDF encontrado no diretório atual.')
        
    #-----------------------------------------------------------------------------------------

    # Obtém o diretório atual do script
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Nome do diretório a ser pesquisado
    diretorio_pesquisado = "PDF paginas"  # Substitua pelo nome do diretório que você está procurando

    # Caminho completo do diretório pesquisado
    caminho_pesquisado = os.path.join(diretorio_atual, diretorio_pesquisado)

    # Verifica se o diretório pesquisado existe
    if os.path.exists(caminho_pesquisado) and os.path.isdir(caminho_pesquisado):
        # Lista todos os arquivos no diretório pesquisado
        arquivos = os.listdir(caminho_pesquisado)

        # Conta o número de arquivos no diretório pesquisado
        num_arquivos = len(arquivos)

    #-------------------------------------------------------------------------------------

    # Nome dos diretórios a serem criados
    diretorios = ['imagens', 'documentos']

    # Obtém o caminho absoluto do diretório do script atual
    diretorio_script = os.path.dirname(os.path.abspath(__file__))

    # Percorre a lista de diretórios
    for diretorio in diretorios:
        # Caminho completo para o novo diretório
        caminho_diretorio = os.path.join(diretorio_script, diretorio)
        
        # Verifica se o diretório já existe
        if not os.path.exists(caminho_diretorio):
            # Cria o diretório
            os.makedirs(caminho_diretorio)

    #-------------------------------------------------------------------------------------

    imageIndex = 0
    documento = 1

    # Obtenha o diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construa o caminho completo para o diretório "PDF paginas"
    pdf_directory = os.path.join(script_dir, "PDF paginas")

    # Construa o caminho completo para o diretório "imagens"
    imagens_directory = os.path.join(script_dir, "imagens")

    # Verifique se o diretório "imagens" existe, caso contrário, crie-o
    if not os.path.exists(imagens_directory):
        os.makedirs(imagens_directory)

    for numero in range(num_arquivos):
        pdf_path = os.path.join(pdf_directory, f"pagina_{numero+1}.pdf")
        pdf = aw.Document(pdf_path)
        pdf.save(os.path.join("documentos", f"pdf{documento}.docx"))

        # Carregue a versão DOCX do PDF
        doc_path = os.path.join("documentos", f"pdf{documento}.docx")
        doc = aw.Document(doc_path)

        documento += 1

        # Recuperar todas as formas
        shapes = doc.get_child_nodes(aw.NodeType.SHAPE, True)

        # Loop através de formas
        for shape in shapes:
            shape = shape.as_shape()
            if shape.has_image:

                # Definir o nome do arquivo de imagem
                imageFileName = f"{imageIndex}{aw.FileFormatUtil.image_type_to_extension(shape.image_data.image_type)}"

                # Salvar a imagem no diretório "imagens"
                shape.image_data.save(os.path.join(imagens_directory, imageFileName))
                imageIndex += 1

    #----------------------------------------------------------------

    # Obtém o diretório atual do script
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # Diretório das imagens
    diretorio_imagens = os.path.join(diretorio_atual, 'imagens')  # Substitua pelo diretório correto

    # Altura e largura mínimas desejadas
    altura_minima = 50
    largura_minima = 50

    # Verifica se o diretório das imagens existe
    if os.path.exists(diretorio_imagens) and os.path.isdir(diretorio_imagens):
        # Lista todos os arquivos no diretório das imagens
        arquivos = os.listdir(diretorio_imagens)

        # Percorre cada arquivo no diretório das imagens
        for arquivo in arquivos:
            caminho_imagem = os.path.join(diretorio_imagens, arquivo)

            # Verifica se o arquivo é uma imagem
            if os.path.isfile(caminho_imagem) and arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # Abre a imagem usando a biblioteca PIL
                imagem = Image.open(caminho_imagem)

                # Obtém a altura e largura da imagem
                largura, altura = imagem.size

                imagem.close()

                # Verifica se a imagem atende aos requisitos mínimos
                if largura < largura_minima or altura < altura_minima:
                    os.remove(caminho_imagem)

                else:
                    print(f"A imagem '{arquivo}' atende aos requisitos mínimos.")
                
    else:
        print(f"O diretório '{diretorio_imagens}' não foi encontrado.")

    #------------------------------------------------------------------

    # Obtém o caminho absoluto do diretório do script atual
    diretorio_script = os.path.dirname(os.path.abspath(__file__))

    # Nome do diretório das imagens (localizado ao lado do script)
    nome_diretorio = 'imagens'

    # Caminho completo para o diretório das imagens
    diretorio = os.path.join(diretorio_script, nome_diretorio)

    # Caminho para a imagem de referência
    imagem_referencia = os.path.join(diretorio_script, "Image.ExportImages.0_.png")

    # Carrega a imagem de referência
    imagem_referencia = Image.open(imagem_referencia)

    # Percorre todas as imagens no diretório
    for nome_arquivo in os.listdir(diretorio):
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)
        
        # Verifica se o arquivo é uma imagem
        if os.path.isfile(caminho_arquivo) and nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Carrega a imagem do diretório
            imagem_diretorio = Image.open(caminho_arquivo)
            
            # Compara os pixels das duas imagens
            if imagem_diretorio.mode == imagem_referencia.mode and imagem_diretorio.size == imagem_referencia.size and list(imagem_diretorio.getdata()) == list(imagem_referencia.getdata()):
                # Exclui a imagem do diretório
                os.remove(caminho_arquivo)
                print(f"A imagem {nome_arquivo} foi excluída.")
            
    imagem_diretorio.close()
    imagem_referencia.close()

    #------------------------------------------------------------------------------------------

    def excluir_primeira_e_ultima_imagem(diretorio):
        # Obter a lista de arquivos no diretório
        arquivos = os.listdir(diretorio)

        # Verificar se há pelo menos duas imagens no diretório
        if len(arquivos) < 2:
            print("O diretório não contém pelo menos duas imagens.")
            return

        # Ordenar a lista de arquivos numericamente
        arquivos.sort(key=lambda x: int(x.split(".")[0]))

        # Excluir a primeira imagem
        caminho_primeira_imagem = os.path.join(diretorio, arquivos[0])
        os.remove(caminho_primeira_imagem)
        print(f"Imagem {arquivos[0]} excluída.")

        # Excluir a última imagem
        caminho_ultima_imagem = os.path.join(diretorio, arquivos[-1])
        os.remove(caminho_ultima_imagem)
        print(f"Imagem {arquivos[-1]} excluída.")

    # Diretório das imagens
    diretorio_imagens = "imagens"

    # Chamar a função para excluir a primeira e a última imagem
    excluir_primeira_e_ultima_imagem(diretorio_imagens)

    #------------------------------------------------------------------------------------------

    def extract_number(filename):
        match = re.search(r'_(\d+)\.txt$', filename)
        if match:
            return int(match.group(1))
        return -1


    def extract_image_number(filename):
        match = re.search(r'(\d+)\.\w+$', filename)
        if match:
            return int(match.group(1))
        return -1


    def combinar_diretorios():
        diretorio_atual = os.getcwd()

        diretorio_texto = None
        for diretorio in os.listdir(diretorio_atual):
            if os.path.isdir(os.path.join(diretorio_atual, diretorio)):
                arquivos = os.listdir(os.path.join(diretorio_atual, diretorio))
                if any(arquivo.endswith('.txt') for arquivo in arquivos):
                    diretorio_texto = os.path.join(diretorio_atual, diretorio)
                    break

        if diretorio_texto is None:
            print("Não foi possível encontrar o diretório com arquivos .txt.")
            return

        arquivos_txt = sorted([arquivo for arquivo in os.listdir(diretorio_texto) if arquivo.endswith('.txt')], key=extract_number)

        diretorio_imagens = os.path.join(diretorio_atual, 'imagens')
        arquivos_imagens = sorted([arquivo for arquivo in os.listdir(diretorio_imagens) if arquivo.endswith(('.jpeg', '.jpg', '.png'))], key=extract_image_number)

        pdf_path = os.path.join(diretorio_atual, f'{nome_sem_extensao}_editado.pdf')
        c = canvas.Canvas(pdf_path, pagesize=letter)

        margin = 20  # Margem esquerda
        y = 750  # Posição vertical inicial
        leading = 14  # Espaçamento entre linhas

        for arquivo_txt in arquivos_txt:
            arquivo_txt_path = os.path.join(diretorio_texto, arquivo_txt)
            c.setFont("Helvetica", 12)  # Define a fonte e o tamanho do texto

            with open(arquivo_txt_path, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
                for linha in linhas:
                    linha = linha.strip()
                    if y <= margin:
                        c.showPage()  # Cria uma nova página
                        y = 750  # Reinicia a posição vertical

                    if linha.startswith('<image:'):
                        if arquivos_imagens:
                            imagem_nome = arquivos_imagens.pop(0)
                            imagem_path = os.path.join(diretorio_imagens, imagem_nome)
                            if os.path.isfile(imagem_path):
                                imagem_width_scaled = 0
                                imagem_height_scaled = 0

                                # Abre a imagem usando a PIL
                                imagem = Image.open(imagem_path)

                                # Obtém as dimensões originais da imagem
                                imagem_width_original, imagem_height_original = imagem.size

                                # Define as condições com base nas medidas originais
                                if imagem_height_original <= 200:

                                    imagem_width_scaled = 570
                                    imagem_height_scaled = 144

                                elif imagem_height_original > 200 and imagem_height_original <= 340:

                                    imagem_width_scaled = 570
                                    imagem_height_scaled = 280

                                elif imagem_height_original > 340 and imagem_height_original < 700:
                                    imagem_width_scaled = 570
                                    imagem_height_scaled = 360
                                
                                elif imagem_height_original >= 700:
                                    imagem_width_scaled = 570
                                    imagem_height_scaled = 480


                                if y - imagem_height_scaled < margin:
                                    c.showPage()  # Cria uma nova página
                                    y = 750  # Reinicia a posição vertical

                                c.drawImage(imagem_path, margin, y - imagem_height_scaled,
                                            width=imagem_width_scaled, height=imagem_height_scaled, preserveAspectRatio=True)
                                y -= imagem_height_scaled + leading # Adiciona o espaçamento após a imagem
                    else:
                        c.drawString(margin, y, linha)
                        y -= leading

                        # Verifica se a próxima linha cabe na página atual
                        if y <= margin - 10:
                            c.showPage()  # Cria uma nova página
                            y = 750  # Reinicia a posição vertical

            c.showPage()
            y = 750  # Reinicia a posição vertical

        c.save()
        print(f"Arquivo PDF criado em: {pdf_path}")


    combinar_diretorios()

    imagem.close()

    #------------------------------------------------------------------------------------------
    
    # Obtém o diretório atual
    diretorio_atual = os.getcwd()

    # Verifica se o nome do diretório atual é "Editor de PDF"
    if os.path.basename(diretorio_atual) == "Editor de PDF":

        # Função para encontrar e excluir os diretórios
        def procurar_e_excluir_diretorios(diretorio):
            for root, dirs, files in os.walk(diretorio, topdown=False):
                for nome_dir in dirs:
                    caminho_dir = os.path.join(root, nome_dir)
                    shutil.rmtree(caminho_dir)
                    print(f"Diretório excluído: {caminho_dir}")

            print("Todos os diretórios foram excluídos.")

        # Chama a função para procurar e excluir os diretórios no diretório atual e em seus subdiretórios
        procurar_e_excluir_diretorios(diretorio_atual)

    else:
        print("O nome do diretório atual não é 'Editor de PDF'.")