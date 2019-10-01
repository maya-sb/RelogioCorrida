from geopy import distance
import Time
import utm
import Geral

#Função que obtém as longitudes e latitudes do arquivo
def obterAngulos(linhas_arq):
    angulos = []
    registro = False
    pausa = False
    var = False
    for linha in linhas_arq:
        if linha[0] == "e":
            pausa = True
        if linha[0] == "i" or ((linha[0] =="p" or linha[0] == "r") and len(linha)<3):
            pausa = False
        if linha[0] == "r" and len(linha)>3:
            registro = True
        if registro == True and pausa == True:
            angulos.append(("-","-"))
            pausa = False
        if linha[0] == "l" and registro == True:
            latitude = float(linha[2:-1])
        if linha[0] == "n" and registro == True:
            longitude = float(linha[2:-1])
            angulos.append((latitude,longitude))
        if linha[0] == "#":
            registro = False
    return angulos

#Função que transforma as longitudes e latitudes do arquivo em coordenadas
def obterCoordenadas(linhas_arq):
    coord = []
    posicoes = Geral.calcularKM(linhas_arq)
    lista_latlon = obterAngulos(linhas_arq)

    for lat, lon in lista_latlon:
        la, lo, a, b = utm.from_latlon(lat, lon)
        coord.append((la, lo))
    return coord, posicoes

#Função que calcula a distância entre as longitudes e latitudes do arquivo
def calculaDistancia(lista_latlon):
    distancia_total = 0
    anterior = lista_latlon[0]
    pausa = False

    lista_distancias = []

    for atual in lista_latlon[1:]:
        if atual[0] == "-":
            pausa = True
        else:
            if pausa == False:
                dis = str(distance.distance(anterior,atual))
                lista_distancias.append(float(dis[:-2]))
                distancia_total = float(dis[:-2]) + distancia_total
            else:
                pausa = False
            anterior = atual

    return distancia_total, lista_distancias

#Função que calcula a duração total entre períodos escolhidos, podendo excluir pausas
def obterDuracao(linhas_arq):
    duracao_total = Time.obterDuracaoTotal(linhas_arq)
    antes = 0
    pausa = False

    for linha in linhas_arq:
        if linha[0] == "e" :
            if antes != 0 and pausa == True:
                depois = Time.obterHora(int(linha[2:-1]))
                tempo_pausa = depois - antes
                duracao_total = duracao_total - tempo_pausa
                antes = 0
            else:
                antes = Time.obterHora(int(linha[2:-1]))
            pausa = not pausa

        if linha[0] == "i" or linha[0] == "f" or ((linha[0] == "r" or linha[0] == "p") and len(linha)<3):
            pausa = not pausa

    return duracao_total

#Função que calcula a duração em segundos entre registros
def obterTempos(linhas_arq):
    tempos = []
    lista_ts = Geral.obterTimestamp(linhas_arq)
    anterior = Time.obterHora(int(lista_ts[0]))

    for linha in lista_ts:
        posterior = Time.obterHora(int(linha))
        duracao = posterior - anterior
        duracao = duracao.total_seconds()
        if duracao != 0:
            tempos.append(duracao)
        anterior = posterior
    return tempos

#Função que obtém os bpm's do arquivo
def obterBPM(linhas_arq):
    bpm = []
    for linha in linhas_arq:
        if linha[0] == "b":
            bpm.append(linha[2:-1])
    bpm = [int(x) for x in bpm]
    return bpm

#Função que calcula a média de bpm
def calcularMediaBPM(linhas_arq):
    lista_bpm = obterBPM(linhas_arq)
    lista = lista_bpm[1:]
    lista_tempos = obterTempos(linhas_arq)

    if lista_bpm == []:
        return Exception

    if len(lista_bpm) == 1:
        media = lista_bpm[0]
        return media
    else:
        media = 0
        for indice, bpm in enumerate(lista):
            media = media + bpm*lista_tempos[indice]
        media = media/sum(lista_tempos)
        return media

#Função que obtém as altitudes do arquivo
def obterAltitudes(linhas_arq):
    altitudes = []
    for linha in linhas_arq:
        if linha[0] == "a":
            altitudes.append(linha[2:-1])
    altitudes = [float(x) for x in altitudes]
    return altitudes

#Função que calcula o ritmo médio entre todos
def obterRitmoMedio(linhas_arq):
    distancia, lista = calculaDistancia(obterAngulos(linhas_arq))
    duracao = obterDuracao(linhas_arq)
    duracao_min = Time.ConverterDuracaoMinuto(duracao)
    ritmo = duracao_min/distancia
    return ritmo

#Função que obtém os ritmos do arquivo
def obterListaRitmo(linhas_arq):
    lista_ritmos = []
    distancia, lista_distancias = calculaDistancia(obterAngulos(linhas_arq))
    lista_duracao = obterTempos(linhas_arq)

    for x in range(len(lista_distancias)):
        if lista_distancias[x] == 0:
            ritmo = 0
        else:
            ritmo = (lista_duracao[x]/60)/lista_distancias[x]
        lista_ritmos.append(ritmo)
    return lista_ritmos

#Função que obtém o último registro de passo para futuros cálculos
def obterUltimoPasso(linhas_arq):
    reversa = list(reversed(linhas_arq))
    registro = False

    for linha in reversa:
        if linha[0] == "#":
            registro = True
        if linha[0] == "p" and registro == True:
            passos = int(linha[2:-1])
            break
        if linha[0] == "r":
            registro = False

    return passos

#Função que calcula a cadência da passos
def obterCadencia(linhas_arq):
    passos = obterUltimoPasso(linhas_arq)

    duracao = Time.obterDuracaoTotal(linhas_arq)
    duracao_min = Time.ConverterDuracaoMinuto(duracao)
    cadencia = passos / duracao_min

    return cadencia
