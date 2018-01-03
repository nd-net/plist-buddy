from funcparserlib.lexer import make_tokenizer, Token, LexerError
from re import VERBOSE

escaped = r"""
    \\                                  # Escape
      ((?P<standard>["\\/bfnrt\$])      # Standard escapes
    | (u(?P<unicode>[0-9A-Fa-f]{4})))   # uXXXX
    """
unescaped = r"""
    [^"\\]                              # Unescaped: avoid ["\\]
    """,
}

def tokenizer():
    specs = [
        ("Comment", (r"#.*$", )),
        ("Space", (r"\s+",)),
        ("String", (r'"({} | {})*"'.format(unescaped, escaped), VERBOSE)),
        ("Integer", (r"""
            [+-]?
            [0-9]([0-9_]*[0-9])?(?!\.)
            """, VERBOSE)),
        ("PrefixedInteger", (r"""
            [+-]?
            (0o|0O|0o|0O|0x|0X)
            [0-9a-fA-F]([0-9a-fA-F_]*[0-9a-fA-F])?
            """, VERBOSE)),
        ("Real", (r"""
            [+-]?
            (
              [0-9][0-9_]*\.?[0-9_]*
            |
              \.[0-9][0-9_]*
            )
            [Ee][+-]?[0-9_]+
            """, VERBOSE)),
        ("Real", (r"""
            [+-]?
            (
              [0-9][0-9_]*\.?[0-9_]*
            |
              \.[0-9][0-9_]*
            )
            """, VERBOSE)),
        ("Name", (r"[A-Za-z_][A-Za-z_0-9]*",)),
        ("PathSeparator", (r":",)),
    ]
    return make_tokenizer(specs)
    