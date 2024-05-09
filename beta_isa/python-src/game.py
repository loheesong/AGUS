import numpy
# import test 

WIDTH = 30
HEIGHT = 15 
PLAYER_LENGTH = 5
MAX_AMMO = 3
MAX_LIVES = 3

def display_screen(players_pos, balls_info):
    """
    (0,0) origin is defined top left
    takes in position of all objects and draw it to screen 
    """
    screen = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]
    BALL = "O"
    PLAYER = "|"

    # draw balls 
    i = 0
    while i < 6:
        x = balls_info[i*3]
        y = balls_info[i*3+1]
        if x != -1 and y != -1:
            screen[y][x] = BALL
        i = i + 1

    # draw player 
    i = 0
    while i < 2:
        player = i*2
        x = players_pos[player]
        y = players_pos[player+1]
        j = 0
        while j < PLAYER_LENGTH:
            screen[y+j][x] = PLAYER
            j = j + 1
        i = i + 1
    # prepare output 
    ans = "" 
    for row in screen:
        out = " ".join(row)
        ans += out + "\n"
    print(ans)

def display_ammo_lives(ammo_lives_counter):
    print(f"p1 ammo: {ammo_lives_counter[0]}", f"p1 lives: {ammo_lives_counter[1]}", f"p2 ammo: {ammo_lives_counter[2]}", f"p2 lives: {ammo_lives_counter[3]}")

def is_win(players_pos, balls_info, ammo_lives_counter) -> bool:
    """
    Trigger end, ammo, lives when balls are at goal line. Also destroy balls 
    """
    i = 0
    while i < 6:
        # ball 0 1 2 belongs to p1, ball 3 4 5 belongs to p2
        ball = i*3
        ball_x = balls_info[ball]
        ball_y = balls_info[ball+1]

        # selects which player fired ball, 0 means ball belongs to p1, 1 means ball belongs to p2 
        player = int(ball >= 9)
        other_player = 2-2*player
        other_playerx = players_pos[other_player]
        other_playery = players_pos[other_player+1]
        ammo_lives_i = player*2
        # ball intersects player 
        if  ball_x == other_playerx:
            # other player defended successfully 
            if ball_y < other_playery or ball_y > other_playery + PLAYER_LENGTH -1:
                # lose 1 life 
                ammo_lives_counter[ammo_lives_i+1] = ammo_lives_counter[ammo_lives_i+1] - 1
            # destroy ball 
            balls_info[ball] = -1
            balls_info[ball+1] = -1
            balls_info[ball+2] = -1
            ammo = ammo_lives_counter[ammo_lives_i]
            # regen 1 ammo, keep below max ammo
            if ammo <= MAX_AMMO-1:
                ammo_lives_counter[ammo_lives_i] = ammo + 1
        i = i + 1

    # check lives to determine game state 
    return ammo_lives_counter[1] == 0 or ammo_lives_counter[3] == 0 

def poll_input() -> list[int]:
    """this function will work differently in beta assembly. Press enter without typing to skip input"""
    # left right aim fire 
    print("Format: up down aim fire")
    p1_in = input("P1 input: ")
    p2_in = input("P2 input: ")
    blank = [0,0,0,0]
    if p1_in != "" and p2_in != "":
        return [int(i) for i in (p1_in.split() + p2_in.split())]
    elif p1_in != "":
        return [int(i) for i in (p1_in.split() + blank)]
    elif p2_in != "":
        return [int(i) for i in (blank + p2_in.split())]
    else:
        return blank + blank

def update_ball_pos(balls_info):
    OFFSET = 1
    # update balls 
    i = 0 
    while i < 6:
        ball = i*3
        x = balls_info[ball]
        y = balls_info[ball+1]
        c = balls_info[ball+2]

        # only offset x if x != -1 aka ball must exist 
        # p1 balls move right, p2 balls move left 
        x = x + (x != -1)*(OFFSET - 2*(i>=3))

        # TODO: might want to optimise this if else 
        if c == 0:
            # if reach top boundary
            if y == 0:
                c = c ^ 1 
                y = y + OFFSET
            else:
                y = y - OFFSET
        elif c == 1:
            # if reach bottom boundary
            if y == HEIGHT-1:
                c = c ^ 1
                y = y - OFFSET
            else:
                y = y + OFFSET 
        balls_info[ball] = x
        balls_info[ball+1] = y
        balls_info[ball+2] = c
        i = i + 1

