import pygame
import sys
import os

# ==========================================
# INICIALIZAÇÃO
# ==========================================

pygame.init()

LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Sangueteria")

relogio = pygame.time.Clock()


# ==========================================
# CORES
# ==========================================

FUNDO = (35, 20, 45)
ROSA = (255, 105, 175)
ROSA_CLARO = (255, 170, 210)
ROXO = (105, 55, 145)
ROXO_ESCURO = (55, 30, 70)
BRANCO = (255, 255, 255)
PRETO = (20, 10, 25)


# ==========================================
# FONTES
# ==========================================

titulo = pygame.font.Font(None, 70)
titulo_menor = pygame.font.Font(None, 55)
fonte = pygame.font.Font(None, 36)
fonte_pequena = pygame.font.Font(None, 28)
fonte_mini = pygame.font.Font(None, 23)


# ==========================================
# CONTROLE DAS TELAS
# ==========================================

tela_atual = "menu"

receita_selecionada = None


# ==========================================
# RECEITAS
# ==========================================

receitas = [
    "Radio-Glow Shake",
    "Bio-Spooky",
    "Cosmic Boo-cake",
    "Steampunk Choco-Pie"
]


# ==========================================
# CIENTISTAS
# ==========================================

cientistas = [
    {
        "nome": "Marie Curie",
        "receita": "Radio-Glow Shake",
        "imagem": "imagens/marie_curie.png"
    },
    {
        "nome": "Rosalind Franklin",
        "receita": "Bio-Spooky",
        "imagem": "imagens/rosalind_franklin.png"
    },
    {
        "nome": "Katherine Johnson",
        "receita": "Cosmic Boo-cake",
        "imagem": "imagens/katherine_johnson.png"
    },
    {
        "nome": "Ada Lovelace",
        "receita": "Steampunk Choco-Pie",
        "imagem": "imagens/ada_lovelace.png"
    }
]


# ==========================================
# FUNÇÃO PARA ESCREVER TEXTO
# ==========================================

def texto(msg, fonte_usada, cor, x, y):

    imagem = fonte_usada.render(
        msg,
        True,
        cor
    )

    tela.blit(
        imagem,
        (x, y)
    )


# ==========================================
# FUNÇÃO PARA CENTRALIZAR TEXTO
# ==========================================

def texto_centralizado(msg, fonte_usada, cor, y):

    imagem = fonte_usada.render(
        msg,
        True,
        cor
    )

    x = (LARGURA - imagem.get_width()) // 2

    tela.blit(
        imagem,
        (x, y)
    )


# ==========================================
# BOTÃO
# ==========================================

