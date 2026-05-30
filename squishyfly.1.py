import pygame
import random


# INICIALIZAR PYGAME

pygame.init()


# CONFIGURACIÓN DE VENTANA

ANCHO = 500
ALTO = 700

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Squishy Fly")

FPS = 60
reloj = pygame.time.Clock()


# FUENTE

fuente = pygame.font.SysFont("Arial", 35)


# CARGAR IMÁGENES

fondo_img = pygame.image.load("background-day.png").convert()
base_img = pygame.image.load("base.png").convert_alpha()
pajaro_img = pygame.image.load("yellowbird-midflap.png").convert_alpha()
tuberia_img = pygame.image.load("pipe-green.png").convert_alpha()
gameover_img = pygame.image.load("message.png").convert_alpha()

# Escalar imágenes
fondo_img = pygame.transform.scale(fondo_img, (ANCHO, ALTO))
base_img = pygame.transform.scale(base_img, (ANCHO, 110))
pajaro_img = pygame.transform.scale(pajaro_img, (55, 40))
tuberia_img = pygame.transform.scale(tuberia_img, (90, 500))
gameover_img = pygame.transform.scale(gameover_img, (250, 180))


# COLORES

NEGRO = (0, 0, 0)


# VARIABLES DEL JUEGO

gravedad = 0.5
fuerza_salto = -9

velocidad_tuberia = 4
intervalo_tuberia = 1500
espacio_tuberias = 180

record = 0



# CLASE PÁJARO

class Pajaro:
    def __init__(self):
        self.x = 90
        self.y = ALTO // 2
        self.ancho = 55
        self.alto = 40
        self.velocidad = 0

    def saltar(self):
        self.velocidad = fuerza_salto

    def mover(self):
        self.velocidad += gravedad
        self.y += self.velocidad

    def dibujar(self):
        rotacion = -self.velocidad * 3
        imagen_rotada = pygame.transform.rotate(
            pajaro_img, rotacion
        )
        pantalla.blit(imagen_rotada, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.ancho,
            self.alto
        )



# CLASE TUBERÍA

class Tuberia:
    def __init__(self):
        self.x = ANCHO
        self.ancho = 90

        self.altura_superior = random.randint(
            100,
            ALTO - espacio_tuberias - 250
        )

        self.altura_inferior = (
            ALTO
            - self.altura_superior
            - espacio_tuberias
        )

        self.punto_contado = False

    def mover(self):
        self.x -= velocidad_tuberia

    def dibujar(self):

        # Tubería superior
        tuberia_superior = pygame.transform.flip(
            tuberia_img,
            False,
            True
        )

        pantalla.blit(
            tuberia_superior,
            (self.x, self.altura_superior - 500)
        )

        # Tubería inferior
        pantalla.blit(
            tuberia_img,
            (
                self.x,
                ALTO - self.altura_inferior
            )
        )

    def colision(self, pajaro):

        rect_pajaro = pajaro.get_rect()

        rect_superior = pygame.Rect(
            self.x,
            0,
            self.ancho,
            self.altura_superior
        )

        rect_inferior = pygame.Rect(
            self.x,
            ALTO - self.altura_inferior,
            self.ancho,
            self.altura_inferior
        )

        return (
            rect_pajaro.colliderect(rect_superior)
            or rect_pajaro.colliderect(rect_inferior)
        )

    def fuera_pantalla(self):
        return self.x + self.ancho < 0



# REINICIAR JUEGO
def reiniciar_juego():
    global velocidad_tuberia

    velocidad_tuberia = 4

    pajaro = Pajaro()
    tuberias = []

    puntos = 0

    tiempo_tuberia = pygame.time.get_ticks()

    juego_activo = True

    return (
        pajaro,
        tuberias,
        puntos,
        tiempo_tuberia,
        juego_activo
    )


# INICIAR

(
    pajaro,
    tuberias,
    puntos,
    tiempo_tuberia,
    juego_activo
) = reiniciar_juego()


# BUCLE PRINCIPAL

corriendo = True

while corriendo:

    reloj.tick(FPS)

    
    # EVENTOS
    
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.KEYDOWN:

            # Saltar
            if (
                evento.key == pygame.K_SPACE
                and juego_activo
            ):
                pajaro.saltar()

            # Reiniciar
            if (
                evento.key == pygame.K_r
                and not juego_activo
            ):
                (
                    pajaro,
                    tuberias,
                    puntos,
                    tiempo_tuberia,
                    juego_activo
                ) = reiniciar_juego()

   
    # ACTUALIZAR JUEGO
    
    if juego_activo:

        pajaro.mover()

        tiempo_actual = pygame.time.get_ticks()

        # Crear tuberías
        if (
            tiempo_actual - tiempo_tuberia
            > intervalo_tuberia
        ):
            tuberias.append(Tuberia())
            tiempo_tuberia = tiempo_actual

        # Actualizar tuberías
        for tuberia in tuberias:

            tuberia.mover()

            # Colisión
            if tuberia.colision(pajaro):
                juego_activo = False

            # Puntos
            if (
                tuberia.x + tuberia.ancho
                < pajaro.x
                and not tuberia.punto_contado
            ):

                puntos += 1
                tuberia.punto_contado = True

                # Aumentar dificultad
                if puntos % 5 == 0:
                    velocidad_tuberia += 0.5

        # Eliminar tuberías fuera de pantalla
        tuberias = [
            t for t in tuberias
            if not t.fuera_pantalla()
        ]

        # Colisión techo/suelo
        if (
            pajaro.y < 0
            or pajaro.y + pajaro.alto
            > ALTO - 110
        ):
            juego_activo = False

    # Record
    if puntos > record:
        record = puntos

    
    # DIBUJAR
    
    pantalla.blit(fondo_img, (0, 0))

    # Tuberías
    for tuberia in tuberias:
        tuberia.dibujar()

    # Base
    pantalla.blit(base_img, (0, ALTO - 110))

    # Pájaro
    pajaro.dibujar()

    # Texto
    texto_puntos = fuente.render(
        f"Puntos: {puntos}",
        True,
        NEGRO
    )

    pantalla.blit(texto_puntos, (20, 20))

    texto_record = fuente.render(
        f"Record: {record}",
        True,
        NEGRO
    )

    pantalla.blit(texto_record, (20, 60))

    texto_velocidad = fuente.render(
        f"Velocidad: {int(velocidad_tuberia)}",
        True,
        NEGRO
    )

    pantalla.blit(texto_velocidad, (20, 100))

    # Game Over
    if not juego_activo:

        pantalla.blit(
            gameover_img,
            (
                ANCHO // 2 - 125,
                220
            )
        )

        texto_reiniciar = fuente.render(
            "Presiona R para reiniciar",
            True,
            NEGRO
        )

        pantalla.blit(
            texto_reiniciar,
            (55, 430)
        )

    pygame.display.update()

pygame.quit()