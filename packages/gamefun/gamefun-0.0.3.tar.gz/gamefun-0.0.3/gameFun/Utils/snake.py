import pygame

class SnakeGame:
    def __init__(self, width=500, height=500):
        pygame.init()
        self.width = width
        self.height = height
        self.snake_block_size = 10
        self.snake_length = 1
        self.snake_list = [[250, 250]]
        self.speed = 10
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'green': (0, 255, 0),
            'red': (255, 0, 0)
        }
        self.food_x = -100
        self.food_y = -100
        self.score = 0
        self.font = pygame.font.SysFont(None, 25)
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simple Snake Game")
        self.clock = pygame.time.Clock()

    def draw_snake(self, snake_list):
        for x, y in snake_list:
            pygame.draw.rect(self.window, self.colors['green'], (x, y, self.snake_block_size, self.snake_block_size))
    
    def draw_food(self):
        # self.food_size = self.snake_block_size
        pygame.draw.rect(self.window, self.colors['red'], (self.food_x, self.food_y, self.snake_block_size, self.snake_block_size))

    def display_message(self, msg, color):
        message_text = self.font.render(msg, True, self.colors[color])
        self.window.blit(message_text, [self.width / 6, self.height / 6])

    def run(self, update_snake_position=None, 
            radom_food_function=None, 
            check_collision_well=None,
            check_collision_snake=None,
            reset_game=None,
            snake_eat_food=None,
            current_direction=""):
        """
        Start and run the main loop of the snake game.

        This function controls the game's main loop and continues running until the game is over. It updates the game state, processes user input, moves the snake, generates food, checks for collisions, and updates the display.

        Args:
            update_snake_position (callable, optional): 
                A function that updates the snake's head position based on the user's keyboard input. It should accept the current event, the snake head's x and y coordinates, and the current movement direction as arguments. It should return the updated head x and y coordinates along with the new movement direction. If this function is not provided, the snake will not move.

            random_food_function (callable, optional): 
                A function to randomly generate the position of the food within the game area. It should accept the game area's width, height, and the food size as arguments and return the x and y coordinates for the food within the game area. If this function is not provided, food will not appear in the game.

            check_collision_well (callable, optional): 
                A function to check if the snake has collided with the wall. It should accept the snake head's x and y coordinates, the game's width and height, and a boolean indicating if the game is over. It should return a boolean indicating if the game should end due to collision.

            check_collision_snake (callable, optional): 
                A function to check if the snake has collided with itself. It should accept the snake head's x and y coordinates, the list of all snake segments, and a boolean indicating if the game is over. It returns a boolean indicating if the game should end due to self-collision.

            reset_game (callable, optional): 
                A function that resets the game state. It is called when the game ends and should set up initial values for the snake head's x and y coordinates, the snake's length, the food's x and y coordinates, and the current direction.

            snake_eat_food (callable, optional): 
                A function that handles the snake eating the food. It should accept the snake head's x and y coordinates, the food's x and y coordinates, the game's width and height, the snake block size, the snake's length, and the current score. It should update the position of the food, the length of the snake, and the score.

            current_direction (str, optional): 
                A string representing the current direction of the snake's movement. Valid values are "left", "right", "up", and "down". If not provided, defaults to an empty string, which indicates that the snake will not move at the start of the game.

        The method sets up a game loop that runs until the game is over, handling events such as keyboard inputs, updating the snake and food positions, and redrawing the screen on each loop iteration. If the snake hits the edges of the game area, the game will end.

        During the loop, if a reset is needed (the game is over and `reset_game` is provided), it will reset the game state. If the snake eats food and `snake_eat_food` is provided, it will handle scoring and snake growth. Collisions are checked with the walls and the snake itself using `check_collision_well` and `check_collision_snake`. If a collision occurs, `game_over` becomes True, ending the game.
        """
        game_over = False
        self.snake_list = [[self.head_x, self.head_y]]
        while True:
            if (reset_game is not None) and game_over:
                game_over = False
                self.head_x, self.head_y, self.snake_length, self.food_x, self.food_y, current_direction = reset_game(self.width, self.height, self.snake_block_size)
                self.snake_list = [[self.head_x, self.head_y]]
            elif game_over:
                pygame.quit()
                return
            
            while not game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                # 生成食物
                if radom_food_function is not None and self.food_x == -100 and self.food_y == -100:
                    self.food_x, self.food_y =  radom_food_function(self.width, self.height, self.snake_block_size)

                head_x, head_y = self.snake_list[-1]
                if update_snake_position is not None:
                    head_x, head_y, current_direction = update_snake_position(event, head_x, head_y, current_direction)
                
                # 蛇吃食物
                if snake_eat_food is not None:
                    self.food_x, self.food_y, self.snake_length, self.score = snake_eat_food(head_x, head_y, self.food_x, self.food_y, self.width, self.height, self.snake_block_size, self.snake_length, self.score)

                # 添加新的蛇头位置
                self.snake_list.append([head_x, head_y])
                # print(str(self.snake_list[-1]) + " " + str(self.snake_length))
                # 确保蛇只有一个方块（蛇头），后续可以添加身体增长的功能
                if len(self.snake_list) > self.snake_length:
                    del self.snake_list[0]
                
                self.window.fill(self.colors['white'])
                self.draw_food()
                self.draw_snake(self.snake_list)
                self.display_message("Score: " + str(self.score), 'black')
                pygame.display.update()
                self.clock.tick(self.speed)

                if check_collision_well is not None:
                    game_over = check_collision_well(head_x, head_y, self.width, self.height, game_over)
                
                if check_collision_snake is not None:
                    game_over = check_collision_snake(head_x, head_y, self.snake_list, game_over)
