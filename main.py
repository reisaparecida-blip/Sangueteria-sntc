import pygame
import sys
import math
import random
import os

pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Sangueteria")
clock = pygame.time.Clock()

# ============================================================
# CORES
# ============================================================
FUNDO = (35, 20, 45)
ROXO = (105, 55, 145)
ROXO2 = (70, 35, 90)
ROSA = (255, 105, 175)
ROSA2 = (255, 175, 215)
BRANCO = (255, 255, 255)
AMARELO = (255, 220, 100)
VERDE = (90, 235, 150)
AZUL = (85, 190, 255)
VERMELHO = (235, 70, 105)
MARROM = (130, 75, 55)
CREME = (250, 225, 190)
CINZA = (175, 175, 185)
PRETO = (20, 12, 28)
LARANJA = (255, 155, 70)

titulo = pygame.font.Font(None, 64)
grande = pygame.font.Font(None, 42)
fonte = pygame.font.Font(None, 30)
pequena = pygame.font.Font(None, 21)

# ============================================================
# IMAGENS DAS CIENTISTAS
# A pasta "imagens" deve ficar junto deste main.py
# ============================================================
PASTA_IMAGENS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "imagens"
)

CAMINHOS_CIENTISTAS = {
    "radio": os.path.join(PASTA_IMAGENS, "Marie cury.png"),
    "dna": os.path.join(PASTA_IMAGENS, "Rosalind Franklin.png"),
    "espaco": os.path.join(PASTA_IMAGENS, "Katherine Johnson.png"),
    "codigo": os.path.join(PASTA_IMAGENS, "Ada lovelace.png"),
}

IMAGENS_CIENTISTAS = {}

for tipo, caminho in CAMINHOS_CIENTISTAS.items():
    try:
        if os.path.exists(caminho):
            IMAGENS_CIENTISTAS[tipo] = pygame.image.load(caminho).convert()
    except pygame.error:
        pass

# ============================================================
# RECEITAS
# ============================================================
receitas = [
    {
        "nome": "Radio-Glow Shake",
        "cientista": "Marie Curie",
        "cor": VERDE,
        "ingredientes": [
            ("Isotopo de Radio-Glow", 1),
            ("Baga Eletrica de Pantano", 2),
            ("Essencia de Radiacao Fashion", 1),
        ],
        "processos": ["blender", "decorar"],
    },
    {
        "nome": "Bio-Spooky",
        "cientista": "Rosalind Franklin",
        "cor": (190, 100, 255),
        "ingredientes": [
            ("Extrato de Planta Trepadeira Mutante", 1),
            ("Soro de Raio-X Fotografico", 1),
            ("Essencia de Estilo Genetico", 2),
        ],
        "processos": ["blender", "decorar"],
    },
    {
        "nome": "Cosmic Boo-cake",
        "cientista": "Katherine Johnson",
        "cor": AZUL,
        "ingredientes": [
            ("Acucar Gravitacional Lunar", 1),
            ("Massa de Baunilha das Trevas", 1),
            ("Granulado Estrela Cadente", 3),
        ],
        "processos": ["blender", "forno", "decorar"],
    },
    {
        "nome": "Steampunk Choco-Pie",
        "cientista": "Ada Lovelace",
        "cor": AMARELO,
        "ingredientes": [
            ("Massa de Baunilha Sombria", 1),
            ("Geleia de Frutas Vermelhas Ciberneticas", 1),
            ("Engrenagem de Chocolate Binario", 8),
        ],
        "processos": ["forno", "decorar"],
    },
]

cientistas = [
    ("Marie Curie", "Radio-Glow Shake", "radio"),
    ("Rosalind Franklin", "Bio-Spooky", "dna"),
    ("Katherine Johnson", "Cosmic Boo-cake", "espaco"),
    ("Ada Lovelace", "Steampunk Choco-Pie", "codigo"),
]

# ============================================================
# ESTADO DO JOGO
# ============================================================
rodando = True
tela_atual = "menu"
receita_i = 0
pontos = 0

ingredientes = []
arrastando = None
processo_ok = False
tempo_processo = 0.0
decoracoes = []
confeito = None
particulas = []
animacao = 0.0

# ============================================================
# UTILIDADES
# ============================================================
def txt(s, f, c, x, y):
    tela.blit(f.render(s, True, c), (x, y))


