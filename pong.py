import pygame

# ------------------<< main class >>---------------------------
class pong:
	# ---------
	# CONSTANTS
	# ---------
	WHITE = (255, 255, 255)
	WIDTH, HEIGHT = 900, 500
	BLACK = (0, 0, 0)
	RED = (255, 0, 0)

	def __init__(self,player1,player2):
		# ---------
		# VARIABLES
		# ---------
		self.player1=player1
		self.player2=player2
		self.playing = False
		
		# SCREEN
		pygame.init()
		self.screen = pygame.display.set_mode( (self.WIDTH, self.HEIGHT) )
		pygame.display.set_caption('PONG')
		self.clock = pygame.time.Clock()
		self.draw_board()
		# -------
		# OBJECTS
		# -------
		self.paddle1 = Paddle( self.screen, self.WHITE, 15, self.HEIGHT//2 - 60, 20, 120 )
		self.paddle2 = Paddle( self.screen, self.WHITE, self.WIDTH - 20 - 15, self.HEIGHT//2 - 60, 20, 120 )
		self.ball = Ball( self.screen, self.WHITE, self.WIDTH//2, self.HEIGHT//2, 12 )
		self.collision = CollisionManager()
		self.score1 = PlayerScore( self.screen, '0', self.WIDTH//4, 15 )
		self.score2 = PlayerScore( self.screen, '0', self.WIDTH - self.WIDTH//4, 15 )
  
	# methods
	def draw_board(self):
		self.screen.fill( self.BLACK )
		pygame.draw.line( self.screen, self.WHITE, (self.WIDTH//2, 0), (self.WIDTH//2, self.HEIGHT), 5 )

	def restart(self):
		self.draw_board()
		self.score1.restart()
		self.score2.restart()
		self.ball.restart_pos()
		self.paddle1.restart_pos()
		self.paddle2.restart_pos()


class Paddle(pong):
	def __init__(self, screen, color, posX, posY, width, height):
		self.screen = screen
		self.color = color
		self.posX = posX
		self.posY = posY
		self.width = width
		self.height = height
		self.state = 'stopped'
		self.draw()

	def draw(self):
		pygame.draw.rect( self.screen, self.color, (self.posX, self.posY, self.width, self.height) )

	def move(self):
		# moving up
		if self.state == 'up':
			self.posY -= 10

		# moving down
		elif self.state == 'down':
			self.posY += 10

	def clamp(self):
		if self.posY <= 0:
			self.posY = 0

		if self.posY + self.height >=pong.HEIGHT:
			self.posY = pong.HEIGHT - self.height

	def restart_pos(self):
		self.posY = pong.HEIGHT//2 - self.height//2
		self.state = 'stopped'
		self.draw()

class Ball(pong):
	def __init__(self, screen, color, posX, posY, radius):
		self.screen = screen
		self.color = color
		self.posX = posX
		self.posY = posY
		self.dx = 0
		self.dy = 0
		self.radius = radius
		self.draw()

	def draw(self):
		pygame.draw.circle( self.screen, self.color, (self.posX, self.posY), self.radius )

	def start(self):
		# this will be random
		self.dx = 15
		self.dy = 5

	def move(self):
		self.posX += self.dx
		self.posY += self.dy

	def wall_collision(self):
		self.dy = -self.dy

	def paddle_collision(self):
		self.dx = -self.dx

	def restart_pos(self):
		self.posX = pong.WIDTH//2
		self.posY = pong.HEIGHT//2
		self.dx = 0
		self.dy = 0
		self.draw()

class PlayerScore(pong):
	def __init__(self, screen, points, posX, posY):
		self.screen = screen
		self.points = points
		self.posX = posX
		self.posY = posY
		self.font = pygame.font.SysFont("monospace", 80, bold=True)
		self.label = self.font.render(self.points, 0, pong.WHITE)
		self.show()

	def show(self):
		self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))

	def increase(self):
		points = int(self.points) + 1
		self.points = str(points)
		self.label = self.font.render(self.points, 0, pong.WHITE)

	def restart(self):
		self.points = '0'
		self.label = self.font.render(self.points, 0, pong.WHITE)

class CollisionManager(pong):
	def __init__(self):
		print("init CollisionManager")
	def between_ball_and_paddle1(self, ball, paddle):
		ballX = ball.posX
		ballY = ball.posY
		paddleX = paddle.posX
		paddleY = paddle.posY

		# y is in collision area?
		if ballY + ball.radius > paddleY and ballY - ball.radius < paddleY + paddle.height:
			# x is in collision area?
			if ballX - ball.radius <= paddleX + paddle.width:
				# collision
				return True

		# no collision
		return False

	def between_ball_and_paddle2(self, ball, paddle):
		ballX = ball.posX
		ballY = ball.posY
		paddleX = paddle.posX
		paddleY = paddle.posY

		# y is in collision?
		if ballY + ball.radius > paddleY and ballY - ball.radius < paddleY + paddle.height:
			# x is in collision?
			if ballX + ball.radius >= paddleX:
				# collision
				return True

		# no collision
		return False

	def between_ball_and_walls(self, ball):
		ballY = ball.posY

		# top collision
		if ballY - ball.radius <= 0:
			return True

		# bottom collision
		if ballY + ball.radius >= pong.HEIGHT:
			return True

		# no collision
		return False

	def between_ball_and_goal1(self, ball):
		return ball.posX + ball.radius <= 0

	def between_ball_and_goal2(self, ball):
		return ball.posX - ball.radius >= pong.WIDTH

