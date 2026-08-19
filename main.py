import pygame
import sys

pygame.init()

# Tela
LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Sangueteria")

# Cores
FUNDO = (35, 20, 45)
ROSA = (255, 120, 180)
BRANCO = (255, 255, 255)
ROXO = (100, 50, 140)

# Fontes
titulo = pygame.font.Font(None, 80)
fonte = pygame.font.Font(None, 40)
fonte_pequena = pygame.font.Font(None, 30)

# Controle das telas
tela_atual = "menu"

receita_selecionada = None

# Receitas
receitas = [
    "Radio-Glow Shake",
    "Bio-Spooky",
    "Cosmic Boo-cake",
    "Steampunk Choco-Pie"
]


def texto(msg, fonte_usada, cor, x, y):
    imagem = fonte_usada.render(msg, True, cor)
    tela.blit(imagem, (x, y))


def botao(nome, x, y, largura, altura):

    retangulo = pygame.Rect(x, y, largura, altura)

    pygame.draw.rect(
        tela,
        ROXO,
        retangulo,
        border_radius=15
    )

    texto(
        nome,
        fonte,
        BRANCO,
        x + 15,
        y + 8
    )

    return retangulo


def seta_voltar():

    area = pygame.Rect(25, 25, 80, 60)

    pygame.draw.line(
        tela,
        ROSA,
        (70, 55),
        (110, 55),
        6
    )

    pygame.draw.polygon(
        tela,
        ROSA,
        [
            (70, 55),
            (95, 35),
            (95, 75)
        ]
    )

    return 
arearodando = True


while rodando:

    tela.fill(FUNDO)


    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False


        if evento.type == pygame.MOUSEBUTTONDOWN:


            # MENU

            if tela_atual == "menu":

                if jogar.collidepoint(evento.pos):

                    # agora o JOGAR abre direto o livro
                    tela_atual = "receitas"


                if sair.collidepoint(evento.pos):

                    rodando = False



            # LIVRO DE RECEITAS

            elif tela_atual == "receitas":

                if voltar.collidepoint(evento.pos):

                    tela_atual = "menu"


                for i, bot in enumerate(botoes_receitas):

                    if bot.collidepoint(evento.pos):

                        receita_selecionada = receitas[i]
                        tela_atual = "preparo"



            # TELA DA RECEITA

            elif tela_atual == "preparo":

                if voltar.collidepoint(evento.pos):

                    tela_atual = "receitas"



    # =====================
    # MENU PRINCIPAL
    # =====================

    if tela_atual == "menu":

        texto(
            "SANGUETERIA",
            titulo,
            ROSA,
            190,
            100
        )


        jogar = botao(
            "JOGAR",
            300,
            260,
            200,
            60
        )


        sair = botao(
            "SAIR",
            300,
            360,
            200,
            60
        )



    # =====================
    # LIVRO DE RECEITAS
    # =====================

    elif tela_atual == "receitas":

        voltar = seta_voltar()


        texto(
            "LIVRO DE RECEITAS",
            titulo,
            ROSA,
            120,
            60
        )


        botoes_receitas = []

        y = 180


        for receita in receitas:

            bot = botao(
                receita,
                220,
                y,
                360,
                55
            )


            botoes_receitas.append(bot)

            y += 80
                # =====================
    # TELA DA RECEITA
    # =====================

    elif tela_atual == "preparo":

        voltar = seta_voltar()


        texto(
            receita_selecionada,
            titulo,
            ROSA,
            100,
            90
        )


        pygame.draw.line(
            tela,
            ROSA,
            (100, 180),
            (700, 180),
            3
        )


        texto(
            "INGREDIENTES",
            fonte,
            ROSA,
            100,
            230
        )


        if receita_selecionada == "Radio-Glow Shake":

            texto(
                "Ingredientes da receita",
                fonte_pequena,
                BRANCO,
                100,
                280
            )

            texto(
                "Vamos adicionar a receita do PDF aqui.",
                fonte_pequena,
                BRANCO,
                100,
                320
            )


        else:

            texto(
                "Ingredientes em breve!",
                fonte_pequena,
                BRANCO,
                100,
                280
            )


        texto(
            "MODO DE PREPARO",
            fonte,
            ROSA,
            100,
            400
        )


        texto(
            "Modo de preparo em breve!",
            fonte_pequena,
            BRANCO,
            100,
            450
        )



    pygame.display.update()



pygame.quit()
sys.exit()