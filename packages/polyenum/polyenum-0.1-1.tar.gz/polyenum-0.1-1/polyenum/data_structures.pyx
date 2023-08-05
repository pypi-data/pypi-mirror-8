# coding=utf-8
#------------------------------------------------------------------
# File: data_structures.pyx    Author(s): Alexandre Blondin Massé
#                                         Simon Désaulniers
# Date: 2014-06-05
#------------------------------------------------------------------
# Data structures for polyomino enumeration
#------------------------------------------------------------------

from libc.stdlib cimport malloc, free
from data_structures cimport PartialPolyomino, PartialTree, PartialSnake, PartialNorthSnake, Polyomino

# Type declarations

cdef struct Site: # Ordered pair for the kink
    int lower     # The lower cell in the kink
    int upper     # The upper cell in the kink

# Data structures

cdef class PartialPolyomino:
    r"""
    A partial polyomino used in Jensen's algorithm for enumeration purposes.

    This is the fundamental data structure used in Jensen's paper [1]_. The
    constructor only allows the instantiation of empty partial polyominoes.
    Partial polyominoes can be extended with an empty cell or an occupied cell
    via the method ``extend``.

    Following Jensen's conventions, the addition of a new cell is constrained
    by rules to ensure that the partial polyomino yields at least one valid
    polyomino (i.e. it is fully connected and it touches the four sides of the
    inscribed rectangle). Each cell can be either ``0``, ``1``, ``2``, ``3``
    or ``4``, where ``0`` means that the cell is not occupied, while the
    remaining values keeps track of the connection relations.

    An important concept of Jensen's algorithm is that of *boundary*,
    corresponding to the list of each last cell in the row to have been filled
    (or not).  Initially, the boundary is by default a column of 0's. Each
    time the state of a new cell is updated, the boundary moves downward until
    the bottom of the column is reached and then it starts with the next
    column.

    INPUT:

    - ``height`` -- a positiver integer indicating the maximal height of the
      partial polyomino
    - ``width`` -- a positiver integer indicating the maximal width of the
      partial polyomino

    EXAMPLES::

        sage: PartialPolyomino(3, 4)
        Partial polyomino inscribed in a 3 by 4 rectangle with boundary [0, 0, 0]
        []
        []
        []
        sage: PartialPolyomino(3, 4).extend(occupied=True)
        Partial polyomino inscribed in a 3 by 4 rectangle with boundary [1, 0, 0]
        [1]
        []
        []
        sage: PartialPolyomino(3, 4).extend(occupied=True).extend(occupied=False)
        Partial polyomino inscribed in a 3 by 4 rectangle with boundary [1, 0, 0]
        [1]
        [0]
        []

    Creating the `L`-shaped tetromino inscribed in a `3 \times 2` rectangle::

        sage: pp = PartialPolyomino(3, 2)
        sage: for state in [True, True, True, False, False, True]:
        ....:     pp = pp.extend(occupied=state)
        sage: pp
        Partial polyomino inscribed in a 3 by 2 rectangle with boundary [0, 0, 1]
        [4, 0]
        [3, 0]
        [2, 1]
        sage: pp.is_polyomino()
        True

    REFERENCES:

    .. [1] I. Jensen
    .. [2] I. Jensen
    .. [3] D. Knuth

    """

    # Basic methods

    def __cinit__(self, int height, int width, bint allow_kiss=True):
        r"""
        Creates an instance of partial polyomino. Each column is encoded by a
        positive integer. The value for each cell can be obtained via the
        ``get_cell`` method.

        See also ``PartialPolyomino`` for more details.

        INPUT:

        - ``height`` -- a positiver integer indicating the maximal height of the
          partial polyomino
        - ``width`` -- a positiver integer indicating the maximal width of the
          partial polyomino
        - ``allow_kiss`` (default: True) boolean for specifying if kisses are
          allowed.

        EXAMPLE::

            sage: PartialPolyomino(1, 2)
            Partial polyomino inscribed in a 1 by 2 rectangle with boundary [0]
            []
        """
        self.matrix = <int**>malloc((height) * sizeof(int*))
        for i from 0 <= i < height:
            self.matrix[i] = <int*>malloc((width) * sizeof(int))
            for j from 0 <= j < width:
                self.matrix[i][j] = 0
        self.height = height
        self.width = width
        self.allow_kiss = allow_kiss
        self.current_height = 0
        self.current_width = 0
        self.touched_left = False
        self.touched_top = False
        self.touched_bottom = False
        self.num_cells = 0

    def __dealloc__(self):
        r"""
        Delete an instance of a partial polyomino.

        See ``PartialPolyomino`` for more details.
        """
        if self.matrix is not NULL:
            for i from 0 <= i < self.height:
                if self.matrix[i] is not NULL:
                    free(self.matrix[i])
            free(self.matrix)
            self.matrix = NULL

    def __repr__(self):
        r"""
        Returns a string representation of self.

        EXAMPLE::

            sage: PartialPolyomino(1, 2)
            Partial polyomino inscribed in a 1 by 2 rectangle with boundary [0]
            []
        """
        return self._to_string() % 'polyomino'

    def _to_string(self):
        r"""
        Returns a string representation of self with room for substitution
        (useful for inheriting classes).

        EXAMPLE::

            sage: print PartialPolyomino(1, 2)._to_string()
            Partial %s inscribed in a 1 by 2 rectangle with boundary [0]
            []
        """
        s = 'Partial %s inscribed in a %s by %s rectangle with boundary %s\n' %\
            ('%s',\
             self.height,\
             self.width,\
             [self._get_boundary_cell(i) for i in range(self.height)])
        for i in range(self.height):
            if i < self.current_height:
                right_limit = self.current_width + 1
            else:
                right_limit = self.current_width
            s += '%s\n' % [self.get_cell(i, j) for j in range(right_limit)]
        return s[:-1]

    cpdef PartialPolyomino clone(self):
        r"""
        Creates a deep copy of self.

        OUTPUT:

            A partial polyomino

        EXAMPLE::

            sage: pp = PartialPolyomino(3, 2)
            sage: pp2 = pp.clone()
            sage: pp = pp.extend(occupied=True)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [1, 0, 0]
            [1]
            []
            []
            sage: pp2
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [0, 0, 0]
            []
            []
            []
        """
        cdef PartialPolyomino pp
        pp = PartialPolyomino(self.height, self.width, self.allow_kiss)
        for i from 0 <= i < self.height:
            for j from 0 <= j < self.width:
                pp.matrix[i][j] = self.matrix[i][j]
        pp.current_height = self.current_height
        pp.current_width = self.current_width
        pp.touched_left = self.touched_left
        pp.touched_top = self.touched_top
        pp.touched_bottom = self.touched_bottom
        pp.num_cells = self.num_cells
        return pp

    cpdef int get_cell(self, int i, int j):
        r"""
        Returns the value of the cell at row ``i`` and column ``j``.

        The returned value is between ``0`` and ``4``. For simplifying some
        operations, if the indices ``i`` and ``j`` reference outer cells, the
        value ``0`` (empty cell) is returned.

        INPUT:

        - ``i`` -- the row number of the cell
        - ``j`` -- the column number of the cell

        OUTPUT:

        The corresponding value as an integer

        EXAMPLE::

        sage: pp = PartialPolyomino(3, 2).extend(True).extend(True).extend(False).extend(True)
        sage: pp
        Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 2, 0]
        [4, 4]
        [2]
        [0]
        sage: pp.get_cell(1, 1)
        0
        sage: pp.get_cell(12, 0)
        0
        sage: pp.get_cell(0, 1)
        4
        """
        if j >= 0 and j < self.width and i >= 0 and i < self.height:
            return self.matrix[i][j]
        else:
            return 0

    cpdef bint is_occupied(self, int i, int j):
        r"""
        Returns True if and only if the cell at indices ``(i,j)`` is occupied.

        By default, if the indices are outside the current matrix, the value
        ``0`` is returned.

        INPUT:

        - ``i`` -- the row number of the cell
        - ``j`` -- the column number of the cell

        OUTPUT:

        A boolean

        EXAMPLE::

            sage: pp = PartialPolyomino(3, 2).extend(True).extend(True).extend(False).extend(True)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 2, 0]
            [4, 4]
            [2]
            [0]
            sage: [[pp.is_occupied(i, j) for j in range(2)] for i in range(3)]
            [[True, True], [True, False], [False, False]]
        """
        return self.get_cell(i, j) != 0

    cpdef int _get_boundary_cell(self, int i):
        r"""
        Returns the value of the boundary cell at row ``i`` 

        INPUT:

        ``i`` -- the row number of the cell

        OUTPUT:

        The value of the cell as an integer

        EXAMPLE::

            sage: pp = PartialPolyomino(3, 2).extend(True).extend(True).extend(False).extend(True)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 2, 0]
            [4, 4]
            [2]
            [0]
            sage: [pp._get_boundary_cell(i) for i in range(3)]
            [4, 2, 0]
        """
        if i < self.current_height:
            return self.get_cell(i, self.current_width)
        else:
            return self.get_cell(i, self.current_width - 1)

    cpdef _set_boundary_cell(self, int i, int value):
        r"""
        Sets the value of the boundary cell at row ``i``.

        This method should not be used directly without updating correctly the
        whole data structure.

        INPUT:

        ``i`` -- the row number of the cell
        ``value`` -- the value of the cell between ``0`` and ``4``

        EXAMPLE::

            sage: pp = PartialPolyomino(3, 2).extend(True).extend(True).extend(False).extend(True)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 2, 0]
            [4, 4]
            [2]
            [0]
            sage: pp._set_boundary_cell(2, 1)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 2, 1]
            [4, 4]
            [2]
            [0]
        """
        if i < self.current_height:
            self.matrix[i][self.current_width] = value
        else:
            self.matrix[i][self.current_width - 1] = value

    cpdef bint is_boundary_connected(self):
        r"""
        Returns True if and only if the boundary is connected.

        Checking if the boundary is connected is sufficient to make sure that
        the complete polyomino is connected as well.

        OUTPUT:

        A boolean

        EXAMPLE:

            sage: pp = PartialPolyomino(3, 2)
            sage: for state in [True, False, True, True, False, True]:
            ....:     pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [1, 0, 1]
            [1, 1]
            [0, 0]
            [1, 1]
            sage: pp.is_boundary_connected()
            False
            sage: pp = PartialPolyomino(3, 2)
            sage: for state in [True, True, True, True, False, True]:
            ....:     pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 0, 2]
            [4, 4]
            [3, 0]
            [2, 2]
            sage: pp.is_boundary_connected()
            True
        """
        cdef int c = 0
        cdef int h = 0
        while h < self.height and c <= 1:
            if self._get_boundary_cell(h) == 1 or self._get_boundary_cell(h) == 2:
                c += 1
            h += 1
        return c == 1

    cpdef int get_upper_cell(self):
        r"""
        Returns the value of the cell above the current cell.

        In many cases, when updating the current cell with state ``occupied``
        or ``empty``, the configuration can be decided by local consultation
        and updating of the upper cell. In some other cases, the updating is
        not local, but depends of the upper cell.

        See also ``get_lower_cell``.

        OUTPUT:

        An integer

        EXAMPLE::

            sage: pp = PartialPolyomino(3, 2).extend(True).extend(True).extend(False).extend(True)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 2, 0]
            [4, 4]
            [2]
            [0]
            sage: pp.get_upper_cell()
            4
        """
        if self.current_height == 0:
            return 0
        else:
            return self._get_boundary_cell(self.current_height - 1)

    cpdef int get_lower_cell(self):
        r"""
        Returns the value of the cell to the left of the current cell.

        See also ``get_upper_cell``.

        OUTPUT:

        An integer

        EXAMPLE::

            sage: pp = PartialPolyomino(3, 2).extend(True).extend(True).extend(False).extend(True)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 2, 0]
            [4, 4]
            [2]
            [0]
            sage: pp.get_lower_cell()
            2
        """
        return self._get_boundary_cell(self.current_height)

    cpdef _set_upper_cell(self, int value):
        r"""
        Sets the cell above the current cell with the given value.

        This method should be used together with a correct updating of the
        columns to preserve the integrity of self.

        INPUT:

        The updated value for the lower cell

        EXAMPLE::

            sage: pp = PartialPolyomino(3, 2).extend(True).extend(True).extend(False).extend(True)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 2, 0]
            [4, 4]
            [2]
            [0]
            sage: pp._set_lower_cell(1)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 1, 0]
            [4, 4]
            [2]
            [0]
        """
        if self.current_height != 0:
            self._set_boundary_cell(self.current_height - 1, value)

    cpdef _set_lower_cell(self, int value):
        r"""
        Sets the cell to the left of the current cell with the given value.

        This method should be used together with a correct updating of the
        columns to preserve the integrity of self.

        INPUT:

        The updated value for the lower cell

        EXAMPLE::

            sage: pp = PartialPolyomino(3, 2).extend(True).extend(True).extend(False).extend(True)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 2, 0]
            [4, 4]
            [2]
            [0]
            sage: pp._set_lower_cell(1)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 1, 0]
            [4, 4]
            [2]
            [0]
        """
        self.matrix[self.current_height][self.current_width] = value

    cpdef int get_cell_degree(self, int i, int j):
        r"""
        Returns the degree of the cell in self.

        The *degree* of a cell is the sum of its number of horizontal and
        vertical neighbors.

        If the cell is empty, it returns -1.

        INPUT:

        - ``i`` -- the row number of the cell
        - ``j`` -- the column number of the cell

        OUTPUT:

        The number of neighbors as an integer

        EXAMPLE

            sage: pp = PartialPolyomino(3, 2)
            sage: for state in [True, True, True, True, False, True]:
            ....:     pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 0, 2]
            [4, 4]
            [3, 0]
            [2, 2]
            sage: [[pp.get_cell_degree(i, j) for j in range(2)] for i in range(3)]
            [[2, 1], [2, -1], [2, 1]]

        """
        cdef int d = 0
        if not self.is_occupied(i, j):
            return -1
        else:
            if self.get_cell(i - 1, j) != 0: d += 1
            if self.get_cell(i + 1, j) != 0: d += 1
            if self.get_cell(i, j - 1) != 0: d += 1
            if self.get_cell(i, j + 1) != 0: d += 1
        return d

    cpdef bint is_polyomino(self):
        r"""
        Returns True if and only if the current partial polyomino is an
        inscribed polyomino.

        OUTPUT:

        A boolean

        EXAMPLES::

            sage: pp = PartialPolyomino(3, 2)
            sage: for state in [True, True, True, True, False, True]:
            ....:     pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 0, 2]
            [4, 4]
            [3, 0]
            [2, 2]
            sage: pp.is_polyomino()
            True

        The partial polyomino must have fully completed the last column to be
        considered as a valid polyomino::

            sage: pp = PartialPolyomino(3, 2)
            sage: for state in [True, True, True, True, False]:
            ....:     pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 0, 2]
            [4, 4]
            [3, 0]
            [2]
            sage: pp.is_polyomino()
            False

        Moreover, it must be inscribed in the rectangle::

            sage: pp = PartialPolyomino(3, 3)
            sage: for state in [True, True, True, True, False, True]:
            ....:     pp = pp.extend(occupied=state)
            sage: pp.is_polyomino()
            False
        """
        return self.touched_bottom and\
               self.touched_top and\
               self.current_height == 0 and\
               self.current_width == self.width and\
               self.is_boundary_connected()

    cpdef Polyomino to_polyomino(self, bint check):
        r"""
        Converts the current partial polyomino to a polyomino object.

        If it is not a polyomino, then it returns None.

        INPUT:

        ``check`` -- (default: True) a boolean indicating whether to check if
        the partial polyomino is indeed a polyomino

        OUTPUT:

        A polyomino

        EXAMPLE::

            sage: pp = PartialPolyomino(3, 2)
            sage: for state in [True, True, True, True, False, True]:
            ....:     pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 0, 2]
            [4, 4]
            [3, 0]
            [2, 2]
            sage: pp.to_polyomino()
            Polyomino: ['111', '101']
        """
        if not check or self.is_polyomino():
            return Polyomino(self.height, self.width, self)
        else:
            return None

    # Pruning

    cpdef int bound_top_border_touching(self):
        r"""
        Returns the minimum number of cells required to make the current
        partial polyomino touch the top border.

        OUTPUT:

        The minimum number of cells as an integer

        EXAMPLES::

        If we want to construct a polyomino in a `3 \times 3` rectangle and if
        only the last row is filled so far, then we need at least `3` cells to
        connect it to the top::

            sage: pp = PartialPolyomino(3, 3)
            sage: for state in [False, False, True, False, False]: pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 3 rectangle with boundary [0, 0, 1]
            [0, 0]
            [0, 0]
            [1]
            sage: pp.bound_top_border_touching()
            3

        Clearly, if it already touches the top, it returns 0::

            sage: pp = PartialPolyomino(3, 2)
            sage: for state in [True, True, True, True, False]: pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 0, 2]
            [4, 4]
            [3, 0]
            [2]
            sage: pp.bound_top_border_touching()
            0
        """
        cdef int h
        if self.touched_top:
            return 0
        else:
            h = 0
            while self._get_boundary_cell(h) == 0:
                h += 1
            if h >= self.current_height:
                h += 1
            return h

    cpdef int bound_bottom_border_touching(self):
        r"""
        Returns the minimum number of cells required to make the current
        partial polyomino touch the bottom border.

        OUTPUT:

        The minimum number of cells as an integer

        EXAMPLES::

        In the example below, it suffices to occupy the current cell to connect
        the partial polyomino to the bottom::

            sage: pp = PartialPolyomino(3, 3)
            sage: for state in [False, True, False, True, True]: pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 3 rectangle with boundary [4, 2, 0]
            [0, 4]
            [1, 2]
            [0]
            sage: pp.bound_bottom_border_touching()
            1

        If it already touches the bottom, it returns 0::

            sage: pp = PartialPolyomino(3, 2)
            sage: for state in [True, True, True, True, False]: pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 2 rectangle with boundary [4, 0, 2]
            [4, 4]
            [3, 0]
            [2]
            sage: pp.bound_top_border_touching()
            0
        """
        cdef int h
        if self.touched_bottom:
            return 0
        else:
            h = self.height - 1
            while self._get_boundary_cell(h) == 0:
                h -= 1
            return self.height - 1 - h

    cpdef int bound_right_border_touching(self):
        r"""
        Returns the minimum number of cells required to make the current
        partial polyomino touch the right border.

        OUTPUT:

        The minimum number of cells as an integer

        EXAMPLE::

            sage: pp = PartialPolyomino(3, 3)
            sage: for state in [False, True, False, True, True]: pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 3 rectangle with boundary [4, 2, 0]
            [0, 4]
            [1, 2]
            [0]
            sage: pp.bound_right_border_touching()
            1
        """
        cdef int h = 0
        while self._get_boundary_cell(h) == 0:
            h += 1
        if h >= self.current_height:
            return self.width - self.current_width
        else:
            return self.width - self.current_width - 1

    cpdef int bound_make_connected(self):
        r"""
        Returns the minimum number of cells required to connect all
        connected components.

        OUTPUT:

        The minimum number of cells required as an integer.

        .. TODO::

        Currently return 0. See [Knuth2001]_.

        REFERENCES:

        .. [Knuth2001] D. Knuth. *Polynum.w*
           http://www-cs-faculty.stanford.edu/~knuth/programs/polynum.w
        """
        return 0

    cpdef int min_area(self):
        r"""
        Returns a lower bound of the area that can be realized by any extension
        of self.

        OUTPUT:

        A lower bound on the area as an integer

        .. TODO::

            Currently, the lower bound is bad. Should be improved.

        EXAMPLE:

        In the example below, the minimum area should be 5 instead of 3::

            sage: pp = PartialPolyomino(3, 3)
            sage: for state in [False, True, False, True, True]: pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 3 rectangle with boundary [4, 2, 0]
            [0, 4]
            [1, 2]
            [0]
            sage: pp.min_area()
            3
        """
        if self.num_cells == 0:
            return self.height + self.width - 1
        else:
            # TODO: Improve bounding using Knuth's algorithm for the minimum
            # connectivity problem
            return self.bound_top_border_touching() +\
                   self.bound_bottom_border_touching() +\
                   self.bound_right_border_touching() +\
                   self.num_cells - 2

    cpdef int max_area(self):
        r"""
        TODO
        """
        cdef int w1, h1, w2, h2
        w1 = self.width - self.current_width - 1
        h1 = self.current_height
        w2 = self.width - self.current_width
        h2 = self.height - self.current_height
        if h2 != 1:
            return three_quarters(w1, h1) + three_quarters(w2, h2) + self.num_cells
        else:
            return three_quarters(w1, self.height) + self.num_cells + 1

    # Extension

    cpdef bint is_extendable(self):
        r"""
        Returns True if self can be extended into a polyomino.

        OUTPUT:

        A boolean

        EXAMPLE::

            sage: pp = PartialPolyomino(3, 3)
            sage: for state in [False, True, False, True, True]: pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 3 rectangle with boundary [4, 2, 0]
            [0, 4]
            [1, 2]
            [0]
            sage: pp.is_extendable()
            True

        If the left side has not been touched, it is not extendable::

            sage: pp = PartialPolyomino(3, 3)
            sage: for state in [False, False, False]: pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 3 rectangle with boundary [0, 0, 0]
            [0]
            [0]
            [0]
            sage: pp.is_extendable()
            False
        """
        if self.current_width == self.width:
            return False
        elif self.current_width != 0 and not self.touched_left:
            return False
        else:
            return True

    cpdef bint creates_kiss(self, bint occupied):
        r"""
        Returns True if and only if setting the current cell status to
        ``occupied`` creates a kiss in self, i.e. two occupied cells sharing a
        corner without intermediary cells.

        INPUT:

        ``occupied`` -- a boolean indicating whether the new cell is occupied
        or empty

        OUTPUT:

        A boolean

        EXAMPLES::

        TODO
        """
        cpdef int h = self.current_height
        cpdef int w = self.current_width
        return occupied == self.is_occupied(h - 1, w - 1) and\
               self.is_occupied(h - 1, w) == self.is_occupied(h, w - 1) and\
               occupied != self.is_occupied(h - 1, w)

    cpdef PartialPolyomino extend(self, bint occupied):
        r"""
        Extends self with a new cell, either occupied or empty.

        None is returned if the extension is not possible.

        INPUT:

        ``occupied`` -- (default: True) a boolean indicating whether the new
        cell should be occupied or empty

        OUTPUT

        The extended partial polyomino if it exists, otherwise, None

        EXAMPLES::

        First, consider the following partial polyomino::

            sage: pp = PartialPolyomino(3, 3)
            sage: for state in [False, True, False, True]: pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 3 by 3 rectangle with boundary [1, 1, 0]
            [0, 1]
            [1]
            [0]

        It can be extended with an occupied cell::

            sage: pp.extend(occupied=True)
            Partial polyomino inscribed in a 3 by 3 rectangle with boundary [4, 2, 0]
            [0, 4]
            [1, 2]
            [0]

        But not with an empty cell, otherwise the cell in the second row, first
        column would be disconnected::

            sage: pp.extend(occupied=False)
            sage: pp.extend(occupied=False) is None
            True
        """
        cdef PartialPolyomino other
        cdef int lower
        cdef int upper
        cdef Site site
        site.lower = -1
        site.upper = -1
        if not self.is_extendable():
            return None
        if not self.allow_kiss and self.creates_kiss(occupied):
            return None
        other = self.clone()
        lower = other.get_lower_cell()
        upper = other.get_upper_cell()
        site = other._transition(lower, upper, occupied)
        if site.lower == -1:
            return None
        other._set_lower_cell(site.lower)
        other._set_upper_cell(site.upper)
        other._relabel(lower, upper, occupied)
        if occupied:
            other.num_cells += 1
            if other.current_width == 0: other.touched_left = True
            if other.current_height == 0: other.touched_top = True
            if other.current_height == other.height - 1: other.touched_bottom = True
        if other.current_height == other.height - 1:
            other.current_width += 1
            other.current_height = 0
        else:
            other.current_height += 1
        return other

    cpdef _bar_update_upward(self):
        r"""
        Updates the starting of the component in an upward direction.

        More precisely, the algorithm goes upward and finds the first matching
        cell that will become the starting cell of the connected component.

        EXAMPLE:

        This method is called in the following situation::

            sage: pp = PartialPolyomino(4, 2)
            sage: for state in [True, True, True, True, True, True, False]: pp = pp.extend(occupied=state)
            sage: pp
            Partial polyomino inscribed in a 4 by 2 rectangle with boundary [4, 3, 0, 2]
            [4, 4]
            [3, 3]
            [3, 0]
            [2]

        If one wishes to extend ``pp`` with an empty cell, then the starting
        point of the connected component must be updated so that it is at the
        second row::

            sage: pp.extend(occupied=False)
            Partial polyomino inscribed in a 4 by 2 rectangle with boundary [4, 2, 0, 0]
            [4, 4]
            [3, 2]
            [3, 0]
            [2, 0]

        The contribution of the ``_bar_update_upward` method is then as follows::

            sage: pp._set_lower_cell(0); pp._set_upper_cell(0)
            sage: pp
            Partial polyomino inscribed in a 4 by 2 rectangle with boundary [4, 3, 0, 0]
            [4, 4]
            [3, 3]
            [3, 0]
            [2]
            sage: pp._bar_update_upward()
            sage: pp
            Partial polyomino inscribed in a 4 by 2 rectangle with boundary [4, 2, 0, 0]
            [4, 4]
            [3, 2]
            [3, 0]
            [2]
        """
        cdef int stacked = 0
        cdef int h = self.current_height - 1
        while stacked > 0 or\
              (self._get_boundary_cell(h) != 3 and self._get_boundary_cell(h) != 4):
            if self._get_boundary_cell(h) == 2:
                stacked += 1
            elif self._get_boundary_cell(h) == 4:
                stacked -= 1
            h -= 1
        if self._get_boundary_cell(h) == 3:
            self._set_boundary_cell(h, 2)
        else:
            self._set_boundary_cell(h, 1)

    cpdef _bar_update_downward(self):
        r"""
        Updates the ending of the component in an downward direction.

        More precisely, the algorithm goes downward and finds the first matching
        cell that will become the ending cell of the connected component.

        EXAMPLE:

        This method is called in the following situation::

            sage: pp = PartialPolyomino(4, 3)
            sage: for state in 'xxxxx-xx': pp = pp.extend(occupied=state=='x')
            sage: pp
            Partial polyomino inscribed in a 4 by 3 rectangle with boundary [4, 0, 3, 2]
            [4, 4]
            [3, 0]
            [3, 3]
            [2, 2]

        If one wishes to extend ``pp`` with an empty cell, then the ending
        point of the connected component must be updated so that it is at the
        third row::

            sage: pp.extend(occupied=False)
            Partial polyomino inscribed in a 4 by 3 rectangle with boundary [0, 0, 4, 2]
            [4, 4, 0]
            [3, 0]
            [3, 3]
            [2, 2]

        The contribution of the ``_bar_update_downward` method is then as follows::

            sage: pp._set_lower_cell(0); pp._set_upper_cell(0)
            sage: pp
            Partial polyomino inscribed in a 4 by 3 rectangle with boundary [0, 0, 3, 2]
            [4, 4]
            [3, 0]
            [3, 3]
            [2, 2]
            sage: pp._bar_update_downward()
            sage: pp
            Partial polyomino inscribed in a 4 by 3 rectangle with boundary [0, 0, 4, 2]
            [4, 4]
            [3, 0]
            [3, 3]
            [2, 2]
        """
        cdef int stacked = 0
        cdef int h = self.current_height + 1
        while stacked > 0 or\
              (self._get_boundary_cell(h) != 3 and self._get_boundary_cell(h) != 2):
            if self._get_boundary_cell(h) == 4:
                stacked += 1
            elif self._get_boundary_cell(h) == 2:
                stacked -= 1
            h += 1
        if self._get_boundary_cell(h) == 3:
            self._set_boundary_cell(h, 4)
        else:
            self._set_boundary_cell(h, 1)

    cpdef _hat_update_upward(self):
        r"""
        Updates the boundary to merge two connected components.

        EXAMPLE:

        This method is called in the following situation::

            sage: pp = PartialPolyomino(5, 3)
            sage: for state in 'xxxxxx---xx-xx': pp = pp.extend(occupied=state=='x')
            sage: pp
            Partial polyomino inscribed in a 5 by 3 rectangle with boundary [4, 0, 4, 2, 2]
            [4, 4, 4]
            [3, 0, 0]
            [3, 0, 4]
            [3, 0, 2]
            [2, 2]

        If one wishes to extend ``pp`` with an occupied cell, then the two
        connected components are merged and the ``4`` in the 3rd row is
        replaced by ``4``::

            sage: pp.extend(occupied=True)
            Partial polyomino inscribed in a 5 by 3 rectangle with boundary [4, 0, 3, 3, 2]
            [4, 4, 4]
            [3, 0, 0]
            [3, 0, 3]
            [3, 0, 3]
            [2, 2, 2]

        The contribution of the ``_hat_update_upward` method is then as follows::

            sage: pp._set_lower_cell(2); pp._set_upper_cell(3)
            sage: pp
            Partial polyomino inscribed in a 5 by 3 rectangle with boundary [4, 0, 4, 3, 2]
            [4, 4, 4]
            [3, 0, 0]
            [3, 0, 4]
            [3, 0, 3]
            [2, 2]
            sage: pp._hat_update_upward()
            sage: pp
            Partial polyomino inscribed in a 5 by 3 rectangle with boundary [4, 0, 3, 3, 2]
            [4, 4, 4]
            [3, 0, 0]
            [3, 0, 3]
            [3, 0, 3]
            [2, 2]
        """
        cdef int stacked = 0
        cdef int h = self.current_height - 1
        while stacked > 0 or self._get_boundary_cell(h) != 4:
            if self._get_boundary_cell(h) == 2:
                stacked += 1
            elif self._get_boundary_cell(h) == 4:
                stacked -= 1
            h -= 1
        self._set_boundary_cell(h, 3)

    cpdef _hat_update_downward(self):
        r"""
        Updates the boundary to merge two connected components.

        EXAMPLE:

        This method is called in the following situation::

            sage: pp = PartialPolyomino(6, 4)
            sage: for state in 'xxxxxxx----xx-xx-xxx': pp = pp.extend(occupied=state=='x')
            sage: pp
            Partial polyomino inscribed in a 6 by 4 rectangle with boundary [4, 3, 4, 2, 0, 2]
            [4, 4, 4, 4]
            [3, 0, 0, 3]
            [3, 0, 4]
            [3, 0, 2]
            [3, 0, 0]
            [2, 2, 2]

        If one wishes to extend ``pp`` with an occupied cell, then the two
        connected components are merged and the ``2`` in the 4th row is
        replaced by ``3``::

            sage: pp.extend(occupied=True)
            Partial polyomino inscribed in a 6 by 4 rectangle with boundary [4, 3, 3, 3, 0, 2]
            [4, 4, 4, 4]
            [3, 0, 0, 3]
            [3, 0, 4, 3]
            [3, 0, 2]
            [3, 0, 0]
            [2, 2, 2]

        The contribution of the ``_hat_update_downward` method is then as follows::

            sage: pp._set_lower_cell(3); pp._set_upper_cell(3)
            sage: pp
            Partial polyomino inscribed in a 6 by 4 rectangle with boundary [4, 3, 3, 2, 0, 2]
            [4, 4, 4, 4]
            [3, 0, 0, 3]
            [3, 0, 4]
            [3, 0, 2]
            [3, 0, 0]
            [2, 2, 2]
            sage: pp._hat_update_downward()
            sage: pp
            Partial polyomino inscribed in a 6 by 4 rectangle with boundary [4, 3, 3, 3, 0, 2]
            [4, 4, 4, 4]
            [3, 0, 0, 3]
            [3, 0, 4]
            [3, 0, 2]
            [3, 0, 0]
            [2, 2, 2]
        """
        cdef int stacked = 0
        cdef int h = self.current_height + 1
        while stacked > 0 or self._get_boundary_cell(h) != 2:
            if self._get_boundary_cell(h) == 4:
                stacked += 1
            elif self._get_boundary_cell(h) == 2:
                stacked -= 1
            h += 1
        self._set_boundary_cell(h, 3)

    cpdef _relabel(self, int lower, int upper, bint occupied):
        r"""
        Updates the boundary when changes are not local.

        INPUT:

        - ``lower`` -- the value of the lower cell of the kink
        - ``upper`` -- the value of the upper cell of the kink
        - ``occupied`` -- a boolean indicating whether the new cell is occupied
          or empty

        EXAMPLE:

            sage: pp = PartialPolyomino(4, 2)
            sage: for state in 'xxxxxx-': pp = pp.extend(occupied=state=='x')
            sage: pp
            Partial polyomino inscribed in a 4 by 2 rectangle with boundary [4, 3, 0, 2]
            [4, 4]
            [3, 3]
            [3, 0]
            [2]
            sage: pp._set_lower_cell(0); pp._set_upper_cell(0)

        Here, we see that the ``3`` of the 2nd row must be relabelled byt ``2``
        as it is the new starting point of the cell::

            sage: pp._relabel(2, 0, False)
            sage: pp
            Partial polyomino inscribed in a 4 by 2 rectangle with boundary [4, 2, 0, 0]
            [4, 4]
            [3, 2]
            [3, 0]
            [2]
        """
        if not occupied:
            if lower == 2 and upper >= 0 and upper <= 2:
                self._bar_update_upward()
            elif lower == 4 and upper >= 0 and upper <= 3:
                self._bar_update_downward()
        else:
            if lower == 2 and upper == 2: self._hat_update_upward()
            if lower == 3 and upper == 2: self._hat_update_upward()
            if lower == 4 and upper == 3: self._hat_update_downward()

    cpdef Site _transition(self, int lower, int upper, bint occupied):
        r"""
        Returns the new lower and upper values of the current kink.
        This is the matrix transition found in Jensen's paper.

        +---+-------+-------+-------+-------+-------+
        |   |   0   |   1   |   2   |   3   |   4   |
        +---+-------+-------+-------+-------+-------+
        | 0 | 00 10 | 01 24 | 02 23 | 03 33 | 04 34 |
        +---+-------+-------+-------+-------+-------+
        | 1 | ++ 10 | No 24 | No 23 | No 33 | No No |
        +---+-------+-------+-------+-------+-------+
        | 2 | 00 20 | 01 23 | 02 23 | 02 23 | 01 24 |
        +---+-------+-------+-------+-------+-------+
        | 3 | 00 30 | 01 33 | 02 33 | 03 33 | 04 34 |
        +---+-------+-------+-------+-------+-------+
        | 4 | 00 40 | 01 34 | 02 33 | 03 33 | No No |
        +---+-------+-------+-------+-------+-------+

        In each cell, the first pair corresponds with the case where the cell
        is not occupied and the second pair with the case where the cell is
        occupied.

        INPUT:

        - ``lower`` -- the value of the lower cell of the kink
        - ``upper`` -- the value of the upper cell of the kink
        - ``occupied`` -- a boolean indicating whether the new cell is occupied
          or empty

        OUTPUT:

        An ordered pair of new values for the lower and upper cell

        EXAMPLES::

            sage: pp = PartialPolyomino(4, 2)
            sage: pp._transition(2, 3, True)['lower'], pp._transition(2, 3, True)['upper']
            (2, 3)
            sage: pp._transition(0, 0, False)['lower'], pp._transition(0, 0, False)['upper']
            (0, 0)

        When the transition is forbidden, the pair `(-1,-1)` is returned::

            sage: pp._transition(1, 4, False)['lower'], pp._transition(1, 4, False)['upper']
            (-1, -1)
        """
        cdef Site site
        site.lower = -1
        site.upper = -1

        if occupied:
            if lower == 0:
                if upper == 0:   site.lower = 1;\
                                 site.upper = 0
                elif upper == 1: site.lower = 2;\
                                 site.upper = 4
                elif upper == 2: site.lower = 2;\
                                 site.upper = 3
                elif upper == 3: site.lower = 3;\
                                 site.upper = 3
                elif upper == 4: site.lower = 3;\
                                 site.upper = 4
            elif lower == 1:
                if upper == 0:   site.lower = 1;\
                                 site.upper = 0
                elif upper == 1: site.lower = 2;\
                                 site.upper = 4
                elif upper == 2: site.lower = 2;\
                                 site.upper = 3
                elif upper == 3: site.lower = 3;\
                                 site.upper = 3
            elif lower == 2:
                if upper == 0:   site.lower = 2;\
                                 site.upper = 0
                elif upper == 1: site.lower = 2;\
                                 site.upper = 3
                elif upper == 2: site.lower = 2;\
                                 site.upper = 3
                elif upper == 3: site.lower = 2;\
                                 site.upper = 3
                elif upper == 4: site.lower = 2;\
                                 site.upper = 4
            elif lower == 3:
                if upper == 0:   site.lower = 3;\
                                 site.upper = 0
                elif upper == 1: site.lower = 3;\
                                 site.upper = 3
                elif upper == 2: site.lower = 3;\
                                 site.upper = 3
                elif upper == 3: site.lower = 3;\
                                 site.upper = 3
                elif upper == 4: site.lower = 3;\
                                 site.upper = 4
            elif lower == 4:
                if upper == 0:   site.lower = 4;\
                                 site.upper = 0
                elif upper == 1: site.lower = 3;\
                                 site.upper = 4
                elif upper == 2: site.lower = 3;\
                                 site.upper = 3
                elif upper == 3: site.lower = 3;\
                                 site.upper = 3
        else:
            if lower == 0:
                if upper == 0:   site.lower = 0;\
                                 site.upper = 0
                elif upper == 1: site.lower = 0;\
                                 site.upper = 1
                elif upper == 2: site.lower = 0;\
                                 site.upper = 2
                elif upper == 3: site.lower = 0;\
                                 site.upper = 3
                elif upper == 4: site.lower = 0;\
                                 site.upper = 4
            elif lower == 2:
                if upper == 0:   site.lower = 0;\
                                 site.upper = 0
                elif upper == 1: site.lower = 0;\
                                 site.upper = 1
                elif upper == 2: site.lower = 0;\
                                 site.upper = 2
                elif upper == 3: site.lower = 0;\
                                 site.upper = 2
                elif upper == 4: site.lower = 0;\
                                 site.upper = 1
            elif lower == 3:
                if upper == 0:   site.lower = 0;\
                                 site.upper = 0
                elif upper == 1: site.lower = 0;\
                                 site.upper = 1
                elif upper == 2: site.lower = 0;\
                                 site.upper = 2
                elif upper == 3: site.lower = 0;\
                                 site.upper = 3
                elif upper == 4: site.lower = 0;\
                                 site.upper = 4
            elif lower == 4:
                if upper == 0:   site.lower = 0;\
                                 site.upper = 0
                elif upper == 1: site.lower = 0;\
                                 site.upper = 1
                elif upper == 2: site.lower = 0;\
                                 site.upper = 2
                elif upper == 3: site.lower = 0;\
                                 site.upper = 3
        return site

