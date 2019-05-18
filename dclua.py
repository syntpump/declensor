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

    def findWordInModel(self, word: str, model):
        """Search suffix of given word in the model and return its coordinates.

        Args:
            word (str): Word to look for.
            model (dict): Model to search in.

        Returns:
            tuple:
                [0]: Found suffix.
                [1]: Coordinates.

        """

        def _search(li: list, word):
            """Recursive function for searching in list. Each recursion
            `coords` list increase with new coordinate.
            Complexity is n^d, where d is dimensionality, but at worst case
            d=4 with n<10, so that not so much.

            Returns:
                str: Found suffix.

            """

            for index, el in enumerate(li):

                if el == word[-len(el):]:
                    return el

                if type(el) is list:
                    found = _search(el, word)
                    if found:
                        return found
            return None

        return _search(model, word)

    def findWordInModels(self, word, models):
        """Search suffix of given word in bundle of models.

        ! This function might cost pretty much.
        Complexity is m*n^d, where m is number of models, n is an average
        number of subarrays on each level and d is dimensionality.

        Args:
            models (iterable): Models to search in.
            word (str): Word to look for.

        Returns:
            tuple:
                [0]: Found suffix.
                [1]: Model in which it was found.

        """

        for model in models:
            found = self.findWordInModel(word, model)
            if found:
                return found, model

        return None

    def _getByCoord(self, array, vector):
        """Return element from `array` which coordinates was passed by
        `vector`.

        Args:
            array (list): Multidimensional array to search in.
            vector (list, tuple): Coordinates of element to return.

        Returns:
            *: Found element.

        """
        if vector:
            return self._getByCoord(
                array[vector[0]], vector[1:])
        else:
            return array

    def findModel(self, word, properties, bundle):
        """Find model of declension of suffix of the given word.

        Args:
            word (str): Given word.
            bundle (iterable): Bundle of models of declension for all suffixes
                in this POS (list of models for different suffixes).

        Returns:
            tuple:
                [0]: Recognized suffix.
                [1]: Found model.

        """

        for model in bundle:
            suffix = self._getByCoord(model)
            if word[-len(suffix):] == suffix:
                return suffix, model

        # The edge case.
        return None
