import dataclasses
from abc import ABC
from random import randint
from typing import Optional


# Added this dataclass to simplify working with coordinates and to improve the readability of code/reduce chances of
# bugs
@dataclasses.dataclass
class Coordinate:
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
    # We need this to check if the game has ended. Once this is zero then the game is over
    __hitpoints: int = 17

    def __init__(self, board: Optional[list[list[int]]] = None):
        if board:
            self.__board = board

    def detect_hit(self, x: int, y: int) -> bool:

        try:
            row = self.__board[x]
            col = row[y]
        except IndexError:
            # If our machine targets cords out of range consider it a miss. This was the quickest way to stop out of 
            # bounds shots from breaking the game
            return False

        if col == 1:
            # mark a hit on the board so that we can't double count hits
            self.__board[x][y] = "x"
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
        # TODO: Complete this function

        if self.__hitpoints <= 0:
            return True
        return False

    def get_score(self) -> int:
        """ Gets the score. """
        return self.__shots


# I chose to use a handler pattern here to implement the target selection logic
# I reckoned it was going to be simpler to understand and extend vs a procedural approach
# It also matched how I was thinking about the problem in my head
class MachineTargetSelector():

    def __init__(self):

        self.__actions_list = [RandomShot()]
        self.missed_shots = []
        self.__last_checkboard_pos = None

    def take_turn(self, game: BattleShips):

        # Iterate through list of actions
        # If action returns extra action then append to list
        # Pop current action off list prior to appending

        for action in self.__actions_list:

            new_actions = action.execute(game=game, missed_shots=self.missed_shots)

            self.__actions_list.pop(0)

            if new_actions:
                self.__actions_list.extend(new_actions)

            if len(self.__actions_list) == 0:
                self.__actions_list.append(RandomShot())

        return

# We had a couple classes all using the same interface/doing the same thing. So I added an ABC to keep things clean
# This also meant I could use clear/accurate type hints within my functions
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

        new_Coordinate = Coordinate(x=new_x, y=new_y)

        hit_occurred = game.fire(x=new_x, y=new_y)

        if hit_occurred:
            print('Directional Shot Hit Ship -> Adding New Directional Shot')
            return [DirectionalShot(x_delta=self._x_delta, y_delta=self._y_delta, starting_cord=new_Coordinate)]

        # if no hit occurs we return None, here so that our machine stops making moves in this direction
        else:
            missed_shots.append(new_Coordinate)
            print(
                f'Directional Shot Missed {new_x},{new_y} {self._x_delta} {self._y_delta} {self._starting_cord}->  Returning None')

        return None


class RandomShot(MachineAction):

    def execute(self, game: BattleShips, missed_shots: list) -> [MachineAction]:

        new_cord_found = False

        # Give the bot memory to stop us from shooting the same place twice
        while new_cord_found is False:
            cord = Coordinate(x=randint(0, 9), y=randint(0, 9))
            if cord not in missed_shots:
                new_cord_found = True

        hit_occurred = game.fire(x=cord.x, y=cord.y)

        if hit_occurred:
            # We now want to fire around the location of the hit up/down/left/right
            # cords start at 0,0 x is across
            # We may have to stick some logic here to handle hits out of bounds?
            print('Random Shot hit ship -> Starting Directional Approach')
            return [DirectionalShot(starting_cord=cord, x_delta=-1, y_delta=0),  # Up
                    DirectionalShot(starting_cord=cord, x_delta=1, y_delta=0),  # Down
                    DirectionalShot(starting_cord=cord, x_delta=0, y_delta=-1),  # Left
                    DirectionalShot(starting_cord=cord, x_delta=0, y_delta=1)]  # Right

        print(f'RandomShot Missed {cord}-> Returning RandomShot')

        missed_shots.append(cord)
        return [RandomShot()]


def play_game(game: BattleShips) -> int:
    '''
    Simulates playing the game.

    This should implement the functionality to shoot on the board until the game is won,
    while minimising the shots taken.
    '''
    # TODO: Complete this function

    """
    
    ----- Notes on my process ------

    In this approach I first tried a completely random shot selection strategy to validate the game logic worked
    
    It was quickly obvious that this approach was not going to pass our tests as it was incredibly inefficient
    
    So I moved to an approach based on firing random shots until a hit occurred and then scanning the area around a hit
   
    If a hit was seen we would scan a cord adjacent to the hit (UP/DOWN/LEFT/RIGHT)
    
    If further hits where seen then we would carry on in the direction of the ship, switching direction when a miss 
    occurred
    
    This allowed me to incrementally improve my algorithm with the least amount of work. The test still failed 
    however scoring an average of 226 shots!
    
    At this point I had about 10 mins remaining so I added memory to the random shot strategy to try and reduce the 
    count of wasted shots. This reduced the average to 102 shots, however this still failed the tests. 
    
    At this point it would have been simpler to just hit each tile on the board sequentially! 
    
    At the time I suspect the lack of boundary detection in the DirectionalShot class might explain why the number 
    of hits was greater than the number of locations on the board!
    
    With very little time remaining I pivoted to a third approach. Replacing the random shot component with a 
    checkerboard scan. I had to complete this after the test concluded however. Honestly I was just really eager to 
    see if I could get it working!

    After about an 1 hours experimentation it was complete.This approach reduced the average number of shots to about 
    63 shots. Ultimately scoring 800. This implementation is in the 'battleships_with_checkerboard_approach.py' file
    """

    """
    ---- What might I change to improve the algorithm----
    
    1. On the Initial Attempt --> Moving to a checkerboard approach from a random shot approach
    
        We know that ships are at least two squares long,
         
        Hitting every 2nd tile means we can hit at least 1 coordinate per ship. 
        
        Allowing us to get a rough idea of each ship location with just 50 shots. A big improvement from 100 shots with 
        the random approach used previously.
         

    2. After implementing the checkerboard approach -> Using the knowledge of past hits to reduce wasted shots
    
    The approach definitely could have benefited from memoization. 
    
    Hits/misses from the DirectionalShot class should have removed co-ords from the 
    CheckerboardShotGenerator.grid_cords property. This would have reduced the size of the problem space
    
    Taken further we could have used knowledge about the board state to infer where ships might be.
    
    By grouping tiles into spaces based on ship length and then shooting the center space we could effectively 
    eliminate x tiles per shot!

    """

    target_selector = MachineTargetSelector()

    while not game.is_game_over():
        target_selector.take_turn(game=game)

    return game.get_score()


if __name__ == '__main__':
    game = BattleShips()
    print(play_game(game))
