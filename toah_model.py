"""
TOAHModel:  Model a game of Tour of Anne Hoy
Cheese:   Model a cheese with a given (relative) size
IllegalMoveError: Type of exceptions thrown when an illegal move is attempted
MoveSequence: Record of a sequence of (not necessarily legal) moves. You will
need to return MoveSequence object after solving an instance of the 4-stool
Tour of Anne Hoy game, and we will use that to check the correctness of your
algorithm.
"""


# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Bogdan Simion, Jacqueline Smith, Dan Zingaro, Ritu Chaturvedi, Samar Sabie
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
#


class TOAHModel:
    """ Model a game of Tour Of Anne Hoy.

    Model stools holding stacks of cheese, enforcing the constraint
    that a larger cheese may not be placed on a smaller one.
    """

    def __init__(self, number_of_stools):
        """ Create new TOAHModel with empty stools
        to hold stools of cheese.

        @param TOAHModel self:
        @param int number_of_stools:
        @rtype: None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> (M.get_number_of_stools(), M.number_of_moves()) == (4,0)
        True
        >>> M.get_number_of_cheeses()
        5
        """
        self.number_of_stools = number_of_stools
        # you must have _move_seq as well as any other attributes you choose
        self._move_seq = MoveSequence([])
        self._stools = []
        i = 0
        while i < number_of_stools:
            self._stools.append([])
            i += 1
        self.moves_ = 0

    def fill_first_stool(self, number_of_cheese):
        """ Adds number_of_cheese cheese rounds to the first stool

        @type self: TOAHModel
        @type number_of_cheese: int
        @rtype None
        """
        for i in range(number_of_cheese, 0, -1):
            self._stools[0].append(Cheese(i))

    def get_move_seq(self):
        """ Return the move sequence

        @type self: TOAHModel
        @rtype: MoveSequence

        >>> toah = TOAHModel(2)
        >>> toah.get_move_seq() == MoveSequence([])
        True
        """
        return self._move_seq

    def __eq__(self, other):
        """ Return whether TOAHModel self is equivalent to other.

        Two TOAHModels are equivalent if their current
        configurations of cheeses on stools look the same.
        More precisely, for all h,s, the h-th cheese on the s-th
        stool of self should be equivalent the h-th cheese on the s-th
        stool of other

        @type self: TOAHModel
        @type other: TOAHModel
        @rtype: bool

        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0, 1)
        >>> m1.move(0, 2)
        >>> m1.move(1, 2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0, 3)
        >>> m2.move(0, 2)
        >>> m2.move(3, 2)
        >>> m1 == m2
        True
        """
        return (type(self) == type(other)) and (self._stools == other._stools)

    def _cheese_at(self, stool_index, stool_height):
        # """ Return (stool_height)th from stool_index stool, if possible.
        #
        # @type self: TOAHModel
        # @type stool_index: int
        # @type stool_height: int
        # @rtype: Cheese | None
        #
        # >>> M = TOAHModel(4)
        # >>> M.fill_first_stool(5)
        # >>> M._cheese_at(0,3).size
        # 2
        # >>> M._cheese_at(0,0).size
        # 5
        # """
        if 0 <= stool_height < len(self._stools[stool_index]):
            return self._stools[stool_index][stool_height]
        else:
            return None

    def move(self, start_stool, dest_stool):
        """
        @type start_stool: int
        @type dest_stool: int
        @rtype None

        >>> h = TOAHModel(4)
        >>> h.fill_first_stool(5)
        >>> h.move(0, 1)
        >>> h.move(0, 3)
        >>> h.move(1, 3)
        >>> r = TOAHModel(4)
        >>> r.fill_first_stool(5)
        >>> r.move(0, 2)
        >>> r.move(0, 3)
        >>> r.move(2, 3)
        >>> h == r
        True
        """
        self._move_seq.add_move(start_stool, dest_stool)

        if len(self._stools[dest_stool]) == 0:
            moved_cheese = self._stools[start_stool].pop()
            self._stools[dest_stool].append(moved_cheese)
        elif self._stools[dest_stool][-1].size > self._stools[start_stool][-1].size:
            moved_cheese = self._stools[start_stool].pop()
            self._stools[dest_stool].append(moved_cheese)
        else:
            raise IllegalMoveError("Cannot place a bigger cheese on top of a smaller cheese!")

        self.moves_ += 1


    def get_number_of_cheeses(self):
        """Return the number of cheeses in the toah model.

        @type self: TOAHModel
        @rtype: int
        """
        sum_ = 0
        for stool in self._stools:
            i = 0
            while i < len(stool):
                sum_ += 1
                i += 1
        return sum_

    def get_number_of_stools(self):
        """Return the number of stools in the toah model.

        @type self: TOAHModel
        @rtype: int
        """

        return self.number_of_stools

    def __str__(self):
        """
        Depicts only the current state of the stools and cheese.

        @param TOAHModel self:
        @rtype: str
        """
        all_cheeses = []
        for height in range(self.get_number_of_cheeses()):
            for stool in range(self.get_number_of_stools()):
                if self._cheese_at(stool, height) is not None:
                    all_cheeses.append(self._cheese_at(stool, height))
        max_cheese_size = max([c.size for c in all_cheeses]) \
            if len(all_cheeses) > 0 else 0
        stool_str = "=" * (2 * max_cheese_size + 1)
        stool_spacing = "  "
        stools_str = (stool_str + stool_spacing) * self.get_number_of_stools()

        def _cheese_str(size):
            # helper for string representation of cheese
            if size == 0:
                return " " * len(stool_str)
            cheese_part = "-" + "--" * (size - 1)
            space_filler = " " * int((len(stool_str) - len(cheese_part)) / 2)
            return space_filler + cheese_part + space_filler

        lines = ""
        for height in range(self.get_number_of_cheeses() - 1, -1, -1):
            line = ""
            for stool in range(self.get_number_of_stools()):
                c = self._cheese_at(stool, height)
                if isinstance(c, Cheese):
                    s = _cheese_str(int(c.size))
                else:
                    s = _cheese_str(0)
                line += s + stool_spacing
            lines += line + "\n"
        lines += stools_str

        return lines

    def get_cheese_location(self, cheese):
        """Return a the index of the stool that the cheese is on.


        @param self: TOAHModel
        @param cheese: Cheese
        @rtype: int

        >>>
        """

        for stool in self._stools:
            if cheese in stool:
                return self._stools.index(stool)

    def add(self, cheese, stool):
        """Add cheese to stool number stool.

        @param self: TOAHModel
        @param cheese: Cheese
        @param stool: int
        @rtype: None
        """

        self._stools[stool].append(cheese)

    def get_top_cheese(self, stool):
        """Return the cheese at the top of stool

        @type self: TOAHModel
        @type stool: int
        @rtype Cheese
        """
        if len(self._stools[stool]) != 0:
            return self._stools[stool][-1]

    def number_of_moves(self):
        """Return the number of moves made

        @type self: TOAHModel
        """
        return self.moves_

    def get_stools(self):
        """Return the stools in self

        @type self: TOAHModel
        @rtype: list"""

        return self._stools