def center(s, f, c, y):
    im = f.render(s, True, c)
    tela.blit(im, ((LARGURA - im.get_width()) // 2, y))


def botao(s, x, y, w, h):
    r = pygame.Rect(x, y, w, h)

    pygame.draw.rect(
        tela, PRETO, r.move(0, 6),
        border_radius=min(24, h // 2)
    )
    pygame.draw.rect(
        tela, ROXO, r,
        border_radius=min(24, h // 2)
    )
    pygame.draw.rect(
        tela, ROSA, r, 3,
        border_radius=min(24, h // 2)
    )

    brilho = pygame.Rect(
        x + 7, y + 6,
        w - 14, max(5, h // 5)
    )
    pygame.draw.rect(
        tela, (175, 105, 205),
        brilho,
        border_radius=min(10, h // 4)
    )

    f = fonte
    im = f.render(s, True, BRANCO)

    if im.get_width() > w - 20:
        f = pygame.font.Font(
            None, max(18, int(fonte.get_height() * 0.72))
        )
        im = f.render(s, True, BRANCO)

    tela.blit(
        im,
        (x + (w - im.get_width()) // 2,
         y + (h - im.get_height()) // 2)
    )

    return r


def voltar():
    return botao("<", 25, 25, 72, 52)


def efeito(x, y, c=ROSA, n=12):
    for _ in range(n):
        a = random.random() * math.tau
        v = random.uniform(1, 3)
        particulas.append([
            x,
            y,
            math.cos(a) * v,
            math.sin(a) * v - 1,
            random.randint(18, 35),
            c
        ])


def atualiza_particulas():
    for p in particulas[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[3] += 0.05
        p[4] -= 1

        if p[4] <= 0:
            particulas.remove(p)


def desenha_particulas():
    for p in particulas:
        pygame.draw.circle(
            tela,
            p[5],
            (int(p[0]), int(p[1])),
            3
        )

# ============================================================
# ÍCONES DOS INGREDIENTES
# ============================================================
def icone(nome, cx, cy, s=0.7):
    n = nome.lower()

    if "baga" in n or "frutas vermelhas" in n:
        for ox, oy, c in [
            (-9, 3, VERMELHO),
            (9, 3, ROSA),
            (0, -7, VERMELHO)
        ]:
            pygame.draw.circle(
                tela, c,
                (int(cx + ox * s), int(cy + oy * s)),
                int(13 * s)
            )

        pygame.draw.polygon(
            tela, VERDE,
            [
                (cx, cy - 16 * s),
                (cx - 8 * s, cy - 23 * s),
                (cx, cy - 20 * s),
                (cx + 8 * s, cy - 23 * s),
                (cx + 5 * s, cy - 15 * s),
            ]
        )

    elif "planta" in n:
        pygame.draw.line(
            tela, VERDE,
            (cx, cy + 18 * s),
            (cx, cy - 18 * s),
            max(2, int(5 * s))
        )
        pygame.draw.ellipse(
            tela, VERDE,
            (cx - 25 * s, cy - 10 * s, 24 * s, 13 * s)
        )
        pygame.draw.ellipse(
            tela, (70, 190, 120),
            (cx + 1 * s, cy - 18 * s, 24 * s, 13 * s)
        )

    elif any(k in n for k in ["soro", "essencia", "isotopo", "geleia"]):
        pygame.draw.rect(
            tela, BRANCO,
            (cx - 13 * s, cy - 18 * s, 26 * s, 36 * s),
            border_radius=5
        )

        pygame.draw.rect(
            tela,
            VERDE if "isotopo" in n else ROSA2,
            (cx - 9 * s, cy - 7 * s, 18 * s, 22 * s),
            border_radius=4
        )

        pygame.draw.rect(
            tela, CINZA,
            (cx - 8 * s, cy - 25 * s, 16 * s, 8 * s),
            border_radius=3
        )

    elif "acucar" in n:
        pygame.draw.polygon(
            tela, BRANCO,
            [
                (cx - 18 * s, cy + 10 * s),
                (cx - 13 * s, cy - 12 * s),
                (cx + 13 * s, cy - 12 * s),
                (cx + 18 * s, cy + 10 * s)
            ]
        )
        pygame.draw.circle(
            tela, AMARELO,
            (int(cx), int(cy)),
            max(2, int(4 * s))
        )

    elif "massa" in n:
        pygame.draw.ellipse(
            tela, CREME,
            (cx - 28 * s, cy - 16 * s, 56 * s, 32 * s)
        )
        pygame.draw.ellipse(
            tela, (220, 180, 145),
            (cx - 13 * s, cy - 7 * s, 26 * s, 14 * s)
        )

    elif "granulado" in n:
        for ox, oy, c in [
            (-12, -5, ROSA),
            (0, 7, AMARELO),
            (12, -7, AZUL),
            (7, 8, VERDE)
        ]:
            pygame.draw.circle(
                tela, c,
                (int(cx + ox * s), int(cy + oy * s)),
                max(2, int(4 * s))
            )

    elif "engrenagem" in n:
        pygame.draw.circle(
            tela, AMARELO,
            (int(cx), int(cy)),
            int(15 * s)
        )
        pygame.draw.circle(
            tela, MARROM,
            (int(cx), int(cy)),
            int(6 * s)
        )

        for a in range(0, 360, 45):
            px = cx + math.cos(math.radians(a)) * 20 * s
            py = cy + math.sin(math.radians(a)) * 20 * s

            pygame.draw.rect(
                tela, AMARELO,
                (px - 4 * s, py - 4 * s, 8 * s, 8 * s),
                border_radius=2
            )

    else:
        pygame.draw.circle(
            tela, ROSA2,
            (int(cx), int(cy)),
            int(16 * s)
        )

# ============================================================
# INGREDIENTES
# ============================================================
def criar_ingredientes():
    global ingredientes

    ingredientes = []

    pos = [
        (35, 190), (265, 190),
        (35, 270), (265, 270),
        (35, 350), (265, 350),
        (35, 430), (265, 430),
        (35, 510), (265, 510)
    ]

    k = 0

    for nome, q in receitas[receita_i]["ingredientes"]:
        for u in range(q):
            x, y = pos[k]

            ingredientes.append({
                "nome": nome,
                "x": x,
                "y": y,
                "ox": x,
                "oy": y,
                "w": 195,
                "h": 62,
                "colocado": False,
                "arrastando": False,
                "u": u + 1
            })

            k += 1


def iniciar():
    global pontos, processo_ok
    global tempo_processo, decoracoes
    global confeito, arrastando

    pontos = 0
    processo_ok = False
    tempo_processo = 0.0
    decoracoes = []
    confeito = None
    arrastando = None

    criar_ingredientes()

# ============================================================
# FUNDO / CENÁRIO
# ============================================================
def parede():
    tela.fill(FUNDO)

    # Parede com padrão discreto
    for y in range(0, 450, 42):
        pygame.draw.line(
            tela,
            (55, 30, 68),
            (0, y),
            (800, y),
            1
        )

    for x in range(25, 800, 75):
        for y in range(20, 450, 70):
            pygame.draw.circle(
                tela,
                (62, 35, 78),
                (x, y),
                3 + ((x + y) // 10) % 4
            )

    # Prateleira
    pygame.draw.rect(
        tela, (72, 39, 55),
        (0, 115, 800, 12)
    )
    pygame.draw.rect(
        tela, (110, 62, 72),
        (0, 127, 800, 4)
    )

    # Frascos
    for x, c, h in [
        (55, AZUL, 42),
        (95, VERDE, 32),
        (700, ROSA, 38),
        (745, AMARELO, 48)
    ]:
        pygame.draw.rect(
            tela, c,
            (x, 115 - h, 24, h),
            border_radius=8
        )
        pygame.draw.rect(
            tela, BRANCO,
            (x + 6, 108 - h, 12, 8),
            border_radius=3
        )

    # Tubos de ensaio
    for x, c in [
        (160, AZUL),
        (188, ROSA),
        (216, VERDE)
    ]:
        pygame.draw.rect(
            tela, (190, 220, 235),
            (x, 75, 17, 48),
            border_radius=7
        )
        pygame.draw.rect(
            tela, c,
            (x + 3, 98, 11, 21),
            border_radius=5
        )

    # Moléculas decorativas discretas
    for cx, cy in [
        (625, 70),
        (675, 95),
        (290, 72)
    ]:
        pygame.draw.circle(
            tela, ROSA2, (cx, cy), 5
        )
        pygame.draw.circle(
            tela, AZUL, (cx + 18, cy + 12), 5
        )
        pygame.draw.line(
            tela, ROSA2,
            (cx + 4, cy + 3),
            (cx + 15, cy + 9),
            2
        )

# ============================================================
# TELAS
# ============================================================
def menu():
    parede()

    center("SANGUETERIA", titulo, ROSA, 150)
    center("LABORATORIO DE DOCES", grande, BRANCO, 220)
    center(
        "Prepare, misture, asse e decore!",
        fonte, ROSA2, 265
    )

    pygame.draw.ellipse(
        tela, PRETO, (245, 365, 315, 45)
    )
    pygame.draw.rect(
        tela, (125, 75, 58),
        (215, 335, 370, 70),
        border_radius=22
    )
    pygame.draw.rect(
        tela, (195, 130, 85),
        (225, 325, 350, 55),
        border_radius=22
    )

    icone("Isotopo de Radio-Glow", 310, 340, 0.75)
    icone("Granulado Estrela Cadente", 390, 340, 0.8)
    icone("Engrenagem de Chocolate Binario", 475, 340, 0.75)

    return (
        botao("JOGAR", 300, 420, 200, 60),
        botao("CIENTISTAS", 270, 490, 260, 55),
        botao("SAIR", 300, 555, 200, 42)
    )


def receitas_tela():
    parede()

    b = voltar()

    center("LIVRO DE RECEITAS", titulo, ROSA, 50)
    center(
        "Escolha uma receita para preparar",
        fonte, BRANCO, 120
    )

    bs = []

    for i, r in enumerate(receitas):
        x, y = [
            (55, 190),
            (415, 190),
            (55, 340),
            (415, 340)
        ][i]

        q = pygame.Rect(x, y, 330, 115)

        pygame.draw.rect(
            tela, ROXO, q,
            border_radius=18
        )
        pygame.draw.rect(
            tela, ROSA, q, 3,
            border_radius=18
        )

        icone(
            r["ingredientes"][0][0],
            x + 40, y + 50, .65
        )

        txt(
            r["nome"], fonte, BRANCO,
            x + 80, y + 20
        )
        txt(
            r["cientista"], pequena, ROSA2,
            x + 80, y + 65
        )

        bs.append(q)

    return b, bs


def preparo():
    parede()

    b = voltar()
    r = receitas[receita_i]

    center(r["nome"], titulo, ROSA, 50)
    center(
        "Cientista: " + r["cientista"],
        fonte, BRANCO, 115
    )

    pygame.draw.rect(
        tela, ROXO2,
        (75, 170, 650, 235),
        border_radius=20
    )
    pygame.draw.rect(
        tela, ROSA,
        (75, 170, 650, 235),
        3,
        border_radius=20
    )

    txt(
        "INGREDIENTES",
        grande, ROSA,
        105, 195
    )

    y = 250

    for nome, q in r["ingredientes"]:
        icone(nome, 125, y + 8, .55)
        txt(
            f"{q}x {nome}",
            pequena, BRANCO,
            155, y
        )
        y += 42

    center(
        "Cada receita tem uma etapa especial de preparo!",
        pequena, ROSA2, 430
    )

    return b, botao("COMEÇAR", 300, 490, 200, 55)


def bancada():
    pygame.draw.rect(
        tela, (57, 28, 74),
        (0, 450, 800, 150)
    )
    pygame.draw.rect(
        tela, ROXO,
        (0, 450, 800, 7)
    )


# ============================================================
# TIGELA
# ============================================================
def tigela():
    # sombra
    pygame.draw.ellipse(
        tela, PRETO,
        (455, 365, 310, 55)
    )

    # corpo externo da tigela
    pygame.draw.ellipse(
        tela, (85, 155, 210),
        (445, 270, 315, 165)
    )

    # parte superior
    pygame.draw.ellipse(
        tela, (210, 240, 250),
        (460, 258, 285, 105)
    )

    # interior
    pygame.draw.ellipse(
        tela, (75, 110, 170),
        (475, 282, 255, 86)
    )

    pygame.draw.ellipse(
        tela, (238, 250, 255),
        (492, 290, 220, 62)
    )

    # borda da tigela
    pygame.draw.arc(
        tela,
        BRANCO,
        (460, 258, 285, 105),
        math.pi,
        math.tau,
        5
    )

    feitos = [
        i for i in ingredientes
        if i["colocado"]
    ]

    for k, i in enumerate(feitos):
        icone(
            i["nome"],
            515 + (k % 5) * 43,
            325 + (k // 5) * 25,
            .42
        )

    center("TIGELA", fonte, BRANCO, 395)


def ingrediente(i):
    if i["colocado"]:
        return

    q = pygame.Rect(
        i["x"], i["y"],
        i["w"], i["h"]
    )

    if i["arrastando"]:
        pygame.draw.rect(
            tela, PRETO, q.move(4, 4),
            border_radius=14
        )

    pygame.draw.rect(
        tela, ROXO, q,
        border_radius=14
    )
    pygame.draw.rect(
        tela, ROSA, q, 2,
        border_radius=14
    )

    icone(
        i["nome"],
        i["x"] + 30,
        i["y"] + 31,
        .58
    )

    f = pequena

    if pequena.size(i["nome"])[0] >= 135:
        f = pygame.font.Font(None, 17)

    txt(
        i["nome"], f, BRANCO,
        i["x"] + 57,
        i["y"] + 9
    )

    if i["u"] > 1:
        txt(
            "unidade " + str(i["u"]),
            pygame.font.Font(None, 16),
            ROSA2,
            i["x"] + 57,
            i["y"] + 38
        )


def ingredientes_tela():
    parede()

    r = receitas[receita_i]
    b = voltar()

    txt(
        r["nome"], grande, ROSA,
        115, 28
    )
    txt(
        "Cientista: " + r["cientista"],
        pequena, BRANCO,
        118, 72
    )
    txt(
        "Pontos: " + str(pontos),
        fonte, AMARELO,
        650, 32
    )

    center(
        "ARRASTE OS INGREDIENTES PARA A TIGELA!",
        fonte, ROSA2, 110
    )

    bancada()
    tigela()

    for i in ingredientes:
        ingrediente(i)

    feitos = sum(
        i["colocado"] for i in ingredientes
    )

    txt(
        f"INGREDIENTES: {feitos}/{len(ingredientes)}",
        fonte, BRANCO,
        500, 180
    )

    c = None

    if feitos == len(ingredientes):
        center(
            "TODOS OS INGREDIENTES!",
            grande, VERDE, 455
        )
        c = botao(
            "CONTINUAR",
            300, 505, 200, 55
        )

    return b, c


# ============================================================
# LIQUIDIFICADOR
# ============================================================
def liquidificador():
    parede()

    r = receitas[receita_i]
    b = voltar()

    txt(r["nome"], grande, ROSA, 115, 28)
    txt(
        "Liquidificador magico",
        fonte, ROSA2, 115, 72
    )
    txt(
        "Pontos: " + str(pontos),
        fonte, AMARELO, 650, 32
    )

    center(
        "MISTURE A RECEITA!",
        titulo, ROSA, 105
    )

    x, y = 430, 170

    pygame.draw.ellipse(
        tela, PRETO,
        (x - 15, y + 190, 220, 30)
    )

    pygame.draw.rect(
        tela, ROXO,
        (x + 35, y + 135, 150, 65),
        border_radius=18
    )
    pygame.draw.rect(
        tela, ROSA,
        (x + 35, y + 135, 150, 65),
        3,
        border_radius=18
    )

    pygame.draw.polygon(
        tela, (180, 225, 240),
        [
            (x + 45, y + 25),
            (x + 175, y + 25),
            (x + 160, y + 150),
            (x + 60, y + 150)
        ]
    )

    pygame.draw.polygon(
        tela, r["cor"],
        [
            (x + 57, y + 80),
            (x + 164, y + 80),
            (x + 157, y + 142),
            (x + 65, y + 142)
        ]
    )

    pygame.draw.rect(
        tela, (70, 65, 80),
        (x + 38, y + 10, 145, 24),
        border_radius=8
    )

    pygame.draw.line(
        tela, BRANCO,
        (x + 110, y + 115),
        (x + 88, y + 105),
        3
    )
    pygame.draw.line(
        tela, BRANCO,
        (x + 110, y + 115),
        (x + 132, y + 105),
        3
    )

    if not processo_ok:
        for k in range(5):
            pygame.draw.circle(
                tela, ROSA2,
                (
                    int(x + 70 +
                        ((animacao * 50 + k * 25) % 80)),
                    int(
                        y + 95 +
                        math.sin(animacao * 5 + k) * 12
                    )
                ),
                6
            )

    pygame.draw.circle(
        tela,
        ROSA if processo_ok else AMARELO,
        (x + 110, y + 165),
        12
    )

    # Barra de progresso de 5 segundos
    pygame.draw.rect(
        tela, ROXO2,
        (x + 25, y + 215, 170, 14),
        border_radius=7
    )

    pygame.draw.rect(
        tela, ROSA,
        (
            x + 25,
            y + 215,
            int(170 * min(tempo_processo / 5.0, 1.0)),
            14
        ),
        border_radius=7
    )

    center(
        "Clique em MISTURAR para ativar o liquidificador",
        pequena, BRANCO, 430
    )

    if processo_ok:
        center(
            "MISTURA PERFEITA!",
            grande, VERDE, 465
        )
        return (
            b,
            botao("CONTINUAR", 300, 520, 200, 55),
            None
        )

    return (
        b,
        None,
        botao("MISTURAR", 300, 520, 200, 55)
    )


# ============================================================
# FORNO
# ============================================================
def forno():
    parede()

    r = receitas[receita_i]
    b = voltar()

    txt(r["nome"], grande, ROSA, 115, 28)
    txt(
        "Forno de laboratorio",
        fonte, ROSA2, 115, 72
    )
    txt(
        "Pontos: " + str(pontos),
        fonte, AMARELO, 650, 32
    )

    center(
        "HORA DE ASSAR!",
        titulo, ROSA, 100
    )

    x, y = 265, 145

    pygame.draw.ellipse(
        tela, PRETO,
        (x - 15, y + 325, 300, 28)
    )

    pygame.draw.rect(
        tela, ROXO,
        (x, y, 270, 315),
        border_radius=22
    )

    pygame.draw.rect(
        tela, ROSA,
        (x, y, 270, 315),
        4,
        border_radius=22
    )

    pygame.draw.rect(
        tela, ROXO2,
        (x + 20, y + 20, 230, 50),
        border_radius=10
    )

    txt(
        "FORNO DE LABORATORIO",
        pequena, BRANCO,
        x + 37, y + 36
    )

    pygame.draw.rect(
        tela, (60, 35, 60),
        (x + 30, y + 90, 210, 150),
        border_radius=12
    )

    pygame.draw.rect(
        tela, CINZA,
        (x + 30, y + 90, 210, 150),
        4,
        border_radius=12
    )

    if processo_ok:
        pygame.draw.rect(
            tela, (130, 60, 50),
            (x + 36, y + 96, 198, 138),
            border_radius=9
        )
        pygame.draw.circle(
            tela, LARANJA,
            (x + 135, y + 165),
            48
        )
        pygame.draw.circle(
            tela, AMARELO,
            (x + 135, y + 160),
            30
        )

    pygame.draw.rect(
        tela, CINZA,
        (x + 60, y + 180, 150, 35),
        border_radius=7
    )

    pygame.draw.rect(
        tela, MARROM,
        (x + 75, y + 168, 120, 30),
        border_radius=12
    )

    pygame.draw.circle(
        tela,
        ROSA if processo_ok else AMARELO,
        (x + 65, y + 270),
        13
    )
    pygame.draw.circle(
        tela,
        VERDE if processo_ok else CINZA,
        (x + 135, y + 270),
        13
    )
    pygame.draw.circle(
        tela, AZUL,
        (x + 205, y + 270),
        13
    )

    pygame.draw.rect(
        tela, ROXO2,
        (x + 40, y + 295, 190, 12),
        border_radius=6
    )

    pygame.draw.rect(
        tela, LARANJA,
        (
            x + 40,
            y + 295,
            int(190 * min(tempo_processo / 5.0, 1.0)),
            12
        ),
        border_radius=6
    )

    center(
        "Clique em ASSAR para ligar o forno",
        pequena, BRANCO, 485
    )

    if processo_ok:
        center(
            "ASSADO PERFEITO!",
            grande, VERDE, 450
        )
        return (
            b,
            botao("CONTINUAR", 300, 525, 200, 55),
            None
        )

    return (
        b,
        None,
        botao("ASSAR", 300, 525, 200, 55)
    )


# ============================================================
# DECORAÇÃO
# ============================================================
def decor(t, x, y, s=1):
    if t == "morango":
        pygame.draw.circle(
            tela, VERMELHO,
            (int(x), int(y)),
            int(12 * s)
        )
        pygame.draw.polygon(
            tela, VERDE,
            [
                (x, y - 7),
                (x - 8, y - 15),
                (x, y - 12),
                (x + 8, y - 15)
            ]
        )

    elif t == "chocolate":
        pygame.draw.circle(
            tela, MARROM,
            (int(x), int(y)),
            int(12 * s)
        )
        pygame.draw.circle(
            tela, CREME,
            (int(x - 4 * s), int(y - 3 * s)),
            max(1, int(2 * s))
        )

    elif t == "estrela":
        pts = []

        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            rr = 15 * s if k % 2 == 0 else 7 * s
            pts.append(
                (
                    x + math.cos(a) * rr,
                    y + math.sin(a) * rr
                )
            )

        pygame.draw.polygon(
            tela, AMARELO, pts
        )

    elif t == "engrenagem":
        pygame.draw.circle(
            tela, AMARELO,
            (int(x), int(y)),
            int(11 * s)
        )
        pygame.draw.circle(
            tela, MARROM,
            (int(x), int(y)),
            int(4 * s)
        )

    else:
        pygame.draw.circle(
            tela, ROSA,
            (int(x), int(y)),
            int(9 * s)
        )


def decoracao():
    parede()

    r = receitas[receita_i]
    b = voltar()

    txt(r["nome"], grande, ROSA, 115, 28)
    txt(
        "Estacao de decoracao",
        fonte, ROSA2, 115, 72
    )
    txt(
        "Pontos: " + str(pontos),
        fonte, AMARELO, 650, 32
    )

    center(
        "DECORE SUA RECEITA!",
        titulo, ROSA, 100
    )

    pygame.draw.ellipse(
        tela, PRETO,
        (100, 390, 585, 105)
    )
    pygame.draw.ellipse(
        tela, (150, 90, 60),
        (105, 350, 580, 145)
    )
    pygame.draw.ellipse(
        tela, (195, 130, 85),
        (120, 360, 550, 120)
    )

    if "Shake" in r["nome"] or "Spooky" in r["nome"]:
        pygame.draw.rect(
            tela, (180, 230, 245),
            (330, 305, 140, 130),
            border_radius=20
        )
        pygame.draw.rect(
            tela, r["cor"],
            (340, 345, 120, 80),
            border_radius=14
        )
        pygame.draw.rect(
            tela, ROSA2,
            (350, 290, 100, 25),
            border_radius=8
        )

    else:
        pygame.draw.ellipse(
            tela, CREME,
            (285, 330, 230, 100)
        )
        pygame.draw.ellipse(
            tela,
            MARROM if "Choco" in r["nome"] else AZUL,
            (300, 340, 200, 65)
        )

    for d in decoracoes:
        decor(d[0], d[1], d[2])

    pygame.draw.rect(
        tela, ROXO2,
        (620, 175, 150, 230),
        border_radius=18
    )
    pygame.draw.rect(
        tela, ROSA,
        (620, 175, 150, 230),
        2,
        border_radius=18
    )

    txt(
        "CONFEITOS",
        pequena, BRANCO,
        650, 192
    )

    tipos = (
        ["morango", "confeito", "estrela"]
        if "Shake" in r["nome"]
        else
        (
            ["confeito", "chocolate", "estrela"]
            if "Spooky" in r["nome"]
            else
            (
                ["estrela", "confeito", "morango"]
                if "Cosmic" in r["nome"]
                else
                ["engrenagem", "chocolate", "confeito"]
            )
        )
    )

    bs = []

    for k, t in enumerate(tipos):
        q = pygame.Rect(
            640, 230 + k * 52,
            110, 40
        )

        pygame.draw.rect(
            tela, ROXO, q,
            border_radius=10
        )
        pygame.draw.rect(
            tela, ROSA, q, 2,
            border_radius=10
        )

        decor(
            t,
            660,
            250 + k * 52,
            .55
        )

        txt(
            t.upper(),
            pygame.font.Font(None, 15),
            BRANCO,
            680,
            243 + k * 52
        )

        bs.append((q, t))

    center(
        "Escolha um confeito e clique na comida",
        pequena, BRANCO, 505
    )

    return (
        b,
        bs,
        botao("PRONTO!", 300, 535, 200, 50)
    )


# ============================================================
# RESULTADO
# ============================================================
def resultado():
    tela.fill(FUNDO)

    center(
        "RECEITA PRONTA!",
        titulo, ROSA, 70
    )
    center(
        "PARABENS!",
        grande, AMARELO, 145
    )
    center(
        receitas[receita_i]["nome"],
        grande, BRANCO, 205
    )
    center(
        "Pontuacao: " + str(pontos),
        fonte, ROSA2, 255
    )

    pygame.draw.ellipse(
        tela, (195, 130, 85),
        (285, 305, 230, 120)
    )
    pygame.draw.ellipse(
        tela, CREME,
        (300, 315, 200, 80)
    )

    for k in range(8):
        decor(
            ["morango", "estrela", "confeito"][k % 3],
            330 + (k % 4) * 45,
            340 + (k // 4) * 35,
            .6
        )

    return (
        botao(
            "JOGAR NOVAMENTE",
            230, 470, 340, 50
        ),
        botao(
            "VOLTAR AO LIVRO",
            230, 530, 340, 50
        )
    )


# ============================================================
# RETRATO DAS CIENTISTAS
# ============================================================
def desenhar_retrato(x, y, tipo, w=132, h=150):
    img = IMAGENS_CIENTISTAS.get(tipo)

    if img is None:
        pygame.draw.rect(
            tela, ROXO2,
            (x, y, w, h),
            border_radius=16
        )

        center_text = pygame.font.Font(
            None, 18
        ).render(
            "imagem nao encontrada",
            True, ROSA2
        )

        tela.blit(
            center_text,
            (
                x + (w - center_text.get_width()) // 2,
                y + h // 2 - 9
            )
        )
        return

    iw, ih = img.get_size()

    # Mantem a proporcao e escolhe um enquadramento
    # diferente para cada imagem.
    proporcao = w / h

    crop_w = min(iw, int(ih * proporcao))
    crop_h = min(ih, int(crop_w / proporcao))

    foco = {
        # Marie: pessoa central
        "radio": 0.52,

        # Rosalind: pessoa mais para a direita
        "dna": 0.66,

        # Katherine: pessoa fica mais para a esquerda.
        # Esse valor corrige o enquadramento dela.
        "espaco": 0.34,

        # Ada: pessoa central
        "codigo": 0.54,
    }.get(tipo, 0.50)

    cx = int(iw * foco)

    left = int(cx - crop_w / 2)
    top = int((ih - crop_h) / 2)

    left = max(0, min(iw - crop_w, left))
    top = max(0, min(ih - crop_h, top))

    crop = img.subsurface(
        pygame.Rect(
            left,
            top,
            crop_w,
            crop_h
        )
    ).copy()

    crop = pygame.transform.smoothscale(
        crop,
        (w, h)
    )

    # Moldura limpa, sem rabiscos por cima.
    pygame.draw.rect(
        tela, PRETO,
        (x + 4, y + 5, w, h),
        border_radius=16
    )

    tela.blit(crop, (x, y))

    pygame.draw.rect(
        tela, ROSA2,
        (x, y, w, h),
        3,
        border_radius=16
    )


# ============================================================
# TELA DAS CIENTISTAS
# ============================================================
def cientistas_tela():
    parede()

    # Cabecalho limpo
    pygame.draw.rect(
        tela, (48, 24, 60),
        (0, 0, LARGURA, 125)
    )

    pygame.draw.line(
        tela, ROSA,
        (0, 124),
        (LARGURA, 124),
        3
    )

    b = voltar()

    center(
        "CIENTISTAS",
        titulo, ROSA, 35
    )

    center(
        "Conheca quem inspirou nossas receitas",
        fonte, BRANCO, 88
    )

    # Cartoes mais organizados.
    pos = [
        (30, 150),
        (410, 150),
        (30, 365),
        (410, 365)
    ]

    areas = {
        "radio": "QUIMICA",
        "dna": "BIOLOGIA / DNA",
        "espaco": "MATEMATICA / ESPACO",
        "codigo": "COMPUTACAO",
    }

    for i, (nome, rec, tipo) in enumerate(cientistas):
        x, y = pos[i]

        q = pygame.Rect(
            x, y, 360, 190
        )

        # sombra
        pygame.draw.rect(
            tela, PRETO,
            q.move(0, 5),
            border_radius=24
        )

        # cartao
        pygame.draw.rect(
            tela, (76, 39, 96),
            q,
            border_radius=24
        )

        pygame.draw.rect(
            tela, ROSA,
            q, 3,
            border_radius=24
        )

        # foto
        desenhar_retrato(
            x + 14,
            y + 20,
            tipo,
            132,
            150
        )

        # texto
        txt(
            nome,
            fonte,
            BRANCO,
            x + 165,
            y + 27
        )

        txt(
            rec,
            pequena,
            ROSA2,
            x + 165,
            y + 68
        )

        txt(
            areas[tipo],
            pygame.font.Font(None, 18),
            AMARELO,
            x + 165,
            y + 104
        )

        # Apenas um detalhe pequeno e fixo no cartao.
        # Nada de linhas curvas atravessando a tela.
        if tipo == "radio":
            for k, c in enumerate([
                VERDE, AZUL, ROSA
            ]):
                pygame.draw.circle(
                    tela,
                    c,
                    (x + 180 + k * 18, y + 145),
                    4
                )

        elif tipo == "dna":
            pygame.draw.line(
                tela, AZUL,
                (x + 180, y + 138),
                (x + 205, y + 153),
                2
            )
            pygame.draw.line(
                tela, ROSA,
                (x + 205, y + 138),
                (x + 180, y + 153),
                2
            )
            pygame.draw.circle(
                tela, AZUL,
                (x + 180, y + 138),
                3
            )
            pygame.draw.circle(
                tela, ROSA,
                (x + 205, y + 138),
                3
            )

        elif tipo == "espaco":
            pygame.draw.circle(
                tela, AZUL,
                (x + 193, y + 148),
                11, 2
            )
            pygame.draw.circle(
                tela, AMARELO,
                (x + 193, y + 148),
                3
            )

        else:
            pygame.draw.circle(
                tela, AMARELO,
                (x + 194, y + 148),
                10, 3
            )
            pygame.draw.circle(
                tela, MARROM,
                (x + 194, y + 148),
                3
            )

    return b


# ============================================================
# LOOP PRINCIPAL
# ============================================================
while rodando:
    dt = clock.tick(60) / 1000.0
    animacao += dt

    atualiza_particulas()

    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            rodando = False

        # ----------------------------------------------------
        # CLIQUE
        # ----------------------------------------------------
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            p = e.pos

            # MENU
            if tela_atual == "menu":
                j, c, s = menu()

                if j.collidepoint(p):
                    tela_atual = "receitas"

                elif c.collidepoint(p):
                    tela_atual = "cientistas"

                elif s.collidepoint(p):
                    rodando = False

            # RECEITAS
            elif tela_atual == "receitas":
                b, bs = receitas_tela()

                if b.collidepoint(p):
                    tela_atual = "menu"

                else:
                    for i, q in enumerate(bs):
                        if q.collidepoint(p):
                            receita_i = i
                            tela_atual = "preparo"
                            break

            # PREPARO
            elif tela_atual == "preparo":
                b, c = preparo()

                if b.collidepoint(p):
                    tela_atual = "receitas"

                elif c.collidepoint(p):
                    iniciar()
                    tela_atual = "ingredientes"

            # INGREDIENTES
            elif tela_atual == "ingredientes":
                b, c = ingredientes_tela()

                if b.collidepoint(p):
                    tela_atual = "receitas"
                    arrastando = None

                elif c and c.collidepoint(p):
                    proc = receitas[receita_i]["processos"][0]
                    processo_ok = False
                    tempo_processo = 0.0
                    tela_atual = proc

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
                            arrastando = i
                            i["arrastando"] = True
                            i["dx"] = p[0] - i["x"]
                            i["dy"] = p[1] - i["y"]
                            break

            # LIQUIDIFICADOR
            elif tela_atual == "blender":
                b, c, m = liquidificador()

                if b.collidepoint(p):
                    tela_atual = "ingredientes"

                elif c and c.collidepoint(p):
                    pontos += 25
                    processo_ok = False
                    tempo_processo = 0.0

                    procs = receitas[receita_i]["processos"]

                    if "forno" in procs:
                        tela_atual = "forno"
                    else:
                        tela_atual = "decorar"

                elif (
                    m
                    and m.collidepoint(p)
                    and not processo_ok
                    and tempo_processo <= 0
                ):
                    tempo_processo = 0.01
                    efeito(
                        540, 285,
                        VERDE, 15
                    )

            # FORNO
            elif tela_atual == "forno":
                b, c, a = forno()

                if b.collidepoint(p):
                    tela_atual = "ingredientes"

                elif c and c.collidepoint(p):
                    pontos += 30
                    processo_ok = False
                    tempo_processo = 0.0

                    if "decorar" in receitas[receita_i]["processos"]:
                        tela_atual = "decorar"
                    else:
                        tela_atual = "resultado"

                elif (
                    a
                    and a.collidepoint(p)
                    and not processo_ok
                    and tempo_processo <= 0
                ):
                    tempo_processo = 0.01
                    efeito(
                        400, 300,
                        LARANJA, 15
                    )

            # DECORAÇÃO
            elif tela_atual == "decorar":
                b, bs, pr = decoracao()

                if b.collidepoint(p):
                    tela_atual = "ingredientes"

                elif pr.collidepoint(p):
                    pontos += 20 + len(decoracoes) * 5
                    tela_atual = "resultado"

                else:
                    for q, t in bs:
                        if q.collidepoint(p):
                            confeito = t
                            break

                    if (
                        confeito
                        and 120 < p[0] < 600
                        and 300 < p[1] < 455
                    ):
                        decoracoes.append(
                            (confeito, p[0], p[1])
                        )
                        efeito(
                            p[0], p[1],
                            ROSA, 10
                        )
                        pontos += 5
                        confeito = None

            # RESULTADO
            elif tela_atual == "resultado":
                j, l = resultado()

                if j.collidepoint(p):
                    iniciar()
                    tela_atual = "ingredientes"

                elif l.collidepoint(p):
                    tela_atual = "receitas"

            # CIENTISTAS
            elif tela_atual == "cientistas":
                b = cientistas_tela()

                if b.collidepoint(p):
                    tela_atual = "menu"

        # ----------------------------------------------------
        # ARRASTAR INGREDIENTE
        # ----------------------------------------------------
        if (
            e.type == pygame.MOUSEMOTION
            and tela_atual == "ingredientes"
            and arrastando
        ):
            arrastando["x"] = (
                e.pos[0] - arrastando["dx"]
            )
            arrastando["y"] = (
                e.pos[1] - arrastando["dy"]
            )

        # ----------------------------------------------------
        # SOLTAR INGREDIENTE
        # ----------------------------------------------------
        if (
            e.type == pygame.MOUSEBUTTONUP
            and e.button == 1
            and tela_atual == "ingredientes"
            and arrastando
        ):
            i = arrastando
            i["arrastando"] = False

            tig = pygame.Rect(
                445, 275, 315, 150
            )

            obj = pygame.Rect(
                i["x"],
                i["y"],
                i["w"],
                i["h"]
            )

            if tig.colliderect(obj):
                i["colocado"] = True
                i["x"] = -500
                i["y"] = -500
                pontos += 10

                efeito(
                    600, 335,
                    ROSA, 12
                )

            else:
                i["x"] = i["ox"]
                i["y"] = i["oy"]

            arrastando = None

    # ========================================================
    # PROCESSO DO LIQUIDIFICADOR: 5 SEGUNDOS
    # ========================================================
    if (
        tela_atual == "blender"
        and not processo_ok
        and tempo_processo > 0
    ):
        tempo_processo += dt

        if random.random() < 0.45:
            efeito(
                540 + random.randint(-35, 35),
                285 + random.randint(-25, 45),
                ROSA2,
                2
            )

        if tempo_processo >= 5.0:
            tempo_processo = 5.0
            processo_ok = True
            pontos += 15

            efeito(
                540, 285,
                VERDE, 30
            )

    # ========================================================
    # PROCESSO DO FORNO: 5 SEGUNDOS
    # ========================================================
    if (
        tela_atual == "forno"
        and not processo_ok
        and tempo_processo > 0
    ):
        tempo_processo += dt

        if random.random() < 0.30:
            efeito(
                400 + random.randint(-40, 40),
                300 + random.randint(-20, 25),
                LARANJA,
                2
            )

        if tempo_processo >= 5.0:
            tempo_processo = 5.0
            processo_ok = True
            pontos += 20

            efeito(
                400, 300,
                AMARELO, 30
            )

    # ========================================================
    # DESENHA A TELA ATUAL
    # ========================================================
    if tela_atual == "menu":
        menu()

    elif tela_atual == "receitas":
        receitas_tela()

    elif tela_atual == "preparo":
        preparo()

    elif tela_atual == "ingredientes":
        ingredientes_tela()

    elif tela_atual == "blender":
        liquidificador()

    elif tela_atual == "forno":
        forno()

    elif tela_atual == "decorar":
        decoracao()

    elif tela_atual == "resultado":
        resultado()

    elif tela_atual == "cientistas":
        cientistas_tela()

    desenha_particulas()
    pygame.display.flip()

pygame.quit()
sys.exit()
