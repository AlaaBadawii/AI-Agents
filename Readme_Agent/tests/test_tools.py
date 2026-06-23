"""Test tools"""

from ..tools import list_files, read_file_content, terminate

print(list_files())

print(read_file_content("tools.py"))
terminate("End of test")
