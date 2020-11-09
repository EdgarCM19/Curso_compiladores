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

    '''
    def predic(self):
        self.predic = {str(clave) : [] for clave in self.P}
        for production in self.P:
            self.getPredic(production)

    def getPredic(self, production):
        symbol, produc = production
        alpha = set()
        for prod in list(produc) :
            if(prod in self.N):
                alpha = alpha.union(set(self.first[prod]))
            elif prod in self.T:
                temp = set()
                temp.add(prod)   
                alpha = alpha.union(temp)
                break
            if 'ε' in alpha or 'ε' in produc:
                self.predic.setdefault(str(production), []).append(list(alpha.difference('ε').union(self.follow[symbol])))
            else :
                self.predic.setdefault(str(production), []).append(list(alpha))
    '''
    
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

    def analyze(self):
        stack = list()
        stack.append('$')
        stack.append(self.S)
        log = ""
        print("Inicio del analisis sintactico")
        while True :
            #-----
            #print('[Pila]>{}'.format(stack))
            log += '[Pila]>{} ||| '.format(stack) 
            #print('[Entrada]>{}'.format(list(reversed(la_buena))))
            log += '[Entrada]>{} ||| '.format(list(reversed(la_buena)))
            #-----
            A = stack[len(stack) - 1]
            a = la_buena[len(la_buena) - 1]
            if A in self.T + ['$']:
                if A == a :
                    #print('[Salida]>Emparejar {}'.format(a))
                    log += ('[Salida]>Emparejar {} \n'.format(a))
                    stack.pop()
                    if len(stack) != 0:
                        a = analex()
                        a = la_buena[len(la_buena) - 1]
                else :
                    print('Se encontro : {} pero se esperaba {}'.format(a, A))
                    break
            else :
                if self.table[A][a] != '@':
                    #print('[Salida]>{}'.format(self.table[A][a]))
                    _, producs = self.table[A][a]
                    log += ('[Salida]>{} -> {} \n'.format(_, " ".join(producs)))
                    stack.pop()
                    for ci in reversed(producs):
                        if ci != 'ε':
                            stack.append(ci)
                else :
                    #for predi in self.predic:
                    print('Se encontro : {} pero se esperaba {}'.format(a, A))    
                    break
            if A == '$':
                break
        print(log)
        print("Analisis sintactico finalizado")
            


lex_cad = ['id', '+', 'id', '*', 'id', '$']
la_buena = list(reversed(lex_cad))
def analex():
    return la_buena.pop()



no_term = ['E', 'E\'', 'T', 'T\'', 'F']
term = ['id', '+', '-', '*', '/', '(', ')']
prod = [
    #('X', 'E'),
    ('E', ['T', 'E\'']),        
    ('E\'', ['+', 'T', 'E\'']), 
    ('E\'', ['-', 'T', 'E\'']), 
    ('E\'', ['ε']),
    ('T', ['F', 'T\'']),        
    ('T\'', ['*', 'F', 'T\'']),
    ('T\'', ['/', 'F', 'T\'']),
    ('T\'', ['ε']),
    ('F', ['(', 'E', ')']),     
    ('F',   ['id']),
]
'''

no_term = ['A', 'B']
term = ['a', 'b', 'c']
prod = [     
    ('A', ['a', 'b', 'B']),
    ('A', ['B', 'b']),       
    ('B', ['b']),
    ('B', ['c']),
]
'''

algo = Grammar(no_term, term, 'E', prod)
print(algo)
algo.first()
for nonTer in algo.N:
    print('First ({}) = {}'.format(nonTer, algo.first[nonTer]))

print("---------")
algo.follows()
for nonTer in algo.N:
    print('Follows ({}) = {}'.format(nonTer, algo.follow[nonTer]))
print("---------")

algo.predic()
print('Predict')
for production, set_predic in algo.predic:
    print("{} -> {} = {}".format(production[0], "".join(production[1]), '{' + ", ".join(set_predic) + '}'))

#print(algo.predic)

print("---------")
if algo.isLL1():
    print("La gramatica es LL(1)")
algo.createTable()
algo.saveTable()
#for production in algo.P:
#    print(algo.predic[production])

algo.analyze()







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