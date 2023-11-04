class BooleTruthTable:
    def __init__(self, sentence):
        s = sentence.split()
        self.atomics = []
        for c in s:
            if len(c) == 1 and not c.isalpha():
                raise NameError('Invalid atomic name. Must be alphabetic character.')
            if len(c) == 2 and c != 'or':
                raise NameError(f'Invalid connective name {c}.')
            if len(c) == 3 and (c != 'not' and c != 'and'):
                raise NameError(f'Invalid connective name {c}.')
            if len(c) != 1 and len(c) != 2 and len(c) != 3:
                raise NameError(f'Invalid sentence.')
        for c in s:
            if len(c) == 1:
                self.atomics.append(c)
        self.sentence = sentence

    def checkTrue(self, l):
        for d in l:
            for k in d:
                if k not in self.atomics:
                    if not k.isprintable():
                        k = 'not printable'
                    raise NameError(f'Invalid atomic name {k}.')
                exec(f'{k} = {d[k]}')
            if not eval(self.sentence):
                return False
        return True
    
    def checkFalse(self, l):
        for d in l:
            for k in d:
                if k not in self.atomics:
                    if not k.isprintable():
                        k = 'not printable'
                    raise NameError(f'Invalid atomic name {k}.')
                exec(f'{k} = {d[k]}')
            if eval(self.sentence):
                return False
        return True
