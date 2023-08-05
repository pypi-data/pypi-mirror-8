# coding=utf-8
#------------------------------------------------------------------
# File: enumeration.pyx    Author(s): Alexandre Blondin Massé
#                                     Simon Désaulniers
# Date: 2014-01-08
#------------------------------------------------------------------
# The code for enumeration of polyominoes
#------------------------------------------------------------------

# distutils: language = c++

from libc.stdlib cimport malloc, free
from cpython.exc cimport PyErr_CheckSignals
from data_structures cimport PartialPolyomino, PartialTree, PartialSnake, PartialNorthSnake, Polyomino
from enumerators cimport Enumerator, InscribedPolyominoesEnumerator, InscribedTreeEnumerator, InscribedSnakeEnumerator, InscribedNorthSnakeEnumerator, PolyominoesEnumerator

# Enumerators

cdef class Enumerator(object):
    r"""
    Interface of an Enumerator.
    """

    cpdef set_area(self, int area):
        self.area = area

    cpdef get_area(self):
        return self.area 

    cpdef set_width(self, int width):
        self.width = width

    cpdef get_width(self):
        return self.width 

    cpdef set_height(self, int height):
        self.height = height

    cpdef get_height(self):
        return self.height 

    def reset(self):
        raise NotImplementedError, "This method should be overridden"

    cpdef bint has_next(self):
        raise NotImplementedError, "This method should be overridden"

    cpdef int count(self):
        raise NotImplementedError, "This method should be overridden"

    cpdef str lookingFor(self):
        r"""
        Says what the enumerator is looking for.
        """
        return self.what_looking_for

