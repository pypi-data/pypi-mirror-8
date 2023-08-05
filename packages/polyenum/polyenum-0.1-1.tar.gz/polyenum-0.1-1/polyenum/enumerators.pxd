# coding=utf-8
#------------------------------------------------------------------
# File: enumeration.pyx    Author(s): Alexandre Blondin Massé
#                                     Simon Désaulniers
# Date: 2014-01-08
#------------------------------------------------------------------
# The code for enumeration of polyominoes
#------------------------------------------------------------------

# distutils: language = c++

from data_structures cimport Polyomino

# Enumerators

cdef class Enumerator:
    cdef str what_looking_for
    cdef int area
    cdef int width
    cdef int height
    cdef Polyomino polyomino
    cdef bint found
    cpdef get_height(self)
    cpdef get_width(self)
    cpdef get_area(self)
    cpdef set_area(self, int area)
    cpdef set_width(self, int width)
    cpdef set_height(self, int height)
    cpdef bint has_next(self)
    cpdef int count(self)
    cpdef str lookingFor(self)

cdef class InscribedPolyominoesEnumerator(Enumerator):
    cdef object partials
    cdef bint allow_kiss
    cdef bint verbose
    cpdef _update_to_next(self)
    cpdef next_obj(self)
    cpdef bint has_next(self)
    cpdef int print_all(self)
    cpdef int count(self)

cdef class InscribedTreeEnumerator(InscribedPolyominoesEnumerator):
    cdef int leaves
    cpdef _update_to_next(self)
    cpdef next_obj(self)
    cpdef bint has_next(self)

cdef class InscribedSnakeEnumerator(InscribedTreeEnumerator):
    pass

cdef class InscribedNorthSnakeEnumerator(InscribedSnakeEnumerator):
    pass

cdef class PolyominoesEnumerator(Enumerator):
    cdef InscribedPolyominoesEnumerator enumerator
    cdef bint return_transposed
    cdef int current_height, current_width
    cdef bint allow_kiss
    cdef bint verbose
    cpdef _update_to_next(self)
    cpdef Polyomino next_obj(self)
    cpdef bint has_next(self)
    cpdef int print_all(self)
    cpdef int count(self)
