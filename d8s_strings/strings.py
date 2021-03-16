import re
import string
import sys
from typing import Any, Iterable, List, Tuple, Union
import unicodedata

# from textblob import TextBlob


# TODO: add a function to get a substring between two given characters
# TODO: write function to split a given string up into subparts of a given length

NO_ISASCII_AVAILABLE = sys.version_info.major == 3 and sys.version_info.minor <= 6


def string_chars_at_start(string: str, chars: Iterable) -> Iterable[str]:
    """."""
    for char in string:
        if char in chars:
            yield char
        else:
            break


def string_chars_at_start_len(string: str, chars: Iterable) -> int:
    """."""
    return len(list(string_chars_at_start(string, chars)))


def a10n(string: str) -> str:
    """."""
    if len(string) <= 3:
        return string

    abbreviation = f'{string[0]}{len(string[1:-1])}{string[-1]}'
    return abbreviation


def string_remove_index(string: str, index: int) -> str:
    """Remove the item from the string at the given index."""
    string_list = list(string)
    del string_list[index]
    return ''.join(string_list)


def string_replace_index(string: str, index: int, replacement: str) -> str:
    """Replace the character in the string at the given index with the replacement."""
    string_list = list(string)
    string_list[index] = replacement
    return ''.join(string_list)


# def _string_blobify(string: str) -> TextBlob:
#     """Return a textblob for the given string."""
#     return TextBlob(string)


# def string_words(string: str) -> List[str]:
#     blob = _string_blobify(string)
#     return blob.words


def string_remove_before(string: str, stop_string: str):
    """Remove everything from the start of the given string until the stop_string."""
    # we have to re-add the stop_string because otherwise it would not be included
    return f'{stop_string}{string.split(stop_string, maxsplit=1)[-1]}'


def string_remove_after(string: str, start_string: str):
    """Remove everything after the start_string to the end of the given string."""
    split_string = string.split(start_string)
    if len(split_string) > 1:
        # we have to re-add the start_string to the next-to-last item, otherwise, it will not be included
        split_string[-2] += start_string
    return text_join(start_string, *split_string[:-1])


def string_is_palindrome(string: str) -> bool:
    """Return whether or not the given string is a palindrome."""
    is_palindrome = string == string_reverse(string)
    return is_palindrome


def string_reverse(string: str) -> str:
    """Reverse the given string."""
    return string[::-1]


def indefinite_article(word):
    """Return the word with the appropriate indefinite article."""
    inflect_engine = _inflect_engine()
    return inflect_engine.a(word).split(' ')[0]


def is_plural(possible_plural: str) -> bool:
    """Return whether or not the possible_plural is plural."""
    plural = False
    inflect_engine = _inflect_engine()
    pluralized_word = inflect_engine.plural(possible_plural)
    # for possible results from inflect_engine.compare, see https://github.com/jazzband/inflect/blob/master/inflect.py
    result = inflect_engine.compare(possible_plural, pluralized_word)
    if ':' in result:
        first_char = result.split(':')[0]
        if first_char == 'p':
            plural = True
    return plural


def pluralize(word: str) -> str:
    """Make the word plural."""
    inflect_engine = _inflect_engine()
    if is_plural(word):
        return word
    else:
        return inflect_engine.plural(word)


def is_singular(possible_singular: str) -> bool:
    """Return whether or not the possible_singular is singular."""
    # this is a repetition of the code from the is_plural function and does not simply return `not is_plural` because...
    # there are many different responses possible from inflect_engine.compare and there are cases where inflect_engine.compare...
    # cannot compare the two words
    singular = False
    inflect_engine = _inflect_engine()
    pluralized_word = inflect_engine.plural(possible_singular)
    # for possible results from inflect_engine.compare, see https://github.com/jazzband/inflect/blob/master/inflect.py
    result = inflect_engine.compare(possible_singular, pluralized_word)
    if ':' in result:
        first_char = result.split(':')[0]
        if first_char == 's':
            singular = True
    return singular


def singularize(word: str) -> str:
    """Make the word singular."""
    inflect_engine = _inflect_engine()
    if is_singular(word):
        return word
    else:
        return inflect_engine.singular_noun(word)


