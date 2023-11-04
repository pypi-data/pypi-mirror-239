# -*- coding: utf-8 -*-

from abc import ABC

from pip_services4_expressions.tokenizers.ITokenizerState import ITokenizerState


class ICommentState(ITokenizerState, ABC):
    """
    Defines an interface for tokenizer state that processes comments.
    """
