""" implementation of class Sack
"""



class Sack:
    """ A Sack with elements in no particular order.
    """

    def __init__(self):
        """ Create a new, empty Sack self.

        @param Sack self: this Sack
        @rtype: None
        """
        # pairs as keys get put in a dict in
        # unpredictable order... unlike ints
        self._key = (-1, 0)
        self._storage = {}

    def add(self, obj):
        """ Add object obj to random position of Sack self.

        @param Sack self: this Sack
        @param object obj: object to place on Sack
        @rtype: None
        """
        self._key = (self._key[0] + 1, 0)
        self._storage[self._key] = obj

    def remove(self):
        """ Remove and return some random element of Sack self.

        Assume Sack self is not empty.

        @param Sack self: this Sack
        @rtype: object

        >>> s = Sack()
        >>> s.add(7)
        >>> s.remove()
        7
        """
        return self._storage.popitem()[1]

    def is_empty(self):
        """ Return whether Sack self is empty.

        @param Sack self: this Sack
        @rtype: bool
        """
        return len(self._storage) == 0


if __name__ == "__main__":
    import doctest
    doctest.testmod()
