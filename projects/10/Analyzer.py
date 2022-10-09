import re
from pathlib import Path as p
import sys

class Tokenizer:
    keyword=['class', 'constructor', 'function', 'method', 'field',
             'static', 'var', 'int', 'char','boolean','void','true',
             'false','null','this','let','do','if','else','while','return']
    symbol=['{',"}","(",")","[","]",".",",",";","+","-","*","/","&","|","<",">","=","~"]
    identifier=re.compile(r'^[^\d][\w\d_]*')
    def tokenize(self,filepath):
        with open(filepath,'r') as file:
            content='\1'.join(file.readlines())
            # remove comments and spaces
            content=re.sub('//.*?\n|/\*.*?\*/','',content,flags=re.S).split('\1')
            for i in range(len(content)):
                content[i]=re.sub(r'\n|\t','',content[i])
            content=[i.strip() for i in content if i.strip()]

            tokens=[]
            #patterns=[re.compile('('+i+')') for i in self.keyword]
            patterns=[re.compile('(\\'+i+')') for i in self.symbol if i!='.']
            for row in content:
                for pattern in patterns:
                    row=pattern.sub(r' \1 ',row)
                def splitter(s):
                    def replacer(m):
                        return m.group(0).replace(" ", "\0")
                    parts = re.sub('".+?"',replacer, s).split()
                    parts = [p.replace("\0", " ") for p in parts]
                    return parts
                tokens+=splitter(row)
            return self.tag(tokens)
    def tag(self,tokens):
        for i in range(len(tokens)):
            tokens[i]=[tokens[i],self.type(tokens[i])]
            if(tokens[i][1]=='stringConstant'):
                tokens[i][0]=tokens[i][0][1:len(tokens[i][0])-1]
        return tokens
    def type(self,token):
        if(token in self.keyword):
            return 'keyword'
        elif(token in self.symbol):
            return 'symbol'
        elif(re.fullmatch(r'\d+',token)!=None and int(token)<32768):
            return 'integerConstant'
        elif(re.fullmatch(r'".*?"',token)!=None):
            return 'stringConstant'
        else:
            return 'identifier'

