import turtle
import Time
import Distancias

#Função que desenha gráfico de percurso
def GraficoPercurso(linhas_arq):
    coord, posicoes = Distancias.obterCoordenadas(linhas_arq)

    coordX = []
    coordY = []

    for x,y in coord:
        coordX.append(x/5)
        coordY.append(y/5)

    coordX = transladarPontos(coordX,max(coordX))
    coordY = transladarPontos(coordY,max(coordY))

    turtle.screensize(max(coordX)+50,max(coordY)+50)
    turtle.title("Percurso")
    Yeojin = turtle.Turtle()

    Yeojin.color("#FF4500")
    Yeojin.write("Início", font=("Arial",9,"normal"))
    Yeojin.color("#4B0082")
    Yeojin.shape("circle")
    Yeojin.shapesize(0.3)
    Yeojin.hideturtle()
    Yeojin.penup()
    Yeojin.goto(coordX[0],coordY[0])
    Yeojin.pendown()

    for x in range(len(coordX)-1):
        Yeojin.goto(coordX[x],coordY[x])
        if x in posicoes:
            Yeojin.color("#FF4500")
            Yeojin.stamp()
            Yeojin.color("#4B0082")

    Yeojin.write("Fim", font=("Arial", 9, "normal"))
    #turtle.done()

#Função que soma as durações para formar gráfico
def calculaTempo(tempo):
    novo_tempo = []
    soma = 0
    for x in tempo:
        soma = soma + x
        novo_tempo.append(soma)
    return novo_tempo

#Função que translada pontos
def transladarPontos(lista, tamanho):
    novos_pontos = []
    novo_ponto = 0
    for x in lista:
        novo_ponto = x - (tamanho - 20)
        novos_pontos.append(novo_ponto)
    return novos_pontos

#Função que numero eixo
def numerarEixoX(tempo, lista):
    KimLip = turtle.Turtle()
    KimLip.hideturtle()
    KimLip.speed(100)
    KimLip.penup()
    KimLip.goto(lista[0],-20)

    minutos = [abs(x/60) for x in tempo]

    maior = lista.index(lista[-1])
    maior = int(maior)
    k =(maior)/5
    for x in range(0, maior, int(k)):
        KimLip.goto(lista[x],-20)
        min, seg = Time.transformaMinutos(minutos[x])
        KimLip.write(str("{:.2f}".format(minutos[x])), font=("Arial", 8, "normal"))
        #KimLip.write(str("{}:{}".format(min,seg)), font=("Arial", 8, "normal"))

    KimLip.goto(maior, -20)
    min, seg = Time.transformaMinutos(minutos[-1])
    KimLip.write(str("{:.2f}".format(minutos[-1])), font=("Arial", 8, "normal"))
    #KimLip.write(str("{}:{}".format(min, seg)), font=("Arial", 8, "normal"))

#Função que numero eixo
def numerarEixoY(lst,lista1):
    Yves = turtle.Turtle()
    Yves.hideturtle()
    Yves.speed(100)
    Yves.penup()
    Yves.goto(lista1[0] - 25,0)
    Yves.left(90)

    maior = int(max(lst))
    k = (maior + 50 )/5

    for x in range(0,maior,int(k)):
        Yves.goto(lista1[0]-25,x)
        Yves.write(str(x), font=("Arial", 8, "normal"))
    Yves.goto(lista1[0]-25,maior)
    Yves.write(str(maior), font=("Arial", 8, "normal"))

#Função que numero eixo
def numerarEixoYZonas(bpm,lista,k):
    Choery = turtle.Turtle()
    Choery.hideturtle()
    Choery.speed(100)
    Choery.penup()
    Choery.goto(lista[0]-25,104-20)
    Choery.left(90)

    for x in range(len(bpm)):
        Choery.write(bpm[x],font=("Arial",8,"normal"))
        Choery.fd(k)

