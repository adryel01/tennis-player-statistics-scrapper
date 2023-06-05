from scrapingTableMatches import results 
from scrapingTableMatches import results_id
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from bs4 import BeautifulSoup

index = 29

# Primeiro elemento da lista de resultados
name = results[index]
jogador_id = results_id[index]
list_dicts = []
new_list = []

jogador_dict = {'jogador_id': jogador_id}


options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
options.add_argument("--headless")  # Executar em modo headless, sem abrir o navegador na tela
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(chrome_options=options, executable_path="/src/chromedriver.exe")

# Acesso ao site
driver.get("https://www.ultimatetennisstatistics.com/topMatchStats/")

# Preenchimento do campo de entrada e clique no botão de pesquisa
player_input = driver.find_element(By.ID, "player")
player_input.click()
player_input.send_keys(name)

sleep(3)

action = ActionChains(driver)
action.move_to_element(player_input).move_by_offset(0, 20).click().perform()

sleep(3)

age_header = driver.find_element(By.XPATH, "//th[contains(text(), 'Age')]")
age_row = age_header.find_element(By.XPATH, "./ancestor::tr")
age_data = age_row.find_element(By.TAG_NAME, "td").text
age_data = age_data[:2]


height_header = driver.find_element(By.XPATH, "//th[contains(text(), 'Height')]")
height_row = height_header.find_element(By.XPATH, "./ancestor::tr")
height_data = height_row.find_element(By.TAG_NAME, "td").text
height_data = height_data[:3]


player_info = { 'age': int(age_data), 'height': int(height_data)}



# print(player_info)

stats_link = driver.find_element(By.XPATH, '//*[@id="playerPills"]/li[9]')
stats_link.click()

sleep(2)

action = ActionChains(driver)
action.move_to_element(stats_link).move_by_offset(0, 30).click().perform()

sleep(4)

html = driver.page_source

# Criar o objeto BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Encontrar a tag com id 'statisticsOverview'
statistics_overview = soup.find(id='statisticsOverview')

# Verificar se foi encontrada alguma tag 'table' dentro de 'statisticsOverview'

if statistics_overview:
    tables = statistics_overview.find_all('table')
    
    # Iterar sobre as tabelas encontradas
    for table in tables:
        # Aqui você pode fazer o que desejar com cada tabela encontrada
        # Por exemplo, imprimir o conteúdo da tabela
        tbodies = table.find_all('tbody')
        
        
        # Iterar sobre as tags 'tbody'
        for tbody in tbodies:
            # Encontrar todas as tags 'td' dentro da tag 'tbody'
            tds = tbody.find_all('td')
            ths = tbody.find_all('th', class_='pct-data')
            
            # Extrair o texto de cada tag 'td'
            values_td = [td.text for td in tds]
            values_th = [th.text.strip() for th in ths]
            
            # Faça o que desejar com os valores extraídos
            # print(values_td)
            # print(values_th)
            
            player_dict = dict(zip(values_td, values_th))
            list_dicts.append(player_dict)
            
            # Faça o que desejar com o dicionário resultante
            # print(player_dict)
    # print(list_dicts)
    
    stats_dict = dict()
    for dictionary in list_dicts:
        stats_dict.update(dictionary)
    
    for key, value in stats_dict.items():
        if "%" in value:
            value = value.replace("%", "")  # Remover o símbolo de porcentagem
            value = float(value)  # Converter para float
            stats_dict[key] = value

    # print(stats_dict)
    new_list.append(stats_dict)
else:
    print("Nenhuma tag com id 'statisticsOverview' encontrada.")
    
new_list.append(jogador_dict)
new_list.append(player_info)
    
combined_dict = dict()
for dictionary in new_list:
    combined_dict.update(dictionary)

print()
print(combined_dict)
print()
# Fechamento do webdriver
driver.quit()
