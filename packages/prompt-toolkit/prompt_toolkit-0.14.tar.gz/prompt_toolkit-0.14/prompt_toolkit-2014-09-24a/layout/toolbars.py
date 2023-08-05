from __future__ import unicode_literals

from pygments.token import Token
from ..renderer import Point
from ..enums import InputMode, IncrementalSearchDirection
from .utils import TokenList

__all__ = (
    'Toolbar',
    'TextToolbar',
    'ArgToolbar',
    'SearchToolbar',
    'CompletionToolbar',
)


class Toolbar(object):
    def __init__(self, token=None):
        self.token = token or Token.Layout.Toolbar

    def write(self, cli, screen):
        width = screen.size.columns
        tokens = self.get_tokens(cli, width)
        tokens = self._adjust_width(tokens, screen.size.columns)
        screen.write_highlighted(tokens)

    def is_visible(self, cli, screen):
        return True # TODO: not visible if abort_or_accept!!

    def _adjust_width(self, tokens, columns):
        """
        Make sure that this list of tokens fit the amount of columns.
        Trim or extend with `toolbar_token`.
        """
        result = TokenList(tokens)

        if len(result) > columns:
            # Trim toolbar
            result = result[:columns - 3]
            result.append((self.toolbar_token, ' > '))
        else:
            # Extend toolbar until the page width.
            result.append((self.token, ' ' * (columns - len(result))))

        return result

    def get_tokens(self, cli, width):
        pass


class TextToolbar(Toolbar):
    def __init__(self, text='', token=None):
        super(TextToolbar, self).__init__(token=token)
        self.text = text

    def get_tokens(self, cli, width):
        return [
            (self.token, self.text),
        ]


class ArgToolbar(Toolbar):
    """
    A simple toolbar which shows the repeat 'arg'.
    """
    def __init__(self, token=None):
        token = token or Token.Layout.Toolbar.Arg
        super(ArgToolbar, self).__init__(token=token)

    def is_visible(self, cli, screen):
        return cli.input_processor.arg is not None

    def get_tokens(self, cli, width):
        return [
            (Token.Layout.Toolbar.Arg, 'Repeat: '),
            (Token.Layout.Toolbar.Arg.Text, str(cli.input_processor.arg)),
        ]


class SearchToolbar(Toolbar):
    def is_visible(self, cli, screen):
        return cli.input_processor.input_mode in (InputMode.INCREMENTAL_SEARCH, InputMode.VI_SEARCH)

    def get_tokens(self, cli, width):
        """
        Tokens for the vi-search prompt.
        """
        line = cli.lines['search']
        vi = cli.input_processor.input_mode == InputMode.VI_SEARCH

        if cli.line.isearch_state.isearch_direction == IncrementalSearchDirection.BACKWARD:
            prefix = '?' if vi else 'I-search backward: '
        else:
            prefix = '/' if vi else 'I-search: '

        return [
            (Token.Prompt.ViSearch.Prefix, prefix),
            (Token.Prompt.ViSearch.Text, line.text),
        ]

    def write(self, cli, screen):
        # Write output.
        super(SearchToolbar, self).write(cli, screen)

        #  Set cursor position.
        line = cli.lines['search']
        screen.cursor_position = Point(screen._y, line.cursor_position)


class CompletionToolbar(Toolbar):
    """
    Helper for drawing the completion menu 'wildmenu'-style.
    (Similar to Vim's wildmenu.)
    """
    def __init__(self, token=None):
        token = token or Token.CompletionToolbar
        super(CompletionToolbar, self).__init__(token=token)

    def is_visible(self, cli, screen):
        return bool(cli.line.complete_state) and len(cli.line.complete_state.current_completions) >= 1

    def get_tokens(self, cli, width):
        """
        Write the menu to the screen object.
        """
        complete_state = cli.line.complete_state
        completions = complete_state.current_completions
        index = complete_state.complete_index  # Can be None!

        # Don't draw the menu if there is just one completion.
        if len(completions) <= 1:
            return []

        # Width of the completions without the left/right arrows in the margins.
        content_width = width - 6

        # Booleans indicating whether we stripped from the left/right
        cut_left = False
        cut_right = False

        # Create Menu content.
        tokens = TokenList()

        for i, c in enumerate(completions):
            # When there is no more place for the next completion
            if len(tokens) + len(c.display) >= content_width:
                # If the current one was not yet displayed, page to the next sequence.
                if i <= (index or 0):
                    tokens = TokenList()
                    cut_left = True
                # If the current one is visible, stop here.
                else:
                    cut_right = True
                    break

            tokens.append((self.token.Completion.Current if i == index else self.token.Completion, c.display))
            tokens.append((self.token, ' '))

        # Extend/strip until the content width.
        tokens.append((self.token, ' ' * (content_width - len(tokens))))
        tokens = tokens[:content_width]

        # Return tokens
        return TokenList([
            (self.token, ' '),
            (self.token.Arrow, '<' if cut_left else ' '),
            (self.token, ' '),
        ]) + tokens + TokenList([
            (self.token, ' '),
            (self.token.Arrow, '>' if cut_right else ' '),
            (self.token, ' '),
        ])
