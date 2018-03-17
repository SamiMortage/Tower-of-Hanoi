"""
ConsoleController: User interface for manually solving
Anne Hoy's problems from the console.
"""

# Copyright 2014, 2017 Dustin Wehr, Danny Heap, Bogdan Simion,
# Jacqueline Smith, Dan Zingaro
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2017.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.


from toah_model import TOAHModel, IllegalMoveError


def move(model, origin, dest):
    """ Apply move from origin to destination in model.

    May raise an IllegalMoveError.

    @param TOAHModel model:
        model to modify
    @param int origin:
        stool number (index from 0) of cheese to move
    @param int dest:
        stool number you want to move cheese to
    @rtype: None
    """

    model.get_move_seq().add_move(origin, dest)

    if len(model.get_stools()[dest]) == 0:
        moved_cheese = model.get_stools()[origin].pop()
        model.get_stools()[dest].append(moved_cheese)
    elif model.get_stools()[dest][-1].size > \
            model.get_stools()[origin][-1].size:
        moved_cheese = model.get_stools()[origin].pop()
        model.get_stools()[dest].append(moved_cheese)


class ConsoleController:
    """ Controller for text console.
    """

    def __init__(self, number_of_cheeses, number_of_stools):
        """ Initialize a new ConsoleController self.

        @param ConsoleController self:
        @param int number_of_cheeses:
        @param int number_of_stools:
        @rtype: None
        """
        self.number_of_cheeses = number_of_cheeses
        self.number_of_stools = number_of_stools
        self.model = TOAHModel(self.number_of_stools)
        self.model.fill_first_stool(self.number_of_cheeses)

    def play_loop(self):
        """ Play Console-based game.

        @param ConsoleController self:
        @rtype: None

        TODO:
        -Start by giving instructions about how to enter moves (which is up to
        you). Be sure to provide some way of exiting the game, and indicate
        that in the instructions.
        -Use python's built-in function input() to read a potential move from
        the user/player. You should print an error message if the input does
        not meet the specifications given in your instruction or if it denotes
        an invalid move (e.g. moving a cheese onto a smaller cheese).
        You can print error messages from this method and/or from
        ConsoleController.move; it's up to you.
        -After each valid move, use the method TOAHModel.__str__ that we've
        provided to print a representation of the current state of the game.
        """

        print("Instructions: Entering '0 2' means move the top cheese from the\
        first stool to the third stool. \n Enter 'e' to exit.")
        print(str(self.model))
        n = 1
        input_ = input("Enter Move {}: ".format(n))
        while input_ != 'e':
            split_ = input_.strip(" ").split(" ")
            if len(split_) != 2 or split_[0].isalpha() or split_[1].isalpha():
                print(IllegalMoveError("Please enter correct values!"))
                print(str(self.model))
                input_ = input("Enter Move {}: ".format(n))
            else:
                origin = int(split_[0])
                dest = int(split_[1])
                if origin > (self.model.get_number_of_stools() - 1) or origin <\
                        0:
                    print(IllegalMoveError("Origin stool does not exist!"))
                    print(str(self.model))
                    input_ = input("Enter Move {}: ".format(n))

                elif dest > (self.model.get_number_of_stools() - 1) or dest < 0:
                    print(IllegalMoveError("Destination stool does not exist!"))
                    print(str(self.model))
                    input_ = input("Enter Move {}: ".format(n))

                elif len(self.model.get_stools()[origin]) == 0:
                    print(IllegalMoveError(
                        "Cannot move to cheese from an empty stool"))
                    print(str(self.model))
                    input_ = input("Enter Move {}: ".format(n))

                elif len(self.model.get_stools()[dest]) != 0 and \
                        self.model.get_stools()[dest][-1].size < \
                        self.model.get_stools()[origin][-1].size:
                    print(IllegalMoveError(
                        "Cannot place a bigger cheese on top of a smaller "
                        "cheese!"))
                    print(str(self.model))
                    input_ = input("Enter Move {}: ".format(n))

                else:
                    move(self.model, origin, dest)
                    print(str(self.model))
                    n += 1
                    input_ = input("Enter Move {}: ".format(n))


if __name__ == '__main__':
    # You should initiate game play here. Your game should be playable by
    # running this file.
    TOAH = ConsoleController(5, 5)
    TOAH.play_loop()
    # Leave lines below as they are, so you will know what python_ta checks.
    # You will need consolecontroller_pyta.txt in the same folder.
    import python_ta

    python_ta.check_all(config="consolecontroller_pyta.txt")