def cardinalize(word: str, count: int) -> str:
    """Return the appropriate form of the given word for the count."""
    inflect_engine = _inflect_engine()
    if is_singular(word):
        # if the word is singular and the count is one, we can return the word
        if count == 1:
            return word
        word = pluralize(word)
    # I know this is using the singular_noun function, but it will return either singular or plural nouns based on the count argument
    return inflect_engine.singular_noun(word, count=count)


def ordinalize(number: int) -> str:
    """Return the appropriate form for the ordinal form of the given number."""
    inflect_engine = _inflect_engine()
    return inflect_engine.ordinal(number)


def string_forms(text):
    """Return multiple forms for the given text."""
    # it is important to lowercase the text before we start so that we can avoid problems when making the text plural
    text = lowercase(text)

    # TODO: may want to standardize casing of the keys... `uppercase` vs. `kebab_case`... either `uppercase` should be `upperCase` or `kebab_case` should be `kebabcase`
    string_forms = {
        'lowercase': lowercase(text),
        'titlecase': titlecase(text),
        'uppercase': uppercase(text),
        'lowercasePlural': lowercase(pluralize(text)),
        'titlecasePlural': titlecase(pluralize(text)),
        'uppercasePlural': uppercase(pluralize(text)),
        'kebab_case': kebab_case(text),
        'kebab_casePlural': kebab_case(pluralize(text)),
        'snake_case': snake_case(text),
        'snake_casePlural': snake_case(pluralize(text)),
        'camel_case': camel_case(text),
        'camel_casePlural': camel_case(pluralize(text)),
        'pascal_case': pascal_case(text),
        'pascal_casePlural': pascal_case(pluralize(text)),
        'lowercaseIndefiniteArticle': lowercase(indefinite_article(text)),
        'titlecaseIndefiniteArticle': titlecase(indefinite_article(text)),
        'uppercaseIndefiniteArticle': uppercase(indefinite_article(text)),
    }

    return string_forms


def _inflect_engine():
    """Return an inflect engine."""
    import inflect

    p = inflect.engine()
    return p


def string_left_pad(string, length: int, *, padding_characters=' '):
    """Pad the given string with the given padding_characters such that the length of the resulting string is equal to the `length` argument. Adapted from the javascript code here: https://www.theregister.co.uk/2016/03/23/npm_left_pad_chaos/."""
    from .strings_temp_utils import number_evenly_divides

    padding_length = length - len(string)

    if padding_length and not number_evenly_divides(len(padding_characters), padding_length):
        message = f'The length of the padding_characters ({len(padding_characters)}) must evenly divide the desired length of the final string ({length}).'
        raise ValueError(message)
    else:
        padding_length = int(padding_length / len(padding_characters))

    left_padded_string = padding_characters * padding_length + string

    return left_padded_string


def string_to_bool(string: str) -> bool:
    """."""
    if lowercase(string) == 'false':
        return False
    else:
        return True


def text_examples(n=10):
    """Create n example texts."""
    from hypothesis.strategies import text

    from d8s_hypothesis import hypothesis_get_strategy_results

    return hypothesis_get_strategy_results(text, n=n)


def string_has_multiple_consecutive_spaces(string):
    """Return True if the given string has multiple, consecutive spaces."""
    pattern = '.*  +.*'
    match_result = re.match(pattern, string)
    return bool(match_result)


def character_examples(n=10):
    """Create n example characters."""
    from hypothesis.strategies import characters

    from d8s_hypothesis import hypothesis_get_strategy_results

    return hypothesis_get_strategy_results(characters, n=n)


def text_abbreviate(text):
    """Abbreviate the given text."""
    if ' ' not in text:
        # split the word based on uppercased characters
        words = string_split_on_uppercase(text, include_uppercase_characters=True)
    else:
        words = text.split(' ')

    first_letters_of_sufficiently_long_words = [word[0] for word in words if len(word) > 3]
    return ''.join(first_letters_of_sufficiently_long_words).upper()


def text_input_is_yes(message):
    """Get yes/no input from the user and return `True` if the input is yes and `False` if the input is no."""
    message = text_ensure_ends_with(message.rstrip('.').rstrip('?'), ' (y/n)')
    result = input(message).strip()
    return string_is_yes(result)


