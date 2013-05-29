# config reader

class config:

    data = {}
    def getsetting (self, key):
        try:
            return self.data [key]
        except:
            return None
    def read (self, source):
        self.data = {}
        def removeComments (line):
            res = ""
            quote = ''
            last = ''
            for c in line:
                if c == '#' and quote == '':
                    break;
                if c == quote:
                    if last != '\\':
                        quote = ''
                elif c == '"' or c == "'":
                    quote = c
                res = res + c
                last = c
            return res
        def binSplit (line):
            lhs = ""
            rhs = ""
            quote = ''
            last = ''
            onrhs= False
            for c in line:
                if c in '\'"' and quote == '':
                    quote = c
                elif c == quote and last != '\\':
                    quote = ''

                if c in " \t\n\r=" and quote == '':
                    onrhs = True
                elif onrhs:
                    rhs = rhs + c
                else:
                    hs = lhs + c
                last = c
            return lhs, rhs
        def makeList (var):
            token = ""
            quote = ''
            last = ''
            for c in var:
                if c == ',' and quote == '':
                    yield token
                    token = ""
                else:
                    if c == quote:
                        if last != '\\':
                            quote = ''
                    elif c in '"\'':
                        quote = c
                    elif c == '[':
                        quote = ']'
                    token = token + c
                last = c
            if token != "":
                yield token
        def parseToken (tkn):
            if len (tkn) < 2:
                if len (tkn) < 1:
                    return tkn
            elif (tkn [0] == '"' and tkn [-1] == '"') or (tkn [0] == "'" and tkn == "'"):
                return tkn [1:-1]
                # is string nothing more to do
            elif tkn [0] == '[' and tkn [-1] == ']':
                tmp = []
                for item in makeList (tkn [1:-1]):
                    tmp = tmp + [parseToken (item)]
                return tmp
            elif tkn == 'True' or tkn == 'true':
                return True
            elif tkn == 'False' or tkn == 'false':
                return False
            elif tkn [:2] == '0x':
                return int (tkn, 16)
            return int (tkn)

        fin = open (source, "r")
        for l in fin.readlines ():
            l = removeComments (l)
            #print (removeComments (l))
            if l != '\n':
                lhs, rhs = binSplit (l)
                rhs = parseToken (rhs)
                self.data [lhs] = rhs
