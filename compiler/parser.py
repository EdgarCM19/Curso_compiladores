from lexer import Scanner
import csv

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
        #print('Buscando el primeros de ' + non_terminal)
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
                print("[ERROR]>El simbolo {} comparte predictivos".format(non_term))
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
        data = []
        temp = []
        temp.append('[N/T]')
        temp.extend(self.T + ['$'])
        data.append(temp)
        for n_t in self.N:
            temp = []
            temp.append(n_t)
            for t in self.T + ['$']:
                temp.append(self.table[n_t][t])
            data.append(temp)
        with open('tabla.csv', 'w', encoding='utf-8') as file_csv:
            writer = csv.writer(file_csv)
            writer.writerows(data)
        '''
        with open('tabla.txt', 'w', encoding='utf-8') as file:
            cad = '[N/T]'
            cad += ' | '.join(self.T + ['$']) + '\n'
            #print(cad)
            for n_t in self.N:
                cad += n_t 
                for t in self.T + ['$']:
                    cad += '| {} |'.format(str(self.table[n_t][t]))
                cad += '\n'
            file.write(cad)
        '''

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
                    log += '\n[ERROR]> Se encontro : {} pero se esperaba {}'.format(a.type, A)
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
rules = [ 
    ('((\/\*[\s\S]*?\*\/)|(\/\/+((.)*)+\n))',                                   't_comment'),
    ('((\<\w*.h\>)|(\"\w*.h\"))',                                               't_lib'),
    ('(\"((.)*)\")',                                                            't_string'),
    ('\{',                                                                      't_brace_o'),
    ('\}',                                                                      't_brace_c'),
    ('\[',                                                                      't_bracket_o'),
    ('\]',                                                                      't_bracket_c'),
    ('\(',                                                                      't_parenthesis_o'),
    ('\)',                                                                      't_parenthesis_c'),
    ('\#',                                                                      't_sharp'),
    ('\,',                                                                      't_comma'),
    ('\.',                                                                      't_dot'),
    ('\;',                                                                      't_semi_colon'),
    ('\?',                                                                      't_question'),
    ('\:',                                                                      't_colon'),
    ('\%\=',                                                                    't_mod_equals'),
    ('\%',                                                                      't_mod'),
    ('\*\=',                                                                    't_multiply_equals'),
    ('\*',                                                                      't_asterisk'),
    ('\+\+',                                                                    't_plus_plus'),
    ('\+\=',                                                                    't_plus_equals'),
    ('\+',                                                                      't_plus'),
    ('\-\-',                                                                    't_sub_sub'),
    ('\-\=',                                                                    't_sub_equals'),
    ('\-',                                                                      't_sub'),
    ('\/\=',                                                                    't_divide_equals'),
    ('\/',                                                                      't_divide'),
    ('\=\=',                                                                    't_comparation'),
    ('\=',                                                                      't_assigment'),
    ('\!\=',                                                                    't_diferent_to'),
    ('\!',                                                                      't_not'),
    ('\<\<',                                                                    't_left_desp'),
    ('\<\=',                                                                    't_less_equals'),
    ('\<',                                                                      't_less'),
    ('\>\>',                                                                    't_rigth_desp'),
    ('\>\=',                                                                    't_great_equals'),
    ('\>',                                                                      't_great'),
    ('\&\&',                                                                    't_and'),
    ('\&\=',                                                                    't_bit_and_equals'),
    ('\&',                                                                      't_ampersand'),
    ('\|\|',                                                                    't_or'),
    ('\|\|',                                                                    't_bit_or'),
    ('\|\=',                                                                    't_bit_or_equals'),
    ('\^\=',                                                                    't_bit_xor_equals'),
    ('\^',                                                                      't_bit_xor'),
    ('\~\=',                                                                    't_c1_equals'),
    ('\~',                                                                      't_c1'),
    ('bool',                                                                    't_kw_bool'),
    ('byte',                                                                    't_kw_byte'),
    ('char',                                                                    't_kw_char'),
    ('t_double',                                                                't_kw_double'),
    ('float',                                                                   't_kw_float'),
    ('int',                                                                     't_kw_int'),
    ('long',                                                                    't_kw_long'),
    ('short',                                                                   't_kw_short'),
    ('unsigned',                                                                't_kw_unsigned'),
    ('string',                                                                  't_kw_string'),
    ('void',                                                                    't_kw_void'),
    ('word',                                                                    't_kw_word'),
    ('define',                                                                  't_define'),
    ('include',                                                                 't_include'),
    ('HIGH',                                                                    't_HIGH'),
    ('LOW',                                                                     't_LOW'),
    ('INPUT_PULLUP',                                                            't_INPUT_PULLUP'),
    ('INPUT',                                                                   't_INPUT'),
    ('OUTPUT',                                                                  't_OUTPUT'),
    ('LED_BUILTIN',                                                             't_LED_BUILTIN'),
    ('break',                                                                   't_break'),
    ('continue',                                                                't_continue'),
    ('do',                                                                      't_do'),
    ('while',                                                                   't_while'),
    ('else',                                                                    't_else'),
    ('for',                                                                     't_for'),
    ('if',                                                                      't_if'),
    ('return',                                                                  't_return'),
    ('switch',                                                                  't_switch'),
    ('case',                                                                    't_case'),
    ('default',                                                                 't_default'),
    ('true',                                                                    't_true'),
    ('false',                                                                   't_false'),
    ('(((\d+)(\.)(\d+)(f)?)|((\d+)(E)(\-|\+)(\d)))',                            't_float'),
    ('((((0)(((x([abcdefABCDEF]|\d){1,8}))|(b([01]+))))|(\d+))(l|L)?(u|U)?)',   't_int'),
    ('(\'.\')',                                                                 't_char'),
    ('(((\_)*[a-zA-Z0-9]*)+)',                                                  't_identifier'),
    ('(.)', 'OTHER'),
]

