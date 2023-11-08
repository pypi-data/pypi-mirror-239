# This file is used to store some CONSTANTS and minor other things

import warnings

REJECTION = "Reject H₀"
ACCEPTATION = "Fail to reject H₀"


def warning_plot():
    def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
        return "%s:%s: %s: %s\n" % (filename, lineno, category.__name__, message)

    warnings.formatwarning = warning_on_one_line

    warnings.warn(
        "This function is experimental and its behavior may not be ideal.", stacklevel=3
    )
