import Time
import Distancias

#Função que questiona o uso de pausa ou não
def considerarPausa():
    op3 = input("Deseja considerar pausas? [s/n]: ")
    print()
    if op3 == "S" or op3 == "s":
        return True
    elif op3 == "N" or op3 == "n":
        return False
    else:
        print("Opção inválida!")
        considerarPausa()

#Função que lê arquivo
def lerArquivo():
    arquivo = input("Por favor, digite o nome do arquivo de entrada: ")
    try:
        arq = open(arquivo, "r")
        linhas_arq = arq.readlines()
        return linhas_arq
    except:
        print("Este arquivo não existe.",end=" ")
        return lerArquivo()

#Função que exclui todos os registros entre as pausas
def lerArquivoPausa(linhas_arq):
    linhas_arq2 = []
    pausa = False
    for linha in linhas_arq:
        if linha[0] == "p" and len(linha)<3:
            pausa = True
        if pausa == False or linha[0]=="e":
            linhas_arq2.append(linha)
        if linha[0] == "r" and len(linha)<3:
            pausa = False
    return linhas_arq2

#Função que verifica a existência de laps
def verificaLap(linhas_arq):
    cont = 0
    for linha in linhas_arq:
        if linha[0] == "r":
            cont = 1
        if linha[0] == "#":
            cont = 0
        if linha[0] == "l" and cont == 0:
            return True
    return False

#Função que verifica a existência de pausas
def verificaPausa(linhas_arq):
    cont = 0
    for linha in linhas_arq:
        if linha[0] == "r":
            cont = 1
        if linha[0] == "#":
            cont = 0
        if linha[0] == "p" and cont == 0:
            return True
    return False

#Função que divide o arquivo em listas de laps
def dividirLap(linhas_arq):
    timestamp_inicial, timestamp_final = linhas_arq[0].split()
    lista_todos_laps = []
    lista_lap = []
    registro = False
    cont = 0
    lista_lap.append("l {}\n".format(str(timestamp_inicial)))
    for linha in linhas_arq[3:]:
        if linha[0] == "r":
            registro = True
        if linha[0] == "#":
            registro = False
        if linha[0] == "l" and registro == False:
            if cont!=0:
                lap = linha
                lista_lap.append(lap)
                lista_todos_laps.append(lista_lap)
                lista_lap = []
        lista_lap.append(linha)
        cont += 1
    lista_lap.append("l {}\n".format(str(timestamp_final)))
    lista_todos_laps.append(lista_lap)
    return lista_todos_laps

#Função que calcula a marcação de km
def calcularKM(linhas_arq):
    dis_total, lista_dis = Distancias.calculaDistancia(Distancias.obterAngulos(linhas_arq))
    soma_dis = lista_dis[0]
    ultima_dis = abs(1 - soma_dis)
    km = []
    posicoes = []

    for pos, x in enumerate(lista_dis[1:]):
        soma = soma_dis + x
        if ultima_dis < abs(1 - soma):
            km.append(soma_dis)
            posicoes.append(pos + 1)
            soma_dis = x
            ultima_dis = abs(1 - soma_dis)
        else:
            soma_dis += x
            ultima_dis = abs(1 - soma_dis)
    km.append(soma_dis)

    return posicoes

#Função que divide o arquivo em listas de km
def dividirKm(linhas_arq):
    posicoes = calcularKM(linhas_arq)
    timestamps = obterTimestamp(linhas_arq)
    time_km = []

    for x in posicoes:
        time_km.append(timestamps[x+1])

    lista_km = [linhas_arq[3]]
    lista_todos_km = []

    x = 0
    for linha in linhas_arq[3:]:
        if x == len(time_km):
            lista_km.append(linha)
        else:
            if linha[2:-1] != time_km[x]:
                lista_km.append(linha)
            else:
                ultimo = obterTimestamp(lista_km)[-1]
                lista_todos_km.append(lista_km)
                lista_km = []
                lista_km.append("r "+ultimo+"\n")
                if x < len(time_km)-1:
                    x += 1
                lista_km.append(linha)
    lista_todos_km.append(lista_km)
    return lista_todos_km

#Função que calcula a variação de altitude entre km
def variacaoAltitude(listas_todos_km):
    var_altitude = []
    var_status = []
    for pos, x in enumerate(listas_todos_km):
        atual = Distancias.obterAltitudes(x)[-1]
        if pos == 0:
            var_altitude.append(0)
            var_status.append("- - -")
        else:
            diferenca = atual - anterior
            var_altitude.append(diferenca)
            if diferenca < 0:
                var_status.append("diminuiu")
            elif diferenca > 0 :
                var_status.append("aumentou")
            else:
                var_status.append("- - -")
        anterior = atual
    return var_status, var_altitude

#Função que obtém as cadências de cada km
def obterCadenciasKM(lista_todos_km):
    inicial = 0
    lista_cadencias = []

    for x in lista_todos_km:
        final = Distancias.obterUltimoPasso(x)

        passos = final - inicial
        inicial = final

        duracao = Distancias.obterDuracao(x)
        duracao_min = Time.ConverterDuracaoMinuto(duracao)
        lista_cadencias.append(passos / duracao_min)
    return lista_cadencias