def text_input_is_no(message):
    """Get yes/no input from the user and return `True` if the input is no and `False` if the input is yes."""
    message = text_ensure_ends_with(message.rstrip('.').rstrip('?'), ' (y/n)')
    result = input(message).strip()
    return string_is_no(result)


def string_is_yes(string):
    """Check if a string is some form of `y` or `yes`."""
    if lowercase(string) == 'y' or lowercase(string) == 'yes':
        return True
    else:
        return False


def string_is_no(string):
    """Check if a string is some form of `n` or `no`."""
    if lowercase(string) == 'n' or lowercase(string) == 'no':
        return True
    else:
        return False


def xor(message, key):
    """."""
    # credits for inspiration to https://stackoverflow.com/a/25475760 and https://en.wikipedia.org/wiki/XOR_cipher#Example_implementation
    from itertools import cycle

    if isinstance(message, str):
        # Text strings contain single characters
        return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(message, cycle(key)))
    else:
        # Python 3 bytes objects contain integer values in the range 0-255
        return bytes_decode_as_string(bytes([a ^ b for a, b in zip(message, cycle(key))]))


def text_join(join_character, *args):
    """Join all of the arguments around the given join_character."""
    sections_to_join = []

    for arg in args:
        sections_to_join.append(arg)

    return join_character.join(sections_to_join)


def string_insert(existing_string, new_string, index):
    """Insert the new_string into the existing_string at the given index."""
    first_section = existing_string[:index]
    second_section = existing_string[index:]
    complete_string = new_string.join([first_section, second_section])
    return complete_string


def base64_encode(input_string):
    """Base64 encode the string."""
    import base64

    return bytes_decode_as_string(base64.b64encode(string_encode_as_bytes(input_string)))


def base64_decode(input_string):
    """Base64 decode the string."""
    import base64

    return bytes_decode_as_string(base64.b64decode(input_string), 'latin-1')


def string_sequence_matcher(string_a, string_b):
    """Create a difflib.SequenceMatcher for the given string."""
    import difflib

    return difflib.SequenceMatcher(None, string_a, string_b)


def strings_diff(string_a, string_b):
    """Return the diff of the two strings."""
    import difflib

    if not isinstance(string_a, list):
        string_a = string_a.splitlines()

    if not isinstance(string_b, list):
        string_b = string_b.splitlines()

    d = difflib.Differ()
    diff = d.compare(string_a, string_b)
    return '\n'.join(diff)


def string_add_to_start_of_each_line(string: str, string_to_add_to_each_line: str):
    """Add the given string_to_add_to_each_line to the beginning of each line in the string."""
    replacement = f'\n{string_to_add_to_each_line}'
    string_with_added_value = re.sub('\n', replacement, string)
    return string_with_added_value


def string_get_closes_matches(word, possible_matches, maximum_matches=3, cutoff=0.6):
    """Return the words from the list of possible matches that are closest to the given word."""
    import difflib

    return difflib.get_close_matches(word, possible_matches, n=maximum_matches, cutoff=cutoff)


# TODO: this can also be used for fuzzy matching... add a tag/rename the function to capture this possibility
def strings_similarity(a: str, b: str):
    """Return the ratio of similarity between the two strings."""
    sequence_matcher = string_sequence_matcher(a, b)

    return sequence_matcher.ratio()


def strings_matching_blocks(a: str, b: str):
    """Return the matching blocks in the given strings."""
    sequence_matcher = string_sequence_matcher(a, b)

    # this function has to be run first so that the sequence_matcher.matching_blocks property is populated
    sequence_matcher.get_opcodes()

    return sequence_matcher.matching_blocks


def strings_longest_matching_block(a: str, b: str):
    """Return the longest matching block in the string."""
    sequence_matcher = string_sequence_matcher(a, b)

    return sequence_matcher.find_longest_match(0, len(sequence_matcher.a), 0, len(sequence_matcher.b))


# TODO: I think I want to singularize the strings_... functions
def strings_diff_opcodes(a: str, b: str):
    """Return the opcodes representing the differences/similarities between two strings."""
    sequence_matcher = string_sequence_matcher(a, b)

    return [i for i in sequence_matcher.get_opcodes()]


