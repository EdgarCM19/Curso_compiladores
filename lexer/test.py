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
import sys

if __name__ == "__main__":
    print(sys.argv)

