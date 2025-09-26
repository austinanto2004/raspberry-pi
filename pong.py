import pygame
import sys

# 1. Initialize Pygame
pygame.init()

# 2. Screen and Display Settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong Game")

# 3. Colors
black = (0, 0, 0)
white = (255, 255, 255)

# 4. Paddle and Ball Properties
paddle_width = 15
paddle_height = 100
ball_radius = 10

# Paddle positions and speed
paddle1_x = 50
paddle1_y = screen_height / 2 - paddle_height / 2
paddle1_speed = 7

paddle2_x = screen_width - 50 - paddle_width
paddle2_y = screen_height / 2 - paddle_height / 2
paddle2_speed = 7

# Ball position and speed
ball_x = screen_width / 2
ball_y = screen_height / 2
ball_speed_x = 5
ball_speed_y = 5

# Score
player1_score = 0
player2_score = 0
font = pygame.font.Font(None, 74)

# Game Clock to control FPS
clock = pygame.time.Clock()

# 5. Game Loop
def game_loop():
    global paddle1_y, paddle2_y, ball_x, ball_y, ball_speed_x, ball_speed_y
    global player1_score, player2_score

    running = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 6. Paddle Movement (User Input)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= paddle1_speed
        if keys[pygame.K_s] and paddle1_y < screen_height - paddle_height:
            paddle1_y += paddle1_speed
        if keys[pygame.K_UP] and paddle2_y > 0:
            paddle2_y -= paddle2_speed
        if keys[pygame.K_DOWN] and paddle2_y < screen_height - paddle_height:
            paddle2_y += paddle2_speed

        # 7. Ball Movement
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # 8. Ball Collisions with top and bottom walls
        if ball_y - ball_radius <= 0 or ball_y + ball_radius >= screen_height:
            ball_speed_y *= -1

        # 9. Ball Collisions with Paddles
        # Player 1 paddle
        if ball_x - ball_radius <= paddle1_x + paddle_width and ball_y >= paddle1_y and ball_y <= paddle1_y + paddle_height:
            ball_speed_x *= -1

        # Player 2 paddle
        if ball_x + ball_radius >= paddle2_x and ball_y >= paddle2_y and ball_y <= paddle2_y + paddle_height:
            ball_speed_x *= -1

        # 10. Scoring
        if ball_x < 0:
            player2_score += 1
            ball_x = screen_width / 2
            ball_y = screen_height / 2
            ball_speed_x *= -1
        
        if ball_x > screen_width:
            player1_score += 1
            ball_x = screen_width / 2
            ball_y = screen_height / 2
            ball_speed_x *= -1

        # 11. Drawing all elements
        screen.fill(black)
        pygame.draw.rect(screen, white, (paddle1_x, paddle1_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, white, (paddle2_x, paddle2_y, paddle_width, paddle_height))
        pygame.draw.circle(screen, white, (int(ball_x), int(ball_y)), ball_radius)
        
        # Draw the scores
        score_text = font.render(f"{player1_score}   {player2_score}", True, white)
        screen.blit(score_text, (screen_width / 2 - score_text.get_width() / 2, 10))

        # Draw the dashed line in the center
        for i in range(0, screen_height, 20):
            pygame.draw.line(screen, white, (screen_width / 2, i), (screen_width / 2, i + 10))

        # 12. Update the display
        pygame.display.flip()

        # 13. Control the game speed
        clock.tick(60)

    # 14. Quit Pygame and exit
    pygame.quit()
    sys.exit()

if _name_ == "_main_":
    game_loop()