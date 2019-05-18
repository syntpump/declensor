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

    # Neutral, singular, second
    (3, 0, 1): '',

    # Neutral, singular, third
    (1, 0, 2): '',

    # Neutral, singular, third
    (2, 0, 2): '',

    # Neutral, singular, third
    (3, 0, 2): '',

    # Adjectives in plural do not have gender. Push it to "neutral".
    # Neutral, plural, first
    (3, 1, 0): '',

    # Neutral, plural, first
    (3, 1, 0): '',

    # Neutral, plural, first
    (3, 1, 0): '',

    # Adjectives in first do not have gender. Push it to "neutral".
    # Neutral, singular, first
    (3, 0, 0): '',
}

# Paste here your dict
with open(input("Enter the file to save in: ")) as fp:
    fp.write(
        json.dumps(
            dclua.DeclenseTrainer(noun)))  # Paste here your dict
