"""Math utilities."""
import numpy as np


def set_sig_figs(
    num: float, n_sig_figs: int = 3, max_digits_to_display_nonscientific: int = 4
) -> str:
    r"""Format a number to a specified number of significant figures.

    Args:
        num: The number to be formatted.
        n_sig_figs: The number of significant figures in the output format. Defaults to :code:`3`.
        max_digits_to_display_nonscientific: The maximum number of digits that there can be to be
            displayed in a non-scientific format. Defaults to :code:`4`.

    Raises:
        ValueError: If the number of significant figure <= 0.

    Returns:
        A string representation of the formatted number to a specified number of significant
        figures.

    Examples:
        >>> set_sig_figs(1234.5678, n_sig_figs=3, max_digits_to_display_nonscientific=3)
        '$1.23 \\times 10^{3}$'
        >>> set_sig_figs(1234.5678, n_sig_figs=3, max_digits_to_display_nonscientific=4)
        '1230'
        >>> set_sig_figs(0.123456, n_sig_figs=4, max_digits_to_display_nonscientific=4)
        '$1.235 \\times 10^{-1}$'
        >>> set_sig_figs(0.123456, n_sig_figs=4, max_digits_to_display_nonscientific=5)
        '0.1235'
        >>> set_sig_figs(-0.987, n_sig_figs=1, max_digits_to_display_nonscientific=4)
        '-1'
        >>> set_sig_figs(149, n_sig_figs=2, max_digits_to_display_nonscientific=2)
        '$1.5 \\times 10^{2}$'
        >>> set_sig_figs(149, n_sig_figs=2, max_digits_to_display_nonscientific=3)
        '150'
        >>> set_sig_figs(150, n_sig_figs=3, max_digits_to_display_nonscientific=2)
        '$1.50 \\times 10^{2}$'
        >>> set_sig_figs(150, n_sig_figs=3, max_digits_to_display_nonscientific=3)
        '150'
    """
    if n_sig_figs < 1:
        raise ValueError(
            f"Number of significant figures (n_sig_figs) must be >= 1, received {n_sig_figs}."
        )
    num_str = f"{num:.{n_sig_figs-1}e}"
    num = float(num_str)
    coefficient, exponent = num_str.split("e")
    exponent = int(exponent)

    if exponent <= 0:
        additional_zeros = -exponent
    else:
        additional_zeros = exponent - n_sig_figs + 1
        additional_zeros = additional_zeros * (additional_zeros > 0)
    n_digits_to_display = n_sig_figs + additional_zeros

    if n_digits_to_display > max_digits_to_display_nonscientific and exponent != 0:
        return rf"${coefficient} \times 10^{{{exponent}}}$"
    decimal_places = n_sig_figs - exponent - 1
    decimal_places = decimal_places * (decimal_places > 0)
    return f"{num:.{decimal_places}f}"


def robust_divide(
    dividend: np.ndarray,
    divisor: np.ndarray,
    neg_inf: float = -np.inf,
    pos_inf: float = np.inf,
    zero_div_zero: float = np.nan,
) -> np.ndarray:
    """Divide a dividend by a divisor, accounting for the scenarios where the divisor is 0.

    Args:
        dividend: Numerator of the division.
        divisor: Denominator of the division.
        neg_inf: Value to return if the divisor is 0 but the dividend is negative. Defaults to
            :code:`-np.inf`.
        pos_inf: Value to return if the divisor is 0 but the dividend is positive. Defaults to
            :code:`np.inf`.
        zero_div_zero: Value to return if both the dividend and the divisor are 0. Defaults to
            :code:`np.nan`.

    Raises:
        ValueError: If the divdend and the divisor are of different shapes.

    Returns:
        Division robust to the divisor being 0.

    Examples:
        >>> robust_divide(np.array([1, -1, 1, 0, 0]), np.array([2, 0, 0, 1, 0]))
        array([ 0.5, -inf,  inf,  0. ,  nan])
        >>> robust_divide(
        ...     np.array([[1, -1, 1], [0, 0, 1]]),
        ...     np.array([[2, 0, 0], [1, 0, 4]]),
        ...     neg_inf=-1/5,
        ...     pos_inf=7,
        ...     zero_div_zero=42,
        ... )
        array([[ 0.5 , -0.2 ,  7.  ],
               [ 0.  , 42.  ,  0.25]])
    """
    if dividend.shape != divisor.shape:
        raise ValueError("robust_divide does not yet broadcast arrays of different shapes.")
    division = np.where(
        divisor != 0,
        np.divide(dividend, divisor, where=divisor != 0),
        np.where(dividend < 0, neg_inf, np.where(dividend > 0, pos_inf, zero_div_zero)),
    )
    return division


def around(x: float, n_decimals: int = 0) -> float:
    """Round a number to a given number of decimal places.

    Args:
        x: Number to round.
        n_decimals: Number of decimal places to round to. Negative numbers refer to places to the
            left of the decimal point. Defaults to 0.

    Returns:
        Rounded number.

    The purpose of this function is to fix `numpy's around <https://numpy.org/doc/stable/reference/g
    enerated/numpy.around.html>`_ 'round half to even' behaviour such as:

        >>> np.around(0.5)
        0.0
        >>> np.around(1.5)
        2.0

    This fix, which is more suited to rounding individual numbers rather than many for statistical
    purposes, has the following beahviours:

        >>> around(0.5)
        1.0
        >>> around(1.5)
        2.0
        >>> around(-0.15, 1)
        -0.1
        >>> around(10.34, 1)
        10.3
        >>> around(1378, -2)
        1400.0
        >>> around(499, -1)
        500.0
    """
    exponent = 10 ** n_decimals
    return np.floor(x * exponent + 0.5) / exponent
