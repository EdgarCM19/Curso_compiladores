class Grammar():
    '''
    Producciones del tipo:
    F -> ( E ) | ident
    Pasan a:
    ('F', '( E ) | ident')
    o a:
    ('F', [['(', 'E', ')'], ['ident']])


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
            f = produc.split(' ')[0]
            if f == non_terminal: continue
            if f in self.T or f == 'ε': 
                prod_first.add(f)
            else : 
                prod_first = prod_first.union(self.getFirst(f))
        return prod_first

no_term = ['E', 'E\'', 'T', 'T\'', 'F']
term = ['+', '*', '(', ')', 'ident']
prod = [
    ('E',   'T E\''),
    ('E\'', '+ T E\''),
    ('E\'', 'ε'),
    ('T',   'F T\''),
    ('T\'', '* F T'),
    ('T\'', 'ε'),
    ('F',   '( E )'),
    ('F',   'ident'),
]

algo = Grammar(no_term, term, 'E', prod)
print(algo)
algo.first()
for nonTer in algo.N:
    print('First ({}) = {}'.format(nonTer, algo.first[nonTer]))
