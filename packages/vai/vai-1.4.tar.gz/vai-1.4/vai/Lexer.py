import pygments
import pygments.lexers
from .SymbolLookupDb import SymbolLookupDb
from .models.TextDocument import CharMeta
import pygments.token
from pygments import lexers, util
import os

# Faster lookup than the one provided in lexers.get_lexer_for_filename.
# Any other attempt has been proved to take around 0.2 secs, which is
# unacceptable. We need the fastest lookup to start as soon as possible
EXTENSION_TO_LEXER = {
    ".py" : lexers.PythonLexer,
    ".rb" : lexers.RubyLexer,
    ".pl" : lexers.PerlLexer,
    ".tcl": lexers.TclLexer,
    ".lua": lexers.LuaLexer,
    ".as" : lexers.ActionScriptLexer,
    ".c"  : lexers.CLexer,
    ".h"  : lexers.CLexer,
    ".cpp" : lexers.CppLexer,
    ".hpp" : lexers.CppLexer,
    ".f"   : lexers.FortranLexer,
    ".f77" : lexers.FortranLexer,
    ".f90" : lexers.FortranLexer,
    ".sh"  : lexers.BashLexer,
    ".bat" : lexers.BatchLexer,
}

def _getLexerInstance(filename):
    """Get the lexer instance from the filename"""
    if filename is None:
        return lexers.TextLexer(stripnl=False, stripall=False)

    # Fast lookup first
    ext = os.path.splitext(filename)[1]
    cls = EXTENSION_TO_LEXER.get(ext)
    if cls is not None:
        return cls(stripnl=False, stripall=False)

    # Slow lookup for less common cases
    try:
        lexer = lexers.get_lexer_for_filename(filename, stripnl=False, stripall=False)
    except util.ClassNotFound:
        lexer = lexers.TextLexer(stripnl=False, stripall=False)

    return lexer


class Lexer:
    def __init__(self):
        self._document = None
        self._lexer = None

    def setModel(self, document):
        self._document = document
        filename = self._document.filename()
        self._lexer = _getLexerInstance(filename)
        self._document.contentChanged.connect(self._lexContents)
        self._lexContents()

    def _lexContents(self):
        if self._lexer is None:
            return

        tokens = self._lexer.get_tokens(self._document.documentText())
        current_line = 1
        current_col = 1
        SymbolLookupDb.clear()
        # Skip the space token

        for token in tokens:
            ttype, token_string = token
            if ttype in [pygments.token.Name, pygments.token.Name.Class, pygments.token.Name.Function]:
                SymbolLookupDb.add(token_string)

            token_lines = token_string.splitlines(True)
            for token_line in token_lines:
                meta = [ttype]*len(token_line)

                self._document.updateCharMeta((current_line, current_col), {CharMeta.LexerToken: meta})
                current_col += len(token_line)
                if token_line.endswith("\n"):
                    current_line += 1
                    current_col = 1

