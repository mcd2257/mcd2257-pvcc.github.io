import pygame 
import sys
import random 
pygame.init() 

cell_size = 30
cell_number = 20
  
gamewindow = pygame.display.set_mode((cell_size*cell_number,cell_size*cell_number )) 
pygame.display.set_caption("Snake")  

gameloops = True

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
            pygame.quit()
            sys.exit()
            
        if not 0 <= self.s.body[0].y < cell_number:
            pygame.quit()
            sys.exit()
            
        for segment in self.s.body[1:]:
            if segment == self.s.body[0]:
                pygame.quit()
                sys.exit()





main = MAIN()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,120) 
         
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
    

