# pytarski

This repo contains a python implementation of Tarski's World. You can install it as a package via pip

```sh
git install pytarski
```

Check the `examples` folder for a sample script highlighting some of the basic features.

To get right to it, you first import the package and create a board

```python
import pytarski as pt

board = pt.TarskiBoard()
```

then you can add objects to the board, where you specify the shape (`cube`, `dodec`, or `tet`), size (`small`, `medium`, or `large`), column (0 - 7), and row (0 - 7) for the object

```python
a = board.add('tet', 'small', 3, 5)
b = board.add('cube', 'medium', 4, 5)
```

and you can now evaluate sentences about the objects using the Tarski's World predicates

```python
sentence1 = pt.tet(a) # True
sentence1 &= pt.leftOf(a, b) # True

sentence2 = pt.dodec(b) # False
sentence2 |= pt.sameCol(a, b) # False

sentence3 = not sentence2 or not sentence1 # True

print(f'Sentence1 is {sentence1}, sentence2 is {sentence2}, and sentence3 is {sentence3}')
```

which will print

```sh
Sentence1 is True, sentence2 is False, and sentence3 is True
```
