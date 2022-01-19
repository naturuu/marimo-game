import pygame #파이 게임 모듈 임포트
import random
import time
import schedule



pygame.init() #파이 게임 초기화
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #화면 크기 설정
clock = pygame.time.Clock() 

pygame.display.set_caption("Marimo game")
#색상 지정
BLACK = (0,0,0)
RED = (255, 0, 0)
OrangeRed =  (255,95,0)
#글씨체와 크기
small_font = pygame.font.SysFont('malgungothic', 36)
large_font = pygame.font.SysFont('malgungothic', 50)
 


score = 0
start_time = int(time.time())

#온도 
global temp
temp = 20
#배경
global bg
bg = 0

#시간이 지날수록 온도가 지정한 만큼 올라가게 함
def addtemp():
    global temp
    temp += 1
#시간이 지날수록 배경이 바뀌게 바뀜
def change():
    global bg
    bg +=1

schedule.every(10).seconds.do(addtemp) #10초에 1도씩 온도가 오름
schedule.every(30).seconds.do(change) #30초마다 물이 더러워진다는 것으로 하여 배경이 변함

 
#변수

background_image = pygame.image.load('background1.jpg')



food_image = pygame.image.load('food.png')
foods = []
for i in range(5):
    food = food_image.get_rect(left=random.randint(0, SCREEN_WIDTH - food_image.get_width()), top=-100)
    foods.append(food)


marimo1_image = pygame.image.load('marimo1.png')
marimo1 = marimo1_image.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 60)

pass1 = False
pass2 = False

while True: #게임 루프
    if bg == 1:
        background_image = pygame.image.load('background2.jpg')
    elif bg >= 2:
        background_image = pygame.image.load('background3.jpg')
    else:
        background_image = pygame.image.load('background1.jpg')
    screen.blit(background_image, (0, 0))

    

    #변수 업데이트
    if bg == 1 or temp >= 30:
        speed = 3
        addscore = 5
    elif bg >= 2 or temp >= 30:
        speed = 1
        addscore = 2
    else:
        speed = 6
        addscore = 10
        
            
    event = pygame.event.poll() #이벤트 처리
    if event.type == pygame.QUIT:
        break
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LSHIFT: #온도를 낮춰주는 키
            if temp >= 21:
                temp -= 1
        if event.key == pygame.K_RSHIFT:
            if temp >= 21:
                temp -= 1
        if event.key == pygame.K_SPACE: #물갈아주는 키 배경이 깨끗해짐
            background_image = pygame.image.load('background1.jpg')
            bg = 0
            screen.blit(background_image, (0, 0))


    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        marimo1.left -= speed
    elif pressed[pygame.K_RIGHT]:
        marimo1.left += speed
  


    for food in foods:
        food.top += 3
        if food.top > SCREEN_HEIGHT:
            foods.remove(food)
            food = food_image.get_rect(left=random.randint(0, SCREEN_WIDTH - food_image.get_width()), top=-100)
            foods.append(food)


    if marimo1.left < 0:
        marimo1.left = 0
    elif marimo1.right > SCREEN_WIDTH:
        marimo1.right = SCREEN_WIDTH

    

    for food in foods:
        if marimo1.colliderect(food): #충돌이 발생했을때
            foods.remove(food)
            food = food_image.get_rect(left=random.randint(0, SCREEN_WIDTH - food_image.get_width()), top=-100)
            foods.append(food)

            #점수증가 및 진화 
            score += addscore
            if score >= 100 and score < 500 and pass1==False: #100점이 되면 마리모가 레벨업함
                marimo1_image = pygame.image.load('marimo2.png')
                marimo1 = marimo1_image.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 50)
                background_image = pygame.image.load('impact.jpg')
                screen.blit(background_image, (0, 0))
                pygame.display.update()
                time.sleep(1)
                pass1 = True
            
            elif score >= 500 and pass2 == False: #500점이 되면 마리모가 레벨업함
                marimo1_image = pygame.image.load('marimo3.png')
                marimo1 = marimo1_image.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT -50)
                background_image = pygame.image.load('impact.jpg')
                screen.blit(background_image, (0, 0))
                pygame.display.update()
                time.sleep(1)
                pass2 = True
        

    #게임진행 시간 나타내기
    current_time = int(time.time())
    play_second = 0 + (current_time - start_time)

    schedule.run_pending()

    #온도초과시 종료
    if temp > 40:
        game_over_image = large_font.render('게임 종료', True, RED)
        screen.blit(game_over_image, game_over_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))
        schedule.clear()
        speed = 0
        pygame.display.update()
        time.sleep(3)
        pygame.quit()
        
        
                
    #화면 그리기

    for food in foods:
        screen.blit(food_image, food)

    screen.blit(marimo1_image, marimo1)


    score_image = small_font.render('점수 {}'.format(score), True, RED)
    screen.blit(score_image, (10, 10))

    if(temp >= 30):
        temp_image = small_font.render('온도 {}'.format(temp), True, OrangeRed)
    else:
        temp_image = small_font.render('온도 {}'.format(temp), True, BLACK)
    screen.blit(temp_image,(550, 50))

    
    play_second_image = small_font.render('시간 {}'.format(play_second), True, BLACK)
    screen.blit(play_second_image, (550,10))

    
    pygame.display.update() #모든 화면 그리기 업데이트
    clock.tick(30) #30 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값

pygame.quit() 