#Função que retorna a hora do registro do bpm
def horaBPM(lista_ts, lista_bpm, bpm):
    pos = lista_bpm.index(bpm)
    ts = int(lista_ts[pos])
    return Time.obterHora(ts).strftime("%H:%M")

#Função que obtém timestamps do registro
def obterTimestamp(linhas_arq):
    ts = []
    for linha in linhas_arq:
        if linha[0] == "r" and len(linha)>3:
            ts.append(linha[2:-1])
    return ts

#Função que calcula a duração do lap
def tempoLap(lista_lap):
    horaInicial = Time.obterHora(int(lista_lap[0][2:-1]))
    horaFinal = Time.obterHora(int(lista_lap[-1][2:-1]))
    tempo = horaFinal - horaInicial
    return tempo

#Função que calcula o ritmo do lap
def obterRitmoLap(x):
    distancia, lista_distancias = Distancias.calculaDistancia(Distancias.obterAngulos(x))
    duracao = tempoLap(x)
    duracao_min = Time.ConverterDuracaoMinuto(duracao)
    ritmo = duracao_min/distancia
    return ritmo

#Função que imprime informações gerais (Item 1)
def imprimirInfo(linhas_arq):
    print(8 * "-" + "Informações Gerais" + 8 * "-")
    print("Data da Corrida:", Time.imprimirDataInicial(linhas_arq))
    print("Horário:", Time.imprimirHoraInicial(linhas_arq))
    print("Duração:", Time.horaInformacao(linhas_arq))

#Função que imprime informações do resumo total(Item 2)
def imprimirResumoTotal(linhas_arq):
    distancia_total, lista_distancias = Distancias.calculaDistancia(Distancias.obterAngulos(linhas_arq))
    print(4 * "-" + "Resumo Total da Atividade" + 4 * "-")
    print("Distância Total: {:.4f}km".format(distancia_total))
    print("Tempo Total:",Distancias.obterDuracao(linhas_arq))
    print("Ritmo Médio: {:.2f} mins/km ".format(Distancias.obterRitmoMedio(linhas_arq)))
    try:
        lista_bpm = Distancias.obterBPM(linhas_arq)
        print("Média de BPM: {:.1f}".format(Distancias.calcularMediaBPM(linhas_arq)))
        print("BPM Máxima:",max(lista_bpm))
        print("BPM Mínimo:",min(lista_bpm))
    except Exception as e:
        #print(str(e))
        pass
    try:
        print("Cadência de Passos: {} passos/min".format(int(Distancias.obterCadencia(linhas_arq))))
    except:
        pass
    try:
        lista_altitude = Distancias.obterAltitudes(linhas_arq)
        print("Altitude Máxima: {:.2f}m".format(max(lista_altitude)))
        print("Altitude Mínima: {:.2f}m".format(min(lista_altitude)))
    except:
        pass

#Função que imprime informações dos km (Item 3)
def imprimirResumoKM(linhas_todos_km):
    cont = 0
    try:
        cadencias = obterCadenciasKM(linhas_todos_km)
    except:
        pass
    print(10 * "-" + "Resumo dos KM" + 10 * "-")
    for x in linhas_todos_km:
        cont +=1
        print(str(cont) +"º KM:")
        print("Tempo:", Distancias.obterDuracao(x))
        print("Ritmo: {:.2f} mins/km".format(Distancias.obterRitmoMedio(x)))
        try:
            print("Cadência de Passos: {} passos/min".format(int(cadencias[cont-1])))
        except:
            pass
        try:
            print("Média de BPM: {:.1f}".format(Distancias.calcularMediaBPM(x)))
        except:
            pass
        try:
            var_status, var_altitude = variacaoAltitude(linhas_todos_km)
            if var_status[cont-1] == "- - -":
                print("Altitude: {}".format(var_status[cont - 1]))
            else:
                print("Altitude: {} {:.2f}m".format(var_status[cont-1], abs(var_altitude[cont-1])))
        except:
            pass
        print()

#Função que imprime informações dos laps(Item 5)
def imprimirResumoLap(linhas_todos_laps):
    cont = 0
    print(9 * "-" + "Resumo dos Laps" + 9 * "-")
    for x in linhas_todos_laps:
        cont +=1
        lista_bpm = Distancias.obterBPM(x)
        lista_ts = obterTimestamp(x)
        print(str(cont) +"º Lap:")
        print("Tempo:",tempoLap(x))
        print("Ritmo: {:.2f} mins/km".format(obterRitmoLap(x)))
        try:
            maximo = max(lista_bpm)
            minimo = min(lista_bpm)
            print("BPM Máximo: {} às {}".format(maximo,horaBPM(lista_ts,lista_bpm,maximo)))
            print("BPM Mínimo: {} às {}".format(minimo,horaBPM(lista_ts,lista_bpm,minimo)))
            print("Média de BPM: {:.1f}".format(Distancias.calcularMediaBPM(x)))
        except:
            pass
        print()
