import time


weywords = '(array|(b)+((reak)|(yte)|(ool)+(ean){0,1})|(c)+((ase)|(har)|(on)+((st)|(tinue)))|(d)+((ef)+((ault)|(ine))|((o)+(uble){0,1}))|else|goto|HIGH|(i)+(f|nt|nclude)|(INPUT)+(_PULLUP){0,1}|((L)+(ED_BUILTIN|OW))|long|OUTPUT|return|short|static|switch|true|unsigned|vo+(id|latile)|while|word)'
number = '(\d+(\.(\d+)*){0,1})'
identifier = '(((_)*[a-zA-Z0-9]*)+)'
operadores = '((\%+\={0,1})|(\*+\={0,1})|(\++\={0,1})|(\-+\={0,1})|(\/+\={0,1})|(\=+\={0,1})|(\>+\={0,1})|(\<+\={0,1})|(\!+\={0,1})|((\&{1,2})+\={0,1})|((\|{1,2})+\={0,1})|(\^+\={0,1})|~)'
strings = '((.)*)'
special = '(\{|\}|\[|\]|\(|\)|\#|\,|\.|\;|\")'

all_re = [special, operadores, number, weywords, identifier,strings]
print("Keywords regular expresion: ", weywords)
time.sleep(0.5)
print("Numbers regular expresion: ", number)
time.sleep(0.5)
print("Identifiers regular expresion: ", identifier)
time.sleep(0.5)
print("Operators regular expresion: ", operadores)
time.sleep(0.5)
print("String regular expresion: ", strings)
time.sleep(0.5)
print("Special symbols regular expresion: ", special)
time.sleep(0.5)
print("Complete regular expresion: ")
print('|'.join(all_re))

test = '(\{|\}|\[|\]|\(|\)|\#|\,|\.|\;)|((\%+\={0,1})|(\*+\={0,1})|(\++\={0,1})|(\-+\={0,1})|(\/+\={0,1})|(\=+\={0,1})|(\>+\={0,1})|(\<+\={0,1})|(\!+\={0,1})|((\&{1,2})+\={0,1})|((\|{1,2})+\={0,1})|(\^+\={0,1})|~)|(\d+(\.(\d+)*){0,1})|(array|(b)+((reak)|(yte)|(ool)+(ean){0,1})|(c)+((ase)|(har)|(on)+((st)|(tinue)))|(d)+((ef)+((ault)|(ine))|((o)+(uble){0,1}))|else|goto|HIGH|(i)+(f|nt|nclude)|(INPUT)+(_PULLUP){0,1}|((L)+(ED_BUILTIN|OW))|long|OUTPUT|return|short|static|switch|true|unsigned|vo+(id|latile)|while|word)|(((_)*[a-zA-Z0-9]*)+)|(("){1}(.)*("){1})'