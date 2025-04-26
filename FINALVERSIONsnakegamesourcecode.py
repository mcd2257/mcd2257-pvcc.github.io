import pygame 
import sys
import random 
pygame.init() 
button_font = pygame.font.SysFont("cambria", 40)
cell_size = 30
cell_number = 20 
gamewindow = pygame.display.set_mode((cell_size*cell_number,cell_size*cell_number )) 
  

gameloops = True

class Button:
    
    def __init__(self, image, xpos, ypos, text_input):
        self.image = image 
        self.xpos = xpos
        self.ypos = ypos
        self.rect = self.image.get_rect(center=(self.xpos, self.ypos))
        self.text_input = text_input
        self.text = button_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.xpos, (self.ypos-12)))

    def update(self):
        gamewindow.blit(self.image, self.rect)
        gamewindow.blit(self.text, self.text_rect)

    
class Snake:
    def __init__(self):
      self.body = [pygame.math.Vector2(5,10),pygame.math.Vector2(4,10) ,pygame.math.Vector2(3,10)]
      self.velocity = pygame.math.Vector2(1,0)
      self.add_segment = False 

    def snake_body(self):
        for segment in self.body:
            xpos = segment.x * cell_size
            ypos = segment.y * cell_size
            segment_shape = pygame.Rect(xpos, ypos, cell_size ,cell_size)
            pygame.draw.rect(gamewindow, "white", segment_shape)
    
    def snake_movement(self):
        
        if self.add_segment == True:
            body_movement = self.body[:]
            body_movement.insert(0,body_movement[0] + self.velocity)
            self.body = body_movement[:]
            self.add_segment = False
            
        else:
            body_movement = self.body[:-1]
            body_movement.insert(0,body_movement[0] + self.velocity)
            self.body = body_movement[:]

    def add_body_segment(self):
        self.add_segment = True

    def snake_reset(self):
        self.body = [pygame.math.Vector2(5,10),pygame.math.Vector2(4,10) ,pygame.math.Vector2(3,10)]
        self.velocity = pygame.math.Vector2(1,0)

class Snake_Food:
    def __init__(self):
        self.random_food_position()
    
    def food(self):
        food_shape = pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y*cell_size), cell_size, cell_size)
        pygame.draw.rect(gamewindow, "blue", food_shape)

    def random_food_position(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = pygame.math.Vector2(self.x,self.y) 

class MAIN:
    
    def __init__(self):
        self.s = Snake()
        self.sf = Snake_Food()

    def update(self):
        self.s.snake_movement()
        self.snake_eat_mechanism()
        self.collision()

    def object_shapes(self):
        self.sf.food()
        self.s.snake_body()

    def snake_eat_mechanism(self):
        if self.sf.pos == self.s.body[0]:
            self.sf.random_food_position()
            self.s.add_body_segment()

        for segment in self.s.body[1:]:
            if segment == self.sf.pos:
                self.sf.random_food_position()

    def collision(self):
        if not 0 <= self.s.body[0].x < cell_number:
            game_over_screen()
            
        if not 0 <= self.s.body[0].y < cell_number:
            game_over_screen()
           
        for segment in self.s.body[1:]:
            if segment == self.s.body[0]:
                game_over_screen()
               

main = MAIN()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,120)   

def game_over_screen():

    gameoverloop = True                                                                                                                                 
    gameoverwindow = pygame.display.set_mode((cell_size*cell_number,cell_size*cell_number ))
    pygame.display.set_caption("Game Over")

    button_surface = pygame.image.load("button.png")
    button_surface = pygame.transform.scale(button_surface, (300,200))
    game_over_button = Button(button_surface, 300,300, "Restart")

    while gameoverloop:

        gameoverwindow.fill("white")
        GAME_OVER_TEXT = button_font.render("GAME OVER", True, "red")
        SCORE_TOTAL_TEXT = button_font.render("your score was:" + " " + str(len(main.s.body)-3), True, "green")
        GAME_OVER_RECT = GAME_OVER_TEXT.get_rect(center=(300,100))
        SCORE_TOTAL_RECT = SCORE_TOTAL_TEXT.get_rect(center=(300, 150))
        gameoverwindow.blit(SCORE_TOTAL_TEXT, SCORE_TOTAL_RECT)
        gameoverwindow.blit(GAME_OVER_TEXT, GAME_OVER_RECT)
        game_over_button
        game_over_button.update()
        

        for event in pygame.event.get():     
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                x,y = pygame.mouse.get_pos()
                if game_over_button.rect.collidepoint(x,y):
                    print("Game Restarted!")
                    main.s.snake_reset()
                    play() 
             
        pygame.display.update()

def play():
    
     
    pygame.display.set_caption("Snake")  
    while gameloops: 
        for event in pygame.event.get():     
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
#Custom event that looks to this event every 120 milliseconds which then calls the update method (snake continuously moves, allows for food to populate after collision, and checks for collisions)
            if event.type == SCREEN_UPDATE:
                main.update() 
#Movement control 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if main.s.velocity.y != -1:
                        main.s.velocity = pygame.math.Vector2(0,1)
                elif event.key == pygame.K_UP:
                    if main.s.velocity.y != 1:
                        main.s.velocity = pygame.math.Vector2(0,-1)
                elif event.key == pygame.K_LEFT:
                    if main.s.velocity.x != 1:
                        main.s.velocity = pygame.math.Vector2(-1,0)
                elif event.key == pygame.K_RIGHT:
                    if main.s.velocity.x != -1:
                        main.s.velocity = pygame.math.Vector2(1,0)
      
           
            gamewindow.fill('black')
            main.object_shapes()
            pygame.display.update() 

def start_menu():
    startmenuloop = True                                                                                                                                 
    startmenuscreen = pygame.display.set_mode((cell_size*cell_number,cell_size*cell_number ))
    pygame.display.set_caption("Start")

    button_surface = pygame.image.load("button.png")
    button_surface = pygame.transform.scale(button_surface, (300,200))
    start_button = Button(button_surface, 300,300, "Play")
    
    while startmenuloop:

        startmenuscreen.fill("white")
        START_MENU_TEXT = button_font.render("SNAKE", True, "red")
        START_MENU_RECT = START_MENU_TEXT.get_rect(center=(300,100))
        startmenuscreen.blit(START_MENU_TEXT, START_MENU_RECT)
        start_button
        start_button.update()
        

        for event in pygame.event.get():     
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                x,y = pygame.mouse.get_pos()
                if start_button.rect.collidepoint(x,y):
                    print("Game Started!")
                    play() 
             
        pygame.display.update()


start_menu()