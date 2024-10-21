import dataclasses
from abc import ABC
from random import randint
from typing import Optional


@dataclasses.dataclass
class Cordinate():
    x: int
    y: int


class BattleShips:
    __shots: int = 0
    __board: list[list[int]] = [
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
    # We need this to check if the game has ended once this is zero. Game is over
    __hitpoints: int = 17

    def __init__(self, board: Optional[list[list[int]]] = None):
        if board:
            self.__board = board

    def detect_hit(self, x: int, y: int) -> bool:

        try:
            row = self.__board[x]
            col = row[y]
        except IndexError:
            # If our machine targets cords out of range consider it a miss
            print(f'hit {x,y} was out of bounds ')
            return False

        if col == 1:
            return True

        return False

    def fire(self, x: int, y: int) -> bool:
        '''
        Fire on a given position.

        This should update the number of shots taken, and return true if the shot hit a ship,
        false otherwise.
        '''
        self.__shots += 1

        hit_occurred = self.detect_hit(x=x, y=y)

        if hit_occurred:
            self.__hitpoints -= 1
            print(f'hit occurred at  {x},{y} - hitpoint value is now {self.__hitpoints}')
            return True

        return False

    def is_game_over(self) -> bool:
        '''
        Indicates if the game has been completed.

        Returns false until all the positions on the ships have been hit.
        '''

        if self.__hitpoints <= 0:
            return True
        return False

    def get_score(self) -> int:
        """ Gets the score. """
        return self.__shots


class MachineTargetSelector():

    def __init__(self):

        self.__actions_list = []
        self.missed_shots = []
        self.__last_checkboard_pos = None
        self.checkboard_generator = CheckerboardShotGenerator()

    def take_turn(self, game: BattleShips):

        # Iterate through list of actions
        # If action returns extra action then append to list
        # Pop current action off list prior to appending

        if len(self.__actions_list) == 0:
            self.__actions_list.append(self.checkboard_generator)

        for action in self.__actions_list:

            new_actions = action.execute(game=game, missed_shots=self.missed_shots)

            self.__actions_list.pop(0)

            if new_actions:
                self.__actions_list.extend(new_actions)

            if len(self.__actions_list) == 0:
                self.__actions_list.append(self.checkboard_generator)

        return


class MachineAction(ABC):

    def __init__(self, **kwargs):
        pass

    def execute(self, game: BattleShips):
        pass


class DirectionalShot(MachineAction):

    def __init__(self, **kwargs):
        self._x_delta = kwargs['x_delta']
        self._y_delta = kwargs['y_delta']
        self._starting_cord = kwargs['starting_cord']

    def execute(self, game: BattleShips, missed_shots: list) -> [MachineAction]:
        new_x = self._starting_cord.x + self._x_delta
        new_y = self._starting_cord.y + self._y_delta

        new_cordinate = Cordinate(x=new_x, y=new_y)

        hit_occurred = game.fire(x=new_x, y=new_y)

        if hit_occurred:
            print('Directional Shot Hit Ship -> Adding New Directional Shot')
            return [DirectionalShot(x_delta=self._x_delta, y_delta=self._y_delta, starting_cord=new_cordinate)]

        # if no hit occurs we return None, here so that our machine stops making moves in this direction

        print(
            f'Directional Shot Missed {new_x},{new_y} {self._x_delta} {self._y_delta} {self._starting_cord}->  Returning None')

        return None


class CheckerboardShotGenerator():

    def __init__(self):
        self.grid_cords = self.__gen_grid_cords()

    def __gen_grid_cords(self):
        grid_cords = []

        length = 100

        count = 0
        x = 0
        y = 0

        while x <= 9:

            # If we have hit the end of an even row then set x to odd value and increment 9
            if y == 10:
                y = 1
                x += 1

            elif y == 9:
                y = 0
                x += 1

            else:
                y += 2
                x = x

            grid_cords.append(Cordinate(x=x, y=y))

            count += 1

        grid_cords.pop(-1)

        return grid_cords

    def get_next_cordinate(self):
        return self.grid_cords.pop(0)

    def execute(self,game:BattleShips,missed_shots):

        new_cord = self.get_next_cordinate()

        hit_occurred = game.fire(x=new_cord.x, y=new_cord.y)

        if hit_occurred:
            # We now want to fire around the location of the hit up/down/left/right
            # cords start at 0,0 x is across
            # We may have to stick some logic here to handle hits out of bounds?
            print('Checkboard Shot hit ship -> Starting Directional Approach')
            return [DirectionalShot(starting_cord=new_cord, x_delta=-1, y_delta=0),  # Up
                    DirectionalShot(starting_cord=new_cord, x_delta=1, y_delta=0),  # Down
                    DirectionalShot(starting_cord=new_cord, x_delta=0, y_delta=-1),  # Left
                    DirectionalShot(starting_cord=new_cord, x_delta=0, y_delta=1)]  # Right

        else:
            print(f'CheckerboardShot Missed {new_cord} -> Returning New Checkerboard Shot')
            return None


#





def play_game(game: BattleShips) -> int:
    '''
    Simulates playing the game.

    This should implement the functionality to shoot on the board until the game is won,
    while minimising the shots taken.
    '''

    # game logic goes here

    # compute if game has ended and return score

    # Setup core game loop
    # Find a cordinate
    # Take a shot
    # Continue until all ships have been sunk

    target_selector = MachineTargetSelector()

    while True:
        # Take an action and fire on board within this class
        target_selector.take_turn(game=game)

        if game.is_game_over():
            break

    return game.get_score()


if __name__ == '__main__':
    CheckerboardShotGenerator()
    game = BattleShips()
    print(play_game(game))
