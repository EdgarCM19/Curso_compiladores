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
        self.N = N;
        self.T = T;
        self.S = S;
        self.P = P;
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

    def first(self):
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
  
    def predic(self):
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
            if not self.isLL1forNonTerminal(nonTer):
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
        self.first()
        self.follows()
        self.predic()
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