def string_common_prefix(a: str, b: str) -> str:
    """Returns the common prefix string from left to right between a and b."""
    from .strings_temp_utils import shortest

    common_prefix = ''

    for index in range(len(shortest([a, b]))):
        if a[index] == b[index]:
            common_prefix += a[index]
        else:
            break

    return common_prefix


def string_common_suffix(a: str, b: str):
    """Returns the common suffix string from left to right between a and b."""
    return string_reverse(string_common_prefix(string_reverse(a), string_reverse(b)))


def characters(input_string):
    """Return all of the characters in the given string."""
    return tuple(input_string)


def hex_to_string(hex_string):
    """Convert the given hex string to ascii."""
    hex_string = hex_string.replace('0x', '').replace(',', '').replace(' ', '')

    return bytes_decode_as_string(bytes.fromhex(hex_string), 'latin-1')


def string_to_hex(ascii_string: str, seperator='') -> str:
    """Convert the given ascii string to hex."""
    hex_string = ''
    for char in ascii_string:
        hex_string += str(hex(character_to_unicode_number(char))).split('x')[-1] + seperator
    hex_string = hex_string.strip(seperator)
    return hex_string


def character_to_unicode_number(character):
    """Convert the given character to its Unicode number. This is the same as the `ord` function in python."""
    return ord(character)


def unicode_number_to_character(unicode_number):
    """Convert the given unicode_number to it's unicode character form. This is the same as the `chr` function in python."""
    return chr(unicode_number)


def hamming_distance(string_1, string_2, as_percent=False):
    """Return the number of positions at which corresponding symbols in string_1 and string_2 are different (this is known as the Hamming Distance). See https://en.wikipedia.org/wiki/Hamming_distance."""
    from .strings_temp_utils import percent

    if len(string_1) != len(string_2):
        raise ValueError('The length of the two strings must be the same')

    hamming_distance = sum(el1 != el2 for el1, el2 in zip(string_1, string_2))

    if as_percent:
        return percent(hamming_distance / len(string_1))
    else:
        return hamming_distance


def from_char_code(integer_list):
    """."""
    return ''.join([chr(int(integer)) for integer in integer_list])


def text_ascii_characters(text: str) -> Tuple[str]:
    """."""
    if NO_ISASCII_AVAILABLE:
        for char in text:
            try:
                char.encode('ascii')
            except UnicodeEncodeError:
                pass  # string is not ascii
            else:
                yield char  # string is ascii
    else:
        for char in text:
            if char.isascii():
                yield char


def text_non_ascii_characters(text: str) -> Tuple[str]:
    """."""
    if NO_ISASCII_AVAILABLE:
        for char in text:
            try:
                char.encode('ascii')
            except UnicodeEncodeError:
                yield char  # string is not ascii
            else:
                pass  # string is ascii
    else:
        for char in text:
            if not char.isascii():
                yield char


# TODO: rename this function
def letter_as_number(letter):
    """."""
    return string.ascii_lowercase.index(lowercase(letter)) + 1


def letter_frequency(letter, text):
    """Find the frequency of the given letter in the given text."""
    return text.count(letter) / len(text)


def string_entropy(text, ignore_case=False):
    """Find the shannon entropy of the text. Inspired by the algorithm here https://web.archive.org/web/20160320142455/https://deadhacker.com/2007/05/13/finding-entropy-in-binary-files/. You can see more here: https://en.wikipedia.org/wiki/Entropy_(information_theory)"""
    import math

    from .strings_temp_utils import deduplicate

    if ignore_case:
        text = text.lower()

    character_code_set = deduplicate([ord(char) for char in text])

    if not text:
        return 0
    entropy = 0
    for char_code in character_code_set:
        p_char = letter_frequency(chr(char_code), text)
        if p_char > 0:
            entropy += -p_char * math.log(p_char, 2)
    return entropy


def substrings(iterable):
    """Find all substrings in the given string."""
    import more_itertools

    return more_itertools.substrings(iterable)


def string_remove_non_alphabetic_characters(string: str):
    """."""
    pass


def string_remove_non_numeric_characters(string: str):
    """."""
    pass


