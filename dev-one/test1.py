# a = 2 ** 10 + 1
# print(a)
#
# import unittest
#
# for i in range(1, 10):
#     for j in range(1, i + 1):
#         print("{}*{} = {} ".format(i, j, (i * j)), end="")
#     print()


# def bubble_sort_for(lst):
#     for i in range(1, len(lst)):
#         for j in range(0, len(lst) - i):
#             if lst[j] > lst[j + 1]:  # 升序用>，降序用<
#                 lst[j], lst[j + 1] = lst[j + 1], lst[j]
#             print(lst)
# 冒泡排序
#
#
# if __name__ == '__main__':
#     a = [1, 3, 2, 8, 4]
#     bubble_sort_for(a)

# #  鸡兔同笼
# title = int(input("头部："))
# jinjia = int(input("脚："))
# numners = jinjia - (title * 2)
# tu = numners // 2
# ji = title - tu
# print("兔子是%s只,鸡是%s只" % (tu, ji))

# strs = 'you are the sunshine!'
# # lists = []
# # for i in strs: #这里是解题的关键1
# #     lists.append(i)
# # print(lists)
# # lists = lists[::-1]#这里是解题的关键2
# # print(lists)
# # strs2 = ''
# # for j in range(len(lists)):
# #     strs2 += lists[j]
# # print(strs2)
# print('you are the sunshine!'[::-1])


# class Node(object):
#     '''定义单链表节点类'''
#
#     def __init__(self, data, next=None):
#         '''data为数据项，next为下一节点的链接，初始化节点默认链接为None'''
#         self.data = data
#         self.next = next
#
#
# # 定义3个节点对象分别为node1、node2和node3
# node1 = None
# node2 = Node(1, None)
# node3 = Node('hello', node2)
# print(node1, node2.data, node2, node3.next)


# a = [['1','2'] for i in range(2)]
#
# b = [['1','2']]*2
#
# a[0][1] = '3'
#
# b[0][0] = '4'
#
# print(a,b)
print("\033[2;31m java.lang.IllegalArgumentException: KFC CrazyThursday need transfer 50$ to Jesse wechat\033[0m")

# import re
#
# str1 = "Python's features"
# str2 = re.match(r'(.*)on(.*?) .*', str1, re.M | re.I)
# print(str2.group1(1))
#