cdef class PartialTree(PartialPolyomino):
    r"""
    A partial tree polyomino for enumeration purposes.

    This is a specialization of PartialPolyomino, but for trees, i.e.
    polyominoes that do not have cycles. This can be used exactly in the same
    manner as for partial polyominoes

    INPUT:

    - ``height`` -- a positiver integer indicating the maximal height of the
      partial polyomino
    - ``width`` -- a positiver integer indicating the maximal width of the
      partial polyomino

    EXAMPLES:

    Constructing the T-shaped tetromino::

        sage: pt = PartialTree(3, 2)
        sage: for state in 'xxx-x-': pt = pt.extend(occupied=state=='x')
        sage: pt
        Partial tree inscribed in a 3 by 2 rectangle with boundary [0, 1, 0]
        [4, 0]
        [3, 1]
        [2, 0]

    Some extensions are forbidden when comparing to partial polyominoes to
    prevent creating cycles::

        sage: pp = PartialPolyomino(2, 2)
        sage: for state in 'xxx': pp = pp.extend(occupied=state=='x')
        sage: pp.extend(occupied=True) is None
        False
        sage: pt = PartialTree(2, 2)
        sage: for state in 'xxx': pt = pt.extend(occupied=state=='x')
        sage: pt.extend(occupied=True) is None
        True
    """

    def __cinit__(self, int height, int width, bint allow_kiss):
        r"""
        Creates an instance of partial tree for enumeration purposes.

        See ``PartialTree`` for more details.

        EXAMPLE::

            sage: PartialTree(3, 2)
            Partial tree inscribed in a 3 by 2 rectangle with boundary [0, 0, 0]
            []
            []
            []
        """
        self.leaves = 0

    def __repr__(self):
        r"""
        Returns a string representation of self.

        EXAMPLE::

            sage: PartialTree(1, 2)
            Partial tree inscribed in a 1 by 2 rectangle with boundary [0]
            []
        """
        return self._to_string() % 'tree'

    cpdef PartialTree clone(self):
        r"""
        Creates a deep copy of self.

        OUTPUT:

            A partial tree

        EXAMPLE::

            sage: pt = PartialTree(3, 2)
            sage: pt2 = pt.clone()
            sage: pt = pt.extend(occupied=True)
            sage: pt
            Partial tree inscribed in a 3 by 2 rectangle with boundary [1, 0, 0]
            [1]
            []
            []
            sage: pt2
            Partial tree inscribed in a 3 by 2 rectangle with boundary [0, 0, 0]
            []
            []
            []
        """
        cdef PartialTree pp
        pp = PartialTree(self.height, self.width, self.allow_kiss)
        for i from 0 <= i < self.height:
            for j from 0 <= j < self.width:
                pp.matrix[i][j] = self.matrix[i][j]
        pp.current_height = self.current_height
        pp.current_width = self.current_width
        pp.touched_left = self.touched_left
        pp.touched_top = self.touched_top
        pp.touched_bottom = self.touched_bottom
        pp.num_cells = self.num_cells
        pp.leaves = self.leaves
        return pp

    cpdef PartialTree extend(self, bint occupied):
        r"""
        Extends self with a new cell, either occupied or empty.

        None is returned if the extension is not possible.

        INPUT:

        ``occupied`` -- (default: True) a boolean indicating whether the new
        cell should be occupied or empty

        OUTPUT

        The extended partial tree if it exists, otherwise, None

        EXAMPLES:

        Constructing the Z-shaped tetromino::

            sage: pt = PartialTree(2, 3)
            sage: for state in 'x-xx-x': pt = pt.extend(occupied=state=='x')
            sage: pt
            Partial tree inscribed in a 2 by 3 rectangle with boundary [0, 1]
            [1, 4, 0]
            [0, 2, 1]

        Some extensions are forbidden when comparing to partial polyominoes to
        prevent creating cycles::

            sage: pp = PartialPolyomino(3, 3)
            sage: for state in 'xxxx-xxx': pp = pp.extend(occupied=state=='x')
            sage: pp.extend(occupied=True) is None
            False
            sage: pt = PartialTree(3, 3)
            sage: for state in 'xxxx-xxx': pt = pt.extend(occupied=state=='x')
            sage: pt.extend(occupied=True) is None
            True
        """
        cdef PartialTree pt = <PartialTree>PartialPolyomino.extend(self, occupied)
        cdef int i, j
        if pt is not None:
            i = self.current_height
            j = self.current_width - 1
            if pt.get_cell_degree(i, j) == 1:
                pt.leaves += 1
            # Could be improved: should not process last column
            # as a whole but cell by cell
            if pt.current_width == pt.width:
                j = self.current_width
                for i from 0 <= i < self.height:
                    if pt.get_cell_degree(i, j) == 1:
                        pt.leaves += 1
        return pt

    cpdef Site _transition(self, int lower, int upper, bint occupied):
        r"""
        Returns the new lower and upper values from the current ones.
        This is the matrix transition found in Jensen's paper, but for
        lattice trees.

        +---+-------+-------+-------+-------+-------+
        |   |   0   |   1   |   2   |   3   |   4   |
        +---+-------+-------+-------+-------+-------+
        | 0 | 00 10 | 01 24 | 02 23 | 03 33 | 04 34 |
        +---+-------+-------+-------+-------+-------+
        | 1 | ++ 10 | No 24 | No 23 | No 33 | No No |
        +---+-------+-------+-------+-------+-------+
        | 2 | 00 20 | 01 23 | 02 23 | 02 No | 01 No |
        +---+-------+-------+-------+-------+-------+
        | 3 | 00 30 | 01 33 | 02 33 | 03 No | 04 No |
        +---+-------+-------+-------+-------+-------+
        | 4 | 00 40 | 01 34 | 02 33 | 03 33 | No No |
        +---+-------+-------+-------+-------+-------+

        In each cell, the first pair corresponds with the case where the cell
        is not occupied and the second pair with the case where the cell is
        occupied.

        INPUT:

        - ``lower`` -- the value of the lower cell of the kink
        - ``upper`` -- the value of the upper cell of the kink
        - ``occupied`` -- a boolean indicating whether the new cell is occupied
          or empty

        OUTPUT:

        An ordered pair of new values for the lower and upper cell

        EXAMPLES::

            sage: pp = PartialPolyomino(4, 2)
            sage: pp._transition(2, 4, True)['lower'], pp._transition(2, 4, True)['upper']
            (2, 4)
            sage: pt = PartialTree(4, 2)
            sage: pt._transition(2, 4, True)['lower'], pt._transition(2, 4, True)['upper']
            (-1, -1)
        """
        cdef Site site
        site.lower = -1
        site.upper = -1
        if occupied:
            if lower == 0:
                if upper == 0:   site.lower = 1;\
                                 site.upper = 0
                elif upper == 1: site.lower = 2;\
                                 site.upper = 4
                elif upper == 2: site.lower = 2;\
                                 site.upper = 3
                elif upper == 3: site.lower = 3;\
                                 site.upper = 3
                elif upper == 4: site.lower = 3;\
                                 site.upper = 4
            elif lower == 1:
                if upper == 0:   site.lower = 1;\
                                 site.upper = 0
                elif upper == 1: site.lower = 2;\
                                 site.upper = 4
                elif upper == 2: site.lower = 2;\
                                 site.upper = 3
                elif upper == 3: site.lower = 3;\
                                 site.upper = 3
            elif lower == 2:
                if upper == 0:   site.lower = 2;\
                                 site.upper = 0
                elif upper == 1: site.lower = 2;\
                                 site.upper = 3
                elif upper == 2: site.lower = 2;\
                                 site.upper = 3
            elif lower == 3:
                if upper == 0:   site.lower = 3;\
                                 site.upper = 0
                elif upper == 1: site.lower = 3;\
                                 site.upper = 3
                elif upper == 2: site.lower = 3;\
                                 site.upper = 3
            elif lower == 4:
                if upper == 0:   site.lower = 4;\
                                 site.upper = 0
                elif upper == 1: site.lower = 3;\
                                 site.upper = 4
                elif upper == 2: site.lower = 3;\
                                 site.upper = 3
                elif upper == 3: site.lower = 3;\
                                 site.upper = 3
        else:
            if lower == 0:
                if upper == 0:   site.lower = 0;\
                                 site.upper = 0
                elif upper == 1: site.lower = 0;\
                                 site.upper = 1
                elif upper == 2: site.lower = 0;\
                                 site.upper = 2
                elif upper == 3: site.lower = 0;\
                                 site.upper = 3
                elif upper == 4: site.lower = 0;\
                                 site.upper = 4
            elif lower == 2:
                if upper == 0:   site.lower = 0;\
                                 site.upper = 0
                elif upper == 1: site.lower = 0;\
                                 site.upper = 1
                elif upper == 2: site.lower = 0;\
                                 site.upper = 2
                elif upper == 3: site.lower = 0;\
                                 site.upper = 2
                elif upper == 4: site.lower = 0;\
                                 site.upper = 1
            elif lower == 3:
                if upper == 0:   site.lower = 0;\
                                 site.upper = 0
                elif upper == 1: site.lower = 0;\
                                 site.upper = 1
                elif upper == 2: site.lower = 0;\
                                 site.upper = 2
                elif upper == 3: site.lower = 0;\
                                 site.upper = 3
                elif upper == 4: site.lower = 0;\
                                 site.upper = 4
            elif lower == 4:
                if upper == 0:   site.lower = 0;\
                                 site.upper = 0
                elif upper == 1: site.lower = 0;\
                                 site.upper = 1
                elif upper == 2: site.lower = 0;\
                                 site.upper = 2
                elif upper == 3: site.lower = 0;\
                                 site.upper = 3
        return site

