""" function.py

Module containing classes representing piece-wise constant and piece-wise
linear functions.

Copyright 2014, Mario Mulansky <mario.mulansky@gmx.net>

Distributed under the BSD License

"""
from __future__ import print_function

import numpy as np
import collections


##############################################################
# PieceWiseConstFunc
##############################################################
class PieceWiseConstFunc(object):
    """ A class representing a piece-wise constant function. """

    def __init__(self, x, y):
        """ Constructs the piece-wise const function.

        :param x: array of length N+1 defining the edges of the intervals of
                  the pwc function.
        :param y: array of length N defining the function values at the
                  intervals.
        """
        # convert parameters to arrays, also ensures copying
        self.x = np.array(x)
        self.y = np.array(y)

    def copy(self):
        """ Returns a copy of itself

        :rtype: :class:`PieceWiseConstFunc`
        """
        return PieceWiseConstFunc(self.x, self.y)

    def almost_equal(self, other, decimal=14):
        """ Checks if the function is equal to another function up to `decimal`
        precision.

        :param other: another :class:`PieceWiseConstFunc`
        :returns: True if the two functions are equal up to `decimal` decimals,
                  False otherwise
        :rtype: bool
        """
        eps = 10.0**(-decimal)
        return np.allclose(self.x, other.x, atol=eps, rtol=0.0) and \
            np.allclose(self.y, other.y, atol=eps, rtol=0.0)

    def get_plottable_data(self):
        """ Returns two arrays containing x- and y-coordinates for immeditate
        plotting of the piece-wise function.

        :returns: (x_plot, y_plot) containing plottable data
        :rtype: pair of np.array

        Example::

            x, y = f.get_plottable_data()
            plt.plot(x, y, '-o', label="Piece-wise const function")
        """

        x_plot = np.empty(2*len(self.x)-2)
        x_plot[0] = self.x[0]
        x_plot[1::2] = self.x[1:]
        x_plot[2::2] = self.x[1:-1]
        y_plot = np.empty(2*len(self.y))
        y_plot[::2] = self.y
        y_plot[1::2] = self.y

        return x_plot, y_plot

    def integral(self, interval=None):
        """ Returns the integral over the given interval.

        :param interval: integration interval given as a pair of floats, if
                         None the integral over the whole function is computed.
        :type interval: Pair of floats or None.
        :returns: the integral
        :rtype: float
        """
        if interval is None:
            # no interval given, integrate over the whole spike train
            a = np.sum((self.x[1:]-self.x[:-1]) * self.y)
        else:
            # find the indices corresponding to the interval
            start_ind = np.searchsorted(self.x, interval[0], side='right')
            end_ind = np.searchsorted(self.x, interval[1], side='left')-1
            assert start_ind > 0 and end_ind < len(self.x), \
                "Invalid averaging interval"
            # first the contribution from between the indices
            a = np.sum((self.x[start_ind+1:end_ind+1] -
                        self.x[start_ind:end_ind]) *
                       self.y[start_ind:end_ind])
            # correction from start to first index
            a += (self.x[start_ind]-interval[0]) * self.y[start_ind-1]
            # correction from last index to end
            a += (interval[1]-self.x[end_ind]) * self.y[end_ind]
        return a

    def avrg(self, interval=None):
        """ Computes the average of the piece-wise const function:
        :math:`a = 1/T int_0^T f(x) dx` where T is the length of the interval.

        :param interval: averaging interval given as a pair of floats, a
                         sequence of pairs for averaging multiple intervals, or
                         None, if None the average over the whole function is
                         computed.
        :type interval: Pair, sequence of pairs, or None.
        :returns: the average a.
        :rtype: float
        """
        if interval is None:
            # no interval given, average over the whole spike train
            return self.integral() / (self.x[-1]-self.x[0])

        # check if interval is as sequence
        assert isinstance(interval, collections.Sequence), \
            "Invalid value for `interval`. None, Sequence or Tuple expected."
        # check if interval is a sequence of intervals
        if not isinstance(interval[0], collections.Sequence):
            # just one interval
            a = self.integral(interval) / (interval[1]-interval[0])
        else:
            # several intervals
            a = 0.0
            int_length = 0.0
            for ival in interval:
                a += self.integral(ival)
                int_length += ival[1] - ival[0]
            a /= int_length
        return a

    def add(self, f):
        """ Adds another PieceWiseConst function to this function.
        Note: only functions defined on the same interval can be summed.

        :param f: :class:`PieceWiseConstFunc` function to be added.
        :rtype: None
        """
        assert self.x[0] == f.x[0], "The functions have different intervals"
        assert self.x[-1] == f.x[-1], "The functions have different intervals"

        # cython version
        try:
            from cython_add import add_piece_wise_const_cython as \
                add_piece_wise_const_impl
        except ImportError:
            print("Warning: add_piece_wise_const_cython not found. Make sure \
that PySpike is installed by running\n 'python setup.py build_ext --inplace'! \
\n Falling back to slow python backend.")
            # use python backend
            from python_backend import add_piece_wise_const_python as \
                add_piece_wise_const_impl

        self.x, self.y = add_piece_wise_const_impl(self.x, self.y, f.x, f.y)

    def mul_scalar(self, fac):
        """ Multiplies the function with a scalar value

        :param fac: Value to multiply
        :type fac: double
        :rtype: None
        """
        self.y *= fac


