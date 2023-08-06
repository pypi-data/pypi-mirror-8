import functools
import re

from flex.constants import (
    PATH,
)
from flex.parameters import (
    find_parameter,
    type_cast_parameters,
)


REGEX_REPLACEMENTS = (
    ('\.', '\.'),
    ('\{', '\{'),
    ('\}', '\}'),
)


def escape_regex_special_chars(api_path):
    """
    Turns the non prametrized path components into strings subtable for using
    as a regex pattern.  This primarily involves escaping special characters so
    that the actual character is matched in the regex.
    """
    def substitute(string, replacements):
        pattern, repl = replacements
        return re.sub(pattern, repl, string)

    return functools.reduce(substitute, REGEX_REPLACEMENTS, api_path)


# matches the parametrized parts of a path.
# eg. /{id}/ matches the `{id}` part of it.
PARAMETER_REGEX = re.compile('(\{[^\}]+})')


def construct_parameter_pattern(parameter):
    """
    Given a parameter definition returns a regex pattern that will match that
    part of the path.
    """
    name = parameter['name']

    return "(?P<{name}>.+)".format(name=name)


def process_path_part(part, parameters):
    """
    Given a part of a path either:
        - If it is a parameter:
            parse it to a regex group
        - Otherwise:
            escape any special regex characters
    """
    if PARAMETER_REGEX.match(part):
        parameter_name = part.strip('{}')
        try:
            parameter = find_parameter(parameters, name=parameter_name, in_=PATH)
        except ValueError:
            pass
        else:
            return construct_parameter_pattern(parameter)
    return escape_regex_special_chars(part)


def get_parameter_names_from_path(api_path):
    return tuple(p.strip('{}') for p in PARAMETER_REGEX.findall(api_path))


def path_to_pattern(api_path, parameters):
    """
    Given an api path, possibly with parameter notation, return a pattern
    suitable for turing into a regular expression which will match request
    paths that conform to the parameter definitions and the api path.
    """
    parts = re.split(PARAMETER_REGEX, api_path)
    pattern = ''.join((process_path_part(part, parameters) for part in parts))

    if not pattern.startswith('^'):
        pattern = "^{0}".format(pattern)
    if not pattern.endswith('$'):
        pattern = "{0}$".format(pattern)

    return pattern


def path_to_regex(api_path, parameters):
    pattern = path_to_pattern(api_path, parameters)
    return re.compile(pattern)


def match_request_path_to_api_path(path_definitions, request_path, base_path=''):
    """
    Given a request_path and a set of api path definitions, return the one that
    matches.

    Anything other than exactly one match is an error condition.
    """
    if request_path.startswith(base_path):
        request_path = request_path[len(base_path):]

    # Convert all of the api paths into Path instances for easier regex matching.
    paths = {
        p: path_to_regex(p, (v or {}).get('parameters', {}))
        for p, v in path_definitions.items()
    }

    matches = [p for p, r in paths.items() if r.match(request_path)]

    if not matches:
        raise LookupError('No paths found for {0}'.format(request_path))
    elif len(matches) > 1:
        raise LookupError('Multipue paths found for {0}.  Found `{1}`'.format(
            request_path, matches,
        ))
    else:
        return matches[0]


def get_path_parameter_values(request_path, api_path, path_parameters):
    raw_values = path_to_regex(
        api_path,
        path_parameters,
    ).match(request_path).groupdict()
    return type_cast_parameters(raw_values, path_parameters)
