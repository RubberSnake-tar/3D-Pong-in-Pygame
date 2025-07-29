import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

red_paddle_position = pygame.Vector3(0, 0, 0)
red_paddle_size = pygame.Vector3(2.5, 0, .5)
red_paddle_speed = 15

blue_paddle_position = pygame.Vector3(0, 0, -30)
blue_paddle_size = pygame.Vector3(2.5, 0, .5)
blue_paddle_speed = 15

ball_position = pygame.Vector3(0, 0, -14.5)
ball_size = .5
ball_speed_x = 10
ball_speed_z = 10

left_wall_position = -9
right_wall_position = 9
wall_size = .7

red_paddle_score = 0
blue_paddle_score = 0

game_over = False

def draw_cube(color):
    vertices = [
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    ]

    faces = [
        (0, 1, 2, 3),
        (1, 5, 7, 2),
        (5, 4, 6, 7),
        (4, 0, 3, 6),
        (0, 4, 5, 1),
        (2, 7, 6, 3)
    ]

    normals = [
        (0, 0, -1),
        (0, 1, 0),
        (0, 0, 1),
        (0, -1, 0),
        (1, 0, 0),
        (-1, 0, 0)
    ]

    glBegin(GL_QUADS)
    glColor3fv(color)
    for i, face in enumerate(faces):
        glNormal3fv(normals[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_plane(color):
    vertices = [
        (-1, 0, -1),
        (1, 0, -1),
        (1, 0, 1),
        (-1, 0, 1)
    ]

    face = (0, 1, 2, 3)

    normal = (0, 1, 0)

    glBegin(GL_QUADS)
    glColor3fv(color)
    glNormal3fv(normal)
    for vertex in face:
        glVertex3fv(vertices[vertex])
    glEnd()

def draw_sphere(color):
    glColor3fv(color)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, ball_size, 32, 32)

def draw_court():
    # Light
    glPushMatrix()
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 5, -15, 1])
    glPopMatrix()

    # Red Paddle
    glPushMatrix()
    glTranslatef(red_paddle_position.x, 0, red_paddle_position.z)
    glScalef(red_paddle_size.x, 1, red_paddle_size.z)
    draw_cube(color=(1, 0, 0))
    glPopMatrix()

    # Blue Paddle
    glPushMatrix()
    glTranslatef(blue_paddle_position.x, 0, blue_paddle_position.z)
    glScalef(blue_paddle_size.x, 1, blue_paddle_size.z)
    draw_cube(color=(0, 0, 1))
    glPopMatrix()

    # Ball
    glPushMatrix()
    glTranslatef(ball_position.x, 0, ball_position.z)
    draw_sphere(color=(1, 1, 1))
    glPopMatrix()

    # Left Wall
    glPushMatrix()
    glTranslatef(left_wall_position, 0, -15)
    glScalef(wall_size, 1, 16)
    draw_cube(color=(.2, .2, .2))
    glPopMatrix()

    # Right Wall
    glPushMatrix()
    glTranslatef(right_wall_position, 0, -15)
    glScalef(wall_size, 1, 16)
    draw_cube(color=(.2, .2, .2))
    glPopMatrix()

    # Floor Line
    glPushMatrix()
    glTranslatef(0, -.99, -15.5)
    glScalef(10, 1, .5)
    draw_plane(color=(.4, .4, .4))
    glPopMatrix()

    # Floor
    glPushMatrix()
    glTranslatef(0, -1, -15.5)
    glScalef(14, 1, 20)
    draw_plane(color=(.7, .7, .7))
    glPopMatrix()

