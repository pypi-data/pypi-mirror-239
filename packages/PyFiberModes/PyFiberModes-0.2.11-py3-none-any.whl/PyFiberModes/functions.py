#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import factorial

# A[(k, m, i)]
derivatives_table = {
    # First derivative
    # Three points
    (1, 3, 0): (-3, 4, -1),
    (1, 3, 1): (-1, 0, 1),
    (1, 3, 2): (1, -4, 3),
    # Four points
    (1, 4, 0): (-11, 18, -9, 2),
    (1, 4, 1): (-2, -3, 6, -1),
    (1, 4, 2): (1, -6, 3, 2),
    (1, 4, 3): (-2, 9, -18, 11),
    # Five points
    (1, 5, 0): (-50, 96, -72, 32, -6),
    (1, 5, 1): (-6, -20, 36, -12, 2),
    (1, 5, 2): (2, -16, 0, 16, -2),
    (1, 5, 3): (-2, 12, -36, 20, 6),
    (1, 5, 4): (6, -32, 72, -96, 50),
    # Six points
    (1, 6, 0): (-274, 600, -600, 400, -150, 24),
    (1, 6, 1): (-24, -130, 240, -120, 40, -6),
    (1, 6, 2): (6, -60, -40, 120, -30, 4),
    (1, 6, 3): (-4, 30, -120, 40, 60, -6),
    (1, 6, 4): (6, -40, 120, -240, 130, 24),
    (1, 6, 5): (-24, 150, -400, 600, -600, 274),

    # Second derivative
    # Three points
    (2, 3, 0): (1, -2, 1),
    (2, 3, 1): (1, -2, 1),
    (2, 3, 2): (1, -2, 1),

    # Four points
    (2, 4, 0): (6, -15, 12, -3),
    (2, 4, 1): (3, -6, 3, 0),
    (2, 4, 2): (0, 3, -6, 3),
    (2, 4, 3): (-3, 12, -15, 6),

    # Five points
    (2, 5, 0): (35, -104, 114, -56, 11),
    (2, 5, 1): (11, -20, 6, 4, -1),
    (2, 5, 2): (-1, 16, -30, 16, -1),
    (2, 5, 3): (-1, 4, 6, -20, 11),
    (2, 5, 4): (11, -56, 114, -104, 35),

    # Six points
    (2, 6, 0): (225, -770, 1070, -780, 305, -50),
    (2, 6, 1): (50, -75, -20, 70, -30, 5),
    (2, 6, 2): (-5, 80, -150, 80, -5, 0),
    (2, 6, 3): (0, -5, 80, -150, 80, -5),
    (2, 6, 4): (5, -30, 70, -20, -75, 50),
    (2, 6, 5): (-50, 305, -780, 1070, -770, 225),

    # Third derivative
    # Four points
    (3, 4, 0): (-1, 3, -3, 1),
    (3, 4, 1): (-1, 3, -3, 1),
    (3, 4, 2): (-1, 3, -3, 1),
    (3, 4, 3): (-1, 3, -3, 1),

    # Five points
    (3, 5, 0): (-10, 36, -48, 28, -6),
    (3, 5, 1): (-6, 20, -24, 12, -2),
    (3, 5, 2): (-2, 4, 0, -4, 2),
    (3, 5, 3): (2, -12, 24, -20, 6),
    (3, 5, 4): (6, -28, 48, -36, 10),

    # Six points
    (3, 6, 0): (-85, 355, -590, 490, -205, 35),
    (3, 6, 1): (-35, 125, -170, 110, -35, 5),
    (3, 6, 2): (-5, -5, 50, -70, 35, -5),
    (3, 6, 3): (5, -35, 70, -50, 5, 5),
    (3, 6, 4): (-5, 35, -110, 170, -125, 35),
    (3, 6, 5): (-35, 205, -490, 590, -355, 85),

    # Fourth derivative
    # Five points
    (4, 5, 0): (1, -4, 6, -4, 1),
    (4, 5, 1): (1, -4, 6, -4, 1),
    (4, 5, 2): (1, -4, 6, -4, 1),
    (4, 5, 3): (1, -4, 6, -4, 1),
    (4, 5, 4): (1, -4, 6, -4, 1),

    # Six points
    (4, 6, 0): (15, -70, 130, -120, 55, -10),
    (4, 6, 1): (10, -45, 80, -70, 30, -5),
    (4, 6, 2): (5, -20, 30, -20, 5, 0),
    (4, 6, 3): (0, 5, -20, 30, -20, 5),
    (4, 6, 4): (-5, 30, -70, 80, -45, 10),
    (4, 6, 5): (-10, 55, -120, 130, -70, 15),

    # Fifth derivative
    # Six points
    (5, 6, 0): (-1, 5, -10, 10, -5, 1),
    (5, 6, 1): (-1, 5, -10, 10, -5, 1),
    (5, 6, 2): (-1, 5, -10, 10, -5, 1),
    (5, 6, 3): (-1, 5, -10, 10, -5, 1),
    (5, 6, 4): (-1, 5, -10, 10, -5, 1),
    (5, 6, 5): (-1, 5, -10, 10, -5, 1),
}


def get_derivative(function, x: float, order: int, n_point: int, central_point: int, delta: float, function_args: tuple) -> float:
    """
    Returns the derivative a the given function

    :param      function:       The function
    :type       function:       function
    :param      x:              parameter to derive
    :type       x:              float
    :param      order:          Differentiation order (1 to 5)
    :type       order:          int
    :param      n_point:        Number of points (3 to 6)
    :type       n_point:        int
    :param      central_point:  Central point (0 to m-1)
    :type       central_point:  int
    :param      delta:          Distance between points
    :type       delta:          float
    :param      args:           The arguments
    :type       args:           list

    :returns:   The value of the derivative
    :rtype:     float
    """

    prefactor = factorial(order) / (factorial(n_point - 1) * delta**order)

    evaluation = [
        derivatives_table[(order, n_point, central_point)][i] * function(x + (i - central_point) * delta, *function_args) for i in range(n_point)
    ]

    return prefactor * sum(evaluation)
