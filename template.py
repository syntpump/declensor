"""This is a template how declension models can be created.
"""

import dclua
import json

# Create declensions with one of the following template

noun = {
    # Infinitive
    (0, 0): '',

    # Singular, nominative
    (1, 0): '',

    # Singular, genitive
    (1, 1): '',

    # Singular, dative
    (1, 2): '',

    # Singular, accusative
    (1, 3): '',

    # Singular, instrumental
    (1, 4): '',

    # Singular, locative
    (1, 5): '',

    # Singular, vocative
    (1, 6): '',

    # Plural, nominative
    (2, 0): '',

    # Plural, genitive
    (2, 1): '',

    # Plural, dative
    (2, 2): '',

    # Plural, accusative
    (2, 3): '',

    # Plural, instrumental
    (2, 4): '',

    # Plural, locative
    (2, 5): '',

    # Plural, vocative
    (2, 6): ''
}

verb = {
    # Infinitive
    (0, 0, 0, 0): '',

    # Verbs in present, first, singular has no gender, so push it to "neutral"
    # Present, first, singular, neutral
    (1, 0, 0, 2): '',

    # Verbs in present, first, plural has no gender, so push it to "neutral"
    # Present, first, plural, neutral
    (1, 0, 1, 2): '',

    # Verbs in present, second, singular has no gender, so push it to "neutral"
    # Present, second, singular, neutral
    (1, 1, 0, 2): '',

    # Verbs in present, second, plural has no gender, so push it to "neutral"
    # Present, second, plural, neutral
    (1, 1, 1, 2): '',

    # Verbs in present, third, singular has no gender, so push it to "neutral"
    # Present, third, singular, neutral
    (1, 2, 0, 2): '',

    # Verbs in present, third, plural has no gender, so push it to "neutral"
    # Present, third, plural, neutral
    (1, 2, 1, 2): '',

    # Verbs in future, first, singular has no gender, so push it to "neutral"
    # Future, first, singular, neutral
    (2, 0, 0, 2): '',

    # Verbs in future, first, plural has no gender, so push it to "neutral"
    # Future, first, plural, neutral
    (2, 0, 1, 2): '',

    # Verbs in future, second, singular has no gender, so push it to "neutral"
    # Future, second, singular, neutral
    (2, 1, 0, 2): '',

    # Verbs in future, second, plural has no gender, so push it to "neutral"
    # Future, second, plural, neutral
    (2, 1, 1, 2): '',

    # Verbs in future, third, singular has no gender, so push it to "neutral"
    # Future, third, singular, neutral
    (2, 2, 0, 2): '',

    # Verbs in future, third, plural has no gender, so push it to "neutral"
    # Future, third, plural, neutral
    (2, 2, 1, 2): '',

    # Verbs in past has no person, so push it to "first"
    # Past, first, singular, masculine
    (3, 0, 0, 0): '',

    # Past, first, singular, feminine
    (3, 0, 0, 1): '',

    # Past, first, singular, neutral
    (3, 0, 0, 2): '',

    # Verbs in past, first, plural do not have gender, push it to "neutral".
    # Past, first, plural, neutral
    (3, 0, 1, 2): '',
}

adjective = {
    # Infinitive
    (0, 0, 0): '',

    # Nominative, singular, masculine
    (1, 0, 0): '',

    # Nominative, singular, feminine
    (1, 0, 1): '',

    # Nominative, singular, neutral
    (1, 0, 2): '',

    # Genitive, singular, masculine
    (2, 0, 0): '',

    # Genitive, singular, feminine
    (2, 0, 1): '',

    # Genitive, singular, neutral
    (2, 0, 2): '',

    # Dative, singular, masculine
    (3, 0, 0): '',

    # Dative, singular, feminine
    (3, 0, 1): '',

    # Dative, singular, neutral
    (3, 0, 2): '',

    # Accusative, singular, masculine
    (4, 0, 0): '',

    # Accusative, singular, feminine
    (4, 0, 1): '',

    # Accusative, singular, neutral
    (4, 0, 2): '',

    # Instrumental, singular, masculine
    (5, 0, 0): '',

    # Instrumental, singular, feminine
    (5, 0, 1): '',

    # Instrumental, singular, neutral
    (5, 0, 2): '',

    # Locative, singular, masculine
    (6, 0, 0): '',

    # Locative, singular, feminine
    (6, 0, 1): '',

    # Locative, singular, neutral
    (6, 0, 2): '',

    # Adjectives in plural do not have gender, put it to `neutral`
    # Nominative, plural, neutral
    (1, 1, 0): '',

    # Genitive, plural, neutral
    (2, 1, 0): '',

    # Dative, plural, neutral
    (3, 1, 0): '',

    # Accusative, plural, neutral
    (4, 1, 0): '',

    # Instrumental, plural, neutral
    (5, 1, 0): '',

    # Locative, plural, neutral
    (6, 1, 0): ''
}

# Paste here your dict
with open(input("Enter the file to save in: ")) as fp:
    fp.write(
        json.dumps(
            dclua.DeclenseTrainer(noun)))  # Paste here your dict