def gl_init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_AMBIENT, [.2, .2, .2, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [.8, .8, .8, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [2, 2, 2, 1])
    
    glRotatef(25, 1, 0, 0)
    glTranslatef(0, -7, -10)

def main():
    pygame.init()
    display = (1200, 800)
    icon_image = pygame.image.load('3D Pong.png')
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('3D Pong')
    pygame.display.set_icon(icon_image)
    clock = pygame.time.Clock()
    deltaTime = 0

    running = True

    global red_paddle_position, blue_paddle_position, ball_position, ball_speed_x, ball_speed_z, game_over, red_paddle_score, blue_paddle_score

    glMatrixMode(GL_PROJECTION)
    gluPerspective(55, (display[0] / display[1]), .1, 50)
    glMatrixMode(GL_MODELVIEW)
    
    gl_init()

    while running:
        deltaTime = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        keys = pygame.key.get_pressed()

        if game_over == False:
            if keys[pygame.K_a]:
                red_paddle_position.x += -red_paddle_speed * deltaTime
            if keys[pygame.K_d]:
                red_paddle_position.x += red_paddle_speed * deltaTime
            if keys[pygame.K_LEFT]:
                blue_paddle_position.x += -blue_paddle_speed * deltaTime
            if keys[pygame.K_RIGHT]:
                blue_paddle_position.x += blue_paddle_speed * deltaTime

            # Red Paddle vs Walls
            if red_paddle_position.x - red_paddle_size.x <= left_wall_position + wall_size:
                red_paddle_position.x = left_wall_position + wall_size + red_paddle_size.x
            if red_paddle_position.x + red_paddle_size.x >= right_wall_position - wall_size:
                red_paddle_position.x = right_wall_position - wall_size - red_paddle_size.x

            # Blue Paddle vs Walls
            if blue_paddle_position.x - blue_paddle_size.x <= left_wall_position + wall_size:
                blue_paddle_position.x = left_wall_position + wall_size + blue_paddle_size.x
            if blue_paddle_position.x + blue_paddle_size.x >= right_wall_position - wall_size:
                blue_paddle_position.x = right_wall_position - wall_size - blue_paddle_size.x

            # Ball vs Walls
            if ball_position.x - ball_size <= left_wall_position + wall_size:
                ball_speed_x = -ball_speed_x
            if ball_position.x + ball_size >= right_wall_position - wall_size:
                ball_speed_x = -ball_speed_x

            # Ball vs Paddles
            if (ball_position.z - ball_size <= red_paddle_position.z + red_paddle_size.z and
                ball_position.z + ball_size >= red_paddle_position.z - red_paddle_size.z and
                ball_position.x - ball_size <= red_paddle_position.x + red_paddle_size.x and
                ball_position.x + ball_size >= red_paddle_position.x - red_paddle_size.x and
                ball_speed_z >= 0):
                ball_speed_z = -ball_speed_z
            if (ball_position.z - ball_size <= blue_paddle_position.z + blue_paddle_size.z and 
                ball_position.z + ball_size >= blue_paddle_position.z - blue_paddle_size.z and
                ball_position.x - ball_size <= blue_paddle_position.x + blue_paddle_size.x and
                ball_position.x + ball_size >= blue_paddle_position.x - blue_paddle_size.x and
                ball_speed_z <= 0):
                ball_speed_z = -ball_speed_z

            ball_position.x += ball_speed_x * deltaTime
            ball_position.z += ball_speed_z * deltaTime

            # Red Paddle Scores
            if ball_position.z <= -33:
                ball_position.x = 0
                ball_position.z = -14.5
                ball_speed_x = -ball_speed_x
                ball_speed_z = -ball_speed_z
                red_paddle_score += 1
                print(f'Player 1: {red_paddle_score}')

            # Blue Paddle Scores
            if ball_position.z >= 3:
                ball_position.x = 0
                ball_position.z = -14.5
                ball_speed_x = -ball_speed_x
                ball_speed_z = -ball_speed_z
                blue_paddle_score += 1
                print(f'Player 2: {blue_paddle_score}')

            if red_paddle_score == 6:
                print('Game Over! Player 1 Wins!')
                game_over = True
            if blue_paddle_score == 6:
                print('Game Over! Player 2 Wins!')
                game_over = True
            
        if keys[pygame.K_SPACE]:
            red_paddle_position = pygame.Vector3(0, 0, 0)
            blue_paddle_position = pygame.Vector3(0, 0, -30)
            ball_position = pygame.Vector3(0, 0, -14.5)
            ball_speed_x = -ball_speed_x
            ball_speed_z = -ball_speed_z
            red_paddle_score = 0
            blue_paddle_score = 0
            game_over = False

        draw_court()

        pygame.display.flip()

    pygame.quit()

main()