cdef class InscribedPolyominoesEnumerator(Enumerator):
    r"""
    Creates an enumerator of polyominoes inscribed in a rectangle of given
    dimensions.

    INPUT:

    - ``area`` -- the area of the polyominoes
    - ``height`` -- the height of the rectangle
    - ``width`` -- the width of the rectangle

    .. NOTE::

        Since Cython does not support the yield statement, the enumerator is an
        object providing the usual ``has_next`` and ``next_obj`` methods.

    EXAMPLES::

    It is easy to enumerate all polyominoes of 4 cells in a `3 \times 2`
    rectangle::

        sage: ipe = InscribedPolyominoesEnumerator(4, 3, 2)
        sage: while ipe.has_next(): print ipe.next_obj()
        Polyomino: ['001', '111']
        Polyomino: ['010', '111']
        Polyomino: ['011', '110']
        Polyomino: ['100', '111']
        Polyomino: ['110', '011']
        Polyomino: ['111', '001']
        Polyomino: ['111', '010']
        Polyomino: ['111', '100']

    Clearly, the number of polyominoes in a `3 \times 5` rectangle and that in
    a `5 \times 3` rectangle should be the same::

        sage: s = 0
        sage: ipe = InscribedPolyominoesEnumerator(11, 3, 5)
        sage: while ipe.has_next():
        ....:     s += 1
        ....:     _ = ipe.next_obj()
        sage: s
        778
        sage: s = 0
        sage: ipe = InscribedPolyominoesEnumerator(11, 5, 3)
        sage: while ipe.has_next():
        ....:     s += 1
        ....:     _ = ipe.next_obj()
        sage: s
        778
    """

    # optional argument leaves only there to prevent having execution errors due
    # to cython.
    def __cinit__(self, int area, int height, int width, bint allow_kiss, bint verbose, bint do_reset=True, int leaves=-1):
        r"""
        Creates a enumerator of inscribed polyominoes.

        INPUT:

        - ``area`` -- the area of the polyominoes
        - ``height`` -- the height of the rectangle
        - ``width`` -- the width of the rectangle
        - ``allow_kiss`` -- a boolean indicating if kisses are allowed.
        - ``verbose`` -- a boolean indicating if the enumeration progress
          should be output

        EXAMPLES:

        Enumerating the 4 polyominoes of 3 cells in a `2 \times 2` rectangle::

            sage: ipe = InscribedPolyominoesEnumerator(3, 2, 2)
            sage: while ipe.has_next(): print ipe.next_obj()
            Polyomino: ['01', '11']
            Polyomino: ['10', '11']
            Polyomino: ['11', '01']
            Polyomino: ['11', '10']
        """
        self.what_looking_for = "polyominoes"
        self.area = area
        self.height = height
        self.width = width
        self.allow_kiss = allow_kiss
        self.verbose = verbose
        if do_reset:
            self.reset()

    def reset(self):
        r"""
        Resets enumerator to initial state.
        """
        self.partials = [PartialPolyomino(self.height, self.width, self.allow_kiss)]
        self._update_to_next()

    cpdef _update_to_next(self):
        r"""
        Computes the next polyomino to be yielded in the enumeration.

        .. NOTE::

            This method should not be called directly, as it might corrupt the
            enumerator

        EXAMPLE:

        The method is called at initialization to point toward the next
        polyomino to be enumerated::

            sage: ipe = InscribedPolyominoesEnumerator(3, 2, 2)
            sage: ipe.next_obj()
            Polyomino: ['01', '11']
        """
        # are the variables ``occupied`` and ``empty`` useless ?
        cdef PartialPolyomino pp, empty, occupied
        self.found = False
        while self.partials and not self.found and not PyErr_CheckSignals():
            if self.verbose and len(self.partials) < 10: print len(self.partials),
            pp = self.partials.pop()
            if pp is not None:
                if pp.is_polyomino() and pp.num_cells == self.area:
                    self.found = True
                    self.polyomino = pp.to_polyomino(check=False)
                else:
                    if pp.min_area() <= self.area:
                        self.partials.append(pp.extend(occupied=False))
                        self.partials.append(pp.extend(occupied=True))

    cpdef next_obj(self):
        r"""
        Returns the next polyomino.

        EXAMPLE:

            sage: ipe = InscribedPolyominoesEnumerator(3, 2, 2)
            sage: ipe.next_obj()
            Polyomino: ['01', '11']
        """
        if self.found:
            polyomino = self.polyomino
            self._update_to_next()
            return polyomino
        else:
            raise StopIteration

    cpdef bint has_next(self):
        r"""
        Indicates whether there is another polyomino to be enumerated.

        EXAMPLE:

            sage: ipe = InscribedPolyominoesEnumerator(3, 2, 2)
            sage: ipe.has_next()
            True
            sage: ipe.has_next()
            True
            sage: ipe.next_obj()
            Polyomino: ['01', '11']
            sage: ipe.has_next()
            True
            sage: ipe.next_obj()
            Polyomino: ['10', '11']
            sage: ipe.next_obj()
            Polyomino: ['11', '01']
            sage: ipe.next_obj()
            Polyomino: ['11', '10']
            sage: ipe.has_next()
            False
            sage: ipe.next_obj()
            Traceback (most recent call last):
            ...
            StopIteration
        """
        return self.found

    cpdef int print_all(self):
        r"""
        TODO: add documentation
        """
        cdef int n = 0
        while self.has_next():
            print self.next_obj().ascii()
            n += 1
        return n

    cpdef int count(self):
        r"""
        TODO: add documentation
        """
        cdef int n = 0
        while self.has_next():
            self.next_obj()
            n += 1
        return n

