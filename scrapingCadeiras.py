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
chrome_driver_path = r"C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe"

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
url_base = 'https://www.kabum.com.br/espaco-gamer/cadeiras-gamer'
driver.get(url_base)

# delay de espera
    # poderia fazer com assincrona
time.sleep(5)

# dicionario vazio para armazenar marcas e precos das cadeiras
dic_produtos = {'marca':[], 'preco':[]}

# contador de páginas
pagina = 1

while True:
    print(f'\nEscaneando Página {pagina}')

    try:
        # espera condição ser satisfeita
            # espera o driver até pegar os dados SE não pegar em 10 segundos ele passa para o próximo
        WebDriverWait(driver,10).until(

            # verif se todos elementos 'productCard' estão acessíveis
            ec.presence_of_all_elements_located(By.CLASS_NAME, 'productCard')

        )
        print('Elementos encontrados com sucesso!')
    except TimeoutException:
        print('Tempo de espera excedido!')
    
    produtos = driver.find_elements(By.CLASS_NAME,'productCard')

    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME, 'nameCard').text.strip()
            preco = produto.find_element(By.CLASS_NAME, 'priceCard').text.strip()

            print(f'{nome} - {preco}')

            dic_produtos['marca'].append(nome)
            dic_produtos['preco'].append(preco)

        except Exception:
            print('Não foi possível coletar dados: ', Exception)
            
    # encontrar acesso aw proxima pagina

    # fechar navegador

    # dataframe

    # salvar dados em csv()


























