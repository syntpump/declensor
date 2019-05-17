"""This module contains class Declensor which allow you to use declension
model.
This class should be initialized optionally with model for verbs (vmodel),
nouns (nmodel) and adjectives (amodel).
The model is a list of multidimensional lists with declensed suffixes.
Properties for declension are given by coordinates. Suffix for infinitive form
should always be placed with zero coordinates.

Example:
---------
| a | b |  1 coordinate - first property, 2 - second property
---------  declense(0, 2) will return 'c'.
| c | d |  'a' is an infinitive suffix.
---------

Structure of verbs model by coordinates:
    1: tense
        [0] - infinitive
        [1] - present
        [2] - future
        [3] - past
    2: person
        [..][0] - first
        [..][1] - second
        [..][2] - third
    3: number
        [..][..][0] - singular
        [..][..][1] - plural
    4: gender
        [..][..][..][0] - masculine
        [..][..][..][1] - feminine
        [..][..][..][2] - neutral
    Infinitive suffix can be found at [0][0][0][0]

Structure of noun model:
    1: gender
        [1] - masculine
        [2] - feminine
        [3] - neutral
    2: number
        [0] - singular
        [1] - plural
    3: case
        [0] - nominative
        [1] - genitive
        [2] - dative
        [3] - accusative
        [4] - instrumental
        [5] - locative
        [6] - vocative
    Infinitive form at [0][0][0]

Structure of adjective model is the same as in noun.


"""


class Declensor:

    def __init__(self, vmodel=None, nmodel=None, amodel=None):
        """Initialize the class and assign vmodel, nmodel and amodel to self.

        Args:
            vmodel, nmodel, amodel (dict): Declension models. See module
                description for info.

        """

        self.vmodel = vmodel
        self.nmodel = nmodel
        self.amodel = amodel

    def getCoordinates(self, suffix: str, model):
        """Search given suffix in the model and return its coordinates.

        Args:
            suffix (str): Suffix to look for.
            model (dict): Model to search in.

        Returns:
            tuple: Found coordinates.

        """

        def _search(li: list, coords: list, suffix):
            """Recursive function for searching in list. Each recursion
            `coords` list increase with new coordinate.
            Complexity is n^d, where d is dimensionality, but at worst case
            d=4 with n<10, so that not so much.
            """

            for index, el in enumerate(li):

                if el == suffix:
                    return coords + [index]

                if type(el) is list:
                    found = _search(
                        el,
                        coords + [index],
                        suffix)
                    if found:
                        return found
            return None

        return tuple(
            _search(model, [], suffix))

    def findModel(word, properties, bundle):
        """Find model of declension of suffix of the given word.

        Args:
            word (str): Given word.
            bundle (list): Model of POS (list of models for different
                suffixes).

        Returns:
            list: Found model.

        """

        def _getByCoord(array, vector):
            """Return element from `array` which coordinates was passed by
            `vector`.
            """

            if vector:
                return _getByCoord(
                    array[vector[0]], vector[1:])
            else:
                return array

        for model in bundle:
            suffix = _getByCoord(model)
            if word[-len(suffix):] == suffix:
                return model

        # The edge case.
        return None
