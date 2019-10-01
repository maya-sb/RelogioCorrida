import Geral
import Distancias
import Graficos

op = ""
op2 = ""

linhas_arq = Geral.lerArquivo()
while linhas_arq == []:
    print("O arquivo está vazio.",end=" ")
    linhas_arq = Geral.lerArquivo()
linhas_arq2 = Geral.lerArquivoPausa(linhas_arq)

while(op!="6"):
    print()
    print(15 * "-" + "MENU" + 15 * "-")
    print("[1] - Informações Gerais")
    print("[2] - Resumo Total da Atividade ")
    print("[3] - Resumo da Atividade (por Km)")
    print("[4] - Resumo dos Laps")
    print("[5] - Gráficos")
    print("[6] - Sair")
    print(34 * "-")
    op = input("Digite uma opção: ")
    print()

    if op == "1":
        Geral.imprimirInfo(linhas_arq)
    elif op == "2":
        if Geral.verificaPausa(linhas_arq):
            if Geral.considerarPausa():
                Geral.imprimirResumoTotal(linhas_arq2)
            else:
                Geral.imprimirResumoTotal(linhas_arq)
        else:
            Geral.imprimirResumoTotal(linhas_arq)
    elif op == "3":
        if Geral.verificaPausa(linhas_arq):
            if Geral.considerarPausa():
                Geral.imprimirResumoKM(Geral.dividirKm(linhas_arq2))
            else:
                Geral.imprimirResumoKM(Geral.dividirKm(linhas_arq))
        else:
            Geral.imprimirResumoKM(Geral.dividirKm(linhas_arq))
    elif op == "4":
        if Geral.verificaLap(linhas_arq):
            listas_todos_laps = Geral.dividirLap(linhas_arq)
            Geral.imprimirResumoLap(listas_todos_laps)
        else:
            print("O arquivo não possui laps!")
    elif op == "5":
        try:
            Graficos.GraficoSobreposicao(linhas_arq)
        except Exception as e:
            exit()
    elif op == "6":
        print("O programa foi finalizado :)")
    else:
        print("Opção Inválida. Digite Novamente.")