#Função que desenha eixos
def desenharEixo(lst,lista,y,x):
    JinSoul = turtle.Turtle()
    JinSoul.pensize(2)
    JinSoul.speed(100)

    Vivi = turtle.Turtle()
    Vivi.pensize(2)
    Vivi.speed(100)

    JinSoul.penup()
    JinSoul.setx(lista[0])
    JinSoul.pendown()
    JinSoul.goto(max(lista)+50,0)
    JinSoul.stamp()
    JinSoul.penup()
    JinSoul.hideturtle()
    JinSoul.right(90)
    JinSoul.fd(25)
    JinSoul.write(x, font=("Arial",8,"normal"))

    Vivi.penup()
    Vivi.setx(lista[0])
    Vivi.left(90)
    Vivi.pendown()
    Vivi.fd(max(lst)+50)
    Vivi.stamp()
    Vivi.penup()
    Vivi.hideturtle()
    Vivi.left(90)
    Vivi.fd(45)
    Vivi.left(90)
    Vivi.fd(15)
    Vivi.write(y, font=("Arial", 8, "normal"))

# Função que desenha as zonas
def retangulo(turtle, tempo, size2):
    tempo = [(x/3) for x in tempo]
    turtle.begin_fill()
    turtle.fd(tempo[-1])
    turtle.left(90)
    turtle.fd(size2)
    turtle.left(90)
    turtle.fd(tempo[-1])
    turtle.left(90)
    turtle.fd(size2)
    turtle.end_fill()

# Função que desenha gráfico de zonas
def GraficoZonas(lista, tempo,tempo_sem_transladar):
    zonas = ["104","114","133","152","172","190"]

    turtle.screensize(max(tempo) + 50, max(lista) + 50)
    turtle.title('Zonas de BPM')

    GoWon = turtle.Turtle()
    GoWon.color()
    GoWon.hideturtle()
    GoWon.pensize(2)
    GoWon.shapesize(5)
    GoWon.penup()
    GoWon.goto(-447, -50)
    GoWon.write("Zonas de BPM:", font = ("Times New Roman", 15, "bold"))

    maxi = turtle.Turtle()
    maxi.hideturtle()
    maxi.color("#E43E3E")
    maxi.speed(100)
    maxi.penup()
    maxi.goto(tempo[0], 171)
    maxi.pendown()
    retangulo(maxi, tempo_sem_transladar, 19)
    maxi.penup()
    maxi.goto(-447 ,-100)
    maxi.write('Máxima', font=('Times New Roman', 20, "bold"))

    inten = turtle.Turtle()
    inten.hideturtle()
    inten.color("#EEB543")
    inten.speed(100)
    inten.penup()
    inten.goto(tempo[0], 152)
    inten.pendown()
    retangulo(inten,  tempo_sem_transladar, 20)
    inten.penup()
    inten.goto(-447, -150)
    inten.write('Intensa', font=('Times New Roman', 20, "bold"))

    mod = turtle.Turtle()
    mod.hideturtle()
    mod.color("#4FEE43")
    mod.speed(100)
    mod.penup()
    mod.goto(tempo[0], 133)
    mod.pendown()
    retangulo(mod,  tempo_sem_transladar, 19)
    mod.penup()
    mod.goto(-447, -200)
    mod.write('Moderada', font=('Times New Roman', 20, "bold"))

    leve = turtle.Turtle()
    leve.hideturtle()
    leve.color("#43BAEE")
    leve.speed(100)
    leve.penup()
    leve.goto(tempo[0], 114)
    leve.pendown()
    retangulo(leve,  tempo_sem_transladar, 19)
    leve.penup()
    leve.goto(-247, -100)
    leve.write('Leve', font=('Times New Roman', 20, "bold"))

    mtL = turtle.Turtle()
    mtL.hideturtle()
    mtL.color("#535758")
    mtL.speed(100)
    mtL.penup()
    mtL.goto(tempo[0], 104)
    mtL.pendown()
    retangulo(mtL,  tempo_sem_transladar, 10)
    mtL.penup()
    mtL.goto(-247, -150)
    mtL.write('Muito Leve', font=('Times New Roman', 20, "bold"))

    desenharEixo(lista,tempo, "BPM","Tempo")
    numerarEixoYZonas(zonas,tempo,20)
    numerarEixoX(tempo_sem_transladar,tempo)

    GoWon.goto(tempo[0], lista[0])
    GoWon.pendown()

    for x in range(len(lista) - 1):
        GoWon.goto(tempo[x], lista[x])

    turtle.done()

