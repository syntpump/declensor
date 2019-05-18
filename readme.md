[![Pypi](https://img.shields.io/pypi/v/dclua.svg)](https://pypi.python.org/pypi/dclua)

# Declensor library

Using `dclua.py` library you can train declension models and declense words. This will just replace suffix of the word to correspond new morphological properties you want the word to have. Here's some topics that will help you understand how it works.

## Morphological vector
Morphological vector is a vector which determines morphology properties for the lexeme. Number on each coordinate determine some property. You can use your vectors for your language, but here's the structure, which is suggested to use for Ukrainian.

### Noun vectors
Noun vectors has 2 coordinates: `[number][case]`. Here's the table, what means each value.

| Coordinate | Number   | Case          |
|------------|----------|---------------|
| 0          |          | Nominative    |
| 1          | Singular | Genitive      |
| 2          | Plural   | Dative        |
| 3          |          | Accusative    |
| 4          |          | Instrumental  |
| 5          |          | Locative      |
| 6          |          | Vocative      |

Infinitive suffix placed at `[0][0]`.

### Verbs vectors
Noun vectors has 4 coordinates: `[tense][person][number][gender]`.

| Coordinate | Tense    | Person        | Number   | Gender    |
|------------|----------|---------------|----------|-----------|
| 0          |          | First         | Singular | Masculine |
| 1          | Present  | Second        | Plural   | Feminine  |
| 2          | Future   | Third         |          | Neutral   |
| 3          | Past     |               |          |           |

Infinitive suffix placed at `[0][0][0][0]`.

### Adjective vectors
Noun vectors has 3 coordinates: `[gender][number][person]`.

| Coordinate | Gender    | Number   | Person        |
|------------|-----------|----------|---------------|
| 0          |           | Singular | First         |
| 1          | Masculine | Plural   | Second        |
| 2          | Feminine  |          | Third         |
| 3          | Neutral   |          |               |

Infinitive suffix placed at `[0][0][0]`.

## Declension model
Declension model is a multidimensional array which contains declensed suffixes, which is indexed using [morphology vectors](#morphological-vector). You can create such model for your word in this way:

```python
model = dclua.DeclenseTrainer.getModel({
  (0,0): 'усмішка',
  (1,0): 'усмішка',
  (1,1): 'усмішки',
  (1,2): 'усмішці',
  #...
  (2,6): 'усмішки'
});
```

Now the model will look like this:
```python
model[0][0] == 'ка'
model[1][0] == 'ка'
model[1][1] == 'ки'
model[1][2] == 'ці'
#...
model[2][6] == 'ки'
```

Every word has its suffix, so you need to create models for each of them in order to use in the future.

`getModel` method also accept `minsize` argument, which determine size of the minimal producing suffix.

## Word declension
Once you have bundle of models for different suffixes, you can use them to declense words. The syntax is following:
```
Declensor.declense(str word, tuple newmporph, iterable models, tuple morphology=None)
```
Suppose, you have `models` variable, which contains models for all suffixes we want. Then you can declense words in the following way:
```python
>>> dcl = dclua.Declensor()
>>> dcl.declense('сонцю', (1,1), models)
<<< 'сонця'
```
The morphology vector of given word will be recognized automatically, so it may take some time to found appropriate declension model in `models`. If you already know the morphology of the word you want to declense, assign it to the `morphology` argument:
```python
>>> dcl = dclua.Declensor()
>>> dcl.declense('сонцю', (1,1), models, morphology=(1,2))
<<< 'сонця'
```

## Train your model
In order to train your model you can use template from `template.txt`.
