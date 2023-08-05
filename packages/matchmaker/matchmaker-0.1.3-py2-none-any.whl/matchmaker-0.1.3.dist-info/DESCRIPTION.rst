Decorators that simplify the creation of Hamcrest matchers.

>From a function (with an optional appropriate docstring), create
hamcrest matchers with minimum extra coding.

The sources can be found in GitHub_.

.. _GitHub: https://github.com/txels/matchmaker/

Examples::

    from matchmaker import matcher

    @matcher
    def is_even(item):
        return item % 2 == 0

    @matcher
    def ends_like(item, data, length=3):
        "String whose last {1} chars match those for '{0}'"
        return item.endswith(data[-length:])

You can then use these in your tests as::

    assert_that(number, is_even())
    assert_that(word, ends_like(other_word, 4))

Errors will display as::

    AssertionError:
    Expected: Is even
         but: was <3>

    AssertionError:
    Expected: String whose last 4 chars match those for 'cello'
         but: was 'hullo'


