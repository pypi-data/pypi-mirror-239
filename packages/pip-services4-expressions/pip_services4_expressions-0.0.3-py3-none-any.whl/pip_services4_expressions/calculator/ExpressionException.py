# -*- coding: utf-8 -*-
from typing import Optional

from pip_services4_commons.errors import BadRequestException


class ExpressionException(BadRequestException):
    """
    Exception that can be thrown by Expression Calculator.
    """

    def __init__(self, trace_id: Optional[str] = None, code: Optional[str] = None, message: Optional[str] = None,
                 line: int = 0, column: int = 0):
        if line != 0 or column != 0:
            message = f"{message} at line {line} and column {column}"
        super(ExpressionException, self).__init__(trace_id, code, message)
