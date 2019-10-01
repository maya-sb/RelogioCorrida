import datetime
import Geral

# Função que retorna a duração total da corrida para o item de Informações Gerais (1)
def horaInformacao(linhas_arq):
    hora = linhas_arq[0].split()
    inicio = int(hora[0])
    fim = int(hora[1])
    duracao = obterHora(fim) - obterHora(inicio)
    return duracao

def transformaMinutos(minutos):
    min = int(minutos)
    seg = int((minutos % 1) * 60)
    return min, seg

# Função que transforma o inteiro em timestamp para cálculos de data
def obterData(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp)
    return date

# Função que transforma o inteiro em timestamp para cálculos de horas
def obterHora(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp)
    return date

#Função que formata a data para impressão
def imprimirDataInicial(linhas_arq):
    dados = linhas_arq[0].split()
    inicio = obterData(int(dados[0]))

    data = inicio.strftime("%d/%m/%Y")
    return data

#Função que formata a hora para impressão
def imprimirHoraInicial(linhas_arq):
    dados = linhas_arq[0].split()
    inicio = obterHora(int(dados[0]))
    hora = inicio.strftime("%H:%M:%S")
    return hora

#Função que calcula a duração total entre registros
def obterDuracaoTotal(linhas_arq):
    times = Geral.obterTimestamp(linhas_arq)
    inicio = times[0]
    fim = times[-1]
    horaInicial = obterHora(int(inicio))
    horaFinal = obterHora(int(fim))
    tempo = horaFinal - horaInicial
    return tempo

#Função que converte duração para minutos
def ConverterDuracaoMinuto(duracao):
    duracao_seg = duracao.total_seconds()
    duracao_min = duracao_seg/60
    return duracao_min