cdef class PartialSnake(PartialTree):
    r"""
    A partial snake polyomino for enumeration purposes.

    This is a specialization of PartialTree, but for snakes, i.e.  polyominoes
    that are trees with exactly two leaves. This can be used exactly in the
    same manner as for partial polyominoes and partial trees.

    INPUT:

    - ``height`` -- a positiver integer indicating the maximal height of the
      partial polyomino
    - ``width`` -- a positiver integer indicating the maximal width of the
      partial polyomino

    EXAMPLES:

    The Z-shaped tetromino is a snake::

        sage: ps = PartialSnake(2, 3)
        sage: for state in 'x-xx-x': ps = ps.extend(occupied=state=='x')
        sage: ps
        Partial snake inscribed in a 2 by 3 rectangle with boundary [0, 1]
        [1, 4, 0]
        [0, 2, 1]

    On the other hand, the T-shaped tetromino is a tree but not a snake, since
    it has 3 leaves::

        sage: pt = PartialTree(3, 2)
        sage: for state in 'xxx-x-': pt = pt.extend(occupied=state=='x')
        sage: pt
        Partial tree inscribed in a 3 by 2 rectangle with boundary [0, 1, 0]
        [4, 0]
        [3, 1]
        [2, 0]
        sage: ps = PartialSnake(3, 2)
        sage: for state in 'xxx-x-': ps = ps.extend(occupied=state=='x')
        sage: ps is None
        True
    """

    def __repr__(self):
        r"""
        Returns a string representation of self.

        EXAMPLE::

            sage: PartialSnake(1, 2)
            Partial snake inscribed in a 1 by 2 rectangle with boundary [0]
            []
        """
        return self._to_string() % 'snake'

    cpdef PartialSnake clone(self):
        r"""
        Creates a deep copy of self.

        OUTPUT:

            A partial snake

        EXAMPLE::

            sage: ps = PartialSnake(3, 2)
            sage: ps2 = ps.clone()
            sage: ps = ps.extend(occupied=True)
            sage: ps
            Partial snake inscribed in a 3 by 2 rectangle with boundary [1, 0, 0]
            [1]
            []
            []
            sage: ps2
            Partial snake inscribed in a 3 by 2 rectangle with boundary [0, 0, 0]
            []
            []
            []
        """
        cdef PartialSnake ps
        ps = PartialSnake(self.height, self.width, self.allow_kiss)
        for i from 0 <= i < self.height:
            for j from 0 <= j < self.width:
                ps.matrix[i][j] = self.matrix[i][j]
        ps.current_height = self.current_height
        ps.current_width = self.current_width
        ps.touched_left = self.touched_left
        ps.touched_top = self.touched_top
        ps.touched_bottom = self.touched_bottom
        ps.num_cells = self.num_cells
        ps.leaves = self.leaves
        return ps

    cpdef PartialSnake extend(self, bint occupied):
        r"""
        Extends self with a new cell, either occupied or empty.

        None is returned if the extension is not possible. The extensions are
        the same as for partial trees except when a third leaves is created.

        INPUT:

        ``occupied`` -- (default: True) a boolean indicating whether the new
        cell should be occupied or empty

        OUTPUT

        The extended partial tree if it exists, otherwise, None

        EXAMPLE:

        As soon as a third leaves is detected, the extension is forbidden::

            sage: ps = PartialSnake(3, 3)
            sage: for state in '-x-xxx-x': ps = ps.extend(occupied=state=='x')
            sage: ps
            Partial snake inscribed in a 3 by 3 rectangle with boundary [0, 4, 2]
            [0, 4, 0]
            [1, 3, 4]
            [0, 2]
            sage: ps.extend(occupied=False) is None
            True
        """
        cdef PartialSnake ps = <PartialSnake>PartialTree.extend(self, occupied)
        if ps is not None and ps.leaves >= 3:
            return None
        else:
            return ps