class Cheese:
    """ A cheese for stacking in a TOAHModel

    === Attributes ===
    @param int size: width of cheese
    """

    def __init__(self, size):
        """ Initialize a Cheese to diameter size.

        @param Cheese self:
        @param int size:
        @rtype: None

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """
        self.size = size

    def __eq__(self, other):
        """ Is self equivalent to other?

        We say they are if they're the same
        size.

        @param Cheese self:
        @param Cheese|Any other:
        @rtype: bool
        """

        return (type(self) == type(other)) and (self.size == other.size)


    def __repr__(self):

        return str(self.size)



class IllegalMoveError(Exception):
    """ Exception indicating move that violate TOAHModel
    """
    pass


class MoveSequence(object):
    """ Sequence of moves in TOAH game
    """

    def __init__(self, moves):
        """ Create a new MoveSequence self.

        @param MoveSequence self:
        @param list[tuple[int]] moves:
        @rtype: None
        """
        # moves - a list of integer pairs, e.g. [(0,1),(0,2),(1,2)]
        self._moves = moves

    def get_move(self, i):
        """ Return the move at position i in self

        @param MoveSequence self:
        @param int i:
        @rtype: tuple[int]

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.get_move(0) == (1, 2)
        True
        """
        # Exception if not (0 <= i < self.length)
        return self._moves[i]

    def add_move(self, src_stool, dest_stool):
        """ Add move from src_stool to dest_stool to MoveSequence self.

        @param MoveSequence self:
        @param int src_stool:
        @param int dest_stool:
        @rtype: None
        """
        self._moves.append((src_stool, dest_stool))

    def length(self):
        """ Return number of moves in self.

        @param MoveSequence self:
        @rtype: int

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.length()
        1
        """
        return len(self._moves)

    def generate_toah_model(self, number_of_stools, number_of_cheeses):
        """ Construct TOAHModel from number_of_stools and number_of_cheeses
         after moves in self.

        Takes the two parameters for
        the game (number_of_cheeses, number_of_stools), initializes the game
        in the standard way with TOAHModel.fill_first_stool(number_of_cheeses),
        and then applies each of the moves in this move sequence.

        @param MoveSequence self:
        @param int number_of_stools:
        @param int number_of_cheeses:
        @rtype: TOAHModel

        >>> ms = MoveSequence([])
        >>> toah = TOAHModel(2)
        >>> toah.fill_first_stool(2)
        >>> toah == ms.generate_toah_model(2, 2)
        True
        """
        model = TOAHModel(number_of_stools)
        model.fill_first_stool(number_of_cheeses)
        for move in self._moves:
            model.move(move[0], move[1])
        return model

    def __repr__(self):
        return str(self._moves)

if __name__ == '__main__':
    #    import doctest
    #    doctest.testmod(verbose=True)
    # Leave lines below to see what python_ta checks.
    # File toahmodel_pyta.txt must be in same folder.
    import python_ta
    python_ta.check_all(config="toahmodel_pyta.txt")
    h = TOAHModel(4)
    h.fill_first_stool(5)
    print(h.get_number_of_stools())
    print(h.get_number_of_cheeses())
