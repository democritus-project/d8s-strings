from typing import Iterable, List, Any


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
