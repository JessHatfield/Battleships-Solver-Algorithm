from battleships import BattleShips, play_game
from copy import deepcopy

def get_average_across_plays(
        board: list[list[int]], average_target: int, validator: str):
    scores = []
    for i in range(10):
        board_copy = deepcopy(board)
        game = BattleShips(board_copy)
        play_game(game)
        scores.append(game.get_score())
        assert game.is_game_over(), f"Fail: {validator}. Game was not won!"
    average = sum(scores) / len(scores)
    assert average < average_target, \
        (f"Fail: {validator}. "
         f"Average score was {average} but should be below {average_target}.")
    return f"Passed: {validator} with score {average}"

default_board = [
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
]

def validate_below(average_target):
    def validator():
        return get_average_across_plays(deepcopy(default_board), average_target, f"validate_below({average_target})")
    return validator

def validate_on_other_boards_corner():
    test_case = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
    ]
    return get_average_across_plays(deepcopy(test_case), 70, "validate_on_other_boards_corner()")

def validate_on_other_boards_vertical_stripes():
    test_case = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    ]
    return get_average_across_plays(
        deepcopy(test_case), 70, "validate_on_other_boards_vertical_stripes()")

def validate_on_other_boards_horizontal_stripes():
    test_case = [
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    return get_average_across_plays(
        deepcopy(test_case), 70, "validate_on_other_boards_horizontal_stripes()")

def validate_fire_method_no_win_with_edgecase():
    game = BattleShips(deepcopy(default_board))
    assert game.fire(1, 0), ("Fail: validate_fire_method_no_win_with_edgecase(). "
                             "Expected fire method to return True.")
    for i in range(20):
        game.fire(1, 0)
    assert not game.is_game_over(), ("Fail: validate_fire_method_no_win_with_edgecase(). "
                                     "Should not have been able to win by firing on same shot.")
    return "Passed: validate_fire_method_no_win_with_edgecase()"

if __name__ == '__main__':
    validators = [
        (validate_below(100), 100),
        (validate_below(90), 100),
        (validate_below(80), 100),
        (validate_below(70), 100),
        (validate_below(65), 100),
        (validate_below(60), 200), # This is hard, so it's worth more points!
        (validate_below(55), 300), # This is really hard, so it's worth more points!
        (validate_on_other_boards_corner, 100),
        (validate_on_other_boards_horizontal_stripes, 100),
        (validate_on_other_boards_vertical_stripes, 100),
        (validate_fire_method_no_win_with_edgecase, 100)
    ]    
    score = 0
    failure_messages = ""
    pass_messages = ""
    for (validator, score_increment) in validators:
        try:
            pass_messages += validator() + "\n"
            score += score_increment
        except AssertionError as e:
            failure_messages += str(e) + "\n"
            continue

    print(f"\n\nFINAL SCORE: {score}\n")
    print(f"FAILURE MESSAGES: \n{failure_messages} \n")
    print(f"PASS MESSAGES:\n{pass_messages} \n\n")
