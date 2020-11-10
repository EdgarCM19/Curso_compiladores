from lexer import Scanner

class Grammar():
    '''
    Producciones del tipo:
    F -> ( E ) | ident
    Pasan a:
    ('F', ['(', 'E', ')'])
    ('F', ['ident'])
    '''
    def __init__(self, N : list, T : list, S : str, P : list):
        self.N = N
        self.T = T
        self.S = S
        self.P = P
        self.initTable()

    def __str__(self):
        cad = ""
        no_term = "{" + ", ".join(self.N) + "}"
        term = "{" + ", ".join(self.T) + "}"
        gram = "G = {" + no_term + ", " + term + ", " + self.S + ", P}\n"
        produc = "Con P:\n"
        for index, prod in enumerate(self.P):
            produc += "P{} = {} -> {}\n".format(index, prod[0], prod[1])
        return gram + produc

    def firstfun(self):
        self.first = {}
        for non_terminal in self.N:
            self.first[non_terminal] = self.getFirst(non_terminal)

    def getFirst(self, non_terminal):
        if non_terminal in self.first: return self.first[non_terminal]
        productions = (prod for symbol, prod in self.P if symbol == non_terminal)
        prod_first = set()
        for produc in productions:
            f = produc[0]
            if f == non_terminal: continue
            if f in self.T or f == 'ε': 
                prod_first.add(f)
            else : 
                prod_first = prod_first.union(self.getFirst(f))
        return prod_first

    def follows(self):
        self.follow = {i: set() for i in self.N}
        for symbol in self.N:
            self.getFollows(symbol)
        

    def getFollows(self, non_terminal):
        added = True
        productions = (prod for prod in self.P if non_terminal in prod[1])
        while(added):
            added = False
            for symbol, prod in productions:
                prod_next = self.follow[symbol]
                for symb in reversed(prod):
                    if symb in self.N:
                        #added = self.union(self.follows[symb], prod_next)
                        t = self.follow[symb]
                        temp = len(t) if t != set() else 0
                        self.follow[symb] = self.follow[symb].union(prod_next)
                        added = temp == len(self.follow)
                    if 'ε' in symb:
                        prod_next = prod_next.union(self.first[symb])
                    else :
                        if symb in self.N :
                            prod_next = self.first[symb].difference('ε').union(self.follow[symbol])
                        else :
                            prod_next.add(symb)
        if(non_terminal == self.S):
                self.follow[non_terminal].update(set('$'))
        return self.follow[non_terminal]
  
    def predicfun(self):
        self.predic = list()
        for symbol in self.N:
            self.getPredic(symbol)

    def getPredic(self, non_terminal):
        for production in self.P:
            symbol, produc = production
            if symbol == non_terminal :
                alpha = set()
                for prod in list(produc) :
                    if(prod in self.N):
                        alpha = alpha.union(set(self.first[prod]))
                    elif prod in self.T:
                        temp = set()
                        temp.add(prod)   
                        alpha = alpha.union(temp)
                        break
                    if not 'ε' in alpha: break
                if 'ε' in alpha or 'ε' in produc:
                    self.predic.append((production, alpha.difference('ε').union(self.follow[symbol])))
                else :
                    self.predic.append((production, set(alpha)))

    
    def isLL1(self):
        for non_term in self.N :
            if not self.isLL1forNonTerminal(non_term):
                return False 
        return True

    def isLL1forNonTerminal(self, non_terminal) -> bool:
        alpha_predic_set = list(predic for produc, predic in self.predic if produc[0] == non_terminal)
        for index, predic in enumerate(alpha_predic_set) :
            alpha = set(predic)
            for pre in alpha_predic_set[index+1:]:
                if len(alpha.intersection(set(pre))) != 0 :
                    return False
        return True

    def createTable(self):
        self.table = {non_term : {term : '@' for term in self.T + ['$'] } for non_term in self.N}
        for predic_item in self.predic:
            produc, pred_set = predic_item
            for item in pred_set :
                self.table[produc[0]][item] = produc        
    #print(str(self.table))

    def saveTable(self):
        with open('tabla.txt', 'w') as file:
            cad = '[N/T]'
            cad += ' | '.join(self.T + ['$']) + '\n'
            #print(cad)
            for n_t in self.N:
                cad += n_t 
                for t in self.T + ['$']:
                    cad += '| {} |'.format(self.table[n_t][t])
                cad += '\n'
            print(cad)

    def initTable(self):
        self.firstfun()
        self.follows()
        self.predicfun()
        self.createTable()
