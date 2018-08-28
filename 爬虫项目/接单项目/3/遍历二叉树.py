# encoding:utf-8
# Time:2018/08/27/20"47
# 定义二叉树的节点
# from Queue import Queue
import queue


class node(object):
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


# 按层次打印
def level_order(tree):
     if tree==None:
        return
     q=[]
     q.append(tree)
     results={}
     level=0
     current_level_num=1
     nextlevelnum=0
     d=[]
     while q:
         current=q.pop(0)
         current_level_num-=1
         d.append(current.data)
         if current.left!=None:
            q.append(current.left)
            nextlevelnum+=1
         if current.right!=None:
            q.append(current.right)
            nextlevelnum+=1
         if current_level_num==0:
            current_level_num=nextlevelnum
            nextlevelnum=0
            results[level]=d
            d=[]
            level+=1
     return results


tree=node(50,  node(20, node(15)),  node(60, node(30), node(70)))
result = level_order(tree)
for k, v in result.items():
    print('第{}层, 值为: {}'.format(k+1, v))