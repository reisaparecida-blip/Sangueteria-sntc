import pygame
import sys
import math
import random
import os

pygame.init()

# ============================================================
# JANELA
# ============================================================
LARGURA, ALTURA = 800, 600

try:
    tela = pygame.display.set_mode(
        (LARGURA, ALTURA),
        pygame.FULLSCREEN | pygame.SCALED
    )
except pygame.error:
    tela = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption("Sangueteria")
clock = pygame.time.Clock()

# ============================================================
# CORES
# ============================================================
FUNDO=(35,20,45); ROXO=(105,55,145); ROXO2=(70,35,90)
ROSA=(255,105,175); ROSA2=(255,175,215); BRANCO=(255,255,255)
AMARELO=(255,220,100); VERDE=(90,235,150); AZUL=(85,190,255)
VERMELHO=(235,70,105); MARROM=(130,75,55); CREME=(250,225,190)
CINZA=(175,175,185); PRETO=(20,12,28); LARANJA=(255,155,70)

titulo=pygame.font.Font(None,64)
grande=pygame.font.Font(None,42)
fonte=pygame.font.Font(None,30)
pequena=pygame.font.Font(None,21)

# ============================================================
# IMAGENS
# SOMENTE AS CIENTISTAS
# ============================================================
PASTA_IMAGENS=os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "imagens"
)

def carregar_imagem(nome):
    caminho=os.path.join(PASTA_IMAGENS,nome)
    try:
        if os.path.exists(caminho):
            return pygame.image.load(caminho).convert_alpha()
    except pygame.error:
        pass
    return None

CAMINHOS_CIENTISTAS={
    "radio":"Marie cury.png",
    "dna":"Rosalind Franklin.png",
    "espaco":"Katherine Johnson.png",
    "codigo":"Ada lovelace.png",
}

IMAGENS_CIENTISTAS={
    tipo:carregar_imagem(nome)
    for tipo,nome in CAMINHOS_CIENTISTAS.items()
}

# ============================================================
# RECEITAS
# ============================================================
receitas=[
    {
        "nome":"Radio-Glow Shake",
        "cientista":"Marie Curie",
        "tipo":"radio",
        "cor":VERDE,
        "ingredientes":[
            ("Isotopo de Radio-Glow",1),
            ("Baga Eletrica de Pantano",2),
            ("Essencia de Radiacao Fashion",1)
        ],
        "processos":["blender","decorar"],
        "quiz":[
            {
                "pergunta":"Marie Curie foi pioneira em estudos sobre o que?",
                "opcoes":["Radioatividade","Culinaria","Astronomia"],
                "correta":0,
                "explicacao":"Marie Curie descobriu elementos radioativos como o Polonio e o Radio!"
            },
            {
                "pergunta":"Quantos Premios Nobel Marie Curie ganhou, em areas diferentes?",
                "opcoes":["Nenhum","Um","Dois"],
                "correta":2,
                "explicacao":"Ela foi a primeira pessoa da historia a ganhar Nobel em duas areas: Fisica e Quimica!"
            },
            {
                "pergunta":"Marie Curie foi a primeira mulher a conquistar o que?",
                "opcoes":["Um Premio Nobel","Pilotar um aviao","Ser prefeita"],
                "correta":0,
                "explicacao":"Ela foi a primeira mulher da historia a ganhar um Premio Nobel, em 1903."
            },
            {
                "pergunta":"Qual elemento quimico tem o nome inspirado no pais natal de Marie Curie?",
                "opcoes":["Polonio","Francio","Germanio"],
                "correta":0,
                "explicacao":"O Polonio foi batizado em homenagem a Polonia, terra natal de Marie Curie."
            }
        ]
    },
    {
        "nome":"Bio-Spooky",
        "cientista":"Rosalind Franklin",
        "tipo":"dna",
        "cor":(190,100,255),
        "ingredientes":[
            ("Extrato de Planta Trepadeira Mutante",1),
            ("Soro de Raio-X Fotografico",1),
            ("Essencia de Estilo Genetico",2)
        ],
        "processos":["blender","decorar"],
        "quiz":[
            {
                "pergunta":"O trabalho de Rosalind Franklin ajudou a descobrir o formato de qual molecula?",
                "opcoes":["DNA","Agua","Sal de cozinha"],
                "correta":0,
                "explicacao":"As imagens de Rosalind Franklin foram essenciais para revelar o formato do DNA."
            },
            {
                "pergunta":"Rosalind Franklin usava qual tecnica para 'fotografar' moleculas minusculas?",
                "opcoes":["Difracao de raios-X","Pintura a oleo","Microscopio de brinquedo"],
                "correta":0,
                "explicacao":"Ela usava difracao de raios-X para revelar estruturas invisiveis a olho nu."
            },
            {
                "pergunta":"O DNA tem o formato de uma...?",
                "opcoes":["Dupla helice (espiral dupla)","Estrela","Cubo"],
                "correta":0,
                "explicacao":"O DNA se parece com uma escada torcida, chamada dupla helice."
            },
            {
                "pergunta":"O que o DNA guarda dentro das nossas celulas?",
                "opcoes":["As instrucoes geneticas do corpo","Receitas de bolo","Fotos antigas"],
                "correta":0,
                "explicacao":"O DNA carrega as instrucoes que determinam como cada ser vivo se desenvolve."
            }
        ]
    },
    {
        "nome":"Cosmic Boo-cake",
        "cientista":"Katherine Johnson",
        "tipo":"espaco",
        "cor":AZUL,
        "ingredientes":[
            ("Acucar Gravitacional Lunar",1),
            ("Massa de Baunilha das Trevas",1),
            ("Granulado Estrela Cadente",3)
        ],
        "processos":["blender","forno","decorar"],
        "quiz":[
            {
                "pergunta":"Katherine Johnson calculava trajetorias para qual orgao espacial?",
                "opcoes":["NASA","Escola de culinaria","Time de futebol"],
                "correta":0,
                "explicacao":"Katherine Johnson foi matematica da NASA e calculou rotas de missoes espaciais."
            },
            {
                "pergunta":"O trabalho de Katherine Johnson ajudou astronautas a...?",
                "opcoes":["Chegar com seguranca ao espaco e voltar","Aprender a cozinhar","Aprender a dancar"],
                "correta":0,
                "explicacao":"Seus calculos garantiram trajetorias seguras para missoes tripuladas da NASA."
            },
            {
                "pergunta":"Katherine Johnson era especialista em qual area?",
                "opcoes":["Matematica","Culinaria","Moda"],
                "correta":0,
                "explicacao":"Ela era uma matematica brilhante, essencial para o programa espacial dos EUA."
            },
            {
                "pergunta":"O filme que conta a historia de Katherine Johnson se chama...?",
                "opcoes":["Estrelas Alem do Tempo","Vingadores","Frozen"],
                "correta":0,
                "explicacao":"O filme 'Estrelas Alem do Tempo' (Hidden Figures) conta a historia dela e de outras cientistas."
            }
        ]
    },
    {
        "nome":"Steampunk Choco-Pie",
        "cientista":"Ada Lovelace",
        "tipo":"codigo",
        "cor":AMARELO,
        "ingredientes":[
            ("Massa de Baunilha Sombria",1),
            ("Geleia de Frutas Vermelhas Ciberneticas",1),
            ("Engrenagem de Chocolate Binario",8)
        ],
        "processos":["forno","decorar"],
        "quiz":[
            {
                "pergunta":"Ada Lovelace e considerada a primeira...?",
                "opcoes":["Programadora de computadores do mundo","Cientista de foguetes","Chef de cozinha"],
                "correta":0,
                "explicacao":"Ada Lovelace escreveu o que hoje reconhecemos como o primeiro programa de computador."
            },
            {
                "pergunta":"Ada Lovelace escreveu instrucoes para qual maquina antiga?",
                "opcoes":["A Maquina Analitica","Um liquidificador","Uma maquina de costura"],
                "correta":0,
                "explicacao":"Ela criou instrucoes para a Maquina Analitica, projetada por Charles Babbage."
            },
            {
                "pergunta":"As instrucoes que Ada Lovelace escreveu, hoje chamamos de...?",
                "opcoes":["Um programa (codigo)","Uma receita de bolo","Uma musica"],
                "correta":0,
                "explicacao":"O que ela escreveu e considerado o primeiro algoritmo feito para ser rodado numa maquina."
            },
            {
                "pergunta":"Em homenagem a Ada Lovelace existe uma linguagem de programacao chamada...?",
                "opcoes":["Ada","Python","Java"],
                "correta":0,
                "explicacao":"A linguagem de programacao 'Ada' foi batizada em sua homenagem."
            }
        ]
    }
]

cientistas=[
    ("Marie Curie","Radio-Glow Shake","radio"),
    ("Rosalind Franklin","Bio-Spooky","dna"),
    ("Katherine Johnson","Cosmic Boo-cake","espaco"),
    ("Ada Lovelace","Steampunk Choco-Pie","codigo")
]

# ============================================================
# ESTADO
# ============================================================
rodando=True
tela_atual="menu"
receita_i=0
pontos=0
pontos_totais=0
ingredientes=[]
arrastando=None
processo_ok=False
tempo_processo=0.0
decoracoes=[]
confeito=None
particulas=[]
animacao=0.0

# Quiz
quiz_index=0
quiz_atual=None
quiz_respondida=False
quiz_selecionada=None
destino_apos_quiz="ingredientes"

# Nome do jogador (pedido so uma vez, na tela final)
nome_jogador=""

# ============================================================
# UTILIDADES
# ============================================================
def txt(s,f,c,x,y):
    tela.blit(f.render(s,True,c),(x,y))

