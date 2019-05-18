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

Suggested structure of verbs model by coordinates:
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
    Full size of this model is 4*3*2*3 = 72

Suggested structure of adjective model:
    1: gender
        [1] - masculine
        [2] - feminine
        [3] - neutral
    2: number
        [0] - singular
        [1] - plural
    3: person
        [0] - first
        [1] - second
        [2] - third
    Infinitive form at [0][0][0]
    Full size of this model is 3*2*3 = 18

Suggested structure of noun model:
    1: number
        [1] - singular
        [2] - plural
    2: case
        [0] - nominative
        [1] - genitive
        [2] - dative
        [3] - accusative
        [4] - instrumental
        [5] - locative
        [6] - vocative
    Infinitive form at [0][0]
    Full size of this model is 2*7 = 14

"""


class Declensor:
    """Declensor class take declension models and give you functions to
    declense words.
    """

    def _findWordInModel(self, word: str, model):
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

                if not el:
                    continue

                if el == word[-len(el):]:
                    return el

                if type(el) is list:
                    found = _search(el, word)
                    if found:
                        return found
            return None

        return _search(model, word)

    def _findWordInModels(self, word, models):
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
            found = self._findWordInModel(word, model)
            if found:
                return found, model

        return None

    def getByCoord(self, array, vector):
        """Return element from `array` which coordinates was passed by
        `vector`.

        Args:
            array (list): Multidimensional array to search in.
            vector (list, tuple): Coordinates of element to return.

        Returns:
            *: Found element.

        """
        if vector:
            return self.getByCoord(
                array[vector[0]], vector[1:])
        else:
            return array

    def _findModel(self, word, properties, bundle):
        """Find model of declension of suffix of the given word.

        Args:
            word (str): Given word.
            properties (tuple, list): Coordinates to look for suffix of
                given form.
            bundle (iterable): Bundle of models of declension for all suffixes
                in this POS (list of models for different suffixes).

        Returns:
            tuple:
                [0]: Recognized suffix.
                [1]: Found model.

        """

        for model in bundle:
            suffix = self.getByCoord(model, properties)
            if word[-len(suffix):] == suffix:
                return suffix, model

        # The edge case.
        return None

    def _changeProperties(self, word, suffix, model, properties):
        """Replace the suffix of the word with the new one.

        Args:
            word (str): Given word.
            suffix (str): Suffix to replace.
            model (list): Model of declension for this suffix.
            properties (list, tuple): Coordinates of new suffix.

        Returns:
            str: Result.

        """

        return word[:-len(suffix)] + self.getByCoord(model, properties)

    def declense(self, word, newmorph, models, morphology=None) -> str:
        """Declense word with given `morphology` to `newmorph` which determines
        new morphology. If the morphology was not given, it will be found
        in the models anyway.

        ! Finding appropriate declension model through models is a little bit
        expensive procedure, so if you know the morphology of passing word,
        it's better to cal this function with `morphology`.

        Args:
            word (str): Given word.
            morphology (list/tuple): Old morphology coordinates.
            newmorph (list/tuple): New morphology coordinates.
            models (iterable): Bundle of models of declensions for POS of word.

        Returns:
            str: Result.

        """

        if not morphology:
            model = self._findWordInModels(word, models)
        else:
            model = self._findModel(word, morphology, models)

        # This variable will raise up from the condition above.
        if not model:
            raise NoModelFound("No appropriate model for this form found.")

        return self._changeProperties(word, *model, newmorph)


class NoModelFound(Exception):
    pass


class DeclenseTrainer:

    @staticmethod
    def _getRootSize(words):
        """Returns the size of unchangeable part of the words in array.

        Args:
            words (iterable)

        Returns:
            int: Size of the part.

        """

        def _compareTwo(word1, word2) -> int:
            """Returns the size of common part of two words.
            """

            counter = 0
            for a, b in zip(word1, word2):
                if a == b:
                    counter += 1
                else:
                    break

            return counter

        comparator = None

        for word in words:

            # Remember and skip the first word.
            if not comparator:
                comparator = word
                continue

            # Remember the common part
            comparator = word[:_compareTwo(word, comparator)]

        return len(comparator)

    @staticmethod
    def getModel(declensions):
        """Produce the declension model for given word.

        Args:
            declensions (dict):
                key (tuple): Morphology vector for given form. See docstring of
                    this module for details.
                value (str): Form of the word.

        Returns:
            list: Produced model.

        """

        def _enlargeList(array, index):
            """Enlarge array, so it will contain given index. Fill the gaps
            with None.
            """

            while len(array) <= index:
                array.append(None)

            if array[index] is None:
                array[index] = []

        def _insertInto(array, value, index, *vector):
            """Insert `value` into given `array` into some coordinates. Example
            of use:
            >>> _insertInto([], "!", 0, 0, 1)
            <<< [[[None, "!"]]]
            """

            _enlargeList(array, index)

            if not vector:
                array[index] = value

            else:
                _insertInto(array[index], value, *vector)

        rootSize = DeclenseTrainer._getRootSize(declensions.values())

        model = list()

        for vector, form in declensions.items():
            _insertInto(model, form[rootSize:], *vector)

        return model
