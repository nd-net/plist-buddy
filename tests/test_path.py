import unittest
from path import Path

class TestPath(unittest.TestCase):

    def test_empty_path(self):
        self.assertEqual(Path().components, tuple())
        self.assertFalse(Path())

    def test_1_element_path_with_strings(self):
        self.assertEqual(Path("hello").components, ("hello", ))
        self.assertTrue(Path("hello"))

    def test_1_element_path_with_paths(self):
        self.assertEqual(Path(Path("hello")).components, ("hello", ))

    def test_1_element_path_with_other_type(self):
        with self.assertRaises(TypeError):
            Path(2)
        
    def test_2_element_path_with_strings(self):
        self.assertEqual(Path("hello", "world").components, ("hello", "world"))
        
    def test_2_element_path_with_paths(self):
        self.assertEqual(Path(Path("hello"), Path("world")).components, ("hello", "world"))

    def test_2_element_path_with_empty_parts(self):
        self.assertEqual(Path("hello", "", "world").components, ("hello", "world"))
        
    def test_eq(self):
        self.assertEqual(Path(), Path())
        self.assertEqual(Path("hello", "world"), Path("hello", "world"))
        self.assertNotEqual(Path("hello", "world"), Path("foo", "bar"))

    def test_str(self):
        self.assertEqual(str(Path()), ":")
        self.assertEqual(str(Path("hello")), ":hello")
        self.assertEqual(str(Path("hello", "world")), ":hello:world")

    def test_repr(self):
        self.assertEqual(repr(Path("hello", "world")), "Path('hello', 'world')")

    def test_join(self):
        self.assertEqual(Path("foo", "bar").join("baz"), Path("foo", "bar", "baz"))
        self.assertEqual(Path("foo", "bar").join(Path("baz")), Path("foo", "bar", "baz"))
