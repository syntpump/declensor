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

    def __init__(self, models):
        """Initialize Declensor with the given models.

        Args:
            models (iterable)

        """

        self.setModels(models)

    @staticmethod
    def getZero(li: list):
        """Returns zero-coordinate of `li`. This method is static in order to
        use it in DeclenseTrainer.
        """

        if type(li) is list:
            return Declensor.getZero(li[0])
        else:
            return li

    def setModels(self, models):
        """Set given iterable of models as the working one. Do not assign your
        models to Declensor.models without this function, because they should
        be sorted in a specific way before use.

        Args:
            models (iterable)

        """

        self.models = sorted(
            models,
            key=lambda model: len(Declensor.getZero(model)),
            reverse=True
        )

    def _fitOrthography(self, word):
        """Fix some orthography mistakes, which can happen after declension.

        Args:
            word (str)

        Returns:
            str

        """

        replacements = [
            # йа -> я, йі -> ї, йу -> ю, йе -> є.
            ('\u0439\u0430', '\u044f'),
            ('\u0439\u0456', '\u0457'),
            ('\u0439\u0443', '\u044e'),
            ('\u0439\u0435', '\u0454'),

            # ьа -> я, ьі -> і, ьу -> ю, ье -> є
            ('\u044c\u0430', '\u044f'),
            ('\u044c\u0456', '\u0456'),
            ('\u044c\u0443', '\u044e'),
            ('\u044c\u0435', '\u0454')
        ]

        for old, new in replacements:
            word = word.replace(old, new)

        return word

    def _findWordInModel(self, word: str, model):
        """Search suffix of given word in the model and return its coordinates.

        Args:
            word (str): Word to look for.
            model (list): Model to search in.

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

    def _findWordInModels(self, word):
        """Search suffix of given word in bundle of models.

        ! This function might cost pretty much.
        Complexity is m*n^d, where m is number of models, n is an average
        number of subarrays on each level and d is dimensionality.

        Args:
            word (str): Word to look for.

        Returns:
            tuple:
                [0]: Found suffix.
                [1]: Model in which it was found.

        """

        for model in self.models:
            found = self._findWordInModel(word, model)
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

        if vector and type(array) is list:
            try:
                return self._getByCoord(
                    array[vector[0]], vector[1:])
            except IndexError:
                return None
        else:
            return array

    def _findModel(self, word, properties):
        """Find model of declension of suffix of the given word.

        Args:
            word (str): Given word.
            properties (tuple, list): Coordinates to look for suffix of
                given form.

        Returns:
            tuple:
                [0]: Recognized suffix.
                [1]: Found model.

        """

        for model in self.models:
            suffix = self._getByCoord(model, properties)

            if not suffix:
                return None

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

        newsuffix = self._getByCoord(model, properties)

        if not suffix or not newsuffix:
            return word

        return word[:-len(suffix)] + self._getByCoord(model, properties)

    def declense(self, word, newmorph, morphology=None) -> str:
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

        Returns:
            str: Result.

        """

        if not morphology:
            model = self._findWordInModels(word)
        else:
            model = self._findModel(word, morphology)

        # This variable will raise up from the condition above.
        if not model:
            raise NoModelFound("No appropriate model for this form found.")

        return self._fitOrthography(
            self._changeProperties(word, *model, newmorph))


class NoModelFound(Exception):
    pass


class DeclenseTrainer:

    GROUPS = [
        list("мвнлрй"),
        list("дзжгґб"),
        list("птсцшчпкхф"),
        list("аіуео"),
        list("яїюєь"),
        list("шчщс")
    ]

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
    def analyze(declensions, minsize=2):
        """Produce the declension model for given word.

        Args:
            declensions (dict):
                key (tuple): Morphology vector for given form. See docstring of
                    this module for details.
                value (str): Form of the word.
            minsize (int): Minimal size of the suffix.

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

        # Decrease rootSize, when suffixes are less than minsize
        for word in declensions.values():
            diff = minsize - len(word[rootSize:])
            if diff > 0:
                rootSize -= diff

        model = list()

        for vector, form in declensions.items():
            _insertInto(model, form[rootSize:], *vector)

        return model

    @staticmethod
    def createModel(words, minsize=2):
        """Syntactic sugar for `analyze` method. Works just the same, but with
        the list of words.
        """

        return [DeclenseTrainer.analyze(word, minsize) for word in words]

    @staticmethod
    def generalizeModel(model, groups: list, threshold=.3):
        """Try to generalize your model to groups of given letters.

        For example, suppose we have groups of vowels and consonants.
        Now, if there are rules for suffix 'baa', 'caa', 'daa' and they produce
        the same sequence ('bara', 'cara', 'dara', etc.), we can consider, that
        the same rule will be the truth for all consonants: 'faa', 'gaa' and so
        on.

        You can give as many groups of letters as you want. It depends on the
        morphology rules of the words you're going to make model for.

        Args:
            model (list)
            groups (iterable)
            threshold (float): Minimal ratio of number of letters in the group
                and number of rules, which can be generalized to that group.
                For example, if there are 15 letters in the group, at least 5
                rules (when threshold=.3) should be considered as they belong
                to that group.

        Returns:
            list: Produced model.

        """

        def _generalize(rule, index, group) -> list:
            """Returns a list of rules generalized to a given group.

            Args:
                index (int): Index of the letter which will be generalized.
                    >>> _generalize(
                            ['abc', ...],
                            index=1,
                            group=['b', 'w', 'v'])
                    <<< [['abc', ...], ['awc', ...], [avc, ...]]

            """

            def _putRecursively(l, index, array):
                """Goes through array recursively and put a given letter `l`
                onto given `index`, if element is a string.
                """
                for i, el in enumerate(array):
                    if type(el) is str:
                        array[i] = el[:index] + l + el[index + 1:]
                    else:
                        array[i] = _putRecursively(l, index, el)
                return array

            return [
                _putRecursively(letter, index, rule[:])
                for letter in group
            ]

        def _deleteGroup(array, group, index):
            """Delete all group members from a given array.

            Args:
                array (iterable)
                group (list)
                index (int): An index of letter to be compared with the group's
                    one.

            """

            result = list()
            deleted = None
            counter = 0

            for rule in array:
                try:
                    if Declensor.getZero(rule)[index] not in group:
                        result.append(rule)
                        counter += 1
                    else:
                        deleted = rule
                except IndexError:
                    continue

            return result, counter, deleted

        def _rulesAreIdentical(a, b, index):
            """Check whether two groups are determine the same suffix (without)
            given index.
            """
            if type(a) is type(b) is not list:
                return a[:index] + a[index + 1:] == b[:index] + b[index + 1:]

            return all(
                _rulesAreIdentical(group1, group2, index)
                for group1, group2 in
                zip(a, b)
            )

        # Array of lengths of infinitive suffixes.
        lengths = [
            len(
                Declensor.getZero(
                    rule))
            for rule in model
        ]

        # Generalized groups will be stored here and added to `model` in
        # the end.
        extended = list()

        for group in groups:

            for index in range(0, max(lengths) + 1):

                reduced, counter, element = _deleteGroup(model, group, index)

                if counter < len(group) * threshold or not element:
                    continue

                extended.append(_generalize(element, index, group))
                model = reduced

        return model + extended
