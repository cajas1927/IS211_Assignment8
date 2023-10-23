import random
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_total = 0

    def roll_die(self):
        roll = random.randint(1, 6)
        if roll == 1:
            self.turn_total = 0
        else:
            self.turn_total += roll
        return roll

    def hold(self):
        self.score += self.turn_total
        self.turn_total = 0

class HumanPlayer(Player):
    def get_decision(self):
        while True:
            decision = input(f"{self.name}, enter 'r' to roll or 'h' to hold: ").strip().lower()
            if decision in ['r', 'h']:
                return decision
            else:
                print("Invalid input. Please enter 'r' to roll or 'h' to hold.")

class ComputerPlayer(Player):
    def get_decision(self):
        if self.score + self.turn_total < 25 and self.score + self.turn_total < 100:
            return 'r'
        else:
            return 'h'

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == 'human':
            return HumanPlayer(name)
        elif player_type == 'computer':
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type. Use 'human' or 'computer'.")

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = random.choice(self.players)

    def switch_player(self):
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]

    def play_game(self):
        while True:
            print(f"{self.current_player.name}'s turn:")
            decision = self.current_player.get_decision()

            if decision == 'r':
                roll = self.current_player.roll_die()
                print(f"{self.current_player.name} rolled a {roll}.")
                print(f"Turn total: {self.current_player.turn_total}, Total score: {self.current_player.score}")

                if self.current_player.turn_total == 0:
                    print(f"{self.current_player.name} rolled a 1. Turn ends with no points added.")
                    self.switch_player()
            elif decision == 'h':
                self.current_player.hold()
                print(f"{self.current_player.name} decided to hold.")
                print(f"Turn total: {self.current_player.turn_total}, Total score: {self.current_player.score}")

                if self.current_player.score >= 100:
                    print(f"{self.current_player.name} wins!")
                    return  # Game ends

            if self.current_player == player1:
                self.current_player = player2
            else:
                self.current_player = player1


class TimedGameProxy(Game):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.timed = True
        self.start_time = time.time()  # Initialize start time when creating the proxy

    def play_game(self):
        while True:
            if time.time() - self.start_time > 60:
                print("One minute has passed. The game is over.")
                break
            print(f"{self.current_player.name}'s turn:")
            decision = self.current_player.get_decision()

            if decision == 'r':
                roll = self.current_player.roll_die()
                print(f"{self.current_player.name} rolled a {roll}.")
                print(f"Turn total: {self.current_player.turn_total}, Total score: {self.current_player.score}")

                if self.current_player.turn_total == 0:
                    print(f"{self.current_player.name} rolled a 1. Turn ends with no points added.")
                    self.switch_player()
            elif decision == 'h':
                self.current_player.hold()
                print(f"{self.current_player.name} decided to hold.")
                print(f"Turn total: {self.current_player.turn_total}, Total score: {self.current_player.score}")

                if self.current_player.score >= 100:
                    print(f"{self.current_player.name} wins!")
                    return  # Game ends

            self.switch_player()

if __name__ == "__main__":
    player1_type = input("Enter player 1 type (human/computer): ")
    player2_type = input("Enter player 2 type (human/computer): ")

    try:
        player1 = PlayerFactory.create_player(player1_type, "Player 1")
        player2 = PlayerFactory.create_player(player2_type, "Player 2")
    except ValueError as e:
        print(e)
        exit()

    if input("Enter 'y' to play a timed game: ").strip().lower() == 'y':
        game = TimedGameProxy(player1, player2)
    else:
        game = Game(player1, player2)

    game.play_game()
