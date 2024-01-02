from collections import OrderedDict
from typing import Any, Generator

from ._decision import decision_tree


__all__ = (
    "IntegerMatcher",
    "LiteralMatcher",
    "Match",
    "Matcher",
    "MatchError",
    "MatchGenerator",
    "StringMatcher",
    "TextMatcher",
    "TupleMatcher",
    "NoneMatcher",
    "OptionalMatcher",
    "OrderedDictMatcher",
    "UnionMatcher"
)


Match = tuple[Any, list[str]]
MatchGenerator = Generator[Match, None, None]


class MatchError(Exception):
    pass


class Matcher:
    def match(self, arguments: list[str]) -> MatchGenerator:
        raise NotImplementedError


def _wrap_matcher(matcher: Matcher):
    def wrapped(arguments: list[str]):
        try:
            for item in matcher.match(arguments):
                yield item, (item[1],), {}
        except MatchError:
            pass

    return wrapped


class IntegerMatcher(Matcher):
    def match(self, arguments: list[str]) -> MatchGenerator:
        try:
            value, *rest = arguments
            value = int(value)
        except ValueError as reason:
            raise MatchError from reason

        yield value, rest


class LiteralMatcher(Matcher):
    def __init__(self, value: str) -> None:
        self._value = value

    def match(self, arguments: list[str]) -> MatchGenerator:
        try:
            value, *rest = arguments
        except ValueError as reason:
            raise MatchError from reason

        if value.lower() != self._value.lower():
            raise MatchError

        yield value, rest


class StringMatcher(Matcher):
    def match(self, arguments: list[str]) -> MatchGenerator:
        try:
            value, *rest = arguments
        except ValueError as reason:
            raise MatchError from reason

        yield value, rest


class TextMatcher(Matcher):
    def match(self, arguments: list[str]) -> MatchGenerator:
        if not arguments:
            raise MatchError

        yield " ".join(arguments), []


class TupleMatcher(Matcher):
    def __init__(self, values: list[Matcher]) -> None:
        self._values = values

    def match(self, arguments: list[str]) -> MatchGenerator:
        matchers = [_wrap_matcher(matcher) for matcher in self._values]

        for decision in decision_tree(matchers)(arguments):
            result = []
            rest = None

            for value, rest in decision:
                result.append(value)

            yield tuple(result), rest


class NoneMatcher(Matcher):
    def match(self, arguments: list[str]) -> MatchGenerator:
        yield None, arguments


OptionalMatcher = lambda value: UnionMatcher(values=[value, NoneMatcher()])


class OrderedDictMatcher(Matcher):
    def __init__(self, values: OrderedDict[str, Matcher]) -> None:
        self._values = values

    def match(self, arguments: list[str]) -> MatchGenerator:
        matcher = TupleMatcher(list(self._values.values()))

        for value, rest in matcher.match(arguments):
            yield OrderedDict(zip(self._values, value)), rest


class UnionMatcher(Matcher):
    def __init__(self, values: list[Matcher]) -> None:
        self._values = values

    def match(self, arguments: list[str]) -> MatchGenerator:
        error = None

        for matcher in self._values:
            try:
                yield from matcher.match(arguments)

                error = None
            except MatchError as reason:
                error = reason

        if error:
            raise error
