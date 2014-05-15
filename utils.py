# coding:utf-8

"""
字典里最小value对应的key
"""
def min_key(dic):
    min_value=min(dic.values())
    for key in dic.keys():
        if dic[key]==min_value:
            return key          