class CompilationEngine:
    label_cnt=0
    def __init__(self):
        self.statements={ 'let'   : self.CompileLet,
                          'if'    : self.CompileIf,
                          'while' : self.CompileWhile,
                          'do'    : self.CompileDo,
                          'return': self.CompileReturn}
        self.field=[]
        self.static=[]
        self.current_scope=None
    def CompileClass(self,tokens):
        res=[]
        tokens.pop(0)
        self.class_name=tokens.pop(0)[0] # <identifier> Main </identifier>
        tokens.pop(0)
        while(tokens[0][0] in ['static','field']):
            self.CompileClassVarDec(tokens)
        while(tokens[0][0] in ['constructor','function','method']):
            res+=self.CompileSubroutineDec(tokens)
        tokens.pop(0)
        res = '\0'.join(res).replace('\0+\0',"\0add\0").replace('\0-\0',"\0sub\0")\
                .replace('\0*\0',"\0call Math.multiply 2\0")\
                .replace('\0/\0',"\0call Math.divide 2\0")\
                .replace('\0&\0',"\0and\0").replace('\0|\0',"\0or\0")\
                .replace('\0~\0',"\0not\0").replace('\0=\0',"\0eq\0")\
                .replace('\0>\0',"\0gt\0").replace('\0<\0',"\0lt\0").split('\0')
        return res
    def CompileClassVarDec(self,tokens:list):
        type=tokens.pop(0)[0] # <keyword> field </keyword>
        if(type == 'field'):
            while(tokens[0][0] != ';'):
                if(tokens[0][0] == ','):
                    tokens.pop(0)
                    tokens.insert(0,([var_type,0]))
                var_type=tokens.pop(0)[0] # type
                var=tokens.pop(0)[0]
                self.field.append([var_type,var])
            tokens.pop(0) # <symbol> ; </symbol>
        else:
            while(tokens[0][0] != ';'):
                if(tokens[0][0] == ','):
                    tokens.pop(0)
                    tokens.insert(0,([var_type,0]))
                var_type=tokens.pop(0)[0] # type
                var=tokens.pop(0)[0]
                self.static.append([var_type,var])
            tokens.pop(0) # <symbol> ; </symbol>
    def CompileSubroutineDec(self,tokens):
        res=[]
        func_type=tokens.pop(0)[0] # <keyword> constructor </keyword>
        return_type=tokens.pop(0)[0]
        func_name=tokens.pop(0)[0] # subroutine name
        self.current_scope={
            'func_name':func_name,
            'func_type':func_type,
            'return_type':return_type,
            'var':[],
            'arg':[]
        }
        tokens.pop(0) # <symbol> ( </symbol>
        self.CompileParameterList(tokens)
        tokens.pop(0) # <symbol> ) </symbol>
        res+=['function '+self.class_name+'.'+func_name+' ']
        if(func_type=='constructor'):
            res+=['push constant '+str(len(self.field))]
            res+=['call Memory.alloc 1']
            res+=['pop pointer 0']
        elif(func_type=='method'):
            res+=['push argument 0']
            res+=['pop pointer 0']
        res+=self.CompileSubroutineBody(tokens)
        var_len=len(self.current_scope['var'])
        res[0]+=str(var_len)
        return res
    def CompileParameterList(self,tokens):
        if(self.current_scope['func_type'] == 'method'):
            self.current_scope['arg'].append('self')
        res=[]
        while(tokens[0][0] != ')'):
            if(tokens[0][0] == ','):
                tokens.pop(0)
            var_type=tokens.pop(0)[0] # type
            var=tokens.pop(0)[0]
            self.current_scope['arg'].append([var_type,var])
        return res
    def CompileVarDec(self,tokens):
        while(tokens[0][0] != ';'):
            if(tokens[0][0] == ','):
                tokens.pop(0)
                tokens.insert(0,([var_type,0]))
            var_type=tokens.pop(0)[0] # type
            var=tokens.pop(0)[0]
            self.current_scope['var'].append([var_type,var])
        tokens.pop(0) # <symbol> ; </symbol>
    def CompileStatements(self,tokens):
        res=[]
        while(tokens[0][0] in ['let','if','while','do','return']):
            res+=self.statements[tokens[0][0]](tokens)
        return res
    def CompileDo(self,tokens):
        res=[]
        tokens.pop(0) # <keyword> do </keyword>
        res+=self.CompileSubroutineCall(tokens)
        tokens.pop(0) # <symbol> ; </symbol>
        res+=['pop temp 0']
        return res
    def CompileLet(self,tokens):
        res=[]
        tokens.pop(0) # <keyword> let </keyword>
        des=tokens.pop(0)[0] # <identifier> varName </identifier>
        if(tokens[0][0] == '['):
            tokens.pop(0) # <symbol> [ </symbol>
            offset=self.CompileExpression(tokens)
            tokens.pop(0) # <symbol> ] </symbol>
        tokens.pop(0) # <symbol> = </symbol>

        res+=self.CompileExpression(tokens)
        tokens.pop(0) # <symbol> ; </symbol>
        try:
            if(offset):
                if(des in [i[1] for i in self.current_scope['var']]):
                    res+=['push local '+str([i[1] for i in self.current_scope['var']].index(des))]
                elif(des in [i[1] for i in self.current_scope['arg']]):
                    res+=['push argument '+str([i[1] for i in self.current_scope['arg']].index(des))]
                elif(des in [i[1] for i in self.field]):
                    res+=['push this '+str([i[1] for i in self.field].index(des))]
                elif(des in [i[1] for i in self.static]):
                    res+=['push this '+str([i[1] for i in self.static].index(des))]
                res+=offset
                res+=['add']
                res+=['pop pointer 1']
                res+=['pop that 0']
        except:
            if(des in [i[1] for i in self.current_scope['var']]):
                res+=['pop local '+str([i[1] for i in self.current_scope['var']].index(des))]
            elif(des in [i[1] for i in self.current_scope['arg']]):
                res+=['pop argument '+str([i[1] for i in self.current_scope['arg']].index(des))]
            elif(des in [i[1] for i in self.field]):
                res+=['pop this '+str([i[1] for i in self.field].index(des))]
            elif(des in [i[1] for i in self.static]):
                res+=['pop static '+str([i[1] for i in self.static].index(des))]
        return res
    def CompileWhile(self,tokens):
        cnt=str(self.label_cnt)
        self.label_cnt+=1
        res=[]
        tokens.pop(0) # <keyword> while </keyword>
        tokens.pop(0) # <symbol> ( </symbol>
        res+=['label L'+cnt+'.1']
        res+=self.CompileExpression(tokens)
        res+=['not']
        res+=['if-goto L'+cnt+'.2']
        tokens.pop(0) # <symbol> ) </symbol>
        tokens.pop(0)# <symbol> { </symbol>
        res+=self.CompileStatements(tokens)
        res+=['goto L'+cnt+'.1']
        res+=['label L'+cnt+'.2']
        tokens.pop(0) # <symbol> } </symbol>
        return res
    def CompileReturn(self,tokens):
        res=[]
        tokens.pop(0) # <keyword> return </keyword>
        if(tokens[0][0] != ';'):
            res+=self.CompileExpression(tokens)
        else:
            if(self.current_scope['return_type'] =='void'):
                res+=['push constant 0']
        tokens.pop(0) # <symbol> ; </symbol>
        res+=['return']
        return res
    def CompileIf(self,tokens):
        cnt=str(self.label_cnt)
        self.label_cnt+=1
        res=[]
        tokens.pop(0) # <keyword> if </keyword>
        tokens.pop(0) # <symbol> ( </symbol>
        res+=self.CompileExpression(tokens) # cond
        res+=['not']
        res+=['if-goto L'+cnt+'.1']
        tokens.pop(0) # <symbol> ) </symbol>
        tokens.pop(0) # <symbol> { </symbol>
        res+=self.CompileStatements(tokens) # s1
        tokens.pop(0) # <symbol> } </symbol>
        res+=['goto L'+cnt+'.2']
        res+=['label L'+cnt+'.1']
        if(tokens[0][0] == 'else'):
            tokens.pop(0) # <keyword> else </keyword>
            tokens.pop(0) # <symbol> { </symbol>
            res+=self.CompileStatements(tokens)
            tokens.pop(0) # <symbol> } </symbol>
        res+=['label L'+cnt+'.2']
        return res
    def CompileExpression(self,tokens):
        res=[]
        res+=self.CompileTerm(tokens)
        while(tokens[0][0] in ['+','-','*','/','&','|','<','>','=']):
            res+=[tokens.pop(0)]
            res+=self.CompileTerm(tokens)
        return self.translate_expression(res)
    def CompileTerm(self,tokens):
        res=[]
        if(tokens[0][1] in ['integerConstant','stringConstant','keyword']):
            if(tokens[0][1] == 'integerConstant'):
                res+=['push constant '+tokens.pop(0)[0]]
            elif(tokens[0][0] == 'false'):
                tokens.pop(0)
                res+=['push constant 0']
            elif(tokens[0][0] == 'true'):
                tokens.pop(0)
                res+=['push constant 0','not']
            elif(tokens[0][0] == 'null'):
                tokens.pop(0)
                res+=['push constant 0']
            elif(tokens[0][0] == 'this'):
                tokens.pop(0)
                res+=['push pointer 0']
            elif(tokens[0][0] == 'that'):
                tokens.pop(0)
                res+=['push pointer 1']
            elif(tokens[0][1] == 'stringConstant'):
                string=tokens.pop(0)[0]
                res+=['push constant '+str(len(string))]
                res+=['call String.new 1']
                for i in string:
                    res+=['push constant '+str(ord(i))]
                    res+=['call String.appendChar 2']
            else:
                res+=[tokens.pop(0)]
        elif(tokens[0][0] == '('):
            res+=[tokens.pop(0)] # <symbol> ( </symbol>
            res+=self.CompileExpression(tokens)
            res+=[tokens.pop(0)] # <symbol> ) </symbol>
        elif(tokens[0][0] in ['-','~']):
            res+=[tokens.pop(0)]
            res+=self.CompileTerm(tokens)
        else:
            if(tokens[1][0] == '['): #a[b]
                res+=[['(', 'symbol']]
                res+=self.CompileExpression([tokens.pop(0),['0','integerConstant']])
                tokens.pop(0) # <symbol> [ </symbol>
                res+=self.CompileExpression(tokens)
                tokens.pop(0) # <symbol> ] </symbol>
                res+=['add']
                res+=['pop pointer 1']
                res+=['push that 0']
                res+=[[')', 'symbol']]
            elif(tokens[1][0] not in ['(','.']):
                symbol=tokens.pop(0)[0]
                if(symbol in [i[1] for i in self.current_scope['var']]):
                    res+=['push local '+str([i[1] for i in self.current_scope['var']].index(symbol))]
                elif(symbol in [i[1] for i in self.current_scope['arg']]):
                    res+=['push argument '+str([i[1] for i in self.current_scope['arg']].index(symbol))]
                elif(symbol in [i[1] for i in self.field]):
                    res+=['push this '+str([i[1] for i in self.field].index(symbol))]
                else:
                    res+=['push static '+str([i[1] for i in self.static].index(symbol))]
            else:
                res+=[['(', 'symbol']]
                res+=self.CompileSubroutineCall(tokens)
                res+=[[')', 'symbol']]
        return res
    def CompileExpressionList(self,tokens):
        res=[]
        while(tokens[0][0] not in [')',']',';']):
            res+=self.CompileExpression(tokens)
            if(tokens[0][0] == ','):
                res+=[tokens.pop(0)] # <symbol> , </symbol>
        return res
    def CompileSubroutineBody(self,tokens):
        res=[]
        tokens.pop(0) # <symbol> { </symbol>
        while(tokens[0][0] == 'var'):
            tokens.pop(0)
            self.CompileVarDec(tokens)
        res+=self.CompileStatements(tokens)
        tokens.pop(0) # <symbol> } </symbol>
        return res
    def CompileSubroutineCall(self,tokens):
        res=[]
        func=tokens.pop(0)[0]
        if('.' not in func):
            class_name=self.class_name
        else:
            symbol=func.split('.')[0]
            tmp={i[1]:i[0] for i in self.current_scope['var']+self.current_scope['arg']+self.field+self.static}
            if(symbol in tmp):
                class_name=tmp[symbol]
                func=func.split('.')[1]
            else:
                class_name=func.split('.')[0]
                func=func.split('.')[1]
        tokens.pop(0) # <symbol> ( </symbol>
        params=self.CompileExpressionList(tokens)
        param_num=0 if not params else params.count([',', 'symbol'])+1
        tokens.pop(0) # <symbol> ) </symbol>
        try:
            is_method=function_table[[[i[0],i[2]] for i in function_table].index([class_name,func])][1]=='method'
        except: #system call
            is_method=False
        if(is_method):
            if(class_name in [i[0] for i in self.current_scope['var']]):
                res+=['push local '+str([i[0] for i in self.current_scope['var']].index(class_name))]
            elif(class_name in [i[0] for i in self.current_scope['arg']]):
                res+=['push argument '+str([i[0] for i in self.current_scope['arg']].index(class_name))]
            elif(class_name in [i[0] for i in self.field]):
                res+=['push this '+str([i[0] for i in self.field].index(class_name))]
            else:
                if(class_name==self.class_name):
                    res+=['push pointer 0']
                else:
                    res+=['push this 0']
        res+=[i for i in params if i!=[',', 'symbol']]
        res+=['call '+class_name+'.'+func+' '+str(param_num+is_method)]
        return res

    def translate_expression(self,tokens:list):
        res=[]
        stack=[]
        i=0
        while(i in range(len(tokens))):
            if(tokens[i][0] not in tokenizer.symbol):
                res.append(tokens[i])
                try:
                    res.append(stack.pop())
                except:
                    i+=1
                    continue
            elif(tokens[i][0]=='('):
                end=tokens.index([')', 'symbol'],i)
                res+=tokens[i+1:end]
                i=end
            else:
                symbol=tokens[i][0]
                if(symbol!='-'):
                    stack.append(tokens[i][0])
                else:
                    if(i==0):
                        stack.append('neg')
                    else:
                        stack.append(tokens[i][0])
            i+=1
        while(stack):
            res.append(stack.pop())
        return res

