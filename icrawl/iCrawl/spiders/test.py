# import pandas as pd
#
# with open('./../../homogenous.csv') as f:
#     content = f.readlines()
# # # you may also want to remove whitespace characters like `\n` at the end of each line
# content = [x.strip() for x in content]
# if content.__contains__("شeیر"):
#     print("yes")
# print(content)
#
# class c:
#     blue = '\033[94m'
#     red = '\033[93m'
#
#
# string = "Marry had. A little lamb"
# part = " had. lamb"
#
# pos = [string.split().index(t) for t in part.split()]
# print(pos)  # prints [1, 4]
# # print(c.blue + (string))
# partwords = part.split()
# for w in string.split():
#     if w in partwords:
#         print(c.red+w)
#     else:
#         print(c.blue+w)
#

import wikipedia
wikipedia.set_lang("fa")
print(wikipedia.page("کاربر:Ehsan j1981").summary)