cdef class PartialNorthSnake(PartialSnake):

    def __init__(self, int height, int width, bint allow_kiss):
        self.has_pillar = [False for _ in range(height - 1)]

    def __repr__(self):
        r"""
        Returns a string representation of self.

        EXAMPLE::

            sage: PartialNorthSnake(1, 2)
            Partial north snake inscribed in a 1 by 2 rectangle with boundary [0]
            []
        """
        return self._to_string() % 'north snake'

    cpdef PartialNorthSnake clone(self):
        r"""
        Creates a deep copy of self.

        OUTPUT:

            A partial north snake

        EXAMPLE::

            sage: ps = PartialSnake(3, 2)
            sage: ps2 = ps.clone()
            sage: ps = ps.extend(occupied=True)
            sage: ps
            Partial north snake inscribed in a 3 by 2 rectangle with boundary [1, 0, 0]
            [1]
            []
            []
            sage: ps2
            Partial north snake inscribed in a 3 by 2 rectangle with boundary [0, 0, 0]
            []
            []
            []
        """
        cdef PartialNorthSnake pns
        pns = PartialNorthSnake(self.height, self.width, self.allow_kiss)
        for i from 0 <= i < self.height:
            for j from 0 <= j < self.width:
                pns.matrix[i][j] = self.matrix[i][j]
        pns.current_height = self.current_height
        pns.current_width = self.current_width
        pns.touched_left = self.touched_left
        pns.touched_top = self.touched_top
        pns.touched_bottom = self.touched_bottom
        pns.num_cells = self.num_cells
        pns.leaves = self.leaves
        pns.has_pillar = [b for b in self.has_pillar]
        return pns

    cpdef PartialNorthSnake extend(self, bint occupied):
        r"""
        Extends self with a new cell, either occupied or empty.

        None is returned if the extension is not possible. The extensions are
        the same as for partial trees except when a third leaves is created.

        INPUT:

        ``occupied`` -- (default: True) a boolean indicating whether the new
        cell should be occupied or empty

        OUTPUT

        The extended partial tree if it exists, otherwise, None

        EXAMPLE:

        As soon as a third leaves is detected, the extension is forbidden::

            sage: pns = PartialNorthSnake(3, 3)
            sage: for state in '-x-xxx-x': pns = pns.extend(occupied=state=='x')
            sage: pns
            Partial north snake inscribed in a 3 by 3 rectangle with boundary [0, 4, 2]
            [0, 4, 0]
            [1, 3, 4]
            [0, 2]
            sage: pns.extend(occupied=False) is None
            True
        """
        cdef PartialNorthSnake pns = <PartialNorthSnake>PartialSnake.extend(self, occupied)
        if pns is None:
            return None
        i = self.current_height - 1
        j = self.current_width
        if occupied and self.is_occupied(i, j):
            if self.has_pillar[i]:
                return None
            else:
                pns.has_pillar[i] = True
        return pns

