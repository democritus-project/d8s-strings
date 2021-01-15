import functools
from typing import Dict, Iterable, List, Any, Union

PYTHON_TYPES_NOT_ALLOWED_AS_DICT_KEYS = (dict, list, set)


def deduplicate(iterable: Iterable) -> list:
    """Deduplicate the iterable."""
    # TODO: will this work for every type except for dicts???
    deduplicated_list = list(set(iterable))
    return deduplicated_list


def sort_by_length(list_arg: List[Any], **kwargs) -> List[Any]:
    """."""
    sorted_list = sorted(list_arg, key=lambda x: len(x), **kwargs)
    return sorted_list


def shortest(list_arg: list) -> Any:
    """."""
    shortest_item = sort_by_length(list_arg)[0]
    return shortest_item


def list_has_index(list_: list, index: Union[str, int]):
    """."""
    index_int = int(index)
    if index_int >= 0 and index_int <= len(list_) - 1:
        return True
    else:
        return False


def list_delete_empty_items(list_arg: list) -> list:
    """Delete items from the list_arg is the item is an empty strings, empty list, zero, False or None."""
    empty_values = ('', [], 0, False, None)
    # TODO: not sure if this is the right way to implement this
    return [i for i in list_arg if i not in empty_values]


def number_evenly_divides(a, b):
    """Return True if a evenly divides b. Otherwise, return False."""
    b_by_a_remainder = b % a
    evenly_divides = b_by_a_remainder == 0
    return evenly_divides


def percent(ratio):
    """Return the ratio as a percentage."""
    if ratio <= 1 and ratio >= 0:
        return round(ratio * 100, 2)
    else:
        # TODO: not sure what to do here
        raise RuntimeError


def is_valid_dict_key(key: Any) -> bool:
    """Return whether or not a dictionary could have the given key."""
    type_is_invalid_key = type(key) in PYTHON_TYPES_NOT_ALLOWED_AS_DICT_KEYS
    return not type_is_invalid_key


def copy_first_arg_dict(func):
    """If the first arg is a dictionary, pass a copy of the dictionary into func."""
    import copy

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        first_arg_dict = args[0]
        other_args = args[1:]

        if isinstance(first_arg_dict, dict):
            first_arg_dict_copy = copy.deepcopy(first_arg_dict)
            return func(first_arg_dict_copy, *other_args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


@copy_first_arg_dict
def dict_add(dictionary: Dict[Any, List[Any]], key: Any, value: Any) -> Dict[Any, List[Any]]:
    """Add the given value to the dictionary at the given key. This function expects that all values of the dictionary parameter are lists."""
    if key in dictionary:
        if not isinstance(dictionary[key], list):
            message = f'The value at the "{key}" key in the dictionary is not a list and the dict_add function requires all values to be a list.'
            raise TypeError(message)
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]
    return dictionary


def dict_flip(dictionary: dict, *, flatten_values: bool = False, flip_lists_and_sets: bool = False) -> dict:
    """Flip the dictionary's keys and values; all of the values become keys and keys become values."""
    import copy

    new_dict = {}

    for key, value in dictionary.items():
        if not is_valid_dict_key(value):
            if flip_lists_and_sets and isinstance(value, (list, set)):
                temp_dict = copy.deepcopy(new_dict)
                for i in value:
                    try:
                        temp_dict = dict_add(temp_dict, i, key)
                    except TypeError as e:
                        message = f'Unable to flip <<{value}>> because it contains items of a type which cannot be the keys for dictionaries.'
                        raise TypeError(message)
                else:
                    new_dict.update(temp_dict)
        else:
            new_dict = dict_add(new_dict, value, key)

    if flatten_values:
        new_dict = dict_delistify_values(new_dict)

    return new_dict


@copy_first_arg_dict
def dict_delistify_values(dictionary: dict) -> dict:
    """For all values in the given dictionary that are lists whose lengths are one, replace the list of length one with the value in the list."""
    # TODO: it would be nice to be able to do this iteratively throughout a dict... currently it only goes through the first level of values - adding a recursive option would be nice... would this principle apply to other functions in this library?
    for k, v in dictionary.items():
        if isinstance(v, list) and len(v) == 1:
            dictionary[k] = v[0]
    return dictionary
