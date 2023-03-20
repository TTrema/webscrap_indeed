from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class Indeed_result:
    def __init__(self, resultados_da_pesquisa:WebDriver):
        self.resultados_da_pesquisa = resultados_da_pesquisa
        self.resultados = self.caixa_de_resultados()

    def caixa_de_resultados(self):      
        return self.resultados_da_pesquisa.find_elements(By.CSS_SELECTOR, 'div[class*="cardOutline tapItem fs-unmask"]')

        
    
    def pull_box_attributes(self):
        collection = []
        for resultado in self.resultados:
            requisito = []
            descricao_do_trabalho = resultado.find_element(By.CSS_SELECTOR, 'span[id*="jobTitle"]').text
            requisitos = resultado.find_elements(By.CLASS_NAME, 'taxoAttribute')
            for item in requisitos:
                requisito.append(item.text)                                 
            empresa = resultado.find_element(By.CLASS_NAME, 'companyName').text
            try:
                link = resultado.find_element(By.CSS_SELECTOR, 'a[id*="job_"]')
                url = link.get_attribute('href')
            except NoSuchElementException:
                link = resultado.find_element(By.CSS_SELECTOR, 'a[id*="sj_"]')
                url = link.get_attribute('href')
            except:
                url = 'Não encontrado'

            if all(keyword not in descricao_do_trabalho.lower() for keyword in ["pleno", "sênior"]) and "python" in descricao_do_trabalho.lower():
                collection.append(
                    [descricao_do_trabalho, empresa, requisito, f'<a href="{url}" target="_blank">{url}</a>']
                )
        
        return collection