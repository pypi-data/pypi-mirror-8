"""
The `Code` object is responsible for parsing a document, received from the
`Line` class.  It's usually tokenized, using a Pygments lexer.
"""
from __future__ import unicode_literals
from pygments.token import Token

__all__ = (
    'Code',
    'CodeBase',
    'Completion',
    'ValidationError',
)


class Completion(object):
    def __init__(self, text, start_position=0, display=None, display_meta=''):
        """
        :param text: The new string that will be inserted into the document.
        :param start_position: Position relative to the cursor_position where the
                               new text will start. The text will be inserted
                               between the start_position and the original
                               cursor position.
        :param display: (optional string) If the completion has to be displayed
                       differently in the completion menu.
        :param display_meta: (Optional string) Meta information about the
                             completion, e.g. the path or source where it's
                             coming from.
        """
        self.text = text
        self.start_position = start_position
        self.display_meta = display_meta

        if display is None:
            self.display = text
        else:
            self.display = display

        assert self.start_position <= 0

    def __repr__(self):
        return 'Completion(text=%r, start_position=%r)' % (self.text, self.start_position)


class ValidationError(Exception):
    def __init__(self, line, column, message=''):
        self.line = line
        self.column = column
        self.message = message


class CodeBase(object):
    """
    Base class for Code implementations.

    The methods in here are methods that are expected to exist for the `Line`
    and `Renderer` classes.
    """
    def __init__(self, document):
        self.document = document

    @property
    def cursor_position(self):
        return self.document.cursor_position

    @property
    def text(self):
        return self.document.text

    def get_tokens(self):
        return [(Token, self.text)]

    def get_common_complete_suffix(self):
        """
        return one `Completion` instance or None.
        """
        # If there is one completion, return that.
        completions = list(self.get_completions())

        # Take only completions that don't change the text before the cursor.
        def doesnt_change_before_cursor(completion):
            end = completion.text[:-completion.start_position]
            return self.document.text_before_cursor.endswith(end)

        completions = [c for c in completions if doesnt_change_before_cursor(c)]

        # Return the common prefix.
        def get_suffix(completion):
            return completion.text[-completion.start_position:]

        return _commonprefix([get_suffix(c) for c in completions])

    def get_completions(self):
        """ Yield `Completion` instances. """
        if False:
            yield

    def validate(self):
        """
        Validate the input.
        If invalid, this should raise `self.validation_error`.
        """
        pass


class SimpleLRUCache(object):
    """
    Very simple LRU cache.

    :param maxsize: Maximum size of the cache. (Don't make it too big.)
    """
    def __init__(self, maxsize=8):
        self.maxsize = maxsize
        self._cache = [] # List of (key, value).

    def get(self, key, getter_func):
        """
        Get object from the cache.
        If not found, call `getter_func` to resolve it, and put that on the top
        of the cache instead.
        """
        # Look in cache first.
        for k, v in self._cache:
            if k == key:
                return v

        # Not found? Get it.
        value = getter_func()
        self._cache.append((key, value))

        if len(self._cache) > self.maxsize:
            self._cache = self._cache[-self.maxsize:]

        return value


class Code(CodeBase):
    """
    Representation of a code document.
    (Immutable class -- caches tokens)

    :attr document: :class:`~prompt_toolkit.line.Document`
    """
    #: The pygments Lexer class to use.
    lexer = None

    #: LRU cache for the lexer.
    #: Often, due to cursor movement and undo/redo operations, it happens that
    #: in a short time, the same document has to be lexed. This is a faily easy
    #: way to cache such an expensive operation.
    #: (Set to ``None`` to disable cache.)
    token_lru_cache = SimpleLRUCache(maxsize=8)

    def __init__(self, document):
        super(Code, self).__init__(document)
        self._tokens = None

    @property
    def _lexer(self):
        """ Return lexer instance. """
        if self.lexer:
            return self.lexer(
                stripnl=False,
                stripall=False,
                ensurenl=False)
        else:
            return None

    def _get_tokens(self):
        if self._lexer:
            def get():
                return list(self._lexer.get_tokens(self.text))

            if self.token_lru_cache:
                return self.token_lru_cache.get((self.lexer, self.text), get)
            else:
                return get()
        else:
            return [(Token, self.text)]

    def get_tokens(self):
        """
        Return the list of tokens for the input text.
        """
        # This implements caching on top of _get_tokens.
        if self._tokens is None:
            self._tokens = self._get_tokens()
        return self._tokens

    def get_tokens_before_cursor(self):
        """ Return the list of tokens that appear before the cursor. If the
        cursor is in the middle of a token, that token will be split.  """
        count = 0
        result = []
        for c in self.get_tokens():
            if count + len(c[1]) < self.cursor_position:
                result.append(c)
                count += len(c[1])
            elif count < self.cursor_position:
                result.append((c[0], c[1][:self.cursor_position - count]))
                break
            else:
                break
        return result


def _commonprefix(strings):
    # Similar to os.path.commonprefix
    if not strings:
        return ''

    else:
        s1 = min(strings)
        s2 = max(strings)

        for i, c in enumerate(s1):
            if c != s2[i]:
                return s1[:i]

        return s1
