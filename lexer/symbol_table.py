class SymbolTable():
    def __init__(self, built_in_func):
        self.symbols = dict()
        self.built_in = built_in_func
        self.buffer = list()
        self.nextToAnalize = 'PROGRAMA'

        self.built_in_types = {
            'int' : 't_int',
            'char' : 't_char',
            'bool' : 't_bool',
            'float' : 't_float',
        }


    def insertSymbol(self, symbol):
        self.symbols.setdefault(symbol, dict())

    def assingType(self, symbol, type_s):
        self.symbols[symbol].setdefault('type', type_s)

    def lookupSymbol(self, symbol):
        return symbol in self.symbols.keys()

    def addToBuffer(self, token):
        self.buffer.append(token)

    def proccessBlock(self, tree_list):
        if self.nextToAnalize == 'VAR':
            type_ = self.built_in_types[tree_list[0].symbol]
            checkTypes = False
            for symbol in tree_list[1:]:
                if symbol.type == 't_assigment':
                    checkTypes = True
                    continue
                if not checkTypes:
                    if self.lookupSymbol(symbol.symbol): 
                        print('Esta duplicada')
                        return
                    else:
                        self.insertSymbol(symbol.symbol)
                else:
                    if symbol.type != type_: 
                        print('Error de que no es el tipo')
            
    


    def __str__(self):
        return  '\n'.join((m_dict for m_dict in self.symbols))

