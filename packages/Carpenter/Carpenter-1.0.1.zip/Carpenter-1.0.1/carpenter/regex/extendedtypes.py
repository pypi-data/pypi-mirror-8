'''
Regular expressions for matching special case types that don't directly map via 
standard operators.
'''

import re
from location import _not_prefixed_impl, _not_followed_impl

'''
This matches any integer based number that has a ##,###,### format with a possible '+-' 
prepended. Numbers without comma separators are not matched.
'''
_contains_comma_sep_numerical_impl = (
    # Can start with or without a '-+'
    r"(?:[-+]?"
    # Can have 1 to 3 numbers
    r"[0-9]{1,3}"
    # Then must have sets of 3 numbers separated by commas
    r"(?:,[0-9]{3})+"
    # That can optionally end with a '.' and number
    r"(?:\.[0-9]*)?)")

contains_comma_sep_numerical_regex = re.compile(_contains_comma_sep_numerical_impl)

'''
Like containsCommaSepNumerical but also doesn't allow for 
trailing or following characters other than whitespace
'''
_comma_sep_numerical_impl = (
    r"(?:"+_not_prefixed_impl+
    _contains_comma_sep_numerical_impl+
    _not_followed_impl+r")")

comma_sep_numerical_regex = re.compile(_comma_sep_numerical_impl)

'''
Matches for integer or float types that end in a percentage sign
'''
_percent_numerical_impl = (
    r"(?:"+_not_prefixed_impl+")"
    r"([-+]?"
    r"[0-9]+"
    r"(?:\.[0-9]*)?)"
    r"(?:%+)"
    r"(?:"+_not_followed_impl+")"
    )

percent_numerical_regex = re.compile(_percent_numerical_impl)

'''
Matches for integer or float types that end in a - or + sign
'''
_estimate_numerical_impl = (
    r"(?:"+_not_prefixed_impl+")"
    r"([-+]?"
    r"[0-9]{1,3}"
    r"(?:[,]?[0-9]{3})*"
    r"(?:\.[0-9]*)?)"
    r"(?:[-+]+)"
    r"(?:"+_not_followed_impl+")"
    )

estimate_numerical_regex = re.compile(_estimate_numerical_impl)


