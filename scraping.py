# webdriver é o arquivo do navegador para simular
from selenium import webdriver

# localizador de elementos
from selenium.webdriver.common.by import By

# service para config path do executavel do chrome driver
from selenium.webdriver.chrome.service import Service

# class que permite executar ações avançadas (o mover do mouse, clique/array)
from selenium.webdriver.common.action_chains import ActionChains

# selenium action chains serve tanto par web scraping quanto teste automatizado
# nem todo site aceita, e o processo é demorado

# class q espera de forma explicita até q uma condition seja true (ex: elemento aparecer)
from selenium.webdriver.support.ui import WebDriverWait

# condicoes esperadas usadas com WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# para tratamento de exceção
from selenium.common.exceptions import TimeoutException

import pandas as pd

# uso funções de tempo
import time

# caminho ChromeDrver

    # >>> ATENÇÃO <<< : para economizar espaço, o chromedriver foi colocado em outra pasta padrão, SEMPRE AJUSTAR QUANDO NECESSÁRIO : >>> ATENÇÃO <<< 
chrome_driver_path = r"..\chromedriver.exe"

# config webdriver (simulador do navegador)
service = Service(chrome_driver_path) # control navegador pelo selenium
options = webdriver.ChromeOptions() # config opções do navegador
# exemplo: Não aparecer na tela a interface acontecendo
# options.add_argument("--headless")
options.add_argument('--disable-gpu') # evitar erros graficos
options.add_argument('--window_size=1920,1080') # define tamanho de tela fixo

# inicialização do webdriver
driver = webdriver.Chrome(service=service, options=options) # o segundo 'service' e 'options' são as variaveis declaradas previamente

# define URL inicial (qual vai ser a primeira url)
url_base = 'https://www.kabum.com.br/hardware/placa-de-video-vga?page_number=1'
driver.get(url_base)

# delay de espera
    # poderia fazer com assincrona
time.sleep(5)

# dicionario vazio para armazenar os dados
dic_produtos = {'nome':[], 'preco':[], 'frete_gratis': []}

# contador de páginas
pagina = 1

while True:
    print(f'\nEscaneando Página {pagina}')

    try:
        # espera condição ser satisfeita
            # espera o driver até pegar os dados SE não pegar em 10 segundos ele passa para o próximo
        WebDriverWait(driver,10).until(

            # verif se todos elementos 'productCard' estão acessíveis
            ec.presence_of_all_elements_located((By.CLASS_NAME, 'productCard'))

        )
        print('Elementos encontrados com sucesso!')
    except TimeoutException:
        print('Tempo de espera excedido!')
    
    produtos = driver.find_elements(By.CLASS_NAME, 'productCard')

    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME, 'nameCard').text.strip()
            preco = produto.find_element(By.CLASS_NAME, 'priceCard').text.strip()

            try:
                produto.find_element(By.CLASS_NAME, 'IconTruck')
                frete_gratis = True
            except:
                frete_gratis = False

            print(f'{nome} - {preco} - {frete_gratis}')

            dic_produtos['nome'].append(nome)
            dic_produtos['preco'].append(preco)
            dic_produtos['frete_gratis'].append(frete_gratis)

        except Exception:
            print('Não foi possível coletar dados: ', Exception)
            
    # encontrar acesso/botão da proxima pagina
    try:
        btn_proximo = WebDriverWait(driver,10).until(
            ec.element_to_be_clickable((By.CLASS_NAME, 'nextLink')) # encontra elemento para clicar com o nome de classe respectivo
        )
        if btn_proximo:
            # simulação de clicar e scrollar para achar btn prox page
                # execute_script da controle ao Selenium
            driver.execute_script('arguments[0].scrollIntoView();', btn_proximo)

            # clicar no elemento
            driver.execute_script('arguments[0].click();', btn_proximo)
            pagina += 1
            print(f'Indo para a página {pagina}')
            time.sleep(5)
        else:
            print('Você chegou na última página')
            break

    except Exception as e:
        print('Não foi possível avançar para a próxima página', e)
        break

# fechar navegador
driver.quit()

# dataframe
df = pd.DataFrame(dic_produtos)

# salvar dados em excel
df.to_excel('webscraping.xlsx', index=False)

print(f'Arquivo salvo com sucesso! ({len(df)}) produtos capturados!')

