def string_remove_non_alpha_numeric_characters(string: str):
    """."""
    pattern = '[^a-zA-Z\d\s]'
    string_after_removal = string_remove(pattern, string)
    return string_after_removal


def string_remove(regex_pattern, input_string, **kwargs):
    """Remove the regex_pattern from the input_string."""
    string_after_removal = re.sub(regex_pattern, '', input_string, **kwargs)
    return string_after_removal


def string_remove_unicode(string: str):
    """Remove all Unicode characters from the given string."""
    string_with_unicode_removed = bytes_decode_as_string(
        string_encode_as_bytes(string, encoding='ascii', errors='ignore')
    )
    return string_with_unicode_removed


def string_remove_numbers(input_string: str, replacement: str = ' '):
    """Remove all numbers from the input_strings."""
    new_string_without_numbers = re.sub('\d+', replacement, input_string)
    return new_string_without_numbers


def string_remove_from_start(input_string, string_to_remove):
    """Remove the string_to_remove from the start of the input_string."""
    if input_string.startswith(string_to_remove):
        updated_string = string_remove(string_to_remove, input_string, count=1)
        return updated_string
    else:
        return input_string


def string_remove_from_end(input_string, string_to_remove):
    """Remove the string_to_remove from the end of the input_string."""
    if input_string.endswith(string_to_remove):
        desired_string_final_index = len(input_string) - len(string_to_remove)
        updated_string = input_string[:desired_string_final_index]
        return updated_string
    else:
        return input_string


def string_as_numbers(input_string: str):
    """."""
    character_list = list(input_string)
    numbers = []
    for char in character_list:
        numbers.append(letter_as_number(char))
    return numbers


def string_in_iterable_fuzzy(input_string, iterable):
    """Find if the given input_string is in one of the strings in an iterable."""
    for item in iterable:
        if input_string in item:
            return True
    return False


# TODO: I'd like to improve this function to offer more granularity (e.g. offer a flag whether or not the match should be greedy)
def string_find_between(input_string: str, start_string: str, end_string: str, *args):
    """Find the string in the input_string that is between the start_string and the end_string."""
    regex = f'{re.escape(start_string)}(.*){re.escape(end_string)}'
    result = re.findall(regex, input_string, *args)
    if result:
        return result[0]
    else:
        return ''


def switch(a, b, text):
    """Switch a and b in the text."""
    from d8s_uuids import uuid4

    a_replacement = str(uuid4())
    b_replacement = str(uuid4())

    text = text.replace(a, a_replacement)
    text = text.replace(b, b_replacement)

    text = text.replace(a_replacement, b)
    text = text.replace(b_replacement, a)

    return text


def string_encode_as_bytes(input_string, encoding='utf-8', **kwargs):
    if isinstance(input_string, str):
        return input_string.encode(encoding, **kwargs)
    else:
        return input_string


def bytes_decode_as_string(bytes_text, encoding='utf-8', **kwargs):
    if isinstance(bytes_text, bytes):
        return bytes_text.decode(encoding, **kwargs)
    else:
        return bytes_text


def string_shorten(input_string, length, suffix='...'):
    """Shorten the given input_string to the given length."""
    if len(input_string) > length:
        return '{}{}'.format(input_string[: length - len(suffix)], suffix)
    else:
        return input_string


def string_split_without_empty(input_string, split_char):
    """Split a input_string on split_char and remove empty entries."""
    from .strings_temp_utils import list_delete_empty_items

    return list_delete_empty_items(input_string.split(split_char))


def string_has_index(string: str, index: Union[str, int]) -> bool:
    """."""
    from .strings_temp_utils import list_has_index

    string_characters = characters(string)
    has_index = list_has_index(string_characters, index)
    return has_index


