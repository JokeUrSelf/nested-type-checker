import unittest
from typing import Union, Optional, Any, Callable
from lib import is_nested_instance


class TestIsNestedInstance(unittest.TestCase):

    def test_true_cases(self):
        self.assertTrue(is_nested_instance(1, int))
        self.assertTrue(is_nested_instance([1], list[int]))
        self.assertTrue(is_nested_instance([1, ""], list[int | str]))
        self.assertTrue(is_nested_instance(1, Union[str, int]))
        self.assertTrue(is_nested_instance("", Union[str, int]))
        self.assertTrue(is_nested_instance("", Optional[str]))
        self.assertTrue(is_nested_instance(None, Optional[str]))
        self.assertTrue(is_nested_instance(1, str | int))
        self.assertTrue(is_nested_instance([1, "", 1], list[Any]))
        self.assertTrue(is_nested_instance([1, "", 1], list))
        for x in [
            {1: [1]},
            {1: [""]},
            {None: [1]},
            {None: [""]},
            {"": [1]},
            {"": [""]},
        ]:
            self.assertTrue(
                is_nested_instance(x, dict[Union[Optional[int], str], list[int | str]])
            )
        self.assertTrue(is_nested_instance((1, 1, 1), tuple[int, ...]))
        self.assertTrue(is_nested_instance({1, (1, 2)}, set[int | tuple[int, ...]]))
        self.assertTrue(
            is_nested_instance(frozenset({1, (1, 2)}), frozenset[int | tuple])
        )

        def f(x: int, y: bool) -> str:
            return ""

        self.assertTrue(is_nested_instance(lambda x: None, Callable))
        self.assertTrue(is_nested_instance(f, Callable[[int, bool], str]))

        class CustomTypeA:
            pass

        self.assertTrue(is_nested_instance([CustomTypeA()], list[CustomTypeA]))

    def test_false_cases(self):
        self.assertRaises(Exception, lambda: is_nested_instance([1, "", 1], list[...]))
        self.assertRaises(Exception, lambda: is_nested_instance([1, "", 1], list[any]))
        self.assertFalse(is_nested_instance([1, ""], list[int]))
        self.assertFalse(is_nested_instance([1, ""], list[str]))
        self.assertRaises(
            TypeError, lambda: is_nested_instance(lambda x: None, callable)
        )


if __name__ == "__main__":
    unittest.main()