# Função que desenha gráfico de ritmo, altitude e bpm
def Grafico(lista,tempo,cor):
    lista = [int(x) for x in lista]

    HyunJin = turtle.Turtle()
    HyunJin.color(cor)
    HyunJin.hideturtle()
    HyunJin.pensize(2)
    HyunJin.penup()

    HyunJin.goto(tempo[0], lista[0])
    HyunJin.pendown()

    for x in range(len(lista) - 1):
        HyunJin.goto(tempo[x], lista[x])

# Função que chama os gráficos
def GraficoSobreposicao(linhas_arq):
    tempo = calculaTempo(Distancias.obterTempos(linhas_arq))
    lst = []

    try:
        bpm = Distancias.obterBPM(linhas_arq)
        b = "b - BPM"
        z = "z - Zonas de BPM"
        lst.append(max(bpm))
    except:
        b = ""
        z = ""

    try:
        alt = Distancias.obterAltitudes(linhas_arq)
        a = "a - Altitude"
        lst.append(max(alt))
    except:
        a = ""

    rit = Distancias.obterListaRitmo(linhas_arq)

    tempo_sem_transladar = tempo
    tempo = [x/3 for x in tempo]
    tempo = transladarPontos(tempo,500-20)

    Chuu = turtle.Turtle()
    Chuu.penup()
    Chuu.hideturtle()
    Chuu.goto(tempo[0],-40)

    lst.append(max(rit))

    global tela
    tela = turtle.Screen()
    turtle.screensize(max(tempo) + 50, max(lst) + 1000)

    op = tela.textinput("Gráficos","Quais gráficos deseja visualizar?\n\np - Percurso\n{}\n\nOu combine:\n{}\n{}\nr - Ritmo\n\n".format(z,a,b))

    while op != None:
        if op == "z":
            GraficoZonas(bpm,tempo,tempo_sem_transladar)
        if op == "p":
            GraficoPercurso(linhas_arq)
        if "b" in op or "a" in op or "r" in op:
            Chuu.write("Legenda:", font=("Arial", 9, "normal"))

            desenharEixo(lst, tempo, "", "Tempo")
            numerarEixoX(tempo_sem_transladar, tempo)
            numerarEixoY(lst, tempo)

            if "b" in op:
                Chuu.color("red")
                Chuu.goto(tempo[0], -80)
                Chuu.write("BPM", font=("Arial", 10, "normal"))
                Grafico(bpm,tempo,"red")

            if "a" in op:
                Chuu.color("#006400")
                Chuu.goto(tempo[0], -120)
                Chuu.write("Altitude", font=("Arial", 10, "normal"))
                Grafico(alt,tempo,"#006400")

            if "r" in op:
                Chuu.color("purple")
                Chuu.goto(tempo[0], -160)
                Chuu.write("Ritmo", font=("Arial", 10, "normal"))
                Grafico(rit,tempo,"purple")

        else:
            erro = "Opção Inválida.\n"
            op = tela.textinput("Gráficos",
                                "{}Quais gráficos deseja visualizar?\n\np - Percurso\n{}\n\nOu combine:\n{}\n{}\nr - Ritmo\n\n".format(
                                    erro,z, a, b))

        if op!=None:
            tela.clear()
            tela.onkey(GraficoSobreposicao(linhas_arq), "Up")
            tela.listen()
        else:
            exit()

    turtle.done()
