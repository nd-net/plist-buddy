import unittest, io
from file_reader import read_lines

def striplead(text):
    if text.startswith("\n"):
        index = 1
        while index < len(text) and text[index] in " \t":
            index += 1
        replacement = text[:index]
        text = text[index:].replace(replacement, "\n")
    return text

def stream(text="", encoding="utf-8", prefix=None, bom=False):
    encoded = striplead(text).encode(encoding)
    if prefix:
        prefix = striplead(prefix).strip() + "\n"
        encoded = prefix.encode(encoding if bom else "utf-8") + encoded
    if bom:
        encoded = "\ufeff".encode(encoding) + encoded
    return io.BytesIO(encoded)

class TestFileReader(unittest.TestCase):
    
    def test_read_empty(self):
        self.assertEqual(list(read_lines(stream())), [])

    def test_read_non_empty_without_anything(self):
        self.assertEqual(list(read_lines(stream(
            encoding="ascii",
            text="""
            foo
            bar
            baz
            """
        ))), [
            "foo\n", "bar\n", "baz\n",
        ])
        self.assertEqual(list(read_lines(stream(
            encoding="utf-8", 
            text="""
            föø
            bär
            båz
            """
        ))), [
            "föø\n", "bär\n", "båz\n",
        ])

    def test_read_non_empty_with_initial_encoding(self):
        self.assertEqual(list(read_lines(stream(
            encoding="iso-8859-1",
            text="""
            föø
            bär
            båz
            """
        ), "iso-8859-1")), [
            "föø\n", "bär\n", "båz\n",
        ])

    # def test_read_non_empty_with_bom(self):
    #     self.assertEqual(list(read_lines(stream(
    #         encoding="utf-8",
    #         bom=True,
    #         text="""
    #         föø
    #         bär
    #         båz
    #         """
    #     ))), [
    #         "föø\n", "bär\n", "båz\n",
    #     ], "UTF-8")
    #     self.assertEqual(list(read_lines(stream(
    #         encoding="utf-16-be",
    #         bom=True,
    #         text="""
    #         föø
    #         bär
    #         båz
    #         """
    #     ))), [
    #         "föø\n", "bär\n", "båz\n",
    #     ], "UTF-16")
    #
    # def test_read_non_empty_with_comment_in_first_line(self):
    #     self.assertEqual(list(read_lines(stream(
    #         encoding="utf-8",
    #         prefix="""
    #         # coding: utf-8
    #         """,
    #         text="""
    #         föø
    #         bär
    #         båz
    #         """
    #     ))), [
    #         "# coding: utf-8\n",
    #         "föø\n", "bär\n", "båz\n",
    #     ], "UTF-8")
    #     self.assertEqual(list(read_lines(stream(
    #         encoding="utf-16-be",
    #         prefix="""
    #         # coding: utf-16-be
    #         """,
    #         text="""
    #         föø
    #         bär
    #         båz
    #         """
    #     ))), [
    #         "# coding: utf-16-be\n",
    #         "föø\n", "bär\n", "båz\n",
    #     ], "UTF-16")
    #
    # def test_read_non_empty_with_comment_in_first_line_and_bom(self):
    #     self.assertEqual(list(read_lines(stream(
    #         encoding="utf-8",
    #         bom=True,
    #         prefix="""
    #         # coding: utf-8
    #         """,
    #         text="""
    #         föø
    #         bär
    #         båz
    #         """
    #     ))), [
    #         "# coding: utf-8\n",
    #         "föø\n", "bär\n", "båz\n",
    #     ], "UTF-8")
    #     self.assertEqual(list(read_lines(stream(
    #         encoding="utf-16-be",
    #         bom=True,
    #         prefix="""
    #         # coding: utf-16-be
    #         """,
    #         text="""
    #         föø
    #         bär
    #         båz
    #         """
    #     ))), [
    #         "# coding: utf-16-be\n",
    #         "föø\n", "bär\n", "båz\n",
    #     ], "UTF-16")
    #     self.assertEqual(list(read_lines(stream(
    #         encoding="utf-16-be",
    #         bom=True,
    #         prefix="""
    #         # coding: utf-16
    #         """,
    #         text="""
    #         föø
    #         bär
    #         båz
    #         """
    #     ))), [
    #         "# coding: utf-16\n",
    #         "föø\n", "bär\n", "båz\n",
    #     ], "UTF-16 without endianness in comment")
    #     with self.assertRaises(ValueError):
    #         list(read_lines(stream(
    #             encoding="utf-16-be",
    #             bom=True,
    #             prefix="""
    #             # coding: utf-8
    #             """,
    #             text="""
    #             föø
    #             bär
    #             båz
    #             """)))
    #
    # def test_read_non_empty_with_comment_in_second_line(self):
    #     self.assertEqual(list(read_lines(stream(
    #         encoding="utf-8",
    #         prefix="""
    #         #!/bin/foo
    #         # coding: utf-8
    #         """,
    #         text="""
    #         föø
    #         bär
    #         båz
    #         """
    #     ))), [
    #         "#!/bin/foo\n",
    #         "# coding: utf-8\n",
    #         "föø\n", "bär\n", "båz\n",
    #     ], "UTF-8")
    #     self.assertEqual(list(read_lines(stream(
    #         encoding="utf-16-be",
    #         prefix="""
    #         #!/bin/foo
    #         # coding: utf-16-be
    #         """,
    #         text="""
    #         föø
    #         bär
    #         båz
    #         """
    #     ))), [
    #         "#!/bin/foo\n",
    #         "# coding: utf-16-be\n",
    #         "föø\n", "bär\n", "båz\n",
    #     ], "UTF-16")
    #
    # def test_read_non_empty_with_comment_in_first_and_second_line(self):
    #     self.assertEqual(list(read_lines(stream(
    #         encoding="utf-8",
    #         prefix="""
    #         # coding: utf-8
    #         # coding: utf-16-be
    #         """,
    #         text="""
    #         föø
    #         bär
    #         båz
    #         """
    #     ))), [
    #         "# coding: utf-8\n",
    #         "# coding: utf-16-be\n",
    #         "föø\n", "bär\n", "båz\n",
    #     ], "UTF-8")
    #     self.assertEqual(list(read_lines(stream(
    #         encoding="utf-16-be",
    #         prefix="""
    #         # coding: utf-16-be
    #         """,
    #         text="""
    #         # coding: utf-8
    #         föø
    #         bär
    #         båz
    #         """
    #     ))), [
    #         "# coding: utf-16-be\n",
    #         "# coding: utf-8\n",
    #         "föø\n", "bär\n", "båz\n",
    #     ], "UTF-16")