cdef class InscribedTreeEnumerator(InscribedPolyominoesEnumerator):
    r"""
    Creates an enumerator of trees inscribed in a rectangle of given
    dimensions.

    This is the same as ``InscribedPolyominoesEnumerator`` but for trees.

    INPUT:

    - ``area`` -- the area of the trees
    - ``height`` -- the height of the rectangle
    - ``width`` -- the width of the rectangle
    - ``leaves`` -- the number of leaves all enumerated polyominoes must have.

    .. NOTE::

        Since Cython does not support the yield statement, the enumerator is an
        object providing the usual ``has_next`` and ``next_obj`` methods.

    EXAMPLES::

    We can enumerate all trees of 5 cells in a `3 \times 2` rectangle (note
    that there is no `2 \times 2` subsquare of fully occupied cells)::

        sage: ite = InscribedTreeEnumerator(5, 3, 2)
        sage: while ite.has_next(): print ite.next_obj()
        Polyomino: ['101', '111']
        Polyomino: ['111', '101']
    """

    def __cinit__(self, int area, int height, int width, bint allow_kiss, bint verbose, bint do_reset=True, int leaves=-1):
        r"""
        Creates a enumerator of inscribed trees.

        INPUT:

        - ``area`` -- the area of the polyominoes
        - ``height`` -- the height of the rectangle
        - ``width`` -- the width of the rectangle
        - ``leaves`` -- the number of leaves all enumerated polyominoes must have.

        EXAMPLES:

        Enumerating the 10 trees of 8 cells in a `3 \times 3` rectangle::

            sage: ite = InscribedTreeEnumerator(7, 3, 3)
            sage: while ite.has_next(): print ite.next_obj()
            Polyomino: ['011', '101', '111']
            Polyomino: ['101', '101', '111']
            Polyomino: ['101', '111', '101']
            Polyomino: ['110', '101', '111']
            Polyomino: ['111', '001', '111']
            Polyomino: ['111', '010', '111']
            Polyomino: ['111', '100', '111']
            Polyomino: ['111', '101', '011']
            Polyomino: ['111', '101', '101']
            Polyomino: ['111', '101', '110']
        """
        self.what_looking_for = "trees"
        self.area = area
        self.height = height
        self.width = width
        self.leaves = leaves
        self.allow_kiss = allow_kiss
        self.verbose = verbose
        if do_reset:
            self.reset()

    def set_leaves(self, leaves):
        self.leaves = leaves

    def get_leaves(self):
        return self.leaves

    def reset(self):
        r"""
        Resets enumerator to default configuration.
        """
        self.partials = [PartialTree(self.height, self.width, self.allow_kiss)]
        self._update_to_next()

    cpdef _update_to_next(self):
        r"""
        TODO
        """
        # are the variables ``occupied`` and ``empty`` useless ?
        cdef PartialTree pt, empty, occupied
        self.found = False
        while self.partials and not self.found and not PyErr_CheckSignals():
            if self.verbose and len(self.partials) < 10: print len(self.partials),
            pt = self.partials.pop()
            if pt is not None:
                if pt.is_polyomino() and pt.num_cells == self.area:
                    if self.leaves == -1 or self.leaves == pt.leaves:
                        self.found = True
                        self.polyomino = pt.to_polyomino(check=False)
                else:
                    if pt.min_area() <= self.area and self.area <= pt.max_area():
                        self.partials.append(pt.extend(occupied=False))
                        self.partials.append(pt.extend(occupied=True))

    cpdef next_obj(self):
        r"""
        Returns the next inscribed tree.

        EXAMPLE:

        Enumerating the two first trees of 5 cells inscribed in a `2 \times 3`
        rectangle::

            sage: ite = InscribedTreeEnumerator(5, 2, 3)
            sage: ite.next_obj()
            Polyomino: ['11', '01', '11']
            sage: ite.next_obj()
            Polyomino: ['11', '10', '11']
        """
        if self.found:
            polyomino = self.polyomino
            self._update_to_next()
            return polyomino
        else:
            raise StopIteration

    cpdef bint has_next(self):
        r"""
        Indicates whether there is another tree to be enumerated.

        EXAMPLE:

            sage: ite = InscribedTreeEnumerator(5, 2, 3)
            sage: ite.has_next()
            True
            sage: ite.next_obj()
            Polyomino: ['11', '01', '11']
            sage: ite.has_next()
            True
            sage: ite.next_obj()
            Polyomino: ['11', '10', '11']
            sage: ite.has_next()
            False
            sage: ite.next_obj()
            Traceback (most recent call last):
            ...
            StopIteration
        """
        return self.found

