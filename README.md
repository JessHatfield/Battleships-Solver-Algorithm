# Context

This was a timed coding challenge I was asked to complete during the interview process of a series A startup.

My final solution can be found in the battleships_with_extra_time.py file. Notes on my solution can be found [here](https://github.com/JessHatfield/Battleships-Solver-Algorithm/blob/0313501fcd009c525d4cbde4c69bf959380192ea/battleships.py#L199).


# Pre-requisites
Before starting the exercise, you should make sure you are familar with Git and able to run python3 applications.

# Setup
We ask you do this as a timed exercise with zoom recording you (video off is fine!) of *one hour* (unless we've discussed otherwise). At the end of the exercise, please either send your solution to us or upload it to github as a private repo and add us to it.

Additionally, please include in your submission, a very brief (1 paragraph) explanation of *one* thing you think would be worth trying to make your
algorithm even better.

# The exercise
This exercise is loosely based on the game of battleships. You are provided with a class `BattleShips` encapsulating a battleships board. Your objective is to implement the `play_game` function using the `fire` and `is_game_over` methods exposed to you by the game class. You are aiming to minimize the number of times the `fire` method is called.

The number of shots is incremented every time the `fire` method is called, and the total number of shots is returned by the get_score function. You should aim to create an algorithm that means that the number of shots on average across the test cases is less than 70 (see also Scoring).

You also need to implement the body of the `fire` and `is_game_over` methods. We advise you spend no more than 10 minutes on these methods to give yourself enough time on the `play_game` function.

You can assume that the board is always the same size (10x10), and that there are always the same number of ships (a total of 17 points). A ship is considered sunk when every single point on it has been hit.

Some notes:
- You can add extra methods, data structures and fields as you see fit to make your code elegant.
- Any additional fields added within the `BattleShips` class should be private
- You should not write getters to expose these to the play_game method (this kinda defeats the point!)
- Do not over fit your solution to the board provided - the scoring has a variety of boards.
- You can use whatever IDE you want, including those with co-pilots. Asking your co-pilot for reminders on syntax etc is fine, but please do not ask them to solve the whole problem.


# Running the game
The code is equipped with a running harness such that it will run your code against the default board, and return the score. You can run this by running `python3 battleships.py`

# Scoring the game
The code is equipped with a scoring harness which runs various tests and gives you a score. To run this, run `python3 scorer.py`. The maximum you can score is 1400. You should be aiming for a score of at least 700 to pass.
