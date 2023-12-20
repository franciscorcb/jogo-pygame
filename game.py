'''A criação desse codigo foi feita se baseando nos seguintes videos:
https://www.youtube.com/playlist?list=PLJ8PYFcmwFOxtJS4EZTGEPxMEo4YdbxdQ
https://www.youtube.com/playlist?list=PL30AETbxgR-fAbwiuU1vDl3owNUPUuVrz 
https://www.youtube.com/watch?v=AY9MnQ4x3zk
tps://www.youtube.com/watch?v=G8MYGDf_9ho&t=47s'''
import pygame
import os
import sys

pygame.init()
pygame.font.init()

LARGURA = 740
ALTURA = 450

janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("jogo gato")
fps = pygame.time.Clock()

imagem_start = pygame.image.load(os.path.join('sprites',"start_img.png")).convert_alpha()
mov_gato = pygame.image.load(os.path.join('sprites', "gatos.png")).convert_alpha()
mov_morcego = pygame.image.load(os.path.join('sprites', "morcegos.png")).convert_alpha()
bloco = pygame.image.load(os.path.join('sprites', "bloco.png")).convert_alpha()
imgpulo=pygame.image.load(os.path.join('sprites',"pulo1.png")).convert_alpha()
imgpulo2=pygame.image.load(os.path.join('sprites',"pulo2.png")).convert_alpha()

musica=pygame.mixer.Sound("musica/song.mp3")
musica.set_volume(0.2)
pulo_som = pygame.mixer.Sound('musica/audio_jump.mp3')
pulo_som.set_volume(0.1)

velocidade_jogo = velocidade_chao = 8
enter_pressionado = colidiu = False
rodar = True
velocidade_morcego=14
velocidade_fundo=1
pontos = 0

class Gato(pygame.sprite.Sprite):
    ALTURA_PULO = -19
    ALTURA_PULO_DUPLO=-25
    def __init__(self):
        super().__init__()
        self.velocidade_y = self.index_lista = 0
        self.gato_pulo = self.pular = False
        self.imagens_gatinho = []
        self.posicao_inicial_y = 320
        self.criar_animacao()
        self.image = self.imagens_gatinho[self.index_lista]
        self.rect = self.image.get_rect(center=(100,320))
        self.mask = pygame.mask.from_surface(self.image)
        
    def criar_animacao(self):
        #loop para gerar a troca de imagens
        for c in range(3):
            img = mov_gato.subsurface((c * 640, 0), (640, 640))
            img = pygame.transform.scale(img, (110, 110))
            self.imagens_gatinho.append(img)

    def pulo(self, pulo_duplo = False):
        if not self.pular:
            self.pular = True
            if pulo_duplo:
                self.velocidade_y = self.ALTURA_PULO_DUPLO
            else:
                self.velocidade_y = self.ALTURA_PULO

    def update(self):
        #Atualização da posição e animação do gato
        if self.pular or self.rect.y < self.posicao_inicial_y:
            self.rect.y += self.velocidade_y
            # Lógica do pulo
            self.velocidade_y += 1.7

        if self.rect.y >=self.posicao_inicial_y:
            self.rect.y = self.posicao_inicial_y
            self.velocidade_y = 0
            self.pular = False

        if not self.pular:
            if self.index_lista > 2:
                self.index_lista = 0
            self.index_lista += 0.6
            self.image = self.imagens_gatinho[int(self.index_lista)]

