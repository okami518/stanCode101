"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics, RestartGame

FRAME_RATE = 0.0000001         # 100 frames per second
NUM_LIVES = 3			# Number of attempts

graphics = RestartGame()
window = graphics.window


def main():

    brick_count = graphics.brick_count
    ball = graphics.ball
    paddle = graphics.paddle
    dx, dy = graphics.get_ball_speed()
    die = 0

    while die < NUM_LIVES:
        graphics.label.text = 'Hits: ' + str(graphics.score)
        if graphics.trigger:
            # 球體運動
            ball.move(dx, dy)
            if ball.y > window.height:
                die += 1
                ball.x = (window.width + ball.width)//2 - ball.width
                ball.y = (window.height + ball.height)//2
                graphics.trigger = False

            # 球的四點
            ball_up = window.get_object_at(ball.x+ball.width//2, ball.y)
            ball_down = window.get_object_at(ball.x+ball.width//2, ball.y+ball.height)
            ball_left = window.get_object_at(ball.x, ball.y + ball.height//2)
            ball_right = window.get_object_at(ball.x+ball.width, ball.y + ball.height//2)
            bl_ball = window.get_object_at(ball.x, ball.y + ball.height)  # bottom-left
            br_ball = window.get_object_at(ball.x + ball.width, ball.y + ball.height)  # bottom-right

            # 球的反彈機制
                # 邊界
            if ball.x+ball.width >= window.width or ball.x <= 0:
                dx = -dx
                # paddle
            if (bl_ball is paddle or br_ball is paddle) and dy > 0 or ball.y <= 0:
                dy = -dy

                # 磚塊
            if ball_up is not None and ball_up is not ball:
                window.remove(ball_up)
                graphics.score += 1
                dy = -dy
            elif ball_down is not None and ball_down is not paddle and ball_down is not ball:
                window.remove(ball_down)
                graphics.score += 1
                dy = -dy
            elif ball_left is not None and ball_left is not paddle and ball_left is not ball:
                window.remove(ball_left)
                graphics.score += 1
                dx = -dx
            elif ball_right is not None and ball_right is not paddle and ball_right is not ball:
                window.remove(ball_right)
                graphics.score += 1
                dx = -dx
            if graphics.score == brick_count:
                graphics.label.x = graphics.label.x-50
                graphics.label.text = 'Congrats!!!'
                break
        pause(FRAME_RATE)


if __name__ == '__main__':
    while True:
        main()
        input("Press Enter to restart...")
        graphics.reset()
