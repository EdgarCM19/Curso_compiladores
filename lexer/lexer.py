import re

class Token():
    def __init__(self, type, lexema, position):
        self.type = type
        self.lexema = lexema
        self.position = position
    
    def __str__(self):
        return "{}>`{}` at {}".format(self.type, self.lexema, self.position)

class ScannerError(Exception):
    def __init__(self, position):
        self.position = position

class Scanner():
    def __init__(self, regular_expresions, buffer):
        self.id = 1
        self.regular_expresions_groups = []
        self.group_types = {}
        self.initRegex(regular_expresions)
        self.position = 0
        self.buffer = buffer

        
    def initRegex(self, regex):
        for _re, _type in regex:
            groupname = 'GROUP%s' % self.id
            self.regular_expresions_groups.append('(?P<%s>%s)' % (groupname, _re))
            self.group_types[groupname] = _type
            self.id += 1
        
        self.regex = re.compile('|'.join(self.regular_expresions_groups))
        self.re_white_spaces_skip = re.compile('\S')
    
    def getToken(self):
        if self.position >= len(self.buffer):
            return None
        else :
            match = self.re_white_spaces_skip.search(self.buffer, self.position)
            if match:
                self.position = match.start()
            else :
                return None
            match = self.regex.match(self.buffer, self.position)
            if match:
                group_name = match.lastgroup
                t_type = self.group_types[group_name]
                token = Token(t_type, match.group(group_name), self.position)
                self.position = match.end()
                return token
            raise ScannerError(self.position)
    
    def getTokens(self):
        while True:
            token = self.getToken()
            if token is None : break
            yield token

def openFile(file_name):
    if file_name.endswith('.ino'):
        with open(file_name, 'r') as file:
            return file.read()
    else :
        return None

if __name__ == "__main__":
    rules = [ 
        ('((\/\*[\s\S]*?\*\/)|(\/\/+((.)*)+\n))',                                                                                   'COMMENT'),
        ('(\"((.)*)\")',                                                                                                            'STRING'),
        ('\{',                                                                                                                      'BRACE_O'),
        ('\}',                                                                                                                      'BRACE_C'),
        ('\[',                                                                                                                      'BRACKET_O'),
        ('\]',                                                                                                                      'BRACKET_C'),
        ('\(',                                                                                                                      'PARENTHESIS_O'),
        ('\)',                                                                                                                      'PARENTHESIS_C'),
        ('\#',                                                                                                                      'PREPROCESSOR'),
        ('\,',                                                                                                                      'COMMA'),
        ('\.',                                                                                                                      'DOT'),
        ('\;',                                                                                                                      'SEMI_COLON'),
        ('(((\+|\-){2})|((\%|\&|\*|\-|\+|\/|\||\^)\=))',                                                                            'COMPOUND'),
        ('(\%|\+|\-|\/)',                                                                                                           'ARITMETHIC'),
        ('\*',                                                                                                                      'ASTERISK'),
        ('\=',                                                                                                                      'ASSIGMENT'),
        ('\&',                                                                                                                      'ASPERSAND'),
        ('\?',                                                                                                                      'QUESTION'),
        ('\:',                                                                                                                      'COLON'),
        ('((\<\<)|(\>\>)|(\^)|(\|)|(\~))',                                                                                          'BITEWISE'),
        ('((\<|\>)(\=)?)|((\=|\!)(\=))',                                                                                            'RELATIONAL'),
        ('(\!|((\&\&|\|\|)))',                                                                                                      'LOGICAL'),
        ('((array)|(b((ool)((ean)?)|(yte)))|(char)|(double)|(float)|(int)|(long)|(s((hort)|(tring)))|(void)|(word)|(unsigned))',    'DATA_TYPE'),
        ('((break)|(c(ase|ontinue))|(d(efault|o))|(else)|(for)|(goto)|(if)|(return)|(switch)|(while))',                             'STRUCTURE_CONTROL'),
        ('((const)|(static)|(volatile))',                                                                                           'SCOPE'),
        ('((false)|(HIGH)|(INPUT(_PULLUP)?)|(LED_BUILTIN)|(LOW)|(OUTPUT)|(true))',                                                  'CONSTANT'),
        ('((include)|(define))',                                                                                                    'DIRECTIVE'),
        ('(((\d+)(\.)(\d+)(f)?)|((\d+)(E)(\-|\+)(\d)))',                                                                            'FLOAT_POINT'),
        ('((((0)(((x([abcdefABCDEF]|\d){1,8}))|(b([01]+))))|(\d+))(l|L)?(u|U)?)',                                                   'INTEGER'),
        ('(((\_)*[a-zA-Z0-9]*)+)',                                                                                                   'IDENTIFIER'),
        ('(.)', 'OTHER')
        #('(array|(b)+((reak)|(yte)|(ool)+(ean){0,1})|(c)+((ase)|(har)|(on)+((st)|(tinue)))|(d)+((ef)+((ault)|(ine))|((o)+(uble){0,1}))|else|goto|HIGH|(i)+(f|nt|nclude)|(INPUT)+(_PULLUP){0,1}|((L)+(ED_BUILTIN|OW))|long|OUTPUT|return|short|static|switch|true|unsigned|vo+(id|latile)|while|word)', 'KEYWORD'),
        #('((0)(((x([abcdefABCDEF]|\d){1,8}))|(b([01]+))))', 'NUMBER'),  
        #('((\%+\={0,1})|(\*+\={0,1})|(\++\={0,1})|(\-+\={0,1})|(\/)|(\=+\={0,1})|(\>+\={0,1})|(\<+\={0,1})|(\!+\={0,1})|((\&{1,2})+\={0,1})|((\|{1,2})+\={0,1})|(\^+\={0,1})|~)',    'OPERATOR'),
        #('(\{|\}|\[|\]|\(|\)|\#|\,|\.|\;)',             'SPECIAL_SYMBOL'),
    ]

    buffer = openFile('test.ino')
    if buffer is None:
        print('Error de lectura de archivo')
        exit(-1)
    scanner = Scanner(rules, buffer)
    try:
        for token in scanner.getTokens():
            if token.type != 'COMMENT':
                print(token)
    except ScannerError as e:
        print('Error at position {}'.format(e.position))