def update_player_pos(players_pos, inputs, balls_info, ammo_lives_counter):
    """updates player, spawn balls if fire """
    # update player, and spawn new ball if fire pressed 
    j = 0
    max_y = HEIGHT - PLAYER_LENGTH
    OFFSET = 1
    while j < 2:
        player = j*2 
        x = players_pos[player]
        y = players_pos[player+1]

        p_input = j*4
        up = inputs[p_input]
        down = inputs[p_input+1]
        aim = inputs[p_input+2]
        fire = inputs[p_input+3]
        
        # if both up and down pressed, player will not move 
        if up and y > 0:
            y = y - OFFSET
        if down and y < max_y:
            y = y + OFFSET
        players_pos[player+1] = y

        if fire:
            b = 0
            while b < 3:
                ball_no = b*3 + j*9
                # will not spawn ball if there is no space 
                if balls_info[ball_no] == -1 and balls_info[ball_no+1] == -1 and balls_info[ball_no+2] == -1:
                    # spawn ball at middle of paddle
                    balls_info[ball_no] = x + 1-2*j # x, spawn ball next to paddle 
                    balls_info[ball_no+1] = y + PLAYER_LENGTH//2 # y, can just set this to +2 if using 5
                    balls_info[ball_no+2] = aim # c
                    ammo_lives_counter[player] = ammo_lives_counter[player] - 1 # decrease ammo 
                    b = 3 # acts like a break statement 
                b = b + 1
        j = j + 1

"""
player position refers to the top of the paddle with height offset with player length 
players_pos: array of 4 ints -> [p1x, p1y, p2x, p2y]
c: maps the aim direction, value either 0(up) 1(down) 2(middle) 
inputs: array of 8 ints, format p1(up down aim fire), p2(up down aim fire), 
    fire is 1 if pressed, aim values: 0 1 2 (see c, line above)
balls_info: array of 18 int values, index 0 - 8 = p1, 9 - 18 = p2, -1 indicates ball not in play 
ammo_lives_counter: array of 4 ints, ammo1 lives1 ammo2 lives2
"""
def main():
    # initialise all variables 
    players_pos = [0,10,WIDTH-1,5]
    balls_info = [-1 for _ in range(18)]
    ammo_lives_counter = [MAX_AMMO, MAX_LIVES, MAX_AMMO, MAX_LIVES]
    players_pos[1], players_pos[3] = 4, 7

    # 0: start, 1: game, 2: end 
    application_state = 1
    winner = 0

    ############################ game loop #############################
    display_screen(players_pos, balls_info)
    display_ammo_lives(ammo_lives_counter)
    while application_state == 1: 
        # check goal state 
        if is_win(players_pos, balls_info, ammo_lives_counter):
            application_state = 2
            # check lives 
            if ammo_lives_counter[1] == 0:
                winner = 1 # p2 wins
            elif ammo_lives_counter[3] == 0:
                winner = 0 # p1 wins 

        # poll inputs: each player: left right fire aim 
        inputs = poll_input()

        # update state of balls and players 
        update_ball_pos(balls_info)
        update_player_pos(players_pos, inputs, balls_info, ammo_lives_counter)

        # draw screen 
        display_screen(players_pos, balls_info)
        display_ammo_lives(ammo_lives_counter)

if __name__ == "__main__":
    main()

"""
Game loop works, tested with P1: 1 0 0 1, P2: 0 1 2 1 then no further inputs 
    P1 ball bounced against top edge, P2 ball went straight 
    both lost a life when ball hit goal, ball is destroyed 
"""