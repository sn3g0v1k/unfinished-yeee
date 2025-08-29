# import os
# from icecream import ic

# notes_directory = "/home/sn3g0v1k/Documents"

# os.mkdir(notes_directory, )


from mdutils.mdutils import MdUtils
from mdutils import Html
mdFile = MdUtils(file_name='Example_Markdown',title='Markdown File Example')
mdFile.create_md_file()
mdFile.write("The following text has been written with ``write`` method. You can use markdown directives to write:" "** bold**, _italics_, ``inline_code``... or ")
mdFile.write("use the following available parameters: \n")
mdFile.write()