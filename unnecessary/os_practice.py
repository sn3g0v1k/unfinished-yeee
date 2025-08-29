import os
from icecream import ic



# ic("Operating System name: ", os.name)
# ic("Current Operating System Name: ", os.uname())
# ic("Current Working Directory: ", os.getcwd())
# ic("files and folders in cwd: ", os.listdir("."))
# ic("Try to get to a file that ain't exist: ")
# try:
#     filename = "abeme.txt"
#     f = open(filename, mode="r")
#     text = f.read()
#     f.close()
# except IOError:
#     ic("Couldn't get to a file: ", filename)

# path = "/home/sn3g0v1k/Downloads"
# ic(path)
# ic("Only directories: ", [i for i in os.listdir(path=path) if os.path.isdir(os.path.join(path, i))])
# ic("Only files: ", [i for i in os.listdir(path=path) if not os.path.isdir(os.path.join(path, i))])
# ic("Everything: ", [i for i in os.listdir(path=path)])

# path = "/home/sn3g0v1k/Downloads"
# for i in os.scandir(path):
#     if i.is_dir:
#         typ = "dir"
#     elif i.is_file:
#         typ = "file"
#     elif i.is_symlink:
#         typ = "link"
#     else:
#         typ = "unknown"
#     print(i.name, typ)

path = "/home/sn3g0v1k/Download"
if os.access(path, os.F_OK): 
    ic("It exists")
else: 
    ic("Doesn't exists")