def center(s,f,c,y):
    im=f.render(s,True,c)
    tela.blit(im,((LARGURA-im.get_width())//2,y))

def texto_ajustado(s,max_largura,tamanho=30,cor=BRANCO):
    f=pygame.font.Font(None,tamanho)

    while f.size(s)[0]>max_largura and tamanho>14:
        tamanho-=1
        f=pygame.font.Font(None,tamanho)

    return f.render(s,True,cor)

def botao(s,x,y,w,h):
    r=pygame.Rect(x,y,w,h)

    mx,my=pygame.mouse.get_pos()
    passa_mouse=r.collidepoint(mx,my)

    # Respiro leve o tempo todo, cresce um pouco mais no hover.
    pulso=math.sin(animacao*3+x*0.01)*1.5
    extra=10 if passa_mouse else 0

    ww=int(w+extra)
    hh=int(h+(extra*h//w if w else 0))
    xx=int(x-(ww-w)//2)
    yy=int(y-(hh-h)//2+pulso)

    raio=min(24,hh//2)

    cor_fundo=(140,75,180) if passa_mouse else ROXO
    cor_borda=AMARELO if passa_mouse else ROSA

    pygame.draw.rect(
        tela,PRETO,
        (xx,yy+6,ww,hh),
        border_radius=raio
    )

    if passa_mouse:
        pygame.draw.rect(
            tela,(255,235,150),
            (xx-4,yy-4,ww+8,hh+8),
            2,
            border_radius=raio+2
        )

    pygame.draw.rect(
        tela,cor_fundo,
        (xx,yy,ww,hh),
        border_radius=raio
    )

    pygame.draw.rect(
        tela,cor_borda,
        (xx,yy,ww,hh),3,
        border_radius=raio
    )

    brilho=pygame.Rect(
        xx+7,yy+6,ww-14,max(5,hh//5)
    )

    pygame.draw.rect(
        tela,(175,105,205),
        brilho,
        border_radius=min(10,hh//4)
    )

    im=texto_ajustado(s,max(10,ww-20),30)

    tela.blit(
        im,
        (
            xx+(ww-im.get_width())//2,
            yy+(hh-im.get_height())//2
        )
    )

    return r

def voltar():
    return botao("<",25,25,72,52)

def barra_cabecalho(altura=140):
    # Painel solido no topo: garante que titulo, pontos e botao
    # de voltar nunca fiquem "brigando" visualmente com a
    # decoracao do cenario atras.
    pygame.draw.rect(
        tela,(24,13,32),
        (0,0,LARGURA,altura)
    )

    pygame.draw.rect(
        tela,ROXO,
        (0,altura-4,LARGURA,4)
    )

    pygame.draw.line(
        tela,(70,40,88),
        (0,altura-8),
        (LARGURA,altura-8),
        1
    )

def texto_multilinha(s,f,cor,x,y,max_largura,espaco=26):
    palavras=s.split(" ")
    linha=""
    yy=y

    for p in palavras:
        teste=(linha+" "+p).strip()

        if f.size(teste)[0]>max_largura and linha:
            txt(linha,f,cor,x,yy)
            yy+=espaco
            linha=p
        else:
            linha=teste

    if linha:
        txt(linha,f,cor,x,yy)
        yy+=espaco

    return yy

def efeito(x,y,c=ROSA,n=12):
    for _ in range(n):
        a=random.random()*math.tau
        v=random.uniform(1,3)

        particulas.append([
            x,y,
            math.cos(a)*v,
            math.sin(a)*v-1,
            random.randint(18,35),
            c
        ])

def atualiza_particulas():
    for p in particulas[:]:
        p[0]+=p[2]
        p[1]+=p[3]
        p[3]+=.05
        p[4]-=1

        if p[4]<=0:
            particulas.remove(p)

def desenha_particulas():
    for p in particulas:
        pygame.draw.circle(
            tela,
            p[5],
            (int(p[0]),int(p[1])),
            3
        )

# ============================================================
# DECORAÇÕES DO CENÁRIO
# ============================================================
def morcego(x,y,escala=1):
    pygame.draw.ellipse(
        tela,PRETO,
        (
            int(x-5*escala),
            int(y-7*escala),
            int(10*escala),
            int(16*escala)
        )
    )

    esquerda=[
        (x-3*escala,y-2*escala),
        (x-20*escala,y-13*escala),
        (x-16*escala,y+5*escala),
        (x-8*escala,y+1*escala),
        (x-4*escala,y+8*escala)
    ]

    direita=[
        (x+3*escala,y-2*escala),
        (x+20*escala,y-13*escala),
        (x+16*escala,y+5*escala),
        (x+8*escala,y+1*escala),
        (x+4*escala,y+8*escala)
    ]

    pygame.draw.polygon(tela,PRETO,esquerda)
    pygame.draw.polygon(tela,PRETO,direita)

def frasco_borbulhante(x,y,cor,escala=1):
    # Erlenmeyer de laboratorio com liquido borbulhando.
    pygame.draw.polygon(
        tela,(210,225,235),
        [
            (x-4*escala,y-40*escala),
            (x+4*escala,y-40*escala),
            (x+26*escala,y+30*escala),
            (x-26*escala,y+30*escala)
        ]
    )

    pygame.draw.polygon(
        tela,cor,
        [
            (x-16*escala,y-2*escala),
            (x+16*escala,y-2*escala),
            (x+22*escala,y+28*escala),
            (x-22*escala,y+28*escala)
        ]
    )

    pygame.draw.rect(
        tela,CINZA,
        (x-6*escala,y-46*escala,12*escala,8*escala),
        border_radius=2
    )

    for k in range(3):
        by=y+18*escala-((animacao*35+k*22)%(42*escala))
        bx=x+math.sin(k+animacao*2)*8*escala

        pygame.draw.circle(
            tela,BRANCO,
            (int(bx),int(by)),
            max(1,int(2.5*escala))
        )

def helice_dna(x,y,altura,escala=1):
    passos=8

    for i in range(passos):
        t=i/(passos-1)
        yy=y+t*altura
        onda=math.sin(animacao*1.5+t*math.tau)

        x1=x-14*escala*onda
        x2=x+14*escala*onda

        pygame.draw.line(
            tela,(90,160,235),
            (x1,yy),(x2,yy),
            max(1,int(2*escala))
        )

        pygame.draw.circle(
            tela,ROSA2,(int(x1),int(yy)),max(1,int(3*escala))
        )

        pygame.draw.circle(
            tela,AZUL,(int(x2),int(yy)),max(1,int(3*escala))
        )

def engrenagem_decorativa(x,y,raio,cor=AMARELO,vel=1):
    ang=animacao*vel

    for k in range(8):
        a=ang+k*(math.tau/8)
        px=x+math.cos(a)*(raio+5)
        py=y+math.sin(a)*(raio+5)

        pygame.draw.circle(
            tela,cor,(int(px),int(py)),max(2,int(raio*0.22))
        )

    pygame.draw.circle(tela,cor,(int(x),int(y)),raio)
    pygame.draw.circle(tela,MARROM,(int(x),int(y)),max(2,int(raio*0.4)))

def monstrinho(x,y,escala=1):
    pygame.draw.circle(
        tela,ROXO,
        (int(x),int(y)),
        int(12*escala)
    )

    for ox in (-4,4):
        pygame.draw.circle(
            tela,BRANCO,
            (
                int(x+ox*escala),
                int(y-2*escala)
            ),
            max(2,int(3*escala))
        )

        pygame.draw.circle(
            tela,PRETO,
            (
                int(x+ox*escala),
                int(y-2*escala)
            ),
            max(1,int(1.5*escala))
        )

# ============================================================
# ÍCONES DE INGREDIENTES
# ============================================================
def icone(nome,cx,cy,s=.7):
    n=nome.lower()

    if "baga" in n or "frutas vermelhas" in n:
        for ox,oy,c in [
            (-9,3,VERMELHO),
            (9,3,ROSA),
            (0,-7,VERMELHO)
        ]:
            pygame.draw.circle(
                tela,c,
                (int(cx+ox*s),int(cy+oy*s)),
                int(13*s)
            )

        pygame.draw.polygon(
            tela,VERDE,
            [
                (cx,cy-16*s),
                (cx-8*s,cy-23*s),
                (cx,cy-20*s),
                (cx+8*s,cy-23*s),
                (cx+5*s,cy-15*s)
            ]
        )

    elif "planta" in n:
        pygame.draw.line(
            tela,VERDE,
            (cx,cy+18*s),
            (cx,cy-18*s),
            max(2,int(5*s))
        )

        pygame.draw.ellipse(
            tela,VERDE,
            (cx-25*s,cy-10*s,24*s,13*s)
        )

        pygame.draw.ellipse(
            tela,(70,190,120),
            (cx+1*s,cy-18*s,24*s,13*s)
        )

    elif any(
        k in n
        for k in ["soro","essencia","isotopo","geleia"]
    ):
        pygame.draw.rect(
            tela,BRANCO,
            (
                cx-13*s,
                cy-18*s,
                26*s,
                36*s
            ),
            border_radius=5
        )

        pygame.draw.rect(
            tela,
            VERDE if "isotopo" in n else ROSA2,
            (
                cx-9*s,
                cy-7*s,
                18*s,
                22*s
            ),
            border_radius=4
        )

        pygame.draw.rect(
            tela,CINZA,
            (
                cx-8*s,
                cy-25*s,
                16*s,
                8*s
            ),
            border_radius=3
        )

    elif "acucar" in n:
        pygame.draw.polygon(
            tela,BRANCO,
            [
                (cx-18*s,cy+10*s),
                (cx-13*s,cy-12*s),
                (cx+13*s,cy-12*s),
                (cx+18*s,cy+10*s)
            ]
        )

        pygame.draw.circle(
            tela,AMARELO,
            (int(cx),int(cy)),
            max(2,int(4*s))
        )

    elif "massa" in n:
        pygame.draw.ellipse(
            tela,CREME,
            (
                cx-28*s,
                cy-16*s,
                56*s,
                32*s
            )
        )

        pygame.draw.ellipse(
            tela,(220,180,145),
            (
                cx-13*s,
                cy-7*s,
                26*s,
                14*s
            )
        )

    elif "granulado" in n:
        for ox,oy,c in [
            (-12,-5,ROSA),
            (0,7,AMARELO),
            (12,-7,AZUL),
            (7,8,VERDE)
        ]:
            pygame.draw.circle(
                tela,c,
                (
                    int(cx+ox*s),
                    int(cy+oy*s)
                ),
                max(2,int(4*s))
            )

    elif "engrenagem" in n:
        pygame.draw.circle(
            tela,AMARELO,
            (int(cx),int(cy)),
            int(15*s)
        )

        pygame.draw.circle(
            tela,MARROM,
            (int(cx),int(cy)),
            int(6*s)
        )

        for a in range(0,360,45):
            px=cx+math.cos(math.radians(a))*20*s
            py=cy+math.sin(math.radians(a))*20*s

            pygame.draw.rect(
                tela,AMARELO,
                (
                    px-4*s,
                    py-4*s,
                    8*s,
                    8*s
                ),
                border_radius=2
            )

    else:
        pygame.draw.circle(
            tela,ROSA2,
            (int(cx),int(cy)),
            int(16*s)
        )

# ============================================================
# CENÁRIO
# ============================================================
def parede():
    tela.fill(FUNDO)

    for y in range(0,600,42):
        pygame.draw.line(
            tela,
            (55,30,68),
            (0,y),
            (800,y),
            1
        )

    for x in range(25,800,75):
        for y in range(20,600,70):
            pygame.draw.circle(
                tela,
                (62,35,78),
                (x,y),
                3+((x+y)//10)%4
            )

    pygame.draw.rect(
        tela,(72,39,55),
        (0,115,800,12)
    )

    pygame.draw.rect(
        tela,(110,62,72),
        (0,127,800,4)
    )

    for x,c,h in [
        (55,AZUL,42),
        (95,VERDE,32),
        (700,ROSA,38),
        (745,AMARELO,48)
    ]:
        pygame.draw.rect(
            tela,c,
            (x,115-h,24,h),
            border_radius=8
        )

        pygame.draw.rect(
            tela,BRANCO,
            (x+6,108-h,12,8),
            border_radius=3
        )

    for x,c in [
        (160,AZUL),
        (188,ROSA),
        (216,VERDE)
    ]:
        pygame.draw.rect(
            tela,(190,220,235),
            (x,75,17,48),
            border_radius=7
        )

        pygame.draw.rect(
            tela,c,
            (x+3,98,11,21),
            border_radius=5
        )

    for cx,cy in [
        (625,70),
        (675,95),
        (290,72)
    ]:
        pygame.draw.circle(
            tela,ROSA2,
            (cx,cy),5
        )

        pygame.draw.circle(
            tela,AZUL,
            (cx+18,cy+12),5
        )

        pygame.draw.line(
            tela,ROSA2,
            (cx+4,cy+3),
            (cx+15,cy+9),
            2
        )

    morcego(105,55,.8)
    morcego(680,55,.7)
    monstrinho(760,170,.8)

    # ------------------------------------------------------
    # DECORACAO EXTRA "LABORATORIO"
    # Fica sempre nas margens (cantos e laterais) para nunca
    # brigar com titulos, cards ou botoes do conteudo central.
    # ------------------------------------------------------

    # Piso quadriculado no rodape.
    for x in range(0,800,40):
        for y in range(560,600,40):
            cor_piso=(46,26,58) if ((x//40+y//40)%2==0) else (40,22,52)

            pygame.draw.rect(
                tela,cor_piso,
                (x,y,40,40)
            )

    pygame.draw.line(
        tela,ROXO2,
        (0,560),(800,560),2
    )

    # Frascos borbulhantes nos cantos inferiores.
    frasco_borbulhante(38,555,VERDE,.85)
    frasco_borbulhante(762,555,ROSA,.85)

    # Helice de DNA discreta na lateral direita.
    helice_dna(778,160,270,.55)

    # Engrenagens steampunk na lateral esquerda.
    engrenagem_decorativa(24,220,16,AMARELO,.6)
    engrenagem_decorativa(24,258,10,CINZA,-.9)

    # Pequeno "poster" de tabela periodica no canto,
    # abaixo da faixa de prateleira.
    for i in range(4):
        for j in range(3):
            px=18+i*15
            py=470+j*15

            pygame.draw.rect(
                tela,
                [AZUL,VERDE,AMARELO,ROSA][(i+j)%4],
                (px,py,12,12),
                border_radius=2
            )

# ============================================================
# MENU
# ============================================================
def menu():
    parede()

    center(
        "SANGUETERIA",
        titulo,
        ROSA,
        150
    )

    center(
        "LABORATORIO DE DOCES",
        grande,
        BRANCO,
        220
    )

    center(
        "Prepare, misture, asse e decore!",
        fonte,
        ROSA2,
        265
    )

    pygame.draw.ellipse(
        tela,PRETO,
        (245,365,315,45)
    )

    pygame.draw.rect(
        tela,(125,75,58),
        (215,335,370,70),
        border_radius=22
    )

    pygame.draw.rect(
        tela,(195,130,85),
        (225,325,350,55),
        border_radius=22
    )

    icone(
        "Isotopo de Radio-Glow",
        310,340,.75
    )

    icone(
        "Granulado Estrela Cadente",
        390,340,.8
    )

    icone(
        "Engrenagem de Chocolate Binario",
        475,340,.75
    )

    return (
        botao("JOGAR",300,420,200,60),
        botao("CIENTISTAS",270,490,260,55),
        botao("SAIR",300,555,200,42)
    )

# ============================================================
# DESENHOS DAS COMIDAS
# AGORA USADOS TAMBÉM NOS CARDS
# ============================================================
def desenhar_base_da_receita(
    r,
    cx=400,
    cy=350,
    escala=1
):
    nome=r["nome"]

    # --------------------------------------------------------
    # RADIO-GLOW SHAKE
    # --------------------------------------------------------
    if "Shake" in nome:

        pygame.draw.ellipse(
            tela,PRETO,
            (
                cx-75*escala,
                cy+65*escala,
                150*escala,
                30*escala
            )
        )

        pygame.draw.polygon(
            tela,(180,230,245),
            [
                (cx-65*escala,cy-65*escala),
                (cx+65*escala,cy-65*escala),
                (cx+50*escala,cy+75*escala),
                (cx-50*escala,cy+75*escala)
            ]
        )

        pygame.draw.polygon(
            tela,r["cor"],
            [
                (cx-54*escala,cy-5*escala),
                (cx+54*escala,cy-5*escala),
                (cx+48*escala,cy+65*escala),
                (cx-48*escala,cy+65*escala)
            ]
        )

        pygame.draw.rect(
            tela,ROSA2,
            (
                cx-55*escala,
                cy-82*escala,
                110*escala,
                25*escala
            ),
            border_radius=8
        )

        # chantilly
        pygame.draw.ellipse(
            tela,BRANCO,
            (
                cx-35*escala,
                cy-105*escala,
                70*escala,
                38*escala
            )
        )

        pygame.draw.circle(
            tela,VERDE,
            (
                int(cx+22*escala),
                int(cy-102*escala)
            ),
            max(2,int(5*escala))
        )

        # canudo
        pygame.draw.line(
            tela,CINZA,
            (
                int(cx+5*escala),
                int(cy-105*escala)
            ),
            (
                int(cx+28*escala),
                int(cy-145*escala)
            ),
            max(2,int(5*escala))
        )

    # --------------------------------------------------------
    # BIO-SPOOKY
    # --------------------------------------------------------
    elif "Spooky" in nome:

        pygame.draw.ellipse(
            tela,PRETO,
            (
                cx-95*escala,
                cy+65*escala,
                190*escala,
                28*escala
            )
        )

        pygame.draw.rect(
            tela,(220,220,235),
            (
                cx-70*escala,
                cy-90*escala,
                140*escala,
                155*escala
            ),
            border_radius=28
        )

        pygame.draw.ellipse(
            tela,(170,150,205),
            (
                cx-70*escala,
                cy-25*escala,
                140*escala,
                100*escala
            )
        )

        pygame.draw.ellipse(
            tela,(90,35,160),
            (
                cx-58*escala,
                cy-10*escala,
                116*escala,
                80*escala
            )
        )

        pygame.draw.rect(
            tela,ROXO,
            (
                cx-40*escala,
                cy-105*escala,
                80*escala,
                28*escala
            ),
            border_radius=8
        )

        pygame.draw.rect(
            tela,CINZA,
            (
                cx-9*escala,
                cy-125*escala,
                18*escala,
                22*escala
            ),
            border_radius=4
        )

        # líquido
        pygame.draw.ellipse(
            tela,ROSA2,
            (
                cx-30*escala,
                cy+5*escala,
                60*escala,
                42*escala
            )
        )

    # --------------------------------------------------------
    # COSMIC BOO-CAKE
    # --------------------------------------------------------
    elif "Cosmic" in nome:

        pygame.draw.ellipse(
            tela,PRETO,
            (
                cx-120*escala,
                cy+50*escala,
                240*escala,
                35*escala
            )
        )

        # base
        pygame.draw.rect(
            tela,ROSA2,
            (
                cx-110*escala,
                cy-60*escala,
                220*escala,
                120*escala
            ),
            border_radius=18
        )

        # camada azul
        pygame.draw.ellipse(
            tela,AZUL,
            (
                cx-110*escala,
                cy-75*escala,
                220*escala,
                65*escala
            )
        )

        # camada inferior
        pygame.draw.ellipse(
            tela,ROSA2,
            (
                cx-110*escala,
                cy+20*escala,
                220*escala,
                55*escala
            )
        )

        # cobertura
        pygame.draw.ellipse(
            tela,(90,45,150),
            (
                cx-90*escala,
                cy-65*escala,
                180*escala,
                50*escala
            )
        )

        # estrelas
        for ox,c in [
            (-65,AMARELO),
            (-20,ROSA),
            (25,AZUL),
            (70,AMARELO)
        ]:
            pygame.draw.circle(
                tela,c,
                (
                    int(cx+ox*escala),
                    int(cy-43*escala)
                ),
                max(2,int(7*escala))
            )

        # lua
        pygame.draw.circle(
            tela,AMARELO,
            (
                int(cx),
                int(cy-82*escala)
            ),
            max(3,int(18*escala))
        )

        pygame.draw.circle(
            tela,(90,45,150),
            (
                int(cx+8*escala),
                int(cy-88*escala)
            ),
            max(2,int(17*escala))
        )

    # --------------------------------------------------------
    # STEAMPUNK CHOCO-PIE
    # TORTA DE CHOCOLATE COM MASSA QUADRICULADA
    # --------------------------------------------------------
    else:

        # sombra da torta
        pygame.draw.ellipse(
            tela,
            PRETO,
            (
                cx-125*escala,
                cy+48*escala,
                250*escala,
                32*escala
            )
        )

        # prato/suporte escuro
        pygame.draw.ellipse(
            tela,
            (55,30,45),
            (
                cx-108*escala,
                cy+35*escala,
                216*escala,
                25*escala
            )
        )

        # corpo da torta - massa
        pygame.draw.polygon(
            tela,
            (190,120,65),
            [
                (cx-105*escala, cy-25*escala),
                (cx+105*escala, cy-25*escala),
                (cx+92*escala, cy+48*escala),
                (cx-92*escala, cy+48*escala)
            ]
        )

        # lateral mais escura
        pygame.draw.polygon(
            tela,
            (125,65,48),
            [
                (cx-92*escala, cy+5*escala),
                (cx+92*escala, cy+5*escala),
                (cx+82*escala, cy+45*escala),
                (cx-82*escala, cy+45*escala)
            ]
        )

        # detalhes verticais da massa
        for ox in [-70,-45,-20,5,30,55,75]:
            pygame.draw.line(
                tela,
                (220,150,85),
                (
                    int(cx+ox*escala),
                    int(cy+12*escala)
                ),
                (
                    int(cx+(ox-3)*escala),
                    int(cy+38*escala)
                ),
                max(1,int(3*escala))
            )

        # topo da torta - massa dourada
        pygame.draw.ellipse(
            tela,
            (225,155,85),
            (
                cx-108*escala,
                cy-45*escala,
                216*escala,
                75*escala
            )
        )

        # borda da torta
        pygame.draw.ellipse(
            tela,
            (160,90,55),
            (
                cx-96*escala,
                cy-38*escala,
                192*escala,
                58*escala
            )
        )

        # recheio de chocolate
        pygame.draw.ellipse(
            tela,
            (75,35,35),
            (
                cx-82*escala,
                cy-30*escala,
                164*escala,
                45*escala
            )
        )

        # brilho do chocolate
        pygame.draw.ellipse(
            tela,
            (145,75,55),
            (
                cx-62*escala,
                cy-20*escala,
                124*escala,
                22*escala
            )
        )

        # ====================================================
        # QUADRICULADO / TRANÇADO DA MASSA
        # ====================================================

        massa = (235,175,100)
        massa_sombra = (195,125,65)

        # faixas diagonais /
        diagonais_1 = [
            (-70,-32,-35,8),
            (-45,-38,-5,8),
            (-20,-40,22,8),
            (5,-40,47,8),
            (30,-38,70,5)
        ]

        for x1,y1,x2,y2 in diagonais_1:
            pygame.draw.line(
                tela,
                massa,
                (
                    int(cx+x1*escala),
                    int(cy+y1*escala)
                ),
                (
                    int(cx+x2*escala),
                    int(cy+y2*escala)
                ),
                max(2,int(7*escala))
            )

        # faixas diagonais \
        diagonais_2 = [
            (70,-32,35,8),
            (45,-38,5,8),
            (20,-40,-22,8),
            (-5,-40,-47,8),
            (-30,-38,-70,5)
        ]

        for x1,y1,x2,y2 in diagonais_2:
            pygame.draw.line(
                tela,
                massa_sombra,
                (
                    int(cx+x1*escala),
                    int(cy+y1*escala)
                ),
                (
                    int(cx+x2*escala),
                    int(cy+y2*escala)
                ),
                max(2,int(7*escala))
            )

        # pequenos detalhes dourados nas interseções
        for ox,oy in [
            (-35,-22),
            (0,-22),
            (35,-22),
            (-18,-8),
            (18,-8)
        ]:
            pygame.draw.circle(
                tela,
                AMARELO,
                (
                    int(cx+ox*escala),
                    int(cy+oy*escala)
                ),
                max(1,int(3*escala))
            )

        # borda superior da torta
        pygame.draw.arc(
            tela,
            (245,190,110),
            (
                cx-108*escala,
                cy-45*escala,
                216*escala,
                75*escala
            ),
            math.pi,
            math.tau,
            max(2,int(4*escala))
        )

        # ====================================================
        # PEQUENAS ENGRENAGENS STEAMPUNK
        # ====================================================

        # engrenagem esquerda
        gx = int(cx-92*escala)
        gy = int(cy-42*escala)
        gr = max(3,int(12*escala))

        pygame.draw.circle(
            tela,
            AMARELO,
            (gx,gy),
            gr
        )

        pygame.draw.circle(
            tela,
            (95,50,35),
            (gx,gy),
            max(2,int(5*escala))
        )

        # engrenagem direita
        gx2 = int(cx+95*escala)
        gy2 = int(cy-15*escala)
        gr2 = max(3,int(10*escala))

        pygame.draw.circle(
            tela,
            (220,155,75),
            (gx2,gy2),
            gr2
        )

        pygame.draw.circle(
            tela,
            (90,45,35),
            (gx2,gy2),
            max(2,int(4*escala))
        )

        # pequenos dentes das engrenagens
        for angulo in range(0,360,45):
            a = math.radians(angulo)

            x1 = int(gx + math.cos(a)*(gr+1))
            y1 = int(gy + math.sin(a)*(gr+1))

            x2 = int(gx + math.cos(a)*(gr+4))
            y2 = int(gy + math.sin(a)*(gr+4))

            pygame.draw.line(
                tela,
                AMARELO,
                (x1,y1),
                (x2,y2),
                max(1,int(3*escala))
            )

        # brilhinhos steampunk
        pygame.draw.circle(
            tela,
            AMARELO,
            (
                int(cx-112*escala),
                int(cy-48*escala)
            ),
            max(1,int(2*escala))
        )

        pygame.draw.circle(
            tela,
            ROSA2,
            (
                int(cx+112*escala),
                int(cy-50*escala)
            ),
            max(1,int(2*escala))
        )
# ============================================================
# CARD DA RECEITA
# SEM IMAGEM DE COMIDA
# ============================================================
def card_comida(r,x,y,w,h):
    # Fundo do card
    pygame.draw.rect(
        tela,PRETO,
        (x,y+7,w,h),
        border_radius=20
    )

    pygame.draw.rect(
        tela,ROXO2,
        (x,y,w,h),
        border_radius=20
    )

    pygame.draw.rect(
        tela,ROSA,
        (x,y,w,h),
        3,
        border_radius=20
    )

    # Pequeno destaque superior
    pygame.draw.rect(
        tela,(125,65,155),
        (x+8,y+5,w-16,10),
        border_radius=5
    )

    # Área da comida
    area_x=x+15
    area_y=y+15
    area_w=125
    area_h=h-30

    pygame.draw.rect(
        tela,(50,25,65),
        (area_x,area_y,area_w,area_h),
        border_radius=15
    )

    pygame.draw.rect(
        tela,ROSA2,
        (area_x,area_y,area_w,area_h),
        2,
        border_radius=15
    )

    # Desenha a comida diretamente pelo pygame
    desenhar_base_da_receita(
        r,
        area_x+area_w//2,
        area_y+area_h//2+3,
        0.36
    )

    # Nome
    nome=texto_ajustado(
        r["nome"],
        200,
        30,
        BRANCO
    )

    tela.blit(
        nome,
        (x+150,y+30)
    )

    # Texto
    txt(
        "Clique para preparar",
        pequena,
        ROSA2,
        x+150,
        y+77
    )

    # Área científica
    pygame.draw.circle(
        tela,
        r["cor"],
        (x+160,y+105),
        5
    )

    areas={
        "Radio-Glow Shake":"QUIMICA",
        "Bio-Spooky":"BIOLOGIA / DNA",
        "Cosmic Boo-cake":"MATEMATICA / ESPACO",
        "Steampunk Choco-Pie":"COMPUTACAO"
    }

    txt(
        areas[r["nome"]],
        pygame.font.Font(None,18),
        AMARELO,
        x+175,
        y+98
    )

# ============================================================
# LIVRO DE RECEITAS
# ============================================================
def receitas_tela():
    parede()

    b=voltar()

    center(
        "LIVRO DE RECEITAS",
        titulo,
        ROSA,
        45
    )

    center(
        "Escolha uma receita para preparar",
        fonte,
        BRANCO,
        115
    )

    bs=[]

    posicoes=[
        (38,185),
        (408,185),
        (38,350),
        (408,350)
    ]

    for i,r in enumerate(receitas):
        x,y=posicoes[i]

        q=pygame.Rect(
            x,y,
            354,
            135
        )

        card_comida(
            r,
            x,y,
            354,
            135
        )

        bs.append(q)

    center(
        "Cada receita combina culinaria, ciencia e criatividade!",
        pequena,
        ROSA2,
        540
    )

    return b,bs

# ============================================================
# INGREDIENTES
# ============================================================
def criar_ingredientes():
    global ingredientes

    ingredientes=[]

    pos=[
        (30,190),
        (260,190),
        (30,270),
        (260,270),
        (30,350),
        (260,350),
        (30,430),
        (260,430),
        (30,510),
        (260,510)
    ]

    k=0

    for nome,q in receitas[receita_i]["ingredientes"]:
        for u in range(q):

            x,y=pos[k]

            ingredientes.append({
                "nome":nome,
                "x":x,
                "y":y,
                "ox":x,
                "oy":y,
                "w":195,
                "h":62,
                "colocado":False,
                "arrastando":False,
                "u":u+1
            })

            k+=1

def iniciar():
    global pontos
    global processo_ok
    global tempo_processo
    global decoracoes
    global confeito
    global arrastando
    global quiz_index

    pontos=0
    processo_ok=False
    tempo_processo=0.0
    decoracoes=[]
    confeito=None
    arrastando=None
    quiz_index=0

    criar_ingredientes()

def bancada():
    pygame.draw.rect(
        tela,(57,28,74),
        (0,450,800,150)
    )

    pygame.draw.rect(
        tela,ROXO,
        (0,450,800,7)
    )

def tigela(r):
    cx,cy=600,345

    total=len(ingredientes)
    feitos_lista=[i for i in ingredientes if i["colocado"]]
    frac=len(feitos_lista)/total if total else 0

    # Sombra suave embaixo da tigela.
    sombra=pygame.Surface((340,80),pygame.SRCALPHA)
    pygame.draw.ellipse(sombra,(0,0,0,90),(0,0,340,80))
    tela.blit(sombra,(cx-170,cy+58))

    # Corpo de vidro da tigela.
    pygame.draw.ellipse(
        tela,(150,205,235),
        (cx-155,cy-75,315,168)
    )

    pygame.draw.ellipse(
        tela,(215,240,250),
        (cx-140,cy-87,285,110)
    )

    pygame.draw.ellipse(
        tela,(95,140,190),
        (cx-125,cy-63,255,90)
    )

    # Liquido: cresce e ganha a cor da receita conforme os
    # ingredientes vao sendo colocados.
    if frac>0:

        base=(248,244,252)
        alvo=r["cor"]

        cor_liq=tuple(
            int(base[k]+(alvo[k]-base[k])*frac)
            for k in range(3)
        )

        altura=18+frac*46

        pygame.draw.ellipse(
            tela,cor_liq,
            (
                cx-120,
                cy-58+(46-altura),
                240,
                int(altura)+42
            )
        )

        pygame.draw.ellipse(
            tela,
            tuple(min(255,c+35) for c in cor_liq),
            (cx-70,cy-52,140,24)
        )

        # Borbulhas subindo, so enquanto tem liquido.
        for k in range(4):
            bx=cx-90+k*55+math.sin(animacao*2+k)*8
            by=cy-10-((animacao*45+k*23)%55)

            pygame.draw.circle(
                tela,BRANCO,
                (int(bx),int(by)),
                max(1,2 if k%2==0 else 3)
            )

    # Brilho de vidro (arco claro na borda).
    pygame.draw.arc(
        tela,BRANCO,
        (cx-140,cy-87,285,110),
        math.pi,math.tau,5
    )

    pygame.draw.arc(
        tela,(255,255,255),
        (cx-118,cy-75,90,40),
        math.pi*0.85,math.pi*1.5,3
    )

    # Todos os ingredientes ja colocados, flutuando no liquido.
    for k,i in enumerate(feitos_lista):
        boiar=math.sin(animacao*2+k)*3

        icone(
            i["nome"],
            cx-85+(k%5)*43,
            cy-20+(k//5)*25+boiar,
            .42
        )

    # Quando esta completo, um brilho dourado convida a continuar.
    if total and frac==1:
        raio=95+math.sin(animacao*4)*6

        pygame.draw.circle(
            tela,AMARELO,
            (int(cx),int(cy-10)),
            int(raio),2
        )

def ingrediente(i):
    if i["colocado"]:
        return

    q=pygame.Rect(
        i["x"],
        i["y"],
        i["w"],
        i["h"]
    )

    mx,my=pygame.mouse.get_pos()
    em_foco=i["arrastando"] or q.collidepoint(mx,my)

    sombra_y=8 if i["arrastando"] else 4

    pygame.draw.rect(
        tela,PRETO,
        q.move(0,sombra_y),
        border_radius=16
    )

    cor_fundo=(135,70,175) if em_foco else ROXO
    cor_borda=AMARELO if em_foco else ROSA

    pygame.draw.rect(
        tela,cor_fundo,
        q,
        border_radius=16
    )

    pygame.draw.rect(
        tela,cor_borda,
        q,
        2,
        border_radius=16
    )

    # Friso claro no topo do card, como os botoes.
    pygame.draw.rect(
        tela,(175,105,205),
        (i["x"]+8,i["y"]+5,i["w"]-16,6),
        border_radius=4
    )

    # Selo redondo atras do icone, pra destacar melhor.
    bx,by=i["x"]+34,i["y"]+34

    pygame.draw.circle(
        tela,(48,24,62),
        (bx,by),24
    )

    pygame.draw.circle(
        tela,ROSA2 if em_foco else ROXO2,
        (bx,by),24,2
    )

    icone(
        i["nome"],
        bx,by,
        .5
    )

    f=pequena

    if pequena.size(i["nome"])[0]>=140:
        f=pygame.font.Font(None,17)

    txt(
        i["nome"],
        f,
        BRANCO,
        i["x"]+62,
        i["y"]+12
    )

    if i["u"]>1:
        txt(
            "unidade "+str(i["u"]),
            pygame.font.Font(None,16),
            ROSA2,
            i["x"]+62,
            i["y"]+40
        )

def ingredientes_tela():
    parede()
    barra_cabecalho()

    r=receitas[receita_i]

    b=voltar()

    txt(
        r["nome"],
        grande,
        ROSA,
        115,
        28
    )

    txt(
        "Pontos: "+str(pontos),
        fonte,
        AMARELO,
        650,
        32
    )

    center(
        "ARRASTE OS INGREDIENTES PARA A TIGELA!",
        fonte,
        ROSA2,
        110
    )

    bancada()
    tigela(r)

    for i in ingredientes:
        ingrediente(i)

    feitos=sum(
        i["colocado"]
        for i in ingredientes
    )

    txt(
        f"INGREDIENTES: {feitos}/{len(ingredientes)}",
        fonte,
        BRANCO,
        500,
        180
    )

    c=None

    if feitos==len(ingredientes):

        center(
            "TODOS OS INGREDIENTES!",
            grande,
            VERDE,
            455
        )

        c=botao(
            "CONTINUAR",
            300,
            505,
            200,
            55
        )

    return b,c

# ============================================================
# LIQUIDIFICADOR
# ============================================================
def liquidificador():
    parede()
    barra_cabecalho()

    r=receitas[receita_i]

    b=voltar()

    txt(
        r["nome"],
        grande,
        ROSA,
        115,
        28
    )

    txt(
        "Liquidificador magico",
        fonte,
        ROSA2,
        115,
        72
    )

    txt(
        "Pontos: "+str(pontos),
        fonte,
        AMARELO,
        650,
        32
    )

    center(
        "MISTURE A RECEITA!",
        titulo,
        ROSA,
        105
    )

    ativo=(not processo_ok) and tempo_processo>0

    tremor=math.sin(animacao*40)*4 if ativo else 0

    x,y=430+tremor,170

    if ativo:
        raio_halo=90+math.sin(animacao*6)*10

        pygame.draw.circle(
            tela,r["cor"],
            (int(x+110),int(y+90)),
            int(raio_halo),
            3
        )

    pygame.draw.ellipse(
        tela,PRETO,
        (x-15,y+190,220,30)
    )

    pygame.draw.rect(
        tela,ROXO,
        (x+35,y+135,150,65),
        border_radius=18
    )

    pygame.draw.rect(
        tela,ROSA,
        (x+35,y+135,150,65),
        3,
        border_radius=18
    )

    pygame.draw.polygon(
        tela,(180,225,240),
        [
            (x+45,y+25),
            (x+175,y+25),
            (x+160,y+150),
            (x+60,y+150)
        ]
    )

    pygame.draw.polygon(
        tela,r["cor"],
        [
            (x+57,y+80),
            (x+164,y+80),
            (x+157,y+142),
            (x+65,y+142)
        ]
    )

    pygame.draw.rect(
        tela,(70,65,80),
        (x+38,y+10,145,24),
        border_radius=8
    )

    pygame.draw.line(
        tela,BRANCO,
        (x+110,y+115),
        (x+88,y+105),
        3
    )

    pygame.draw.line(
        tela,BRANCO,
        (x+110,y+115),
        (x+132,y+105),
        3
    )

    if not processo_ok:
        for k in range(5):
            pygame.draw.circle(
                tela,ROSA2,
                (
                    int(
                        x+70+
                        ((animacao*50+k*25)%80)
                    ),
                    int(
                        y+95+
                        math.sin(animacao*5+k)*12
                    )
                ),
                6
            )

    pygame.draw.circle(
        tela,
        ROSA if processo_ok else AMARELO,
        (x+110,y+165),
        12
    )

    pygame.draw.rect(
        tela,ROXO2,
        (x+25,y+215,170,14),
        border_radius=7
    )

    pygame.draw.rect(
        tela,ROSA,
        (
            x+25,
            y+215,
            int(
                170*
                min(tempo_processo/5.0,1.0)
            ),
            14
        ),
        border_radius=7
    )

    center(
        "Clique em MISTURAR para ativar o liquidificador",
        pequena,
        BRANCO,
        430
    )

    if processo_ok:

        center(
            "MISTURA PERFEITA!",
            grande,
            VERDE,
            465
        )

        return (
            b,
            botao(
                "CONTINUAR",
                300,
                520,
                200,
                55
            ),
            None
        )

    return (
        b,
        None,
        botao(
            "MISTURAR",
            300,
            520,
            200,
            55
        )
    )

# ============================================================
# FORNO
# ============================================================
def forno():
    parede()
    barra_cabecalho()

    r=receitas[receita_i]

    b=voltar()

    txt(
        r["nome"],
        grande,
        ROSA,
        115,
        28
    )

    txt(
        "Forno de laboratorio",
        fonte,
        ROSA2,
        115,
        72
    )

    txt(
        "Pontos: "+str(pontos),
        fonte,
        AMARELO,
        650,
        32
    )

    center(
        "HORA DE ASSAR!",
        titulo,
        ROSA,
        100
    )

    ativo=(not processo_ok) and tempo_processo>0

    tremor=math.sin(animacao*25)*2 if ativo else 0

    x,y=265+tremor,145

    if ativo:
        for i in range(3):
            oy=y-10-i*16+math.sin(animacao*5+i)*5

            pygame.draw.line(
                tela,(255,195,150),
                (x+95,oy),(x+120,oy-14),2
            )

            pygame.draw.line(
                tela,(255,195,150),
                (x+150,oy),(x+175,oy-14),2
            )

    pygame.draw.ellipse(
        tela,PRETO,
        (x-15,y+325,300,28)
    )

    pygame.draw.rect(
        tela,ROXO,
        (x,y,270,315),
        border_radius=22
    )

    pygame.draw.rect(
        tela,ROSA,
        (x,y,270,315),
        4,
        border_radius=22
    )

    pygame.draw.rect(
        tela,ROXO2,
        (x+20,y+20,230,50),
        border_radius=10
    )

    txt(
        "FORNO DE LABORATORIO",
        pequena,
        BRANCO,
        x+37,
        y+36
    )

    pygame.draw.rect(
        tela,(60,35,60),
        (x+30,y+90,210,150),
        border_radius=12
    )

    pygame.draw.rect(
        tela,CINZA,
        (x+30,y+90,210,150),
        4,
        border_radius=12
    )

    if processo_ok:

        pygame.draw.rect(
            tela,(130,60,50),
            (x+36,y+96,198,138),
            border_radius=9
        )

        pygame.draw.circle(
            tela,LARANJA,
            (x+135,y+165),
            48
        )

        pygame.draw.circle(
            tela,AMARELO,
            (x+135,y+160),
            30
        )

    elif ativo:
        pisca=int(180+60*abs(math.sin(animacao*9)))

        pygame.draw.rect(
            tela,(pisca,80,45),
            (x+36,y+96,198,138),
            border_radius=9
        )

    pygame.draw.rect(
        tela,CINZA,
        (x+60,y+180,150,35),
        border_radius=7
    )

    pygame.draw.rect(
        tela,MARROM,
        (x+75,y+168,120,30),
        border_radius=12
    )

    pygame.draw.circle(
        tela,
        ROSA if processo_ok else AMARELO,
        (x+65,y+270),
        13
    )

    pygame.draw.circle(
        tela,
        VERDE if processo_ok else CINZA,
        (x+135,y+270),
        13
    )

    pygame.draw.circle(
        tela,AZUL,
        (x+205,y+270),
        13
    )

    pygame.draw.rect(
        tela,ROXO2,
        (x+40,y+295,190,12),
        border_radius=6
    )

    pygame.draw.rect(
        tela,LARANJA,
        (
            x+40,
            y+295,
            int(
                190*
                min(tempo_processo/5.0,1.0)
            ),
            12
        ),
        border_radius=6
    )

    center(
        "Clique em ASSAR para ligar o forno",
        pequena,
        BRANCO,
        485
    )

    if processo_ok:

        center(
            "ASSADO PERFEITO!",
            grande,
            VERDE,
            450
        )

        return (
            b,
            botao(
                "CONTINUAR",
                300,
                525,
                200,
                55
            ),
            None
        )

    return (
        b,
        None,
        botao(
            "ASSAR",
            300,
            525,
            200,
            55
        )
    )

# ============================================================
# DECORAÇÕES
# ============================================================
def decor(t,x,y,s=1):

    if t=="morango":
        pygame.draw.circle(
            tela,VERMELHO,(int(x),int(y)),int(12*s)
        )
        pygame.draw.polygon(
            tela,VERDE,
            [
                (x,y-7*s),(x-8*s,y-15*s),
                (x,y-12*s),(x+8*s,y-15*s)
            ]
        )

    elif t=="chocolate":
        pygame.draw.circle(
            tela,MARROM,(int(x),int(y)),int(12*s)
        )
        pygame.draw.circle(
            tela,CREME,(int(x-4*s),int(y-3*s)),max(1,int(2*s))
        )

    elif t=="coloridos":
        for ox,oy,c in [
            (-10,-6,VERMELHO),(0,7,AMARELO),
            (10,-5,AZUL),(-5,9,VERDE),(7,9,ROSA)
        ]:
            pygame.draw.circle(
                tela,c,(int(x+ox*s),int(y+oy*s)),max(2,int(4*s))
            )

    elif t=="glitter":
        for ox,oy in [(-8,-8),(8,-7),(-7,8),(8,8),(0,0)]:
            pygame.draw.line(
                tela,BRANCO,
                (int(x+(ox-3)*s),int(y+oy*s)),
                (int(x+(ox+3)*s),int(y+oy*s)),
                max(1,int(2*s))
            )
            pygame.draw.line(
                tela,ROSA2,
                (int(x+ox*s),int(y+(oy-3)*s)),
                (int(x+ox*s),int(y+(oy+3)*s)),
                max(1,int(2*s))
            )

    elif t=="estrela":
        pts=[]
        for k in range(10):
            a=-math.pi/2+k*math.pi/5
            rr=15*s if k%2==0 else 7*s
            pts.append((x+math.cos(a)*rr,y+math.sin(a)*rr))
        pygame.draw.polygon(tela,AMARELO,pts)

    elif t=="morcego":
        pygame.draw.polygon(
            tela,(75,35,95),
            [
                (x-17*s,y-3*s),(x-28*s,y-12*s),
                (x-24*s,y+4*s),(x-14*s,y+1*s),
                (x,y+12*s),(x+14*s,y+1*s),
                (x+24*s,y+4*s),(x+28*s,y-12*s),
                (x+17*s,y-3*s)
            ]
        )
        pygame.draw.circle(tela,ROXO2,(int(x),int(y)),int(10*s))
        pygame.draw.circle(tela,ROSA2,(int(x-4*s),int(y-2*s)),max(1,int(2*s)))
        pygame.draw.circle(tela,ROSA2,(int(x+4*s),int(y-2*s)),max(1,int(2*s)))

    elif t=="calda":
        pygame.draw.line(
            tela,MARROM,(int(x-12*s),int(y-4*s)),
            (int(x+12*s),int(y-4*s)),max(2,int(5*s))
        )
        pygame.draw.line(
            tela,MARROM,(int(x-7*s),int(y-4*s)),
            (int(x-7*s),int(y+10*s)),max(2,int(5*s))
        )
        pygame.draw.circle(
            tela,MARROM,(int(x+7*s),int(y+7*s)),max(2,int(4*s))
        )

    elif t=="cristais":
        pygame.draw.polygon(
            tela,AZUL,
            [
                (x-5*s,y+12*s),(x-12*s,y-4*s),
                (x-4*s,y-13*s),(x+3*s,y-5*s),
                (x+10*s,y-11*s),(x+13*s,y+4*s),
                (x+5*s,y+13*s)
            ]
        )
        pygame.draw.line(
            tela,BRANCO,(int(x-4*s),int(y-9*s)),
            (int(x-7*s),int(y+6*s)),max(1,int(2*s))
        )

    elif t=="engrenagem":
        pygame.draw.circle(tela,AMARELO,(int(x),int(y)),int(11*s))
        pygame.draw.circle(tela,MARROM,(int(x),int(y)),int(4*s))

    else:
        pygame.draw.circle(tela,ROSA,(int(x),int(y)),int(9*s))


def decoracao():
    parede()
    barra_cabecalho()

    r=receitas[receita_i]
    b=voltar()

    txt(r["nome"],grande,ROSA,115,28)
    txt("Estacao de decoracao",fonte,ROSA2,115,72)
    txt("Pontos: "+str(pontos),fonte,AMARELO,650,32)

    center("DECORE SUA RECEITA!",titulo,ROSA,100)

    # Mantem o desenho original da receita exatamente como esta.
    desenhar_base_da_receita(r)

    for d in decoracoes:
        decor(d[0],d[1],d[2])

    # As 8 opcoes ficam sempre visiveis.
    painel=pygame.Rect(615,165,170,285)
    pygame.draw.rect(tela,ROXO2,painel,border_radius=18)
    pygame.draw.rect(tela,ROSA,painel,2,border_radius=18)
    txt("CONFEITOS",pequena,BRANCO,655,180)

    tipos=[
        ("morango","MORANGO"),
        ("chocolate","CHOCOLATE"),
        ("coloridos","COLORIDOS"),
        ("glitter","GLITTER"),
        ("estrela","ESTRELA"),
        ("morcego","MORCEGO"),
        ("calda","CALDA"),
        ("cristais","CRISTAIS")
    ]

    bs=[]
    for k,(t,nome) in enumerate(tipos):
        col=k%2
        row=k//2
        q=pygame.Rect(620+col*82,215+row*50,76,42)

        # A opcao selecionada fica destacada em amarelo.
        pygame.draw.rect(
            tela,AMARELO if confeito==t else ROXO,q,
            border_radius=10
        )
        pygame.draw.rect(
            tela,AMARELO if confeito==t else ROSA,q,2,
            border_radius=10
        )

        decor(t,637+col*82,230+row*50,.38)

        im=texto_ajustado(nome,48,13,BRANCO)
        tela.blit(
            im,
            (q.centerx-im.get_width()//2,q.y+27)
        )

        bs.append((q,t))

    center(
        "Escolha um confeito e clique na comida",
        pequena,BRANCO,465
    )

    return b,bs,botao("PRONTO!",300,510,200,50)

# ============================================================
# QUIZ DE CURIOSIDADES
# ============================================================
def quiz_tela():
    parede()
    barra_cabecalho()

    r=receitas[receita_i]
    q=quiz_atual

    txt(r["cientista"],grande,ROSA,115,28)
    txt("Card de curiosidade cientifica",fonte,ROSA2,115,72)
    txt("Pontos: "+str(pontos),fonte,AMARELO,650,32)

    center("HORA DO QUIZ!",titulo,ROSA,95)

    desenhar_retrato(35,175,r["tipo"],150,170)

    prox_y=texto_multilinha(
        q["pergunta"],fonte,BRANCO,215,175,545,30
    )

    oy=max(prox_y+15,255)

    opcoes_rects=[]

    for idx,opc in enumerate(q["opcoes"]):

        if quiz_respondida:

            if idx==q["correta"]:
                cor_fundo=VERDE
            elif idx==quiz_selecionada:
                cor_fundo=VERMELHO
            else:
                cor_fundo=ROXO2

            rect=pygame.Rect(215,oy,545,52)

            pygame.draw.rect(
                tela,PRETO,rect.move(0,5),border_radius=14
            )
            pygame.draw.rect(
                tela,cor_fundo,rect,border_radius=14
            )
            pygame.draw.rect(
                tela,BRANCO,rect,2,border_radius=14
            )

            letra=chr(65+idx)+")  "+opc
            im=texto_ajustado(letra,rect.w-30,26,BRANCO)

            tela.blit(
                im,
                (rect.x+15,rect.y+(rect.h-im.get_height())//2)
            )

        else:
            letra=chr(65+idx)+")  "+opc
            rect=botao(letra,215,oy,545,52)

        opcoes_rects.append(rect)
        oy+=62

    continuar=None

    if quiz_respondida:

        acertou=quiz_selecionada==q["correta"]

        if acertou:
            center("CORRETO! +15 pontos",fonte,VERDE,oy+6)
        else:
            center("Quase! Veja a explicacao:",fonte,AMARELO,oy+6)

        texto_multilinha(
            q.get("explicacao",""),pequena,ROSA2,215,oy+38,545
        )

        continuar=botao("CONTINUAR",300,540,200,48)

    else:
        center(
            "Toque na resposta que voce acha certa",
            pequena,BRANCO,oy+8
        )

    return opcoes_rects,continuar

def preparar_quiz(destino):
    global tela_atual,quiz_atual,quiz_respondida
    global quiz_selecionada,destino_apos_quiz,quiz_index

    lista=receitas[receita_i]["quiz"]

    quiz_atual=lista[quiz_index%len(lista)]
    quiz_index+=1

    quiz_respondida=False
    quiz_selecionada=None
    destino_apos_quiz=destino
    tela_atual="quiz"

# ============================================================
# PEDIR NOME DO JOGADOR
# ============================================================
def tela_nome():
    parede()
    barra_cabecalho(110)

    center("QUASE LA!",titulo,ROSA,20)

    center(
        "Como podemos te chamar, confeiteira(o)?",
        fonte,BRANCO,140
    )

    caixa=pygame.Rect(190,220,420,64)

    pygame.draw.rect(
        tela,PRETO,caixa.move(0,6),border_radius=16
    )
    pygame.draw.rect(
        tela,ROXO2,caixa,border_radius=16
    )
    pygame.draw.rect(
        tela,ROSA,caixa,3,border_radius=16
    )

    cursor="|" if int(animacao*2)%2==0 else ""

    txt(
        nome_jogador+cursor,
        grande,BRANCO,
        caixa.x+18,caixa.y+14
    )

    center(
        "Digite seu nome e aperte ENTER, ou clique em CONFIRMAR",
        pequena,ROSA2,305
    )

    return botao("CONFIRMAR",300,375,200,55)

# RESULTADO
# ============================================================
def resultado():
    parede()
    barra_cabecalho(90)

    r=receitas[receita_i]

    center("RECEITA PRONTA!",grande,ROSA,20)
    center(
        "Parabens, "+(nome_jogador or "Confeiteira(o)")+"!",
        fonte,AMARELO,60
    )

    center(r["nome"],grande,BRANCO,105)

    txt(
        "Pontos nesta receita: "+str(pontos),
        pequena,ROSA2,240,152
    )

    txt(
        "Pontuacao total: "+str(pontos_totais),
        pequena,AMARELO,240,175
    )

    # Mantem o desenho original da receita sem alterar nada nele.
    desenhar_base_da_receita(r,400,350)

    # CORRIGIDO: usa a mesma posicao absoluta em que a decoracao
    # foi colocada, ja que a comida e desenhada com o mesmo
    # cx=400, cy=350, escala=1 nas duas telas (decoracao e resultado).
    # Antes disso havia um fator de reescala (0.55) que empurrava as
    # decoracoes para perto do centro sem nenhuma relacao com o
    # tamanho real da comida, fazendo elas sumirem ou ficarem
    # deslocadas em relacao ao desenho.
    for d in decoracoes:
        decor(d[0],d[1],d[2])

    center("Sua receita decorada!",fonte,ROSA2,445)

    return (
        botao("JOGAR NOVAMENTE",210,480,380,50),
        botao("VOLTAR AO LIVRO",210,545,380,50)
    )

# ============================================================
# CIENTISTAS
# ============================================================
def desenhar_retrato(
    x,y,tipo,w=128,h=145
):
    img=IMAGENS_CIENTISTAS.get(tipo)

    if img is None:

        pygame.draw.rect(
            tela,ROXO2,
            (x,y,w,h),
            border_radius=18
        )

        im=pygame.font.Font(None,18).render(
            "imagem não encontrada",
            True,
            ROSA2
        )

        tela.blit(
            im,
            (
                x+(w-im.get_width())//2,
                y+h//2-9
            )
        )

        return

    iw,ih=img.get_size()

    lado=min(iw,ih)

    foco={
        "radio":.50,
        "dna":.62,
        "espaco":.34,
        "codigo":.48
    }.get(tipo,.50)

    cx=int(iw*foco)

    left=max(
        0,
        min(
            iw-lado,
            cx-lado//2
        )
    )

    top=max(
        0,
        (ih-lado)//2
    )

    crop=img.subsurface(
        pygame.Rect(
            left,
            top,
            lado,
            lado
        )
    ).copy()

    crop=pygame.transform.smoothscale(
        crop,
        (w,h)
    )

    pygame.draw.rect(
        tela,PRETO,
        (x+4,y+5,w,h),
        border_radius=16
    )

    tela.blit(
        crop,
        (x,y)
    )

    pygame.draw.rect(
        tela,ROSA2,
        (x,y,w,h),
        3,
        border_radius=16
    )

def cientistas_tela():
    parede()

    pygame.draw.rect(
        tela,(48,24,60),
        (0,0,LARGURA,125)
    )

    pygame.draw.line(
        tela,ROSA,
        (0,124),
        (LARGURA,124),
        3
    )

    b=voltar()

    center(
        "CIENTISTAS",
        titulo,
        ROSA,
        35
    )

    center(
        "Conheca quem inspirou nossas receitas",
        fonte,
        BRANCO,
        88
    )

    pos=[
        (30,150),
        (410,150),
        (30,365),
        (410,365)
    ]

    for i,(nome,rec,tipo) in enumerate(cientistas):

        x,y=pos[i]

        q=pygame.Rect(
            x,y,
            360,
            190
        )

        pygame.draw.rect(
            tela,PRETO,
            q.move(0,5),
            border_radius=24
        )

        pygame.draw.rect(
            tela,(76,39,96),
            q,
            border_radius=24
        )

        pygame.draw.rect(
            tela,ROSA,
            q,
            3,
            border_radius=24
        )

        desenhar_retrato(
            x+14,
            y+20,
            tipo,
            132,
            150
        )

        txt(
            nome,
            fonte,
            BRANCO,
            x+165,
            y+27
        )

        txt(
            rec,
            pequena,
            ROSA2,
            x+165,
            y+68
        )

        area={
            "radio":"QUIMICA",
            "dna":"BIOLOGIA / DNA",
            "espaco":"MATEMATICA / ESPACO",
            "codigo":"COMPUTACAO"
        }[tipo]

        txt(
            area,
            pygame.font.Font(None,18),
            AMARELO,
            x+165,
            y+104
        )

        if tipo=="radio":

            for k,c in enumerate([
                VERDE,
                AZUL,
                ROSA
            ]):
                pygame.draw.circle(
                    tela,
                    c,
                    (x+180+k*18,y+145),
                    4
                )

        elif tipo=="dna":

            pygame.draw.arc(
                tela,
                AZUL,
                (x+175,y+133,30,30),
                0,
                math.pi*2,
                2
            )

            pygame.draw.arc(
                tela,
                ROSA,
                (x+188,y+133,30,30),
                0,
                math.pi*2,
                2
            )

        elif tipo=="espaco":

            pygame.draw.circle(
                tela,
                AZUL,
                (x+192,y+148),
                11,
                2
            )

            pygame.draw.circle(
                tela,
                AMARELO,
                (x+192,y+148),
                3
            )

        else:

            pygame.draw.circle(
                tela,
                AMARELO,
                (x+194,y+148),
                10,
                3
            )

            pygame.draw.circle(
                tela,
                MARROM,
                (x+194,y+148),
                3
            )

    return b

# ============================================================
# LOOP
# ============================================================
while rodando:

    dt=clock.tick(60)/1000.0

    animacao+=dt

    atualiza_particulas()

    for e in pygame.event.get():

        # ----------------------------------------------------
        # SAIR
        # ----------------------------------------------------
        if e.type==pygame.QUIT:
            rodando=False

        if (
            e.type==pygame.KEYDOWN
            and e.key==pygame.K_ESCAPE
        ):
            rodando=False

        # ----------------------------------------------------
        # DIGITAR NOME (tela "nome")
        # ----------------------------------------------------
        if (
            e.type==pygame.KEYDOWN
            and tela_atual=="nome"
        ):
            if e.key==pygame.K_BACKSPACE:

                nome_jogador=nome_jogador[:-1]

            elif e.key==pygame.K_RETURN:

                if nome_jogador.strip()=="":
                    nome_jogador="Confeiteira(o)"

                pontos_totais+=pontos
                tela_atual="resultado"

            elif (
                e.unicode
                and e.unicode.isprintable()
                and len(nome_jogador)<14
            ):

                nome_jogador+=e.unicode

        # ----------------------------------------------------
        # CLIQUE
        # ----------------------------------------------------
        if (
            e.type==pygame.MOUSEBUTTONDOWN
            and e.button==1
        ):
            p=e.pos

            # =================================================
            # MENU
            # =================================================
            if tela_atual=="menu":

                j,c,s=menu()

                if j.collidepoint(p):

                    tela_atual="receitas"

                elif c.collidepoint(p):

                    tela_atual="cientistas"

                elif s.collidepoint(p):

                    rodando=False

            # =================================================
            # LIVRO DE RECEITAS
            # =================================================
            elif tela_atual=="receitas":

                b,bs=receitas_tela()

                if b.collidepoint(p):

                    tela_atual="menu"

                else:

                    for i,q in enumerate(bs):

                        if q.collidepoint(p):

                            receita_i=i

                            iniciar()

                            # IMPORTANTE:
                            # Antes dos ingredientes, mostra
                            # um quiz sobre a cientista.
                            preparar_quiz("ingredientes")

                            break

            # =================================================
            # INGREDIENTES
            # =================================================
            elif tela_atual=="ingredientes":

                b,c=ingredientes_tela()

                if b.collidepoint(p):

                    tela_atual="receitas"
                    arrastando=None

                elif c and c.collidepoint(p):

                    procs=receitas[
                        receita_i
                    ]["processos"]

                    processo_ok=False
                    tempo_processo=0.0

                    # Depois dos ingredientes, mostra um quiz
                    # e so entao vai para o PRIMEIRO processo.
                    preparar_quiz(procs[0])

                else:

                    for i in ingredientes:

                        if (
                            not i["colocado"]
                            and pygame.Rect(
                                i["x"],
                                i["y"],
                                i["w"],
                                i["h"]
                            ).collidepoint(p)
                        ):

                            arrastando=i

                            i["arrastando"]=True

                            i["dx"]=[
                                p[0]-i["x"]
                            ][0]

                            i["dy"]=[
                                p[1]-i["y"]
                            ][0]

                            break

            # =================================================
            # LIQUIDIFICADOR
            # =================================================
            elif tela_atual=="blender":

                b,c,m=liquidificador()

                if b.collidepoint(p):

                    tela_atual="ingredientes"

                elif c and c.collidepoint(p):

                    pontos+=25

                    processo_ok=False
                    tempo_processo=0.0

                    procs=receitas[
                        receita_i
                    ]["processos"]

                    # Encontra o próximo processo
                    # depois do blender.
                    indice=procs.index("blender")

                    if indice+1 < len(procs):

                        preparar_quiz(procs[indice+1])

                    else:

                        tela_atual="resultado"

                elif (
                    m
                    and m.collidepoint(p)
                    and not processo_ok
                    and tempo_processo<=0
                ):

                    tempo_processo=.01

                    efeito(
                        540,
                        285,
                        VERDE,
                        15
                    )

            # =================================================
            # FORNO
            # =================================================
            elif tela_atual=="forno":

                b,c,a=forno()

                if b.collidepoint(p):

                    tela_atual="ingredientes"

                elif c and c.collidepoint(p):

                    pontos+=30

                    processo_ok=False
                    tempo_processo=0.0

                    procs=receitas[
                        receita_i
                    ]["processos"]

                    indice=procs.index("forno")

                    if indice+1 < len(procs):

                        preparar_quiz(procs[indice+1])

                    else:

                        tela_atual="resultado"

                elif (
                    a
                    and a.collidepoint(p)
                    and not processo_ok
                    and tempo_processo<=0
                ):

                    tempo_processo=.01

                    efeito(
                        400,
                        300,
                        LARANJA,
                        15
                    )

            # =================================================
            # DECORAÇÃO
            # =================================================
            elif tela_atual=="decorar":

                b,bs,pr=decoracao()

                if b.collidepoint(p):
                    tela_atual="ingredientes"

                elif pr.collidepoint(p):
                    pontos+=20+len(decoracoes)*5

                    if nome_jogador.strip()=="":
                        tela_atual="nome"
                    else:
                        pontos_totais+=pontos
                        tela_atual="resultado"

                else:
                    # Seleciona a decoracao sem coloca-la ainda.
                    clicou_opcao=False

                    for q,t in bs:
                        if q.collidepoint(p):
                            confeito=t
                            clicou_opcao=True
                            break

                    # Depois de selecionar, cada clique na comida coloca
                    # outra unidade e mantem a decoracao selecionada.
                    if (
                        not clicou_opcao
                        and confeito
                        and 120<p[0]<600
                        and 280<p[1]<455
                    ):
                        decoracoes.append(
                            (confeito,p[0],p[1])
                        )

                        efeito(
                            p[0],p[1],ROSA,10
                        )

                        pontos+=5

            # =================================================
            # QUIZ
            # =================================================
            elif tela_atual=="quiz":

                opcoes_rects,continuar=quiz_tela()

                if not quiz_respondida:

                    for idx,q in enumerate(opcoes_rects):

                        if q.collidepoint(p):

                            quiz_selecionada=idx
                            quiz_respondida=True

                            if idx==quiz_atual["correta"]:
                                pontos+=15
                                efeito(400,300,VERDE,20)
                            else:
                                efeito(400,300,ROSA2,10)

                            break

                elif continuar and continuar.collidepoint(p):

                    tela_atual=destino_apos_quiz

            # =================================================
            # PEDIR NOME
            # =================================================
            elif tela_atual=="nome":

                c=tela_nome()

                if c.collidepoint(p):

                    if nome_jogador.strip()=="":
                        nome_jogador="Confeiteira(o)"

                    pontos_totais+=pontos
                    tela_atual="resultado"

            elif tela_atual=="resultado":

                j,l=resultado()

                if j.collidepoint(p):

                    iniciar()

                    preparar_quiz("ingredientes")

                elif l.collidepoint(p):

                    tela_atual="receitas"

            # =================================================
            # CIENTISTAS
            # =================================================
            elif tela_atual=="cientistas":

                b=cientistas_tela()

                if b.collidepoint(p):

                    tela_atual="menu"

        # ====================================================
        # ARRASTAR INGREDIENTE
        # ====================================================
        if (
            e.type==pygame.MOUSEMOTION
            and tela_atual=="ingredientes"
            and arrastando
        ):

            arrastando["x"] = (
                e.pos[0]-arrastando["dx"]
            )

            arrastando["y"] = (
                e.pos[1]-arrastando["dy"]
            )

        # ====================================================
        # SOLTAR INGREDIENTE
        # ====================================================
        if (
            e.type==pygame.MOUSEBUTTONUP
            and e.button==1
            and tela_atual=="ingredientes"
            and arrastando
        ):

            i=arrastando

            i["arrastando"]=False

            tig=pygame.Rect(
                445,
                275,
                315,
                150
            )

            obj=pygame.Rect(
                i["x"],
                i["y"],
                i["w"],
                i["h"]
            )

            if tig.colliderect(obj):

                i["colocado"]=True

                i["x"]=-500
                i["y"]=-500

                pontos+=10

                efeito(
                    600,
                    340,
                    receitas[receita_i]["cor"],
                    14
                )

            else:

                i["x"]=i["ox"]
                i["y"]=i["oy"]

            arrastando=None

    # ========================================================
    # TEMPO DO LIQUIDIFICADOR
    # ========================================================
    if (
        tela_atual=="blender"
        and not processo_ok
        and tempo_processo>0
    ):

        tempo_processo+=dt

        if random.random()<.45:

            efeito(
                540+random.randint(-35,35),
                285+random.randint(-25,45),
                ROSA2,
                2
            )

        if tempo_processo>=5.0:

            tempo_processo=5.0
            processo_ok=True

            pontos+=15

            efeito(
                540,
                285,
                VERDE,
                30
            )

    # ========================================================
    # TEMPO DO FORNO
    # ========================================================
    if (
        tela_atual=="forno"
        and not processo_ok
        and tempo_processo>0
    ):

        tempo_processo+=dt

        if random.random()<.30:

            efeito(
                400+random.randint(-40,40),
                300+random.randint(-20,25),
                LARANJA,
                2
            )

        if tempo_processo>=5.0:

            tempo_processo=5.0
            processo_ok=True

            pontos+=20

            efeito(
                400,
                300,
                AMARELO,
                30
            )

    # ========================================================
    # DESENHA A TELA ATUAL
    # ========================================================
    if tela_atual=="menu":

        menu()

    elif tela_atual=="receitas":

        receitas_tela()

    elif tela_atual=="ingredientes":

        ingredientes_tela()

    elif tela_atual=="blender":

        liquidificador()

    elif tela_atual=="forno":

        forno()

    elif tela_atual=="decorar":

        decoracao()

    elif tela_atual=="quiz":

        quiz_tela()

    elif tela_atual=="nome":

        tela_nome()

    elif tela_atual=="resultado":

        resultado()

    elif tela_atual=="cientistas":

        cientistas_tela()

    desenha_particulas()

    pygame.display.flip()

pygame.quit()
sys.exit()
