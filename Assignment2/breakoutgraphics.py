"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 100      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a label and score
        self.score = 0
        self.label = GLabel('Hits: ' + str(self.score))
        self.label.font = '-50'
        self.window.add(self.label, x=window_width//2-self.label.width//2, y=self.label.height)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.window.add(self.paddle, x=(window_width-paddle_width)//2, y=window_height-paddle_offset)
        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius, ball_radius)
        self.ball.filled = True
        self.window.add(self.ball, x=window_width//2, y=window_height//2)
        # Default initial velocity for the ball
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        # Initialize our mouse listeners
        self.trigger = False
        onmouseclicked(self.ball_move)
        onmousemoved(self.paddle_move)
        # Draw bricks
        self.brick_count = 0
        self.create_bricks()

    def paddle_move(self, position):
        self.paddle.x = position.x - self.paddle.width//2
        if self.paddle.x <= 0:
            self.paddle.x = 0
        elif self.paddle.x >= self.window.width - self.paddle.width:
            self.paddle.x = self.window.width - self.paddle.width

    def ball_move(self, position):
        if self.__dx > MAX_X_SPEED // 2:
            self.__dx *= -1

        self.trigger = True

    def get_ball_speed(self):
        return self.__dx, self.__dy

    def create_bricks(self):
        for i in range(BRICK_ROWS):
            for j in range(BRICK_COLS):
                self.brick_count += 1
                self.brick = GRect(BRICK_WIDTH, BRICK_HEIGHT)
                self.brick.filled = True
                self.brick.fill_color = (i*20, i*20, i*20)
                self.window.add(self.brick,
                                x=(self.brick.width+BRICK_SPACING)*j,
                                y=BRICK_OFFSET+(BRICK_HEIGHT+BRICK_SPACING)*i)


class RestartGame(BreakoutGraphics):
    def reset(self):
        self.create_bricks()

        self.score = 0
        self.ball.x = (self.window.width - self.ball.width) // 2
        self.ball.y = (self.window.height - self.ball.height) // 2
        self.trigger = False
        onmouseclicked(self.reset, )