def string_split_on_uppercase(input_string: str, include_uppercase_characters=False, split_acronyms=True):
    """Split the input_string on uppercase characters. If split_acronyms is False, the function will not split consecutive uppercase letters."""
    from .strings_temp_utils import list_delete_empty_items

    if not split_acronyms and not include_uppercase_characters:
        message = 'If you set the `split_acronyms` to False when calling the `string_split_on_uppercase` function, you must also set the `include_uppercase_characters` (which you did not). The function will continue, but the `split_acronyms` argument will make no difference.'
        raise ValueError(message)

    uppercase_char_array = [char.isupper() for char in input_string]
    split_string = []
    last_uppercase_character_index = 0

    for index, character_is_upper in enumerate(uppercase_char_array):
        if character_is_upper:
            # if we are not splitting acronyms, check to see if the character is part of an acronym
            if include_uppercase_characters and not split_acronyms:
                previous_character_is_upper = uppercase_char_array[index - 1]
                # if the capital letter is preceded and followed by an uppercase letter, continue
                if previous_character_is_upper:
                    # continue to the next character
                    continue

            # if the first character in the input_string is uppercase (index == 0), we don't need to append anything
            if index > 0:
                split_string.append(input_string[last_uppercase_character_index:index])

            if include_uppercase_characters:
                last_uppercase_character_index = index
            else:
                last_uppercase_character_index = index + 1

    split_string.append(input_string[last_uppercase_character_index:])

    # we are using the list_delete_empty_items function b/c if include_uppercase_characters is False and the last character of the input_string is uppercase, an empty string will be erroneously included in the response from this function
    return list_delete_empty_items(split_string)


def string_split_on_lowercase(input_string, include_lowercase_characters=False):
    """Split the string on lowercase characters."""
    from .strings_temp_utils import list_delete_empty_items

    split_string = []
    last_lowercase_character_index = 0

    for index, character in enumerate(input_string):
        if character.islower():
            # if the first character in the string is lowercase (index == 0), we don't need to append anything
            if index > 0:
                split_string.append(input_string[last_lowercase_character_index:index])

            if include_lowercase_characters:
                last_lowercase_character_index = index
            else:
                last_lowercase_character_index = index + 1

    split_string.append(input_string[last_lowercase_character_index:])

    # see the note from the string_split_on_uppercase function
    return list_delete_empty_items(split_string)


def string_split_multiple(string, *splitting_characters):
    """Split a string up based on multiple splitting_characters."""
    split_strings = []

    if splitting_characters:
        # split the string based on the first character we are splitting on
        first_splitting_character = splitting_characters[0]
        split_string = string.split(first_splitting_character)

        # record the other splitting characters
        other_splitting_characters = splitting_characters[1:]

        # split each substring based on the other_splitting_characters and record the results
        for substring in split_string:
            split_strings.extend(string_split_multiple(substring, *other_splitting_characters))
    else:
        # if there are no more characters to split on, record the string - we're done!
        split_strings.append(string)
    return split_strings


def string_reverse_case(input_string):
    """Make lowercase characters uppercased and visa-versa."""
    string_list = []

    for character in characters(input_string):
        if character.isupper():
            string_list.append(lowercase(character))
        elif character.islower():
            string_list.append(uppercase(character))
        else:
            string_list.append(character)

    return ''.join(string_list)


def text_vowels(text):
    """Return all of the vowels in the text."""
    vowels = []
    for character in text:
        if character in 'aeiou':
            vowels.append(character)
    return vowels


def text_vowel_count(text):
    """Count the number of vowels in the text."""
    vowels = text_vowels(text)
    return len(vowels)


def text_consonants(text):
    """Return all of the consonants in the text."""
    consonants = []
    for character in text:
        if character not in 'aeiou':
            consonants.append(character)
    return consonants


def text_consonant_count(text):
    """Count the number of consonants in the text."""
    consonants = text_consonants(text)
    return len(consonants)


def text_input(message='Enter/Paste your content.'):
    """."""
    # TODO: multiline support is nice, but it breaks jupyter notebooks
    print('{} (<NEWLINE> + Ctrl-D or Ctrl-Z ( windows ) to save it)'.format(message))
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    return '\n'.join(contents)


def text_ensure_starts_with(text: str, prefix: str):
    """Make sure the given text starts with the given prefix."""
    if text.startswith(prefix):
        return text
    else:
        return '{}{}'.format(prefix, text)


def text_ensure_ends_with(text: str, suffix: str):
    """Make sure the given text ends with the given suffix."""
    if text.endswith(suffix):
        return text
    else:
        return '{}{}'.format(text, suffix)


def titlecase(item):
    return _handle_casing(item, 'title')