class Parser():

    def __init__(self, lexer: Scanner, grammar : Grammar):
        self.lexer = lexer
        self.grammar = grammar

    def analyze(self):
        stack = list()
        stack.append('$')
        stack.append(self.grammar.S)
        log = ""
        print("Inicio del analisis sintactico")
        while True :
            log += '[Pila]>{} ||| '.format(stack)             
            log += '[Entrada]>{} ||| '.format(', '.join(token.type for token in self.lexer.stack))
            A = stack[len(stack) - 1]
            a = lexer.stackPeek()
            if a is None : break
            if A in self.grammar.T + ['$']:
                if A == a.type :
                    #print('[Salida]>Emparejar {}'.format(a))
                    log += ('[Salida]>Emparejar {} \n'.format(a.type))
                    stack.pop()
                    if len(stack) != 0:
                        a = lexer.stackPop()
                        if a is None : break
                        a = lexer.stackPeek()
                else :
                    log += 'Se encontro : {} pero se esperaba {}'.format(a.type, A)
                    break
            else :
                production = self.grammar.table[A][a.type]
                if production != '@':
                    _, producs = production
                    log += ('[Salida]>{} -> {} \n'.format(_, " ".join(producs)))
                    stack.pop()
                    for ci in reversed(producs):
                        if ci != 'ε':
                            stack.append(ci)
                else :
                    #for predi in self.predic:
                    log += '\n[ERROR]> Se encontro : {} pero se esperaba {}'.format(a.type, A)    
                    break
            if A == '$':
                break
        print(log)
        print("Analisis sintactico finalizado")

'''
rules = [
        ('\+', 't_+'),
        ('\-', 't_-'),
        ('\*', 't_*'),
        ('\/', 't_/'),
        ('\(', 't_('),
        ('\)', 't_)'),
        ('[a-zA-z]', 't_id'),
    ]       

no_term = ['E', 'E\'', 'T', 'T\'', 'F']
term = ['t_id', 't_+', 't_-', 't_*', 't_/', 't_(', 't_)']
prod = [
    #('X', 'E'),
    ('E', ['T', 'E\'']),        
    ('E\'', ['t_+', 'T', 'E\'']), 
    ('E\'', ['t_-', 'T', 'E\'']), 
    ('E\'', ['ε']),
    ('T', ['F', 'T\'']),        
    ('T\'', ['t_*', 'F', 'T\'']),
    ('T\'', ['t_/', 'F', 'T\'']),
    ('T\'', ['ε']),
    ('F', ['t_(', 'E', 't_)']),     
    ('F',   ['t_id']),
]
'''

