import re

class Token():
    '''
    Clase encargada de tener toda la información del token, como el tipo, el lexema 
    que contiene al igual que la posicion donde fue encontrado dicho token.
    '''
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
    '''
    Clase encargada de abrir, procesar y retornar todos los tokens existentes en un archivo de entrada.
    '''
    def __init__(self, regular_expresions, buffer):
        '''
        Recive una lista de tuplas las cuales contienen una expresion regular con el nombre del conjunto de dicha expresion regular.
        Recive un buffer el cual es el texto a procesar. 
        '''
        self.id = 1
        self.regular_expresions_groups = []
        self.group_types = {}
        self.initRegex(regular_expresions)
        self.position = 0
        self.buffer = buffer
        self.initTokenStack()

        
    def initRegex(self, regex):
        '''
        Se encarga de unir todas las expresiones regulares en una sola, dandole formato de
        grupo-expresion <(?<nombre_grupo>expresion_regular)> para poder identificar los matchs.
        '''
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
    
    def initTokenStack(self):
        self.stack = list()
        try:
            for token in self.getTokens():
                if token.type != 't_comment':
                    self.stack.append(token)
        except ScannerError as e:
            print('Error at position {}'.format(e.position))
        #self.stack = list(reversed(self.stack))
        print('[STACK]>')
        for t in self.stack:
            print(t)

    def stackPeek(self):
        if len(self.stack) > 0:
            return self.stack[0]
        else: return None 

    def stackPop(self):
        if len(self.stack) > 0:
            return self.stack.pop(0)
        else : return None


def openFile(file_name):
    if file_name.endswith('.ino'):
        with open(file_name, 'r') as file:
            return file.read()
    else :
        return None

if __name__ == "__main__":
    #Se define la lista de expresiones regulares con su respectivo nombre de grupo.
    
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
        ('\&\&',                                                                    't_ampersand'),
        ('\|\|',                                                                    't_or'),
        ('\|\|',                                                                    't_bit_or'),
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
        ('true',                                                                    't_bool'),
        ('false',                                                                   't_bool'),
        ('(((\d+)(\.)(\d+)(f)?)|((\d+)(E)(\-|\+)(\d)))',                            't_float'),
        ('((((0)(((x([abcdefABCDEF]|\d){1,8}))|(b([01]+))))|(\d+))(l|L)?(u|U)?)',   't_int'),
        ('(\'.\')',                                                                 't_char'),
        ('(((\_)*[a-zA-Z0-9]*)+)',                                                  't_identifier'),
        ('(.)', 'OTHER'),
    ]
    '''
    rules = [
        ('\+', 't_+'),
        ('\-', 't_-'),
        ('\*', 't_*'),
        ('\/', 't_/'),
        ('\(', 't_('),
        ('\)', 't_)'),
        ('\w', 't_id'),
    ]
    '''
    buffer = openFile('test.ino')
    if buffer is None:
        print('Error de lectura de archivo')
        exit(-1)
    scanner = Scanner(rules, buffer)
    for token in scanner.getTokens():
        print(token)