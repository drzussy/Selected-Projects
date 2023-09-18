from typing import Callable
from boggle_model import *
from boggle_gui import *


class Boggle:
    def __init__(self) -> None:
        self._game = Game()
        self._gui = GUI(self._game.board.get_board())
        for location in self._gui.get_square_locations():
            action = self.create_square_functionality(location)
            self._gui.set_square_command(location, action)
        self._gui._start_game_button.configure(command=self.start_boggle)
        self._gui._new_game_button.configure(command=self.reset_boggle)

    def create_square_functionality(self, location):
        def update_gui() -> None:
            # gives each button functionality through the model functions

            # after click the button checks what to do with the click
            update_type = self._game.update_game(location)

            # legal turn
            if update_type == PATH_UPDATED:
                self._gui.press_square(location)
                if self._gui.get_display_label() in ['Not a Word', 'Found a word!', 'Word already found!']:
                    self._gui.reset_display_label()
                self._gui.update_display_label(
                    self._game.board.cell_content(location))

            # clicked on a square that was already clicked
            elif update_type == WORD_FOUND:
                self._gui.add_found_word(self._gui.get_display_label())
                self._gui.reset_display_label()
                self._gui.update_display_label('Found a word!')
                self._gui.set_score(self._game.score)
                self._gui.reset_path_gui()
                if self._game.num_words_left == 0:
                    self._gui.reset_display_label()
                    self._gui.update_display_label(
                        "Congragulations! Found all words!")
                    self._gui.disable_board()

            elif update_type == WORD_ALREADY_FOUND:
                self._gui.reset_display_label()
                self._gui.update_display_label('Word already found!')
                self._gui.set_score(self._game.score)
                self._gui.reset_path_gui()

            elif update_type == NOT_A_WORD:
                self._gui.reset_display_label()
                self._gui.reset_path_gui()
                self._gui.update_display_label('Not a Word')
                self._gui.reset_path_gui()

        return update_gui

    def start_boggle(self):
        boggle._gui.activate_board()
        boggle._gui.start_timer()

    def reset_boggle(self):
        self._game.reset_game()
        self._gui.reset_gui(self._game.board.get_board())

    def run(self) -> None:
        self._gui.run()


if __name__ == "__main__":
    boggle = Boggle()
    boggle.run()