def uppercase(item):
    return _handle_casing(item, 'upper')


def uppercase_first_letter(text):
    """Make the first letter of the text uppercase."""
    return '{}{}'.format(text[0].upper(), text[1:])


def lowercase_first_letter(text):
    """Make the first letter of the text lowercase."""
    return '{}{}'.format(text[0].lower(), text[1:])


def crazycase(text):
    """Make the case of the characters in the given text pseudo-random"""
    import random

    new_text = ''

    for character in text:
        if character in string.ascii_letters:
            casing_options = (lowercase, uppercase)
            casing_action = random.choice(casing_options)
            character = casing_action(character)
        new_text += character

    return new_text


def kebab_case(text):
    """Return the text with a "-" in place of every space."""
    text = text.replace(' ', '-')
    text = text.replace('_', '-')

    return text


def snake_case(text):
    """Return the text with a "_" in place of every space."""
    text = text.replace(' ', '_')
    text = text.replace('-', '_')

    return text


def camel_case(text: str):
    """Return the text with no spaces and every word (except the first one) capitalized."""
    text = text.replace('-', ' ')
    text = text.replace('_', ' ')
    text_list = [word.title() for word in text.split()]
    text_list[0] = text_list[0].lower()

    return ''.join(text_list)


def pascal_case(text: str):
    """Return the text with no spaces and every word capitalized."""
    text_list = [word.title() for word in text.split()]

    return ''.join(text_list)


def sentence_case(text: str):
    """."""
    # TODO: does this already exist?
    raise NotImplementedError


def uppercase_count(text):
    """Count the number of uppercase letters in the given text."""
    return sum([1 for char in text if char.isupper()])


def lowercase_count(text):
    """Count the number of lowercase letters in the given text."""
    return sum([1 for char in text if char.islower()])


def lowercase(item):
    return _handle_casing(item, 'lower')


# TODO: we should be able to validate the values of the `casing` argument
def _handle_casing(item, casing):
    available_casing_types = ('lower', 'title', 'upper')
    if casing not in available_casing_types:
        message = '! Invalid casing type given: {}\nAvailable casing types are: {}'.format(
            casing, available_casing_types
        )
        raise ValueError(message)
    if isinstance(item, str) or isinstance(item, bytes):
        return eval('item.{}()'.format(casing))
    else:
        print('! Democritus cannot yet {}-case an item of type {}'.format(casing, type(item)))
        return item


def string_rotate(text, rot=13):
    """Return the text converted using a Caesar cipher (https://en.wikipedia.org/wiki/Caesar_cipher) in which the text is rotated by the given amount (using the `rot` argument)."""
    # credit for the algorithm: https://github.com/python/cpython/blob/master/Lib/this.py
    d = {}
    for c in (65, 97):
        for i in range(26):
            d[chr(i + c)] = chr((i + rot) % 26 + c)

    return "".join([d.get(c, c) for c in text])


def text_is_english_sentence(text: str) -> bool:
    """Determine whether or not the sentence is likely English."""
    language_detection_data = text_languages(text)

    if language_detection_data[0]['language'] == 'en' and language_detection_data[0]['probability'] >= 0.5:
        return True

    return False


LEET_SPEAK_CONVERSIONS = {'1': 'i', '3': 'e', '4': 'a', '5': 's', '9': 'g', '0': 'o'}


def leet_speak_to_text(leet_speak_text):
    """."""
    translated_text = ''

    for char in leet_speak_text:
        translated_text += LEET_SPEAK_CONVERSIONS.get(char, char)

    return translated_text


def text_to_leet_speak(text):
    """."""
    from .strings_temp_utils import dict_flip, dict_delistify_values

    conversion_dict = dict_flip(LEET_SPEAK_CONVERSIONS)
    conversion_dict = dict_delistify_values(conversion_dict)
    translated_text = ''

    for char in text:
        translated_text += conversion_dict.get(char, char)

    return translated_text


def unicode_to_ascii(text: str):
    """Convert the text to ascii."""
    # credit to https://stackoverflow.com/questions/1207457/convert-a-unicode-string-to-a-string-in-python-containing-extra-symbols#1207479 for this one
    ascii_string = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return ascii_string
