class TarskisWorldObject:
    def __init__(self, shape, size, col, row):
        if shape not in ['cube', 'dodec', 'tet']:
            raise NameError('Invalid shape')
        if size not in ['small', 'medium', 'large']:
            raise NameError('Invalid size')
        if col not in range(8):
            raise NameError('Invalid column')
        if row not in range(8):
            raise NameError('Invalid row')
        self.shape = shape
        self.size = size 
        self.col = col 
        self.row = row

    def __str__(self):
        return f'{self.shape} {self.size} {self.col} {self.row}'
    
class TarskisWorldBoard:
    def __init__(self):
        self.objects = []

    def __str__(self):
        s = ''
        for obj in self.objects:
            s += str(obj) + ', '
        return s[:-2]

    def add(self, shape, size, col, row):
        for obj in self.objects:
            if obj.col == col and obj.row == row:
                if obj.shape == shape and obj.size == size:
                    return obj
                else:
                    raise NameError(f'Object already exists at column {col} and row {row}')
            elif (obj.size == 'large' or size == 'large'):
                if (obj.col == col + 1 or obj.col == col - 1 or obj.col == col) and (obj.row == row + 1 or obj.row == row - 1 or obj.row == row):
                    raise NameError(f'Cannot place an object in a tile surrounding a large object')
        self.objects.append(TarskisWorldObject(shape, size, col, row))
        return self.objects[-1]
    
    def cube(self, object): # check if the object is a cube
        if object.shape == 'cube':
            return True
        return False
    
    def dodec(self, object): # check if the object is a dodecahedron
        if object.shape == 'dodec':
            return True
        return False

    def tet(self, object): # check if the object is a tetrahedron
        if object.shape == 'tet':
            return True
        return False

    def small(self, object): # check if the object is small
        if object.size == 'small':
            return True
        return False
        
    def medium(self, object): # check if the object is medium
        if object.size == 'medium':
            return True
        return False

    def large(self, object): # check if the object is large
        if object.size == 'large':
            return True
        return False

    def sameShape(self, object1, object2): # check of objects are the same shape
        if object1.shape == object2.shape:
            return True
        return False

    def sameSize(self, object1, object2): # check of objects are the same size
        if object1.size == object2.size:
            return True
        return False

    def sameCol(self, object1, object2): # check of objects are in the same column
        if object1.col == object2.col:
            return True
        return False

    def sameRow(self, object1, object2): # check of objects are in the same row
        if object1.row == object2.row:
            return True
        return False

    def sameDiagonal(self, object1, object2): # check if the objects are along the same diagonal
        if not self.sameCol(object1, object2) and not self.sameRow(object1, object2):
            if abs((object1.row - object2.row) / (object1.col - object2.col)) == 1.0:
                return True
        return False

    def smaller(self, object1, object2): # check if object1 is smaller than object2
        if object1.size == 'small' and (object2.size == 'medium' or object2.size == 'large'):
            return True
        if object1.size == 'medium' and object2.size == 'large':
            return True
        return False

    def larger(self, object1, object2): # check if object1 is larger than object2
        if object1.size == 'large' and (object2.size == 'medium' or object2.size == 'small'):
            return True
        if object1.size == 'medium' and object2.size == 'small':
            return True
        return False

    def leftOf(self, object1, object2): # check if object1 is to the left of object2
        if object1.col < object2.col:
            return True
        return False

    def rightOf(self, object1, object2): # check if object1 is to the right of object2
        if object1.col > object2.col:
            return True
        return False

    def frontOf(self, object1, object2): # check if object1 is in front of object2
        if object1.row < object2.row:
            return True
        return False

    def backOf(self, object1, object2): # check if object1 is in back of object2
        if object1.row > object2.row:
            return True
        return False

    def between(self, object1, object2, object3): # check if object1 is between object2 and object3
        if self.sameRow(object1, object2) and self.sameRow(object2, object3):
            if (object2.col < object1.col and object1.col < object3.col) or (object3.col < object1.col and object1.col < object2.col):
                return True
        if self.sameCol(object1, object2) and self.sameCol(object2, object3):
            if (object2.row < object1.row and object1.row < object3.row) or (object3.row < object1.row and object1.row < object2.row):
                return True
        if self.sameDiagonal(object1, object2) and self.sameDiagonal(object2, object3):
            if (object2.col < object1.col and object1.col < object3.col) and (object2.row < object1.row and object1.row < object3.row):
                return True
            if (object2.col < object1.col and object1.col < object3.col) and (object2.row > object1.row and object1.row > object3.row):
                return True
            if (object2.col > object1.col and object1.col > object3.col) and (object2.row < object1.row and object1.row < object3.row):
                return True
            if (object2.col > object1.col and object1.col > object3.col) and (object2.row > object1.row and object1.row > object3.row):
                return True
        return False

    def adjoins(self, object1, object2): # check if object1 adjoins object2
        if not self.large(object1) and not self.large(object2):
            if self.sameRow(object1, object2):
                if object1.col == (object2.col - 1) or object1.col == (object2.col + 1):
                    return True
            if self.sameCol(object1, object2):
                if object1.row == (object2.row - 1) or object1.row == (object2.row + 1):
                    return True
        return False
            