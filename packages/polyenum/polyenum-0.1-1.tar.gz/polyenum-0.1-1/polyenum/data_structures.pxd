# coding=utf-8
#------------------------------------------------------------------
# File: data_structures.pxd    Author(s): Alexandre Blondin Massé
#                                         Simon Désaulniers
# Date: 2014-06-05
#------------------------------------------------------------------
# Data structures for polyomino enumeration
#------------------------------------------------------------------

from libc.stdlib cimport malloc, free

# Type declarations

cdef struct Site: # Ordered pair for the kink
    int lower     # The lower cell in the kink
    int upper     # The upper cell in the kink

# Inline functions

cdef inline int three_quarters(int w, int h):
    if w >= 2 and h >= 2:
        return 3 * (w * h + w % 2 + h % 2) / 4
    elif w == 1:
        return h
    elif h == 1:
        return w
    else:
        return 0

# Data structures

cdef class Polyomino:
    cdef bint** matrix
    cdef int height, width
    cpdef int degree(self, int i, int j)
    cpdef int number_of_leaves(self)
    cpdef Polyomino transpose(self)

cdef class PartialPolyomino:
    cdef int** matrix
    cdef int width, height, current_height, current_width, num_cells
    cdef bint touched_left, touched_top, touched_bottom, allow_kiss
    cpdef PartialPolyomino clone(self)
    cpdef int get_cell(self, int i, int j)
    cpdef bint is_occupied(self, int i, int j)
    cpdef int _get_boundary_cell(self, int i)
    cpdef _set_boundary_cell(self, int i, int value)
    cpdef bint is_boundary_connected(self)
    cpdef int get_upper_cell(self)
    cpdef int get_lower_cell(self)
    cpdef _set_upper_cell(self, int value)
    cpdef _set_lower_cell(self, int value)
    cpdef int get_cell_degree(self, int i, int j)
    cpdef bint is_polyomino(self)
    cpdef Polyomino to_polyomino(self, bint check)
    cpdef int bound_top_border_touching(self)
    cpdef int bound_bottom_border_touching(self)
    cpdef int bound_right_border_touching(self)
    cpdef int bound_make_connected(self)
    cpdef int min_area(self)
    cpdef int max_area(self)
    cpdef bint is_extendable(self)
    cpdef bint creates_kiss(self, bint occupied)
    cpdef PartialPolyomino extend(self, bint occupied)
    cpdef _bar_update_upward(self)
    cpdef _bar_update_downward(self)
    cpdef _hat_update_upward(self)
    cpdef _hat_update_downward(self)
    cpdef _relabel(self, int lower, int upper, bint occupied)
    cpdef Site _transition(self, int lower, int upper, bint occupied)

cdef class PartialTree(PartialPolyomino):
    cdef public int leaves
    cpdef Site _transition(self, int lower, int upper, bint occupied)

cdef class PartialSnake(PartialTree):
    pass

cdef class PartialNorthSnake(PartialSnake):
    cdef public object has_pillar