def generate_func_table(file:p):
    table=[]
    with open(file, 'r') as f:
        content=''.join(f.readlines())
        tmp=re.findall(r'(function|method|constructor) .*? (.*?)(?=\()',content)
        for i in tmp:
            table.append([file.stem,i[0],i[1]])
    return table

if __name__ == '__main__':
    tokenizer=Tokenizer()
    engine=CompilationEngine()
    try:
        path=p(sys.argv[1])
    except:
        path=p(input())
        #path=p('projects/11/ComplexArrays')
    if(path.is_dir()):
        files=list(path.glob('*.jack'))
    else:
        files=[path]

    function_table=[
        ['String','method','dispose'],
        ['String','method','length'],
        ['String','method','charAt'],
        ['String','method','setCharAt'],
        ['String','method','appendChar'],
        ['String','method','eraseLastChar'],
        ['String','method','intValue'],
        ['String','method','setInt'],
        ['String','constructor','new'],
        ['Array','method','dispose'],
    ]
    for file in files:
        function_table+=generate_func_table(file)
    
    for file in files:
        tokens=tokenizer.tokenize(file)
        engine.__init__()
        res=engine.CompileClass(tokens)
        with open(file.with_suffix('.vm'),'w') as f:
            for i in res:
                f.write(i+'\n')