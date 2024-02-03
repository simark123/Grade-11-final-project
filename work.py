import pgzrun
from pgzero.actor import Actor
import random

WIDTH = 800
HEIGHT = 600
player = Actor('martian.png')
player.pos = (WIDTH / 2, HEIGHT - 50)
player.display = True


bullets = []
enemies = []
enemiesSpeed = 1

blockades = []
blockadesvx = 1

timer = 0
seconds_enemies = 0
seconds_blockades = 0
seconds_lives = 0
rate = 10
score = 0
count = 10
lives_lost = 0

life = Actor('explosion.png')
life.pos = 600, 40
life.display = True
life2 = Actor('explosion.png')
life2.pos = 650, 40
life2.display = True
life3 = Actor('explosion.png')
life3.pos = 700, 40
life3.display = True

gain_lives = []
gain_livesSpeed = 1

background = Actor('background1.png')
game_over = False
start_game = True
play_game = False


def update():

    global rate
    global timer
    global seconds_enemies
    global count
    global score
    global enemiesSpeed
    global seconds_blockades
    global seconds_lives
    global start_game
    global lives_lost
    global play_game

    if play_game:
        timer += 1
        if timer == 60:
            seconds_enemies += 1
            seconds_blockades += 1
            seconds_lives += 1
            timer = 0
            enemies.append(Actor('invader.png', pos=(random.randint(0, WIDTH), random.randint(0, 0))))

        if seconds_enemies == 3 and enemiesSpeed <= 10:
            enemiesSpeed += 1
            seconds_enemies = 0

        if seconds_blockades == 15:
            blockades.append(Actor('mm_blue.png', pos=(random.randint(0, 0), random.randint(300, 400))))
            seconds_blockades = 0

        if seconds_lives == 5:
            gain_lives.append(Actor('explosion.png', pos=(random.randint(0, WIDTH), random.randint(0, 0))))
            seconds_lives = 0

        for i in reversed(range(len(gain_lives))):
            gain_lives[i].y += gain_livesSpeed
            if gain_lives[i].colliderect(player):
                if life.display == False and life2.display:
                    life.display = True
                    del gain_lives[i]

            for j in reversed(range(len(gain_lives))):
                gain_lives[j].y += gain_livesSpeed
                if gain_lives[j].colliderect(player):
                    if life3.display and not life2.display:
                        life2.display = True
                        del gain_lives[j]

        for i in reversed(range(len(enemies))):  # moves the enemies down the screen and moves blockades side to side
            enemies[i].y += enemiesSpeed
            if (enemies[i].colliderect(player) or enemies[i].y >= HEIGHT) and not game_over:
                del enemies[i]
                lives_lost += 1
                if life.display:
                    life.display = False
                elif life2.display:
                    life2.display = False
                else:
                    life3.display = False
                break

            j = 0
            while j != len(bullets):
                if bullets[j].y < 0:
                    del bullets[j]
                    break
                if bullets[j].colliderect(enemies[i]) and not game_over:
                    del enemies[i]
                    del bullets[j]
                    score += 1
                    break
                j += 1

        for i in reversed(range(len(blockades))):  # moves the blockades across the screen horizontally
            blockades[i].x += blockadesvx
            for j in reversed(range(len(bullets))):
                if blockades[i].colliderect(bullets[j]):
                    del bullets[j]

        for i in reversed(range(len(bullets))):  # bullets go away when going to the top of the screen
            bullets[i].y += -7

def on_mouse_move(pos):  # moves character along the bottom, only horizontal, with mouse
    player.x = pos[0]


def draw():
    global enemiesSpeed
    global score
    global lives_lost
    global game_over
    screen.clear()
    background.draw()
    if start_game:
        screen.clear()
        background.draw()
        screen.draw.text('Press SPACE to start', (300, 300), color=(0, 0, 0))
        return

    if life3.display == False:
        screen.draw.text('GAME OVER', (350, 240), color=(50, 200, 50))
        screen.draw.text(f'Your Score: {str(score)}', (350, 270), color=(50, 200, 50))
        screen.draw.text(f'Lives Lost: {str(lives_lost)}', (350, 300), color=(50, 200, 50))
        game_over = True
    if player.display:
        player.draw()

    if life.display:
        life.draw()

    if life2.display:
        life2.draw()

    if life3.display:
        life3.draw()

    for x in gain_lives:
        x.draw()

    for x in enemies:
        x.draw()

    for x in bullets:
        x.draw()

    for x in blockades:
        x.draw()
    if life3.display:
        screen.draw.text(f'Score: {str(score)}', (10, 20), color=(50, 200, 50))

def on_key_down(key):
    global start_game
    global game_over
    global play_game
    if start_game:
        if key == keys.SPACE:
            start_game = False
            play_game = True

    else:
        if key == keys.SPACE:
            launch()

def launch():
    if not game_over:
        bullet = Actor('fireball.png')
        bullet.vy = -5
        bullet.pos = (player.x, player.y)
        bullets.append(bullet)


pgzrun.go()
