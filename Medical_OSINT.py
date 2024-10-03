import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import traceback
import time

ascii_art = """
 __  __          _ _           _    ___  ____ ___ _   _ _____ 
|  \/  | ___  __| (_) ___ __ _| |  / _ \/ ___|_ _| \ | |_   _|
| |\/| |/ _ \/ _` | |/ __/ _` | | | | | \___ \| ||  \| | | |  
| |  | |  __/ (_| | | (_| (_| | | | |_| |___) | || |\  | | |  
|_|  |_|\___|\__,_|_|\___\__,_|_|  \___/|____/___|_| \_| |_|  
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⣀⣀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣇⠸⣿⣿⠇⣸⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀
⠀⢀⣠⣴⣶⠿⠋⣩⡿⣿⡿⠻⣿⡇⢠⡄⢸⣿⠟⢿⣿⢿⣍⠙⠿⣶⣦⣄⡀⠀
⠀⠀⠉⠉⠁⠶⠟⠋⠀⠉⠀⢀⣈⣁⡈⢁⣈⣁⡀⠀⠉⠀⠙⠻⠶⠈⠉⠉⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⡿⠛⢀⡈⠛⢿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⣿⣦⣤⣈⠁⢠⣴⣿⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠻⢿⣿⣦⡉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⣦⣈⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⠦⠈⠙⠿⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣤⡈⠁⢤⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠷⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠑⢶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠁⢰⡆⠈⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⠈⣡⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

print(ascii_art)

# Inicializar o driver
driver = webdriver.Chrome() 

try:
    # Acesse o site
    driver.get('https://portal.cfm.org.br/busca-medicos')

    # Aguardar a presença do dropdown do estado
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'uf'))
    )

    # Perguntar qual estado o usuário deseja
    uf = input("Digite a sigla do estado em maiúsculo (ex: RJ): ").strip().upper()

    # Selecionar o estado
    select_element = Select(driver.find_element(By.ID, 'uf'))
    
    # Verificar se o valor existe
    options = [option.get_attribute('value') for option in select_element.options]
    if uf in options:
        select_element.select_by_value(uf)  # valor do estado
    else:
        print("O valor do estado não foi encontrado nas opções.")
        driver.quit()
        exit()

    # Aguardar a atualização do dropdown de municípios
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'municipio'))
    )

    # Perguntar qual município o usuário deseja
    municipio = input("Digite o nome do município: ").strip()

    # Selecionar o município
    select_municipio = Select(driver.find_element(By.ID, 'municipio'))

    # Verificar se o município existe nas opções
    municipios_options = [option.text for option in select_municipio.options]
    if municipio in municipios_options:
        select_municipio.select_by_visible_text(municipio)  # selecionar o município
    else:
        print("O município não foi encontrado nas opções.")
        driver.quit()
        exit()

    # Confirmar o botão
    button = driver.find_element(By.CLASS_NAME, 'btnPesquisar')
    driver.execute_script("arguments[0].click();", button)

    # Esperar até que o reCAPTCHA apareça
    print("Caso apareça reCAPTCHA, resolva-o e pressione Enter para continuar...")
    input("Pressione Enter após resolver o reCAPTCHA...")

    # Lista para armazenar os dados coletados
    todos_dados = []

    # Variável para rastrear o número da página atual
    pagina_atual = 1  # Começa em 1 para facilitar

    while True:
        # Aguardar carregamento da página e a presença dos cartões
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-body'))
        )

        # Coletar todos os cartões de médicos
        cards = driver.find_elements(By.CLASS_NAME, 'card-body')

        for card in cards:
            try:
                nome = card.find_element(By.TAG_NAME, 'h4').text
                crm = card.find_element(By.XPATH, ".//div[contains(b, 'CRM:')]").text
                data_inscricao = card.find_element(By.XPATH, ".//div[contains(b, 'Data de Inscrição:')]").text
                primeira_inscricao = card.find_element(By.XPATH, ".//div[contains(b, 'Primeira inscrição na UF:')]").text
                situacao = card.find_element(By.XPATH, ".//div[contains(b, 'Situação:')]").text
                especialidades = card.find_element(By.XPATH, ".//div[contains(b, 'Especialidades/Áreas de Atuação:')]").text
                endereco = card.find_element(By.XPATH, ".//div[contains(b, 'Endereço:')]").text
                
                # Verificação do telefone
                try:
                    telefone = card.find_element(By.XPATH, ".//div[contains(b, 'Telefone:')]").text
                except NoSuchElementException:
                    telefone = "Não disponível"

                # Montar o texto que será salvo
                dados_medico = [nome, crm, data_inscricao, primeira_inscricao, situacao, especialidades, endereco, telefone]
                todos_dados.append(dados_medico)

            except Exception as e:
                print(f"Ocorreu um erro ao coletar dados de um cartão: {e}")

        # Salvar dados coletados até agora em um arquivo CSV e TXT
        with open('dados_medicos.csv', 'a', newline='', encoding='utf-8') as csvfile, open('dados_medicos.txt', 'a', encoding='utf-8') as txtfile:
            writer = csv.writer(csvfile)
            if pagina_atual == 1:  # Escrever cabeçalho apenas na primeira página
                writer.writerow(['Nome', 'CRM', 'Data de Inscrição', 'Primeira Inscrição na UF', 'Situação', 'Especialidades', 'Endereço', 'Telefone'])
            writer.writerows(todos_dados)

            # Gravar os dados no arquivo de texto com 3 linhas em branco entre os grupos
            for dados in todos_dados:
                txtfile.write('\t'.join(dados) + '\n\n\n')  # 3 linhas em branco entre os dados

        # Limpar a lista para a próxima página
        todos_dados.clear()

        # Navegação pelas páginas
        try:
            pagination = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'paginationjs-pages'))
            )

            # Tentar encontrar o botão da próxima página
            proxima_pagina = pagination.find_element(By.XPATH, f"//li[@data-num='{pagina_atual + 1}']")

            # Se o botão da próxima página existir, clique
            if proxima_pagina:
                print(f"Navegando para a página {pagina_atual + 1}...")
                driver.execute_script("arguments[0].click();", proxima_pagina)
                time.sleep(2)  # Esperar a nova página carregar
                pagina_atual += 1  # Aumentar o número da página atual
            else:
                print("Nenhuma próxima página disponível.")
                break  # Se não houver próxima página, sai do loop

        except Exception as e:
            print(f"Ocorreu um erro ao tentar navegar para a próxima página: {e}")
            break  # Caso ocorra algum erro, sai do loop

    print(f"Total de dados coletados: {pagina_atual * len(todos_dados)}")
    print("Dados exportados para 'dados_medicos.csv' e 'dados_medicos.txt' com sucesso.")

except Exception as e:
    print("Ocorreu um erro:", e)
    traceback.print_exc()
finally:
    # Fechar o driver
    driver.quit()
                  