##############################################################
# PieceWiseLinFunc
##############################################################
class PieceWiseLinFunc:
    """ A class representing a piece-wise linear function. """

    def __init__(self, x, y1, y2):
        """ Constructs the piece-wise linear function.

        :param x: array of length N+1 defining the edges of the intervals of
                  the pwc function.
        :param y1: array of length N defining the function values at the left
                  of the intervals.
        :param y2: array of length N defining the function values at the right
                  of the intervals.
        """
        # convert to array, which also ensures copying
        self.x = np.array(x)
        self.y1 = np.array(y1)
        self.y2 = np.array(y2)

    def copy(self):
        """ Returns a copy of itself

        :rtype: :class:`PieceWiseLinFunc`
        """
        return PieceWiseLinFunc(self.x, self.y1, self.y2)

    def almost_equal(self, other, decimal=14):
        """ Checks if the function is equal to another function up to `decimal`
        precision.

        :param other: another :class:`PieceWiseLinFunc`
        :returns: True if the two functions are equal up to `decimal` decimals,
                  False otherwise
        :rtype: bool
        """
        eps = 10.0**(-decimal)
        return np.allclose(self.x, other.x, atol=eps, rtol=0.0) and \
            np.allclose(self.y1, other.y1, atol=eps, rtol=0.0) and \
            np.allclose(self.y2, other.y2, atol=eps, rtol=0.0)

    def get_plottable_data(self):
        """ Returns two arrays containing x- and y-coordinates for immeditate
        plotting of the piece-wise function.

        :returns: (x_plot, y_plot) containing plottable data
        :rtype: pair of np.array

        Example::

            x, y = f.get_plottable_data()
            plt.plot(x, y, '-o', label="Piece-wise const function")
        """
        x_plot = np.empty(2*len(self.x)-2)
        x_plot[0] = self.x[0]
        x_plot[1::2] = self.x[1:]
        x_plot[2::2] = self.x[1:-1]
        y_plot = np.empty_like(x_plot)
        y_plot[0::2] = self.y1
        y_plot[1::2] = self.y2
        return x_plot, y_plot

    def integral(self, interval=None):
        """ Returns the integral over the given interval.

        :param interval: integration interval given as a pair of floats, if
                         None the integral over the whole function is computed.
        :type interval: Pair of floats or None.
        :returns: the integral
        :rtype: float
        """

        def intermediate_value(x0, x1, y0, y1, x):
            """ computes the intermediate value of a linear function """
            return y0 + (y1-y0)*(x-x0)/(x1-x0)

        if interval is None:
            # no interval given, integrate over the whole spike train
            integral = np.sum((self.x[1:]-self.x[:-1]) * 0.5*(self.y1+self.y2))
        else:
            # find the indices corresponding to the interval
            start_ind = np.searchsorted(self.x, interval[0], side='right')
            end_ind = np.searchsorted(self.x, interval[1], side='left')-1
            assert start_ind > 0 and end_ind < len(self.x), \
                "Invalid averaging interval"
            # first the contribution from between the indices
            integral = np.sum((self.x[start_ind+1:end_ind+1] -
                               self.x[start_ind:end_ind]) *
                              0.5*(self.y1[start_ind:end_ind] +
                                   self.y2[start_ind:end_ind]))
            # correction from start to first index
            integral += (self.x[start_ind]-interval[0]) * 0.5 * \
                        (self.y2[start_ind-1] +
                         intermediate_value(self.x[start_ind-1],
                                            self.x[start_ind],
                                            self.y1[start_ind-1],
                                            self.y2[start_ind-1],
                                            interval[0]
                                            ))
            # correction from last index to end
            integral += (interval[1]-self.x[end_ind]) * 0.5 * \
                        (self.y1[end_ind] +
                         intermediate_value(self.x[end_ind], self.x[end_ind+1],
                                            self.y1[end_ind], self.y2[end_ind],
                                            interval[1]
                                            ))
        return integral

    def avrg(self, interval=None):
        """ Computes the average of the piece-wise linear function:
        :math:`a = 1/T int_0^T f(x) dx` where T is the length of the interval.

        :param interval: averaging interval given as a pair of floats, a
                         sequence of pairs for averaging multiple intervals, or
                         None, if None the average over the whole function is
                         computed.
        :type interval: Pair, sequence of pairs, or None.
        :returns: the average a.
        :rtype: float

        """

        if interval is None:
            # no interval given, average over the whole spike train
            return self.integral() / (self.x[-1]-self.x[0])

        # check if interval is as sequence
        assert isinstance(interval, collections.Sequence), \
            "Invalid value for `interval`. None, Sequence or Tuple expected."
        # check if interval is a sequence of intervals
        if not isinstance(interval[0], collections.Sequence):
            # just one interval
            a = self.integral(interval) / (interval[1]-interval[0])
        else:
            # several intervals
            a = 0.0
            int_length = 0.0
            for ival in interval:
                a += self.integral(ival)
                int_length += ival[1] - ival[0]
            a /= int_length
        return a

    def add(self, f):
        """ Adds another PieceWiseLin function to this function.
        Note: only functions defined on the same interval can be summed.

        :param f: :class:`PieceWiseLinFunc` function to be added.
        :rtype: None
        """
        assert self.x[0] == f.x[0], "The functions have different intervals"
        assert self.x[-1] == f.x[-1], "The functions have different intervals"

        # python implementation
        # from python_backend import add_piece_wise_lin_python
        # self.x, self.y1, self.y2 = add_piece_wise_lin_python(
        #     self.x, self.y1, self.y2, f.x, f.y1, f.y2)

        # cython version
        try:
            from cython_add import add_piece_wise_lin_cython as \
                add_piece_wise_lin_impl
        except ImportError:
            print("Warning: add_piece_wise_lin_cython not found. Make sure \
that PySpike is installed by running\n 'python setup.py build_ext --inplace'! \
\n Falling back to slow python backend.")
            # use python backend
            from python_backend import add_piece_wise_lin_python as \
                add_piece_wise_lin_impl

        self.x, self.y1, self.y2 = add_piece_wise_lin_impl(
            self.x, self.y1, self.y2, f.x, f.y1, f.y2)

    def mul_scalar(self, fac):
        """ Multiplies the function with a scalar value

        :param fac: Value to multiply
        :type fac: double
        :rtype: None
        """
        self.y1 *= fac
        self.y2 *= fac


def average_profile(profiles):
    """ Computes the average profile from the given ISI- or SPIKE-profiles.

    :param profiles: list of :class:`PieceWiseConstFunc` or
                     :class:`PieceWiseLinFunc` representing ISI- or
                     SPIKE-profiles to be averaged.
    :returns: the averages profile :math:`<S_{isi}>` or :math:`<S_{spike}>`.
    :rtype: :class:`PieceWiseConstFunc` or :class:`PieceWiseLinFunc`
    """
    assert len(profiles) > 1

    avrg_profile = profiles[0].copy()
    for i in xrange(1, len(profiles)):
        avrg_profile.add(profiles[i])
    avrg_profile.mul_scalar(1.0/len(profiles))  # normalize

    return avrg_profile