no_term = ['PROGRAMA', 'L_BLOQUES', 'L_BLOQUESP', 'BLOQUE', 'VAR_FUNC', 'VAR', 'CONTROL', 'REPETICION', 'OPER', 'FUNC', 
    'PRE_PRO', 'V_NORMAL', 'V_ARRAY', 'TIPO', 'ASIGNACION', 'VALOR', 'FUNC_CALL', 'OPER_A',
    'OPER_L', 'OPER_B', 'ARIT_OPER', 'LOGIC_OPER', 'COMPOUND_OPER', 'COMP_ARIT', 'IF', 
    'IF_ELIF', 'IF_ELSE', 'SWITCH', 'N_CASE', 'CASE', 'DEFAULT', 'DO_WHILE', 'WHILE', 'FOR', 'FOR_ASIG', 'FOR_COND',
    'FOR_INC', 'RETURN', 'DEFINE', 'INCLUDE', 'TOK_REMP', 'V_NORMALPP', 'V_NORMALP', 'V_ARRAYPP', 'V_ARRAYP',
    'V_ARRAYPPP', 'DIMEN', 'A_INIT', 'OTRO', 'OPER_AP', 'OPER_LP', 'OPER_BP', 'OPER_COMPOU', 'OPER_COMPOUP', 'OPER_COMPOUPP', 'PARAMS', 
    'PARAMSP', 'BLOCKS', 'N_CASEP', 'DO_WHILEP', 'FOR_CONDP', 'FUNCP', 'RETURNP', 'VALOR_ASIG', 'COMP_OPER', 'BITE_OPER', 'V_NORMALASIG', 'V_ARRAYFORM', 'VAR_FUNCP' 
]
term = ['t_lib', 't_string', 't_brace_o', 't_brace_c', 't_bracket_o', 't_bracket_c', 't_parenthesis_o',
    't_parenthesis_c', 't_sharp', 't_comma', 't_dot', 't_semi_colon', 't_question', 't_colon', 't_mod_equals',
    't_mod', 't_multiply_equals', 't_asterisk', 't_plus_plus', 't_plus_equals', 't_plus', 't_sub_sub',
    't_sub_equals', 't_sub', 't_divide_equals', 't_divide', 't_comparation', 't_assigment', 't_diferent_to',
    't_not', 't_left_desp', 't_less_equals', 't_less', 't_rigth_desp', 't_great_equal', 't_great', 't_and', 
    't_ampersand', 't_or', 't_bit_or', 't_bit_xor_equals', 't_bit_xor', 't_c1_equals', 't_c1', 't_kw_bool', 
    't_kw_byte', 't_kw_char', 't_kw_double', 't_kw_float', 't_kw_int', 't_kw_long', 't_kw_short', 't_kw_unsigned', 't_kw_string', 't_kw_void',
    't_kw_word', 't_define', 't_include', 't_HIGH', 't_LOW', 't_INPUT_PULLUP', 't_INPUT', 't_OUTPUT', 't_LED_BUILTIN',
    't_break', 't_continue', 't_do', 't_while', 't_else', 't_for', 't_if', 't_return', 't_switch', 't_case', 't_default',
    't_true', 't_false', 't_float', 't_int', 't_char', 't_identifier', 't_bit_and_equals', 't_bit_or_equals'
]
prod = [
    ('PROGRAMA',        ['L_BLOQUES']),
    #GENERALES
#<<<<<<< HEAD
    ('L_BLOQUES',       ['BLOQUE', 'L_BLOQUESP']),
    ('L_BLOQUESP',      ['L_BLOQUES']),
    ('L_BLOQUESP',      ['ε']),
    ('BLOQUE',          ['VAR']),
    ('BLOQUE',          ['CONTROL']),
    ('BLOQUE',          ['REPETICION']),
    ('BLOQUE',          ['FUNC']),
    ('BLOQUE',          ['PRE_PRO']),
    #VARIABLES  
    ('VAR',             ['V_NORMAL']),
    ('VAR',             ['V_ARRAY']),
    ('V_NORMAL',        ['TIPO', 'V_NORMALPP']),
    ('V_NORMALPP',      ['t_identifier', 'V_NORMALP']),
    ('V_NORMALPP',      ['ASIGNACION', 'V_NORMALP']),
    ('V_NORMALP',       ['V_NORMAL', 'V_NORMALP']),
    ('V_NORMALP',       ['ε']),
    ('V_ARRAY',         ['TIPO', 't_identifier', 'V_ARRAYPP']),
    ('V_ARRAYPP',       ['t_bracket_o', 't_int', 't_bracket_c', 'V_ARRAYPPP']),
    ('V_ARRAYPP',       ['DIMEN', 'A_INIT']),
    ('V_ARRAYPPP',      ['t_semi_colon', 'V_ARRAYP']),
    ('V_ARRAYPPP',      ['t_assigment', 'PARAMS', 't_semi_colon', 'V_ARRAYP']),
    ('V_ARRAYP',        ['t_comma', 'V_ARRAY', 't_semi_colon', 'V_ARRAYP']),
    ('V_ARRAYP',        ['ε']),
    ('DIMEN',           ['t_bracket_o', 't_int', 't_bracket_c', 'DIMEN']),
    ('DIMEN',           ['ε']),
    ('A_INIT',          ['t_brace_o', 'A_INIT', 't_brace_c']),
    ('A_INIT',          ['VALOR_ASIG', 't_comma', 'A_INIT']),
    ('A_INIT',          ['t_semi_colon']),
    ('A_INIT',          ['ε']),
    #=======
    ('L_BLOQUES', ['BLOQUE', 'L_BLOQUESP']),
    ('L_BLOQUESP', ['L_BLOQUES']),
    ('L_BLOQUESP', ['ε']),
    ('BLOQUE', ['VAR_FUNC']),
    ('BLOQUE', ['CONTROL']),
    ('BLOQUE', ['REPETICION']),
    ('BLOQUE', ['PRE_PRO']),
    ('VAR_FUNC', ['TIPO', 't_identifier', 'VAR_FUNCP']),
    ('VAR_FUNCP', ['VAR']),
    ('VAR_FUNCP', ['FUNC']),
    #VARIABLES
    ('VAR', ['V_NORMAL']),
    ('VAR', ['V_ARRAY']),
    ('V_NORMAL', ['t_semi_colon']),
    ('V_NORMAL', ['t_comma', 'V_NORMALP']),
    ('V_NORMAL', ['V_NORMALASIG', 'V_NORMALPP']),
    ('V_NORMALPP', ['V_NORMALP']),
    ('V_NORMALPP', ['t_semi_colon']),
    ('V_NORMALASIG', ['t_assigment', 'VALOR_ASIG']),
    ('V_NORMALP', ['t_identifier','V_NORMAL']),

    ('V_ARRAY', ['V_ARRAYFORM', 'V_ARRAYP']),
    ('V_ARRAYP', ['t_assigment', 'PARAMS', 't_semi_colon']),
    ('V_ARRAYP', ['t_semi_colon']),

    ('V_ARRAYFORM', ['t_bracket_o', 't_int', 't_bracket_c']),

    #>>>>>>> bd07cbdf44bb9a5a2a6c011eadc7c93ef6ceddd8
    #TIPO DE DATOS
    ('TIPO',            ['t_kw_unsigned', 'OTRO']),
    ('TIPO',            ['t_kw_long', 'OTRO']),
    ('TIPO',            ['OTRO']),
    ('OTRO',            ['t_kw_int']),
    ('OTRO',            ['t_kw_float']),
    ('OTRO',            ['t_kw_double']),
    ('OTRO',            ['t_kw_char']),
    ('OTRO',            ['t_kw_bool']),
    ('OTRO',            ['t_kw_short']),
    ('OTRO',            ['t_kw_void']),
    ('TIPO',            ['t_kw_word']),
    ('TIPO',            ['t_kw_byte']),
    ('VALOR',           ['t_string']),
    ('VALOR',           ['t_char']),
    ('VALOR',           ['t_float']),
    ('VALOR',           ['t_int']),
    ('VALOR',           ['t_true']),
    ('VALOR',           ['t_false']),
    ('ASIGNACION',      ['t_identifier', 't_assigment', 'VALOR_ASIG', 't_semi_colon']),
    #('VALOR_ASIG',     ['OPER']),
    ('VALOR_ASIG',      ['VALOR']),
    ('VALOR_ASIG',      ['FUNC_CALL']),
    ('VALOR_ASIG',      ['t_identifier']),
    #OPERACIONES
    ('OPER',            ['OPER_A']),
    ('OPER',            ['OPER_L']),
    ('OPER',            ['OPER_B']),
    ('OPER',            ['OPER_COMPOU']),
    ('OPER_A',          ['t_parenthesis_o', 'OPER_A', 't_parenthesis_c']),
    ('OPER_A',          ['VALOR', 'OPER_AP']),
    ('OPER_A',          ['VALOR_ASIG', 'OPER_AP']),
    ('OPER_AP',         ['ε']),
    ('OPER_AP',         ['ARIT_OPER', 'OPER_A', 'OPER_AP']),
    ('OPER_L',          ['LOGIC_OPER', 'OPER_L', 'OPER_LP']),
    ('OPER_L',          ['t_parenthesis_o', 'OPER_L', 't_parenthesis_c', 'OPER_LP']),
    ('OPER_L',          ['VALOR', 'OPER_LP']),
    ('OPER_L',          ['VALOR_ASIG', 'OPER_LP']),
    ('OPER_LP',         ['ε']),
    ('OPER_LP',         ['COMP_OPER', 'OPER_L', 'OPER_LP']),
    ('OPER_LP',         ['LOGIC_OPER', 'OPER_L', 'OPER_LP']),
    ('OPER_B',          ['t_parenthesis_o', 'OPER_B', 't_parenthesis_c', 'OPER_BP']),
    ('OPER_B',          ['VALOR', 'OPER_BP']),
    ('OPER_B',          ['VALOR_ASIG', 'OPER_BP']),
    ('OPER_BP',         ['ε']),
    ('OPER_BP',         ['BITE_OPER', 'OPER_B', 'OPER_BP']),
    ('OPER_COMPOU',     ['t_identifier', 'OPER_COMPOUP']),
    ('OPER_COMPOU',     ['VALOR']),
    ('OPER_COMPOU',     ['VALOR_ASIG']),
    ('OPER_COMPOUP',    ['COMPOUND_OPER', 'OPER_COMPOUPP']),   
    ('OPER_COMPOUP',    ['COMP_ARIT']),
    ('OPER_COMPOUPP',   ['OPER_A']),
    ('OPER_COMPOUPP',   ['OPER_COMPOU']),
    ('ARIT_OPER',       ['t_plus']),
    ('ARIT_OPER',       ['t_sub']),
    ('ARIT_OPER',       ['t_asterisk']),
    ('ARIT_OPER',       ['t_divide']),
    ('ARIT_OPER',       ['t_mod']),
    ('ARIT_OPER',       ['t_assigment']),
    ('LOGIC_OPER',      ['t_not']),
    ('LOGIC_OPER',      ['t_and']),
    ('LOGIC_OPER',      ['t_or']),
    ('COMP_OPER',       ['t_diferent_to']),
    ('COMP_OPER',       ['t_less']),
    ('COMP_OPER',       ['t_less_equals']),
    ('COMP_OPER',       ['t_great']),
    ('COMP_OPER',       ['t_great_equal']),
    ('COMP_OPER',       ['t_comparation']),
    ('BITE_OPER',       ['t_ampersand']),
    ('BITE_OPER',       ['t_left_desp']),
    ('BITE_OPER',       ['t_rigth_desp']),
    ('BITE_OPER',       ['t_bit_xor']),
    ('BITE_OPER',       ['t_bit_or']),
    ('BITE_OPER',       ['t_c1']),
    ('COMPOUND_OPER',   ['t_mod_equals']),
    ('COMPOUND_OPER',   ['t_bit_and_equals']),
    ('COMPOUND_OPER',   ['t_multiply_equals']),
    ('COMPOUND_OPER',   ['t_plus_equals']),
    ('COMPOUND_OPER',   ['t_sub_equals']),
    ('COMPOUND_OPER',   ['t_divide_equals']),
    ('COMPOUND_OPER',   ['t_bit_xor_equals']),
    ('COMPOUND_OPER',   ['t_bit_or_equals']),
    ('COMP_ARIT',       ['t_plus_plus']),
    ('COMP_ARIT',       ['t_sub_sub']),
    ('FUNC_CALL',       ['t_identifier', 't_parenthesis_o', 'PARAMS', 't_parenthesis_c']),
    ('PARAMS',          ['t_identifier', 'PARAMSP']),
    ('PARAMS',          ['ε']),
    ('PARAMS',          ['VALOR_ASIG', 'PARAMSP']),
    ('PARAMSP',         ['ε']),
    ('PARAMSP',         ['t_comma','PARAMS', 'PARAMSP']),
    #ESTRUCTURAS DE CONTROL
    ('CONTROL',         ['IF']),
    ('CONTROL',         ['IF_ELIF']),
    ('CONTROL',         ['IF_ELSE']),
    ('CONTROL',         ['SWITCH']),
    ('IF',              ['t_if', 't_parenthesis_o', 'OPER_L', 't_parenthesis_c', 'BLOCKS']),
    ('BLOCKS',          ['BLOQUE']),
    ('BLOCKS',          ['t_brace_o', 'L_BLOQUES', 't_brace_c']),
    ('IF_ELIF',         ['IF', 't_if', 't_else ', 't_parenthesis_o', 'OPER_L', 't_parenthesis_c', 'BLOCKS']),
    ('IF_ELSE',         ['IF', 't_else ', 'BLOQUE']),
    ('IF_ELSE',         ['IF_ELIF', 't_else', 't_parenthesis_o', 'L_BLOQUES', 't_parenthesis_c']),
    ('SWITCH',          ['t_switch', 't_parenthesis_o', 'VALOR_ASIG', 't_parenthesis_c', 't_brace_o', 'N_CASE',  'DEFAULT', 't_brace_c']),
    ('N_CASE',          ['CASE', 'N_CASEP']),
    ('N_CASEP',         ['ε']),
    ('N_CASEP',         ['N_CASE']),
    ('CASE',            ['t_case', 'VALOR_ASIG', 't_colon', 'L_BLOQUES', 't_break', 't_semi_colon' ]),
    ('DEFAULT',         ['ε']),
    ('DEFAULT',         ['t_default', 't_colon', 'L_BLOQUES']),
    #ESTRUCTURAS DE REPETICION
    ('REPETICION',      ['DO_WHILE']),
    ('REPETICION',      ['WHILE']),
    ('REPETICION',      ['FOR']),
    ('DO_WHILE',        ['t_do', 'DO_WHILEP']),
    ('DO_WHILEP',       ['BLOQUE', 't_while', 't_parenthesis_o', 'OPER_L', 't_parenthesis_c', 't_semi_colon']),
    ('DO_WHILEP',       ['t_brace_o', 'L_BLOQUES','t_brace_c','t_while', 't_parenthesis_o', 'OPER_L', 't_parenthesis_c', 't_semi_colon']),
    ('WHILE',           ['t_while', 't_parenthesis_o', 'OPER_L', 't_parenthesis_c', 'BLOCKS']),
    ('FOR',             ['t_for', 't_parenthesis_o', 'FOR_ASIG', 't_semi_colon', 'FOR_COND', 't_semi_colon', 'FOR_INC', 't_parenthesis_o', 'BLOCKS']),
    ('FOR_ASIG',        ['VAR']),
    ('FOR_ASIG',        ['ε']),
    ('FOR_ASIG',        ['ASIGNACION' , 'FOR_ASIG']),
    ('FOR_COND',        ['ε']),
    ('FOR_COND',        ['OPER_L', 'FOR_CONDP']),
    ('FOR_CONDP',       ['OPER_L']),
    ('FOR_CONDP',       ['OPER_L', 'FOR_CONDP']),
    ('FOR_INC',         ['ε']),
    ('FOR_INC',         ['OPER_COMPOU']),
    ('FOR_INC',         ['OPER_A', 'FOR_INC']),
    #FUNCIONES
#<<<<<<< HEAD
    ('FUNC',            ['TIPO', 't_identifier', 't_parenthesis_o', 'PARAMS', 't_parenthesis_c', 'FUNCP']),
    ('FUNCP',           ['t_semi_colon']),
    ('FUNCP',           ['t_brace_o', 'L_BLOQUES', 'RETURN', 't_brace_c']),
    ('RETURN',          ['ε']),
    ('RETURN',          ['t_return', 'RETURNP']),
    ('RETURNP',         ['VALOR_ASIG', 't_semi_colon']),
    ('RETURNP',         ['t_semi_colon']),
#=======
    ('FUNC', ['t_parenthesis_o', 'PARAMS', 't_parenthesis_c', 'FUNCP']),
    ('FUNCP', ['t_semi_colon']),
    ('FUNCP', ['t_brace_o', 'L_BLOQUES', 'RETURN', 't_brace_c']),
    ('RETURN', ['t_return', 'RETURNP']),
    ('RETURN', ['ε']),
    ('RETURNP', ['VALOR_ASIG', 't_semi_colon']),
    ('RETURNP', ['t_semi_colon']),
#>>>>>>> bd07cbdf44bb9a5a2a6c011eadc7c93ef6ceddd8
    #PREPROCESADOR
    ('PRE_PRO',         ['DEFINE']),
    ('PRE_PRO',         ['INCLUDE']),
    ('DEFINE',          ['t_sharp', 't_define', 't_identifier', 'TOK_REMP']),
    ('TOK_REMP',        ['t_identifier']),
    ('TOK_REMP',        ['VALOR']),
    ('TOK_REMP',        ['OPER']),
    ('INCLUDE',         ['t_sharp', 't_include', 't_lib']),

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
    grammar = Grammar(no_term, term, 'PROGRAMA', prod)
    '''
    for non_term in grammar.N:
        print('Primeros de {} : {}'.format(non_term, grammar.first[non_term]))
    print('-------------------------------')
    for predic in grammar.predic :
        print(predic)
    print(grammar.isLL1())
    '''
    parser = Parser(lexer, grammar)
    parser.analyze()
    #grammar.saveTable()



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