class Background(pygame.sprite.Sprite):
    #movimentação do background
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load(os.path.join('sprites',"cenario_fundo.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, ALTURA - self.image.get_height()))

    def update(self):
        self.rect.x -= velocidade_fundo
        if self.rect.right < 0:
            self.rect.x = LARGURA

class Chao(pygame.sprite.Sprite):
    #movimentação do chao
    def __init__(self,x):
        super().__init__()
        self.image = pygame.image.load(os.path.join('sprites','chao.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,ALTURA-self.image.get_height()))
    
    def update(self):
        self.rect.x -= velocidade_jogo
        if self.rect.right<0:
            self.rect.x= LARGURA

class Obstaculo(pygame.sprite.Sprite):
    #logica de posicao e velocidade de obstaculos
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.obstaculo_img = bloco
        self.image = pygame.transform.scale(self.obstaculo_img, (90, 90))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(LARGURA, ALTURA - 80))

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -= velocidade_jogo

class Morcego(pygame.sprite.Sprite):
    #logica de movimentação e posição dos morcegos
    TEMPO_DE_ANIMACAO = 0.25
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_morcego=[]

        for attack_morcego in range(2):
            img = mov_morcego.subsurface((attack_morcego*640,0),(640,640))
            img= pygame.transform.scale(img, (100, 100))
            self.imagens_morcego.append(img)

        self.index_lista = 0
        self.image = self.imagens_morcego[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, 300)

    def update(self):
        #logica de movimentacao e posicao do morcego
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -= velocidade_morcego

        if self.index_lista > 1:
            self.index_lista = 0
        self.index_lista += self.TEMPO_DE_ANIMACAO
        self.image = self.imagens_morcego[int(self.index_lista)]

def tela_start():
    start = True
    song2 = pygame.mixer.Sound("musica/song2.mp3")
    song2.set_volume(0.5)
    song2.play()
    clock = pygame.time.Clock()
    frame_atual = 0
    fundo= pygame.image.load(os.path.join('sprites',"cenario_fundo.png")).convert_alpha()
    fundo=pygame.transform.scale(fundo,(860,570))
    imagem_gato = []
    pulo_gato=[]
    pulo_gato2=[]

    for sprite1 in range(2):
        pulo=imgpulo.subsurface((sprite1*496,0),(496,496))
        pulo=pygame.transform.scale(pulo,(346,346))
        pulo_gato.append(pulo)

    for sprite2 in range(2):
        pulo2=imgpulo2.subsurface((sprite2*496,0),(496,496))
        pulo2=pygame.transform.scale(pulo2,(266,286))
        pulo_gato2.append(pulo2)

    for sprite3 in range(2):
        img = imagem_start.subsurface((sprite3 * 480, 0), (480, 340))
        img = pygame.transform.scale(img, (550,410))
        imagem_gato.append(img)

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 90<event.pos[0]<640 and 5<event.pos[1]<415:
                    start = False
                    song2.stop()
                    musica.play(loops=-1)
        janela.fill((0, 0, 0))
        janela.blit(fundo, (-40, -120))
        janela.blit(imagem_gato[frame_atual], (90, 5))
        janela.blit(pulo_gato[frame_atual],(-60,176))
        janela.blit(pulo_gato2[frame_atual],(460,196))
        pygame.display.update()
        clock.tick(3)
        frame_atual = (frame_atual + 1) % len(imagem_gato)

def exibir_mensagem(msg,tamanho_fonte, cor):
    fonte = pygame.font.SysFont('freesansbold',tamanho_fonte,True,False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem,True,cor)
    return texto_formatado 

def reiniciar_jogo():
    global pontos,velocidade_jogo,velocidade_morcego, colidiu, velocidade_chao,musica
    pontos = 0
    velocidade_jogo=8
    velocidade_morcego = 14
    velocidade_chao=1
    colidiu = False
    gato.rect.y = 320
    gato.pular = False
    morcego.rect.x = LARGURA
    obstaculo.rect.x = LARGURA
    musica.play()

def cria_backgrounds(tela):
    #loop para a imagem de fundo
    backgrounds = []
    for imagem in range(3):
        telaBackground = tela(imagem * LARGURA)
        backgrounds.append(telaBackground)
    return backgrounds

#instaciamento dos objetos
todas_sprites = pygame.sprite.Group()

backgrounds = cria_backgrounds(Background)
chaos = cria_backgrounds(Chao)
todas_sprites = pygame.sprite.Group(backgrounds, chaos)

gato=Gato()
morcego=Morcego()
todas_sprites.add(gato)
todas_sprites.add(morcego)

obstaculo = Obstaculo()
grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(obstaculo,morcego)
todas_sprites.add(grupo_obstaculos)

tela_start()
def eventos():
    global rodar, enter_pressionado, colidiu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            pressionouTecla(event)
        elif event.type == pygame.KEYUP:
            eventoTeclaNaoPressionada(event)

def pressionouTecla(event):
    global enter_pressionado, colidiu
    if event.key == pygame.K_SPACE and colidiu == False:
        eventoPuloEpuloDuplo()
    if event.key == pygame.K_RETURN and colidiu == True:
        reiniciar_jogo()
    elif event.key == pygame.K_RETURN:
        enter_pressionado = True

def eventoPuloEpuloDuplo():
    global gato
    if gato.rect.y != gato.posicao_inicial_y:
        pass
    else:
        if enter_pressionado:
            gato.pulo(pulo_duplo=True)
            pulo_som.play()
        else:
            gato.pulo()
            pulo_som.play()

def eventoTeclaNaoPressionada(event):
    global enter_pressionado
    if event.key == pygame.K_RETURN:
        enter_pressionado = False

def verificaColisoes():
    global colidiu, pontos, velocidade_jogo, velocidade_morcego, velocidade_chao
    colisoes = pygame.sprite.spritecollide(gato, grupo_obstaculos, False, pygame.sprite.collide_mask)
    if colisoes and not colidiu:
        colidiu = True

    if not colidiu:
        pontos += 1
        todas_sprites.update()
        pontuacaoEvelocidade()

def pontuacaoEvelocidade():
    global pontos, velocidade_jogo, velocidade_morcego, velocidade_chao
    pontos += 1
    if pontos % 100 == 0:
        if velocidade_jogo < 20 and velocidade_morcego < 20:
            velocidade_morcego += 0.9
            velocidade_jogo += 1
            velocidade_chao += 1

def renderizando_jogo():
    janela.fill((0, 0, 0))
    todas_sprites.draw(janela)
    if colidiu:
        render_telaGameOver()
        musica.stop()
    else:
        atualizaTelaJogo()
    pygame.display.flip()

def render_telaGameOver():
    game_over_text = exibir_mensagem('GAME OVER', 40, (255, 255, 255))
    restart_text = exibir_mensagem('Pressione _ENTER_ para reiniciar', 26, (255, 255, 255))
    posicao_gameOver = LARGURA - 450, ALTURA - 235
    posicao_restart = LARGURA - 510, ALTURA - 200
    janela.blit(game_over_text, posicao_gameOver)
    janela.blit(restart_text, posicao_restart)

def atualizaTelaJogo():
    janela.fill((0, 0, 0))
    todas_sprites.draw(janela)
    score = exibir_mensagem(f"Pontuação: {pontos}", 32, (255, 255, 255))
    janela.blit(score, (550, 20))

while rodar:
    fps.tick(26)
    eventos()
    verificaColisoes()
    renderizando_jogo()