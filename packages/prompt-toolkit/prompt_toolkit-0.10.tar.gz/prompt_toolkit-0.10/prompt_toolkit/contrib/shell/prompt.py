from prompt_toolkit.prompt import Prompt
from pygments.token import Token

from .rules import TokenStream


class ShellPrompt(Prompt):
    def get_tokens_after_input(self):
        def _():
            code = self.line.create_code_obj()
            parts, last_part_token = code._get_lex_result()

            # Don't show help when you're in the middle of typing a 'token'.
            # (Show after having typed the space, or at the start of the line.)
            if not last_part_token.unescaped_text:
                # Parse grammar
                stream = TokenStream(parts)
                trees = list(code.rule.parse(stream))

                # print (trees) ### debug

                if len(trees) > 1:
                    yield (Token.Placeholder.Bracket, '[')

                first = True

                for tree in trees:
                    if not first:
                        yield (Token.Placeholder.Separator, '|')
                    first = False

                    for t in tree.get_help_tokens():
                        yield t

                if len(trees) > 1:
                    yield (Token.Placeholder.Bracket, ']')
        return list(_())
