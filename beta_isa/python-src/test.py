import game

WIDTH = 30
HEIGHT = 15 
PLAYER_LENGTH = 5
MAX_AMMO = 3
MAX_LIVES = 3

def get_default_states():
    balls_info = [
        -1,-1,-1, -1,-1,-1, -1,-1,-1,
        -1,-1,-1, -1,-1,-1, -1,-1,-1
    ]
    players_pos = [
        0,0,
        WIDTH-1,0
    ]
    ammo_lives_counter = [
        3,3,
        3,3 
    ]
    return balls_info, players_pos, ammo_lives_counter

def test_is_win():
    """Tests for is_win function"""
    balls_info, players_pos, ammo_lives_counter = get_default_states()

    # Test 1: p1 ball at p2 goal, ball not blocked 
    balls_info[0], balls_info[1] = WIDTH-1, HEIGHT-1
    ammo_lives_counter[1] = 1
    print("before player pos", players_pos)
    print("before balls info", balls_info)
    print("before ", ammo_lives_counter)
    con = game.is_win(players_pos, balls_info, ammo_lives_counter)
    assert con 
    assert ammo_lives_counter == [3,0,3,3]
    assert balls_info == [-1 for _ in range(18)]
    print("-------------")
    print("after player pos", players_pos)
    print("after balls info", balls_info)
    print("after ", ammo_lives_counter)

    # Test 2: p1 ball blocked by p2
    # balls_info, players_pos, ammo_lives_counter = get_default_states()
    # balls_info[0], balls_info[1], balls_info[2] = WIDTH-1, HEIGHT-1,2
    # ammo_lives_counter[0], ammo_lives_counter[3] = 2,1 #p1 has 1 less ammo from firing ball
    # players_pos[3] = 10
    # con = game.is_win(players_pos, balls_info, ammo_lives_counter)
    # assert not con # not win since ball is blocked 
    # assert ammo_lives_counter == [3, 3, 3, 1]
    # assert balls_info == [-1 for _ in range(18)]

def test_update_ball_pos():
    """Tests for update all obj pos"""

    # Test 1: ball pos, upper reflect 
    balls_info, players_pos, ammo_lives_counter = get_default_states()
    balls_info[0], balls_info[1], balls_info[2] = 3,0,0 # angle up 
    assert balls_info == [3, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    game.update_ball_pos(balls_info)
    assert balls_info == [4, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    # Test 2: ball pos, lower reflect
    balls_info, players_pos, ammo_lives_counter = get_default_states()
    balls_info[15], balls_info[16], balls_info[17] = 3,HEIGHT-1, 1 # angle down 
    assert balls_info == [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, 14, 1]
    game.update_ball_pos(balls_info)
    assert balls_info == [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, 13, 0]

    # Test 3: ball pos, maintain straight path 
    balls_info, players_pos, ammo_lives_counter = get_default_states()
    balls_info[3], balls_info[4], balls_info[5] = 28, 2, 2 
    assert balls_info == [-1, -1, -1, 28, 2, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    game.update_ball_pos(balls_info)
    assert balls_info == [-1, -1, -1, 29, 2, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

def test_update_player_pos():
    # Test 1: player pos, both up, dont go beyond top bound 
    # balls_info, players_pos, ammo_lives_counter = get_default_states()
    # inputs = [1,0,0,1, 1,0,0,0]
    # print("before player pos", players_pos)
    # print("before balls info", balls_info)
    # print("before inputs", inputs)
    # print("before ", ammo_lives_counter)
    # game.update_player_pos(players_pos, inputs, balls_info, ammo_lives_counter)
    # assert players_pos == [0, 0, 29, 0]
    # print("after player pos", players_pos)
    # print("after balls info", balls_info)
    # print("after inputs", inputs)
    # print("after ", ammo_lives_counter)

    # Test 2: player pos, both down, dont go beyond bottom bound 
    # balls_info, players_pos, ammo_lives_counter = get_default_states()
    # players_pos[1], players_pos[3] = 10, 10
    # inputs = [0,1,0,0, 0,1,0,0]
    # print("before player pos", players_pos)
    # print("before balls info", balls_info)
    # print("before inputs", inputs)
    # print("before ", ammo_lives_counter)
    # game.update_player_pos(players_pos, inputs, balls_info, ammo_lives_counter)
    # assert players_pos == [0, 10, 29, 10]
    # print("-------------")
    # print("after player pos", players_pos)
    # print("after balls info", balls_info)
    # print("after inputs", inputs)
    # print("after ", ammo_lives_counter)

    # Test 3: player pos, p1 up, p2 down, not at bounds 
    # balls_info, players_pos, ammo_lives_counter = get_default_states()
    # players_pos[1], players_pos[3] = 4, 7
    # inputs = [1,0,0,0, 0,1,0,0] # p1 dont move, p2 move down 
    # print("before player pos", players_pos)
    # print("before balls info", balls_info)
    # print("before inputs", inputs)
    # print("before ", ammo_lives_counter)
    # game.update_player_pos(players_pos, inputs, balls_info, ammo_lives_counter)
    # assert players_pos == [0, 3, 29, 8]
    # print("-------------")
    # print("after player pos", players_pos)
    # print("after balls info", balls_info)
    # print("after inputs", inputs)
    # print("after ", ammo_lives_counter)

    # Test 4: fire, able to fire
    # balls_info, players_pos, ammo_lives_counter = get_default_states()
    # inputs = [0,0,0,1, 0,0,2,1] #p1 aim up, p2 aim straight 
    # balls_info[0], balls_info[1], balls_info[2] = 3,12,2 #p1 has 1 ball in play 
    # print("before player pos", players_pos)
    # print("before balls info", balls_info)
    # print("before inputs", inputs)
    # print("before ", ammo_lives_counter)
    # game.update_player_pos(players_pos, inputs, balls_info, ammo_lives_counter)
    # assert players_pos == [0,0,29,0] # make sure player didnt move when not triggered 
    # assert balls_info == [3,12,2, 1,2,0, -1,-1,-1, 28,2,2, -1,-1,-1, -1,-1,-1]
    # assert ammo_lives_counter == [2,3, 2,3]
    # print("-------------")
    # print("after player pos", players_pos)
    # print("after balls info", balls_info)
    # print("after inputs", inputs)
    # print("after ", ammo_lives_counter)

    # # Test 5: fire, unable to fire 
    balls_info, players_pos, ammo_lives_counter = get_default_states()
    inputs = [0,0,0,1, 0,0,2,1] #p1 aim up, p2 aim straight
    balls_info = [1 for _ in range(18)] # all 6 balls in play 
    ammo_lives_counter = [0,3, 0,3]
    print("before player pos", players_pos)
    print("before balls info", balls_info)
    print("before inputs", inputs)
    print("before ", ammo_lives_counter)
    game.update_player_pos(players_pos, inputs, balls_info, ammo_lives_counter)
    assert balls_info == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    assert ammo_lives_counter == [0,3, 0,3]
    print("-------------")
    print("after player pos", players_pos)
    print("after balls info", balls_info)
    print("after inputs", inputs)
    print("after ", ammo_lives_counter)

# TODO: game loop test cases 
def four_frame_loop():
    pass 

"""Run test cases here. Toggle comment to choose which test to run"""
# test_is_win()
test_update_ball_pos()
# test_update_player_pos()