cdef class InscribedSnakeEnumerator(InscribedTreeEnumerator):
    r"""
    Creates an enumerator of snakes inscribed in a rectangle of given
    dimensions.

    This is the same as ``InscribedPolyominoesEnumerator`` but for snakes.

    INPUT:

    - ``area`` -- the area of the polyominoes
    - ``height`` -- the height of the rectangle
    - ``width`` -- the width of the rectangle

    .. NOTE::

        Since Cython does not support the yield statement, the enumerator is an
        object providing the usual ``has_next`` and ``next_obj`` methods.

    EXAMPLES::

    We can enumerate all snakes of 7 cells in a `3 \times 3` rectangle::

        sage: ise = InscribedSnakeEnumerator(7, 3, 3)
        sage: while ise.has_next(): print ise.next_obj()
        Polyomino: ['011', '101', '111']
        Polyomino: ['101', '101', '111']
        Polyomino: ['110', '101', '111']
        Polyomino: ['111', '001', '111']
        Polyomino: ['111', '100', '111']
        Polyomino: ['111', '101', '011']
        Polyomino: ['111', '101', '101']
        Polyomino: ['111', '101', '110']
    """

    def __cinit__(self, int area, int height, int width, bint allow_kiss, bint verbose, bint do_reset=True):
        r"""
        Creates a enumerator of inscribed snakes.

        INPUT:

        - ``area`` -- the area of the snakes
        - ``height`` -- the height of the rectangle
        - ``width`` -- the width of the rectangle

        EXAMPLES:

            sage: ise = InscribedSnakeEnumerator(3, 2, 2)
            sage: while ise.has_next(): print ise.next_obj()
            Polyomino: ['01', '11']
            Polyomino: ['10', '11']
            Polyomino: ['11', '01']
            Polyomino: ['11', '10']
        """
        self.what_looking_for = "snakes"
        self.area = area
        self.height = height
        self.width = width
        self.allow_kiss = allow_kiss
        self.verbose = verbose
        if do_reset:
            self.reset()

    def reset(self):
        r"""
        Resets enumerator to initial state.
        """
        self.partials = [PartialSnake(self.height, self.width, self.allow_kiss)]
        self._update_to_next()

cdef class InscribedNorthSnakeEnumerator(InscribedSnakeEnumerator):

    def __cinit__(self, int area, int height, int width, bint allow_kiss, bint verbose, bint do_reset=True):
        self.what_looking_for = "north snakes"
        if do_reset:
            self.reset()

    def reset(self):
        self.partials = [PartialNorthSnake(self.height, self.width, self.allow_kiss)]
        self._update_to_next()

