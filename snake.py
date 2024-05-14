import pygame
import time
import random

snake_speed = 10

window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Internal pygame globals
game_window = None
fps = None


###############################################################################
def main():

	init_window()
	
	# Initialize game state
	score = 0
	level = 1
	direction = 'RIGHT'
	snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
	wall = []
	for y in range(100,380,10):
		wall.append([360,y])
	fruit_position = get_new_fruit_position(wall)
	eat_sound = pygame.mixer.Sound("Dalton_Eat.wav")
	die_sound = pygame.mixer.Sound("Dalton_Die.wav")

	while True:

		# Handle game state
		direction = handle_key_press(direction)
		snake_body = grow_snake(snake_body, direction)
		
		if snake_ate_fruit(snake_body, fruit_position, eat_sound):
			score += 1
			if score % 2 == 0:
				level += 1
			fruit_position = get_new_fruit_position(wall)
		else:
			snake_body.pop()
		
		if check_game_over(snake_body, wall):
			game_over(level, die_sound)
		
		# Display new state
		game_window.fill(black)
		draw_snake(snake_body, direction)
		draw_wall(wall)
		draw_fruit(fruit_position)
		show_level(level)
		update_window(get_snake_speed(level))


###############################################################################
def get_snake_speed(level):
	return 4 + level


###############################################################################
def get_new_fruit_position(wall):
	
	while True:
		x = random.randrange(1, (window_x//10)) * 10
		y = random.randrange(1, (window_y//10)) * 10
		hit_wall = False
		
		for pos in wall:
			if x == pos[0] and y == pos[1]:
				hit_wall = True
				
		if not hit_wall:
			break
	
	return [x,y]


###############################################################################
def init_window():

	global game_window
	global fps
	
	pygame.init()
	pygame.display.set_caption('Dalton\'s Snake Game')
	game_window = pygame.display.set_mode((window_x, window_y))
	fps = pygame.time.Clock()


###############################################################################
def update_window(snake_speed):
	pygame.display.update()
	fps.tick(snake_speed)


###############################################################################
def show_level(level):
	score_font = pygame.font.SysFont("times new roman", 20)
	score_surface = score_font.render('Level : ' + str(level), True, white)
	score_rect = score_surface.get_rect()
	game_window.blit(score_surface, score_rect)


###############################################################################
def game_over(level, die_sound):

	# Die sound
	pygame.mixer.Sound.play(die_sound)
	pygame.mixer.music.stop()
	
	# Create rectangle of Game Over text
	my_font = pygame.font.SysFont('times new roman', 50)
	game_over_surface = my_font.render(
		'Your level is : ' + str(level), True, red)
	game_over_rect = game_over_surface.get_rect()
	game_over_rect.midtop = (window_x/2, window_y/4)
	
	# blit will draw the text on screen
	game_window.blit(game_over_surface, game_over_rect)
	pygame.display.flip()
	
	# after 2 seconds we will quit the program
	time.sleep(2)
	pygame.quit()
	quit()


###############################################################################
def handle_key_press(direction):

	# In case multiple key presses between animation updates
	orig_direction = direction
	
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and orig_direction != 'DOWN':
				direction = 'UP'
			if event.key == pygame.K_DOWN and orig_direction != 'UP':
				direction = 'DOWN'
			if event.key == pygame.K_LEFT and orig_direction != 'RIGHT':
				direction = 'LEFT'
			if event.key == pygame.K_RIGHT and orig_direction != 'LEFT':
				direction = 'RIGHT'

	return direction


###############################################################################
def draw_snake(snake_body, direction):
	for pos in snake_body:
		pygame.draw.rect(game_window, green, 
			pygame.Rect(pos[0], pos[1], 10, 10))
	
	snake_head = snake_body[0]
	if direction == "LEFT" or direction == "RIGHT":
		pygame.draw.rect(game_window, red,
			pygame.Rect(snake_head[0]+4, snake_head[1]+2, 2, 2))
		pygame.draw.rect(game_window, red,
			pygame.Rect(snake_head[0]+4, snake_head[1]+6, 2, 2))
	else:
		pygame.draw.rect(game_window, red,
			pygame.Rect(snake_head[0]+2, snake_head[1]+4, 2, 2))
		pygame.draw.rect(game_window, red,
			pygame.Rect(snake_head[0]+6, snake_head[1]+4, 2, 2))


###############################################################################
def draw_wall(wall):
	for pos in wall:
		pygame.draw.rect(game_window, red, 
			pygame.Rect(pos[0], pos[1], 10, 10))
			
			
###############################################################################
def draw_fruit(fruit_position):
	pygame.draw.rect(game_window, white, 
		pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))


###############################################################################
def check_game_over(snake_body, wall):

	snake_head = snake_body[0]

	# Edge of screen
	if snake_head[0] < 0 or snake_head[0] > window_x-10:
		return True
	if snake_head[1] < 0 or snake_head[1] > window_y-10:
		return True

	# Touching the snake body
	for block in snake_body[1:]:
		if snake_head[0] == block[0] and snake_head[1] == block[1]:
			return True
			
	# Touching the wall
	for block in wall:
		if snake_head[0] == block[0] and snake_head[1] == block[1]:
			return True

	# Not game over
	return False


###############################################################################
def grow_snake(snake_body, direction):

	snake_head = snake_body[0].copy()

	if direction == 'UP':
		snake_head[1] -= 10
	if direction == 'DOWN':
		snake_head[1] += 10
	if direction == 'LEFT':
		snake_head[0] -= 10
	if direction == 'RIGHT':
		snake_head[0] += 10

	snake_body.insert(0, list(snake_head))
	return snake_body


###############################################################################
def snake_ate_fruit(snake_body, fruit_position, eat_sound):

	snake_head = snake_body[0].copy()
	
	if snake_head[0] == fruit_position[0] and snake_head[1] == fruit_position[1]:
		pygame.mixer.Sound.play(eat_sound)
		pygame.mixer.music.stop()
		return True
	else:
		return False


###############################################################################
if __name__ == "__main__":
	main()


