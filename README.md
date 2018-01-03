# plist-buddy

plist-buddy intends to be a drop-in replacement for MacOS's PlistBuddy tool, but with additional features:

* Command Files: Lists of commands should be stored into files which can be read afterwards

* Environment Variable Expansion: There should be a syntax for expanding environment variables when writing plist files

* Diffing: The tool should be able to diff two plist files with another and create a command file to transform the first to the second file

* Time-Based Diffing: The tool should not only diff two plists with each other, but also a plist at one time with the same plist at another time.

* Format Selection: A command for selecting the format (similar to the -x switch)

* File Selection: A command for selecting the file to work with
