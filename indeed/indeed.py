import html
from datetime import datetime

import selenium.common.exceptions
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from indeed.indeed_result import Indeed_result


class Indeed(webdriver.Chrome):
    def __init__(self, teardwon=False):
        self.teardown = teardwon
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("detach", True)

        super(Indeed, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def pagina_inicial(self):
        self.get("https://br.indeed.com/")

    def procurar_trabalho(self, pesquisa):
        search_field = self.find_element(By.ID, "text-input-what")
        search_field.clear()
        search_field.send_keys(pesquisa)
        search_field.send_keys(Keys.RETURN)

    def postado_hoje(self):
        data = self.find_element(By.ID, "filter-dateposted")
        data.click()
        try:
            hoje = self.find_element(By.XPATH, "//a[normalize-space()='Últimas 24 horas']")
            hoje.click()

        except:
            try:
                hoje = self.find_element(By.ID, "filter-dateposted-0")
                hoje.click()
                hoje.send_keys(Keys.RETURN)

            except:
                print("Nenhum método de filtro encontrado")

    def info_trabalho(self, excluir=None, pesquisa=None, qtd_paginas=1):
        table = PrettyTable(field_names=["Descrição do Trabalho", "Empresa", "Requisitos", "Link"])

        for pagina in range(qtd_paginas):
            resultados_da_pesquisa = self.find_element(By.ID, "mosaic-jobResults")
            resultado = Indeed_result(resultados_da_pesquisa)

            table.add_rows(resultado.pull_box_attributes(excluir, pesquisa))

            if pagina + 1 < qtd_paginas:
                try:
                    next_page_link = self.find_element(By.LINK_TEXT, str(pagina + 2))
                    self.execute_script("arguments[0].scrollIntoView();", next_page_link)
                    next_page_link.click()
                except selenium.common.exceptions.ElementClickInterceptedException as e:
                    try:
                        close_button = self.find_element(By.XPATH, "//button[@aria-label='fechar']")
                        close_button.click()
                    except:
                        print("NÃO achou o que fechar")
                        pass
                    next_page_link.click()
            else:
                continue

        print(table)

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        htmlCode = table.get_html_string(format=True)
        htmlCode = html.unescape(htmlCode)
        with open("indeed.html", "w") as f:
            f.write(htmlCode)