no_term = ['PROGRAMA', 'L_BLOQUES', 'BLOQUE', 'VAR', 'CONTROL', 'REPETICION', 'OPER', 'FUNC', 
    'PRE_PRO', 'V_NORMAL', 'V_ARRAY', 'TIPO', 'ASIGNACION', 'PARAMS', 'VALOR', 'FUNC_CALL', 'OPER_A',
    'OPER_L', 'OPER_B', 'OPER_COMPOU', 'ARIT_OPER', 'LOGIC_OPER', 'COMPOUND_OPER', 'COMP_ARIT', 'IF', 
    'IF_ELIF', 'IF_ELSE', 'SWITCH', 'N_CASE', 'CASE', 'DEFAULT', 'DO_WHILE', 'FOR', 'FOR_ASIG', 'FOR_COND',
    'FOR_INC', 'RETURN', 'DEFINE', 'INCLUDE', 'TOK_REMP', 'V_NORMALPP', 'V_NORMALP', 'V_ARRAYPP', 'V_ARRAYP',
    'V_ARRAYPPP', 'DIMEN', 'A_INIT', 'OTRO', 'OPER_AP', 'OPER_LP', 'OPER_COMPOU', 'OPER_COMPOUP', 'PARAMS', 
    'BLOCKS', 'N_CASEP', 'DO_WHILEP', 'FOR_CONDP', 'FUNCP', 'RETURNP' 
]
term = ['t_lib', 't_string', 't_brace_o', 't_brace_c', 't_bracket_o', 't_bracket_c', 't_parenthesis_o',
    't_parenthesis_c', 't_sharp', 't_comma', 't_dot', 't_semi_colon', 't_question', 't_colon', 't_mod_equals',
    't_mod', 't_multiply_equals', 't_asterisk', 't_plus_plus', 't_plus_equals', 't_plus', 't_sub_sub',
    't_sub_equals', 't_sub', 't_divide_equals', 't_divide', 't_comparation', 't_assigment', 't_diferent_to',
    't_not', 't_left_desp', 't_less_equals', 't_less', 't_rigth_desp', 't_great_equals', 't_great', 't_and', 
    't_ampersand', 't_or', 't_bit_or', 't_bit_xor_equals', 't_bit_xor', 't_c1_equals', 't_c1', 't_bool', 
    't_byte', 't_char', 't_double', 't_float', 't_int', 't_long', 't_short', 't_unsigned', 't_string', 't_void',
    't_word', 't_define', 't_include', 't_HIGH', 't_LOW', 't_INPUT_PULLUP', 't_INPUT', 't_OUTPUT', 't_LED_BUILTIN',
    't_break', 't_continue', 't_do', 't_while', 't_else', 't_for', 't_if', 't_return', 't_switch', 't_case', 't_default',
    't_true', 't_false', 't_float', 't_int', 't_char', 't_identifier'
]
prod = [
    ('PROGRAMA', ['L_BLOQUES']),
    #GENERALES
    ('L_BLOQUES', ['BLOQUE', 'L_BLOQUES']),
    ('L_BLOQUES', ['ε']),
    ('BLOQUE', ['VAR']),
    ('BLOQUE', ['CONTROL']),
    ('BLOQUE', ['REPETICION']),
    ('BLOQUE', ['FUNC']),
    ('BLOQUE', ['PRE_PRO']),
    #VARIABLES
    ('VAR', ['V_NORMAL']),
    ('VAR', ['V_ARRAY']),
    ('V_NORMAL', ['TIPO', 'V_NORMALPP']),
    ('V_NORMALPP', ['t_identifier', 'V_NORMALP']),
    ('V_NORMALPP', ['ASIGNACION', 'V_NORMALP']),
    ('V_NORMALP', ['V_NORMAL', 'V_NORMALP']),
    ('V_NORMALP', ['ε']),
    ('V_ARRAY', ['TIPO', 't_identifier', 'V_ARRAYPP']),
    ('V_ARRAYPP', ['t_bracket_o', 't_int', 't_bracket_c', 'V_ARRAYPPP']),
    ('V_ARRAYPP', ['DIMEN', 'A_INIT']),
    ('V_ARRAYPPP', ['t_semi_colon', 'V_ARRAYP']),
    ('V_ARRAYPPP', ['t_assigment', 'PARAMS', 't_semi_colon', 'V_ARRAYP']),
    ('V_ARRAYP', ['t_comma', 'V_ARRAY', 't_semi_colon', 'V_ARRAYP']),
    ('V_ARRAYP', ['ε']),
    ('DIMEN', ['t_']),
    ('A_INIT', ['t_brace_o', 'A_INIT', 't_brace_c']),
    ('A_INIT', ['VALOR_ASIG', 't_comma', 'A_INIT']),
    ('A_INIT', ['t_semi_colon']),
    ('A_INIT', ['ε']),
    #TIPO DE DATOS
    ('TIPO', ['t_kw_unsigned', 'OTRO']),
    ('TIPO', ['t_kw_long', 'OTRO']),
    ('TIPO', ['OTRO']),
    ('OTRO', ['t_kw_int']),
    ('OTRO', ['t_kw_float']),
    ('OTRO', ['t_kw_double']),
    ('OTRO', ['t_kw_char']),
    ('OTRO', ['t_kw_bool']),
    ('OTRO', ['t_kw_short']),
    ('OTRO', ['t_kw_void']),
    ('TIPO', ['t_kw_word']),
    ('TIPO', ['t_kw_byte']),
    ('VALOR', ['t_string']),
    ('VALOR', ['t_char']),
    ('VALOR', ['t_float']),
    ('VALOR', ['t_int']),
    ('VALOR', ['t_true']),
    ('VALOR', ['t_false']),
    ('ASIGNACION', ['t_identifier', 't_assigment', 'VALOR_ASIG', 't_semi_colon']),
    
    ('E\'', ['ε']),
    
]

def openFile(file_name):
    if file_name.endswith('.ino'):
        with open(file_name, 'r') as file:
            return file.read()
    else :
        return None

if __name__ == "__main__":
    
    buffer = openFile('test.ino')
    if buffer is None:
        print('Error de lectura de archivo')
        exit(-1)
    lexer = Scanner(rules, buffer)
    grammar = Grammar(no_term, term, 'E', prod)
    parser = Parser(lexer, grammar)
    parser.analyze()



'''
no_term = ['E', 'E\'', 'T', 'T\'', 'F']
term = ['+', '*', '(', ')', 'ident']
prod = [
    ('E', ['T', 'E\'']),        #('E',   'T E\''),
    ('E\'', ['+', 'T', 'E\'']), #('E\'', '+ T E\''),
    ('E\'', ['ε']),
    ('T', ['F', 'T\'']),        #('T',   'F T\''),
    ('T\'', ['*', 'F', 'T\'']), #('T\'', '* F T'),
    ('T\'', ['ε']),
    ('F', ['(', 'E', ')']),     #('F',   '( E )'),
    ('F',   ['ident']),
]
'''
'''
no_term = ['S', 'A', 'B']
term = ['a', 'b', 'c', 'd', 'e', 'f']
prod = [
    ('S', ['A', 'B']),        
    ('S', ['s']),
    ('A', ['a', 'S', 'c']),
    ('A', ['e', 'B', 'f']),
    ('A', ['ε']),       
    ('B', ['b', 'A', 'd']),
    ('B', ['ε']),
]
'''
'''
no_term = ['A', 'B']
term = ['a', 'b', 'c']
prod = [     
    ('A', ['a', 'b', 'B']),
    ('A', ['B', 'b']),       
    ('B', ['b']),
    ('B', ['c']),
]'''