from indeed.indeed import Indeed

try:
    with Indeed() as bot:
        pesquisa = input("Qual palavra deseja pesquisar? ")
        qtd_paginas = int(input("Quantas páginas deseja incluir na pesquisa? "))
        excluir = input("Quais palavras(separadas por vírgula) deseja excluir da pesquisa? ").lower()
        excluir = [x.strip() for x in excluir.split(",")]
        bot.pagina_inicial()
        bot.procurar_trabalho(pesquisa=pesquisa)
        bot.postado_hoje()
        bot.info_trabalho(excluir=excluir, pesquisa=pesquisa, qtd_paginas=qtd_paginas)

except Exception as e:
    raise