def botao(nome, x, y, largura, altura):

    retangulo = pygame.Rect(
        x,
        y,
        largura,
        altura
    )

    pygame.draw.rect(
        tela,
        ROXO,
        retangulo,
        border_radius=15
    )

    pygame.draw.rect(
        tela,
        ROSA,
        retangulo,
        2,
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


# ==========================================
# SETA VOLTAR
# ==========================================

def seta_voltar():

    area = pygame.Rect(
        25,
        25,
        80,
        60
    )

    pygame.draw.line(
        tela,
        ROSA,
        (70, 55),
        (105, 55),
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

    return area


# ==========================================
# CARREGAR IMAGEM DA CIENTISTA
# ==========================================

def carregar_imagem(caminho):

    if not os.path.exists(caminho):
        return None

    try:

        imagem = pygame.image.load(
            caminho
        ).convert_alpha()

        return imagem

    except:

        return None


# ==========================================
# DESENHAR CARTINHA DA CIENTISTA
# ==========================================

def desenhar_cartinha(cientista, x, y):

    largura = 260
    altura = 165

    carta = pygame.Rect(
        x,
        y,
        largura,
        altura
    )

    # Fundo da carta

    pygame.draw.rect(
        tela,
        ROXO,
        carta,
        border_radius=18
    )

    # Borda

    pygame.draw.rect(
        tela,
        ROSA,
        carta,
        3,
        border_radius=18
    )

    # --------------------------------------
    # ÁREA DA IMAGEM
    # --------------------------------------

    area_imagem = pygame.Rect(
        x + 15,
        y + 15,
        80,
        80
    )

    pygame.draw.rect(
        tela,
        FUNDO,
        area_imagem,
        border_radius=12
    )

    pygame.draw.rect(
        tela,
        ROSA_CLARO,
        area_imagem,
        2,
        border_radius=12
    )

    imagem = carregar_imagem(
        cientista["imagem"]
    )

    if imagem is not None:

        imagem = pygame.transform.smoothscale(
            imagem,
            (70, 70)
        )

        tela.blit(
            imagem,
            (
                x + 20,
                y + 20
            )
        )

    else:

        texto_centralizado_card = "IMAGEM"

        imagem_texto = fonte_mini.render(
            texto_centralizado_card,
            True,
            ROSA_CLARO
        )

        texto_x = (
            area_imagem.centerx
            - imagem_texto.get_width() // 2
        )

        texto_y = (
            area_imagem.centery
            - imagem_texto.get_height() // 2
        )

        tela.blit(
            imagem_texto,
            (
                texto_x,
                texto_y
            )
        )

    # --------------------------------------
    # NOME
    # --------------------------------------

    nome = cientista["nome"]

    if nome == "Marie Curie":

        texto(
            "Marie Curie",
            fonte,
            BRANCO,
            x + 110,
            y + 30
        )

    elif nome == "Rosalind Franklin":

        texto(
            "Rosalind",
            fonte,
            BRANCO,
            x + 110,
            y + 18
        )

        texto(
            "Franklin",
            fonte,
            BRANCO,
            x + 110,
            y + 52
        )

    elif nome == "Katherine Johnson":

        texto(
            "Katherine",
            fonte,
            BRANCO,
            x + 110,
            y + 18
        )

        texto(
            "Johnson",
            fonte,
            BRANCO,
            x + 110,
            y + 52
        )

    elif nome == "Ada Lovelace":

        texto(
            "Ada Lovelace",
            fonte,
            BRANCO,
            x + 110,
            y + 35
        )

    # --------------------------------------
    # RECEITA
    # --------------------------------------

    texto(
        cientista["receita"],
        fonte_mini,
        ROSA_CLARO,
        x + 20,
        y + 120
    )

    return carta


# ==========================================
# LOOP PRINCIPAL
# ==========================================

rodando = True


while rodando:

    # ======================================
    # FUNDO
    # ======================================

    tela.fill(FUNDO)


    # ======================================
    # EVENTOS
    # ======================================

    for evento in pygame.event.get():

        # Fechar jogo

        if evento.type == pygame.QUIT:

            rodando = False


        # Clique do mouse

        if evento.type == pygame.MOUSEBUTTONDOWN:

            posicao = evento.pos


            # ==================================
            # MENU
            # ==================================

            if tela_atual == "menu":

                if jogar.collidepoint(posicao):

                    tela_atual = "receitas"


                elif cientistas_botao.collidepoint(posicao):

                    tela_atual = "cientistas"


                elif sair.collidepoint(posicao):

                    rodando = False


            # ==================================
            # LIVRO DE RECEITAS
            # ==================================

            elif tela_atual == "receitas":

                if voltar.collidepoint(posicao):

                    tela_atual = "menu"


                else:

                    for i, bot in enumerate(
                        botoes_receitas
                    ):

                        if bot.collidepoint(posicao):

                            receita_selecionada = receitas[i]

                            tela_atual = "preparo"


            # ==================================
            # TELA DE PREPARO
            # ==================================

            elif tela_atual == "preparo":

                if voltar.collidepoint(posicao):

                    tela_atual = "receitas"


            # ==================================
            # TELA DAS CIENTISTAS
            # ==================================

            elif tela_atual == "cientistas":

                if voltar.collidepoint(posicao):

                    tela_atual = "menu"


    # ==========================================
    # MENU PRINCIPAL
    # ==========================================

    if tela_atual == "menu":

        texto_centralizado(
            "SANGUETERIA",
            titulo,
            ROSA,
            80
        )

        texto_centralizado(
            "LABORATÓRIO DE DOCES",
            fonte,
            BRANCO,
            175
        )

        jogar = botao(
            "JOGAR",
            315,
            265,
            170,
            60
        )

        cientistas_botao = botao(
            "CIENTISTAS",
            280,
            345,
            240,
            60
        )

        sair = botao(
            "SAIR",
            315,
            425,
            170,
            60
        )


    # ==========================================
    # LIVRO DE RECEITAS
    # ==========================================

    elif tela_atual == "receitas":

        voltar = seta_voltar()

        texto_centralizado(
            "LIVRO DE RECEITAS",
            titulo_menor,
            ROSA,
            55
        )

        botoes_receitas = []

        y = 165

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


    # ==========================================
    # TELA DA RECEITA
    # ==========================================

    elif tela_atual == "preparo":

        voltar = seta_voltar()

        texto(
            receita_selecionada,
            titulo_menor,
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


        # --------------------------------------
        # RADIO-GLOW SHAKE
        # --------------------------------------

        if receita_selecionada == "Radio-Glow Shake":

            texto(
                "Ingredientes da receita",
                fonte_pequena,
                BRANCO,
                100,
                280
            )

            texto(
                "Receita em desenvolvimento.",
                fonte_pequena,
                BRANCO,
                100,
                320
            )


        # --------------------------------------
        # BIO-SPOOKY
        # --------------------------------------

        elif receita_selecionada == "Bio-Spooky":

            texto(
                "Ingredientes da receita",
                fonte_pequena,
                BRANCO,
                100,
                280
            )

            texto(
                "Receita em desenvolvimento.",
                fonte_pequena,
                BRANCO,
                100,
                320
            )


        # --------------------------------------
        # COSMIC BOO-CAKE
        # --------------------------------------

        elif receita_selecionada == "Cosmic Boo-cake":

            texto(
                "Ingredientes da receita",
                fonte_pequena,
                BRANCO,
                100,
                280
            )

            texto(
                "Receita em desenvolvimento.",
                fonte_pequena,
                BRANCO,
                100,
                320
            )


        # --------------------------------------
        # STEAMPUNK CHOCO-PIE
        # --------------------------------------

        elif receita_selecionada == "Steampunk Choco-Pie":

            texto(
                "Ingredientes da receita",
                fonte_pequena,
                BRANCO,
                100,
                280
            )

            texto(
                "Receita em desenvolvimento.",
                fonte_pequena,
                BRANCO,
                100,
                320
            )


        # --------------------------------------
        # MODO DE PREPARO
        # --------------------------------------

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


    # ==========================================
    # TELA DAS CIENTISTAS
    # ==========================================

    elif tela_atual == "cientistas":

        voltar = seta_voltar()

        texto_centralizado(
            "CIENTISTAS",
            titulo_menor,
            ROSA,
            40
        )

        texto_centralizado(
            "Conheça as cientistas das receitas",
            fonte_pequena,
            BRANCO,
            105
        )


        # --------------------------------------
        # CARTA MARIE CURIE
        # --------------------------------------

        desenhar_cartinha(
            cientistas[0],
            120,
            170
        )


        # --------------------------------------
        # CARTA ROSALIND FRANKLIN
        # --------------------------------------

        desenhar_cartinha(
            cientistas[1],
            420,
            170
        )


        # --------------------------------------
        # CARTA KATHERINE JOHNSON
        # --------------------------------------

        desenhar_cartinha(
            cientistas[2],
            120,
            365
        )


        # --------------------------------------
        # CARTA ADA LOVELACE
        # --------------------------------------

        desenhar_cartinha(
            cientistas[3],
            420,
            365
        )


    # ==========================================
    # ATUALIZAR TELA
    # ==========================================

    pygame.display.update()

    relogio.tick(60)


# ==========================================
# ENCERRAMENTO
# ==========================================

pygame.quit()
sys.exit()