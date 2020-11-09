'''
comments = '((\/\*[\s\S]*?\*\/)|(\/\/+((.)*)+\n))'
weywords = '(array|(b)+((reak)|(yte)|(ool)+(ean){0,1})|(c)+((ase)|(har)|(on)+((st)|(tinue)))|(d)+((ef)+((ault)|(ine))|((o)+(uble){0,1}))|else|goto|HIGH|(i)+(f|nt|nclude)|(INPUT)+(_PULLUP){0,1}|((L)+(ED_BUILTIN|OW))|long|OUTPUT|return|short|static|switch|true|unsigned|vo+(id|latile)|while|word)'
number = '(\d+(\.(\d+)*){0,1})'
identifier = '(((_)*[a-zA-Z0-9]*)+)'
operadores = '((\%+\={0,1})|(\*+\={0,1})|(\++\={0,1})|(\-+\={0,1})|(\/+\={0,1})|(\=+\={0,1})|(\>+\={0,1})|(\<+\={0,1})|(\!+\={0,1})|((\&{1,2})+\={0,1})|((\|{1,2})+\={0,1})|(\^+\={0,1})|~)'
strings = '((.)*)'
special = '(\{|\}|\[|\]|\(|\)|\#|\,|\.|\;|\")'

all_re = [special, operadores, number, weywords, identifier,strings]

test = '(\{|\}|\[|\]|\(|\)|\#|\,|\.|\;)|((\%+\={0,1})|(\*+\={0,1})|(\++\={0,1})|(\-+\={0,1})|(\/+\={0,1})|(\=+\={0,1})|(\>+\={0,1})|(\<+\={0,1})|(\!+\={0,1})|((\&{1,2})+\={0,1})|((\|{1,2})+\={0,1})|(\^+\={0,1})|~)|(\d+(\.(\d+)*){0,1})|(array|(b)+((reak)|(yte)|(ool)+(ean){0,1})|(c)+((ase)|(har)|(on)+((st)|(tinue)))|(d)+((ef)+((ault)|(ine))|((o)+(uble){0,1}))|else|goto|HIGH|(i)+(f|nt|nclude)|(INPUT)+(_PULLUP){0,1}|((L)+(ED_BUILTIN|OW))|long|OUTPUT|return|short|static|switch|true|unsigned|vo+(id|latile)|while|word)|(((_)*[a-zA-Z0-9]*)+)|(("){1}(.)*("){1})'

'''
algo = {}
algo0 = set()
algo1 = set()
algo2 = set()
algo0.add('a')
algo0.add('b')
algo0.add('c')
algo1.add('1')
algo1.add('2')
algo1.add('3')
algo1.add('x')
algo2.add('y')
algo2.add('z')
algo2.add('a')
algo['0'] = algo0
algo['1'] = algo1
algo['2'] = algo2

print(len(algo0.intersection(algo1)))

