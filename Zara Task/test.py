import ply.lex as lex

class Symbol:
    def __init__(self, name, symbol_type, value=None):
        self.name = name
        self.type = symbol_type
        self.value = value

    def __repr__(self):
        return f"Symbol(name={self.name}, type={self.type}, value={self.value})"


class SymbolTable:
    def __init__(self):
        self.global_scope = {}
        self.local_scopes = []

    def enter_scope(self, scope_type):
        """Enter a new local scope."""
        self.local_scopes.append({})
        print(f"Entering new scope: {scope_type}")

    def exit_scope(self):
        """Exit the current local scope."""
        if self.local_scopes:
            self.local_scopes.pop()
            print("Exiting current scope.")

    def add_symbol(self, name, symbol_type, value=None, scope='global'):
        """Add a symbol to the symbol table."""
        symbol = Symbol(name, symbol_type, value)
        if scope == 'global':
            self.global_scope[name] = symbol
            print(f"Added global symbol: {name}")
        else:
            if self.local_scopes:
                self.local_scopes[-1][name] = symbol
                print(f"Added local symbol: {name}")

    def get_symbol(self, name):
        """Retrieve a symbol by name."""
        # Check local scopes first
        for scope in reversed(self.local_scopes):
            if name in scope:
                return scope[name]
        # Check global scope
        return self.global_scope.get(name, f"Symbol '{name}' not found.")

    def display_table(self):
        """Display symbols in the global and local scopes."""
        print("\nSymbol Table:")

        # Display global symbols
        for name, symbol in self.global_scope.items():
            print(f"Name: {symbol.name}, Type: {symbol.type}, Value: {symbol.value}")

        # Display local symbols
        for idx, scope in enumerate(self.local_scopes):
            print(f"\nLocal Scope {idx + 1}:")
            for name, symbol in scope.items():
                print(f"Name: {symbol.name}, Type: {symbol.type}, Value: {symbol.value}")



class ZaraLexer:
    tokens = (
        'KEYWORD', 'FLOAT', 'CONSTANT', 'IDENTIFIER', 'PUNCTUATION',
        'STRING_LITERAL', 'OPERATOR'
    )

    reserved = {
        'func': 'KEYWORD', 'int': 'KEYWORD', 'float': 'KEYWORD',
        'string': 'KEYWORD', 'arr': 'KEYWORD', 'stack': 'KEYWORD',
        'while': 'KEYWORD', 'if': 'KEYWORD', 'else': 'KEYWORD',
        'else-if': 'KEYWORD', 'do': 'KEYWORD', 'for': 'KEYWORD',
        'return': 'KEYWORD', 'continue': 'KEYWORD', 'break': 'KEYWORD',
        'in': 'KEYWORD'
    }

    t_ignore = ' \t\n'  # Ignore spaces, tabs, and newlines

    def t_COMMENT(self, t):
        r'\#.*'
        pass

    def t_MULTILINE_COMMENT(self, t):
        r'\*\*([^*]|\*[^*])*\*\*'
        pass

    def t_KEYWORD(self, t):
        r'func|int|float|string|arr|stack|while|if|else|else-if|do|for|return|continue|break|in'
        return t

    def t_FLOAT(self, t):
        r'[+-]?[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?'
        return t

    def t_CONSTANT(self, t):
        r'[+-]?[0-9]+'
        return t

    def t_IDENTIFIER(self, t):
        r'[A-Za-z][A-Za-z0-9]*'
        if t.value in self.reserved:
            t.type = self.reserved[t.value]
        return t

    def t_PUNCTUATION(self, t):
        r'[{},;()\[\]]'
        return t

    def t_STRING_LITERAL(self, t):
        r'"([^"\\\n]|\\[btnrf"\\])*"'
        return t

    def t_OPERATOR(self, t):
        r'\+|\-|\*|\/|>|<|&&|==|>=|<=|=|!|\|\|'
        return t

    def t_error(self, t):
        print(f"Illegal character {t.value[0]}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()


def main():
    # Instantiate the symbol table
    symbol_table = SymbolTable()

    # Initialize the lexer
    zara_lexer = ZaraLexer()
    zara_lexer.build()

    # Sample Zara code
    zara_code = '''
    func factorial(int n) {
        if (n > 1) {
            return n * factorial(n - 1);
        } else {
            return 1;
        }
    }
    '''

    # Run lexer on the Zara code
    print("\nRunning lexical analysis...")
    zara_lexer.input(zara_code)

    # Add symbols to the symbol table based on the tokens
    while True:
        tok = zara_lexer.token()
        if not tok:
            break
        print(f"{tok.type}: {tok.value}")
        # Add identifiers to the symbol table
        if tok.type == 'IDENTIFIER':
            symbol_table.add_symbol(tok.value, 'identifier', None, 'global')
        elif tok.type == 'KEYWORD':
            if tok.value in ['func', 'int', 'float', 'string', 'arr', 'stack']:
                symbol_table.add_symbol(tok.value, 'type', None, 'global')

    # Test adding additional symbols to the symbol table
    symbol_table.add_symbol("factorial", "func", None, "global")
    symbol_table.add_symbol("n", "int", None, "global")

    symbol_table.enter_scope("function")
    symbol_table.add_symbol("result", "int", None, "local")

    # Display symbols after adding
    print("\nSymbol Table after adding symbols:")
    symbol_table.display_table()

    # Exiting scope
    symbol_table.exit_scope()

    # Display symbols after exiting scope
    print("\nSymbol Table after exiting scope:")
    symbol_table.display_table()


# Execute the main function
if __name__ == "__main__":
    main()