cdef class PolyominoesEnumerator(Enumerator):
    r"""
    An enumerator of polyominoes by prescribed area.

    INPUT:

    ``area`` -- the number of cells of the polyominoes

    EXAMPLE:

    All tetrominoes::

        sage: pe = PolyominoesEnumerator(4)
        sage: while pe.has_next(): print pe.next_obj()
        Polyomino: ['1', '1', '1', '1']
        Polyomino: ['1111']
        Polyomino: ['11', '11']
        Polyomino: ['01', '01', '11']
        Polyomino: ['111', '100']
        Polyomino: ['01', '11', '01']
        Polyomino: ['111', '010']
        Polyomino: ['01', '11', '10']
        Polyomino: ['011', '110']
        Polyomino: ['10', '10', '11']
        Polyomino: ['100', '111']
        Polyomino: ['10', '11', '01']
        Polyomino: ['110', '011']
        Polyomino: ['10', '11', '10']
        Polyomino: ['010', '111']
        Polyomino: ['11', '01', '01']
        Polyomino: ['111', '001']
        Polyomino: ['11', '10', '10']
        Polyomino: ['001', '111']

    The sequence `A001168 <http://oeis.org/A001168>`__ found on the OEIS gives the
    number of fixed polyominoes with `n` cells::

        sage: for area in range(1, 6):
        ....:     pe = PolyominoesEnumerator(area)
        ....:     s = 0
        ....:     while pe.has_next():
        ....:         _ = pe.next_obj()
        ....:         s += 1
        ....:     print s
        1
        2
        6
        19
        63
    """

    def __cinit__(self, int area, bint allow_kiss, bint verbose):
        r"""
        Creates an instance of polyomino enumerator.

        INPUT:

        ``area`` -- the number of cells of the polyominoes

        EXAMPLE::

            sage: PolyominoesEnumerator(3).next_obj()
            Polyomino: ['1', '1', '1']
        """
        self.what_looking_for = "polyominoes"
        self.area = area
        self.current_height = 1
        self.current_width = 1
        self.allow_kiss = allow_kiss
        self.verbose = verbose

    cpdef set_area(self, int new_area):
        self.area = new_area

    def reset(self):
        self.enumerator = InscribedPolyominoesEnumerator(self.area, 1, 1, self.allow_kiss,\
                verbose=self.verbose)
        self.return_transposed = False
        self._update_to_next()

    cpdef _update_to_next(self):
        r"""
        Computes the next polyomino to be returned.

        For this purpose, an enumerator of inscribed polyominoes is maintained
        and updated. Whenever some given rectangle is exhausted, the next one
        is computed.

        .. NOTE::

            This method should not be called directly, as it might corrupt the
            enumerator

        EXAMPLE::

            sage: PolyominoesEnumerator(2).next_obj()
            Polyomino: ['1', '1']
        """
        PyErr_CheckSignals()

        self.found = True
        if self.return_transposed:
            self.polyomino = self.polyomino.transpose()
            self.return_transposed = False
        elif self.enumerator.has_next():
            self.polyomino = self.enumerator.next_obj()
            if self.current_height < self.current_width:
                self.return_transposed = True
        else:
            if self.current_width == self.area:
                self.current_height += 1
                self.current_width = self.current_height
            else:
                self.current_width += 1
            if self.current_height <= self.area:
                self.enumerator = InscribedPolyominoesEnumerator(self.area,\
                                                                 self.current_height,\
                                                                 self.current_width,\
                                                                 self.allow_kiss,\
                                                                 verbose=self.verbose)
                if self.enumerator.has_next():
                    self.polyomino = self.enumerator.next_obj()
                    if self.current_height < self.current_width:
                        self.return_transposed = True
                else:
                    self._update_to_next()
            else:
                self.found = False

    cpdef Polyomino next_obj(self):
        r"""
        Returns the next polyomino of given area.

        OUTPUT:

        A polyomino

        EXAMPLE::

            sage: pe = PolyominoesEnumerator(4)
            sage: pe.next_obj()
            Polyomino: ['1', '1', '1', '1']
            sage: pe.next_obj()
            Polyomino: ['1111']
            sage: pe.next_obj()
            Polyomino: ['11', '11']
        """
        if self.found:
            polyomino = self.polyomino
            self._update_to_next()
            return polyomino
        else:
            raise StopIteration

    cpdef bint has_next(self):
        r"""
        Returns False if and only if all polyominoes have been enumerated.

        OUTPUT:

        A boolean

        EXAMPLE::

            sage: pe = PolyominoesEnumerator(2)
            sage: pe.has_next()
            True
            sage: pe.next_obj()
            Polyomino: ['1', '1']
            sage: pe.next_obj()
            Polyomino: ['11']
            sage: pe.has_next()
            False
            sage: pe.next_obj()
            Traceback (most recent call last):
            ...
            StopIteration
        """
        return self.found

    cpdef int print_all(self):
        r"""
        TODO: add documentation
        """
        cdef int n = 0
        while self.has_next():
            print self.next_obj().ascii()
            n += 1
        return n

    cpdef int count(self):
        r"""
        TODO: add documentation
        """
        cdef int n = 0
        while self.has_next():
            self.next_obj()
            n += 1
        return n