cdef class Polyomino:

    def __cinit__(self, int height, int width, PartialPolyomino pp):
        self.matrix = <bint**>malloc((height) * sizeof(bint*))
        for i from 0 <= i < height:
            self.matrix[i] = <bint*>malloc((width) * sizeof(bint))
            for j from 0 <= j < width:
                self.matrix[i][j] = pp.is_occupied(i, j)
        self.height = height
        self.width = width

    def __dealloc__(self):
        if self.matrix is not NULL:
            for i from 0 <= i < self.height:
                if self.matrix[i] is not NULL:
                    free(self.matrix[i])
            free(self.matrix)
            self.matrix = NULL

    def __repr__(self):
        return 'Polyomino:\n%s' % self.ascii()

    cpdef int degree(self, int i, int j):
        cdef int d = 0
        if not self.matrix[i][j]:
            return 0
        if i > 0 and self.matrix[i - 1][j]:
            d += 1
        if i < self.height - 1 and self.matrix[i + 1][j]:
            d += 1
        if j > 0 and self.matrix[i][j - 1]:
            d += 1
        if j < self.width - 1 and self.matrix[i][j + 1]:
            d += 1
        return d

    cpdef int number_of_leaves(self):
        cdef int leaves = 0
        for i from 0 <= i < self.height:
            for j from 0 <= j < self.width:
                if self.degree(i, j) == 1:
                    leaves += 1
        return leaves

    def ascii(self):
        s = ''
        for i in range(self.height):
            for j in range(self.width):
                if self.matrix[i][j]:
                    s += 'X'
                else:
                    s += '-'
            s += '\n'
        return s

    cpdef Polyomino transpose(self):
        cdef Polyomino p
        p = Polyomino(self.width, self.height, PartialPolyomino(self.width,
                      self.height))
        for i from 0 <= i < self.width:
            for j from 0 <= j < self.height:
                p.matrix[i][j] = self.matrix[j][i]
        return p

