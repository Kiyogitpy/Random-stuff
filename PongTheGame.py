import pygame
import sys #used for font

# pygame setup
pygame.init()
screen = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()
running = True
dt = 0
speed = 600
new_height = 60

player_pos = pygame.Vector2(10, screen.get_height() / 2)
player2_pos = pygame.Vector2(screen.get_width() - 30, screen.get_height() / 2)
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_speed = pygame.Vector2(speed / 2, 0)
ball_rect = pygame.Rect(ball_pos.x, ball_pos.y, 20, 20)
player_rect = pygame.Rect(player_pos.x, player_pos.y, 20, 60)
player2_rect = pygame.Rect(player2_pos.x, player2_pos.y, 20, 60)


player_score = 0
player2_score = 0

# Define the font
font = pygame.font.Font(None, 36)  # You can specify the font file path and size


while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from the last frame
    screen.fill("black")
    pygame.draw.rect(screen, "white", ball_rect)
    pygame.draw.rect(screen, "white", player_rect)
    pygame.draw.rect(screen, "white", player2_rect)
    
    # To get the lowest y-coordinate of player_rect (bottom edge)
    player_edge = player_rect.y + player_rect.height
    # To get the lowest y-coordinate of player2_rect (bottom edge)
    player2_edge = player2_rect.y + player2_rect.height

    keys = pygame.key.get_pressed()
    # player1
    if keys[pygame.K_w] and not player_rect.y < 10:
        player_rect.y -= speed * dt
    if keys[pygame.K_s] and not player_edge > 500:
        player_rect.y += speed * dt

    # player2
    if keys[pygame.K_UP] and not player2_rect.y < 10:
        player2_rect.y -= speed * dt
    if keys[pygame.K_DOWN] and not player2_edge > 500:
        player2_rect.y += speed * dt

    # Update ball position based on its speed and delta time
    ball_pos += ball_speed * dt
    ball_rect.x, ball_rect.y = ball_pos.x, ball_pos.y

    # Check for collision with player1
    if ball_rect.colliderect(player_rect):
        ball_speed.x *= -1  # Change ball's horizontal direction on collision

        # Calculate the collision point's relative position on the player's surface
        relative_y_collision = (ball_pos.y + ball_rect.height / 2) - player_rect.center[1]
        # Normalize the relative collision position to a range between -1 and 1
        normalized_collision = relative_y_collision / (player_rect.height / 2)
        # Adjust the ball's vertical speed based on the normalized collision position
        ball_speed.y = normalized_collision * (speed / 2)
        #get current y value of playerpos
        new_height -= 1 
        player_rect = pygame.Rect(player_pos.x, player_rect.y, 20, new_height)
        player2_rect = pygame.Rect(player2_pos.x, player2_rect.y, 20, new_height)

    # Check for collision with player2
    if ball_rect.colliderect(player2_rect):
        ball_speed.x *= -1  # Change ball's horizontal direction on collision

        # Calculate the collision point's relative position on the player's surface
        relative_y_collision = (ball_pos.y + ball_rect.height / 2) - player2_rect.center[1]
        # Normalize the relative collision position to a range between -1 and 1
        normalized_collision = relative_y_collision / (player2_rect.height / 2)
        # Adjust the ball's vertical speed based on the normalized collision position
        ball_speed.y = normalized_collision * (speed / 2)

        new_height -= 1 
        player_rect = pygame.Rect(player_pos.x, player_rect.y, 20, new_height)
        player2_rect = pygame.Rect(player2_pos.x, player2_rect.y, 20, new_height)

    # Check for collision with top and bottom of the screen
    if ball_pos.y < 0 or ball_pos.y > screen.get_height() - 20:
        ball_speed.y *= -1  # Change ball's vertical direction on collision

    if ball_pos.x > screen.get_width():
        player_score += 1
        ball_pos.x = screen.get_width() / 2
    elif ball_pos.x < 0:
        player2_score += 1
        ball_pos.x = screen.get_width() / 2

    player_score_string = str(player_score)
    player2_score_string = str(player2_score)
     # Combine player scores into a single string
    score_text = f"Player 1: {player_score_string}  Player 2: {player2_score_string}"
    score_win_1 = f"Player 1 wins!: {player_score_string}"
    score_win_2 = f"Player 2 wins!: {player2_score_string}"
    # Create a text surface
    text_surface = font.render(score_text, True, (255, 255, 255))
    text_win_player = font.render(score_win_1, True, (255, 255, 255))
    text_win_player2 = font.render(score_win_2, True, (255, 255, 255))
    text_draw = font.render("Draw", True, (255, 255, 255))

    # Calculate the position to center the text on the screen
    text_x = screen.get_width() // 2 - text_surface.get_width() // 2
    text_y = screen.get_height() // 2 - text_surface.get_height() // 2 - 200




    if new_height < 30:
        if player_score > player2_score:
            screen.blit(text_win_player, (text_x,text_y))
        elif player2_score > player_score:
            screen.blit(text_win_player2, (text_x,text_y))
        else:
            screen.blit(text_draw, (text_x,text_y))

        ball_pos = pygame.Vector2(screen.get_width()/2 , screen.get_height()/2 )
    else:
        # Blit the text surface onto the screen at a desired position
        screen.blit(text_surface, (text_x,text_y))

    # Flip() the display to put your work on screen
    pygame.display.flip()

    # Limit FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
