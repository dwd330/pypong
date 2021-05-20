from pong import *
from client import *
import sys,random
from easygui import *  #for form input
#     ..........<<   MAIN task  >>...................
#get user input from gui
msg = "Enter some information"
title = " X O game network"
fieldNames = ["yourName", " play with", "left or right?"]
fieldValues = multenterbox(msg, title, fieldNames)
#assign input 
clientid1=fieldValues[0]
clientid2=fieldValues[1]
tag=fieldValues[2] #x or o tag
if tag=='left':
	myplayer=1
	otherplayer=2
elif tag=='right':
	myplayer=2
	otherplayer=1
else:
	myplayer=1
	otherplayer=2
#start new game 
clientplayer=Client(clientid1,clientid2) #create client opject
mygame=pong(myplayer,otherplayer) #create game opject

def handleotherplayerdata():
	data=clientplayer.get_data()
	if data:
		print(data)
		if data=="w":
			mygame.paddle1.state = 'up'
		elif data=="s":
			mygame.paddle1.state = 'down'
		elif data=="k_up":
			mygame.paddle2.state = 'up'
		elif data =="k_down":
			mygame.paddle2.state = 'down'
		elif data=="p":
			mygame.ball.start()
			mygame.playing = True

		elif data =="stopped":
			mygame.paddle1.state = 'stopped'
			mygame.paddle2.state = 'stopped'

# --------
# MAINLOOP
# --------
while True:
	handleotherplayerdata()
	mygame.clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_p and not mygame.playing:
				mygame.ball.start()
				mygame.playing = True
				clientplayer.send("p")

			if event.key == pygame.K_r and mygame.playing:
				mygame.restart()
				mygame.playing = False

			if event.key == pygame.K_w:
				mygame.paddle1.state = 'up'
				clientplayer.send("w")

			if event.key == pygame.K_s:
				mygame.paddle1.state = 'down'
				clientplayer.send("s")

			if event.key == pygame.K_UP:
				mygame.paddle2.state = 'up'
				clientplayer.send("k_up")

			if event.key == pygame.K_DOWN:
				mygame.paddle2.state = 'down'
				clientplayer.send("k_down")

		if event.type == pygame.KEYUP:
			mygame.paddle1.state = 'stopped'
			mygame.paddle2.state = 'stopped'
			clientplayer.send("stopped")

	if mygame.playing:
		mygame.draw_board()

		# ball
		mygame.ball.move()
		mygame.ball.draw()

		# paddle 1
		mygame.paddle1.move()
		mygame.paddle1.clamp()
		mygame.paddle1.draw()

		# paddle 2
		mygame.paddle2.move()
		mygame.paddle2.clamp()
		mygame.paddle2.draw()

		# wall collision
		if mygame.collision.between_ball_and_walls(mygame.ball):
			print('WALL COLLISION')
			mygame.ball.wall_collision()

		# paddle1 collision
		if mygame.collision.between_ball_and_paddle1(mygame.ball, mygame.paddle1):
			print('COLLISION WITH PADDLE 1')
			mygame.ball.paddle_collision()

		# paddle2 collision
		if mygame.collision.between_ball_and_paddle2(mygame.ball, mygame.paddle2):
			print('COLLISION WITH PADDLE 2')
			mygame.ball.paddle_collision()

		# GOAL OF PLAYER 1 !
		if mygame.collision.between_ball_and_goal2(mygame.ball):
			mygame.draw_board()
			mygame.score1.increase()
			mygame.ball.restart_pos()
			mygame.paddle1.restart_pos()
			mygame.paddle2.restart_pos()
			mygame.playing = False

		# GOAL OF PLAYER 2!
		if mygame.collision.between_ball_and_goal1(mygame.ball):
			mygame.draw_board()
			mygame.score2.increase()
			mygame.ball.restart_pos()
			mygame.paddle1.restart_pos()
			mygame.paddle2.restart_pos()
			mygame.playing = False

	mygame.score1.show()
	mygame.score2.show()

	pygame.display.update()