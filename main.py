from indeed.indeed import Indeed
import time

try:
    with Indeed() as bot:
        bot.pagina_inicial()
        bot.procurar_trabalho('Python')
        bot.postado_hoje()
        bot.info_trabalho(qtd_paginas=4)
        # bot.proxima_pagina()
        # bot.info_trabalho()
except Exception as e:
    raise

