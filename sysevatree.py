# coding:utf-8

"""
构建最大简约法进化系统发育树
使用 sh:
python sysevatree data > eva-tree.txt
"""

import sys
from data import getsnps,keys
from utils import min_key

"""
树节点类
"""
class Node(object):

    #初始化
    def __init__(self,data,left,right):
        self.data=data
        self.left=left
        self.right=right
        
    # 方便print
    def __str__(self,level=0):
        s=("[--"*level)+str(self.data)+"\n"
        if self.left!=None:
            s=s+self.left.__str__(level+1)
        if self.right!=None:
            s=s+self.right.__str__(level+1)
        return s

    # 从子节点推断可能的取值和相应的得分
    def simi_data(self):
        if(isinstance(self.data,str)):
            return  {self.data:0}
        else:
            l_simi=self.left.simi_data()
            r_simi=self.right.simi_data()
            self.data={}
            for key in keys:
                
                if key in l_simi.keys() and key in r_simi.keys() :  #共有
                    self.data[key]=l_simi[key]+r_simi[key]
                elif key in l_simi.keys():                          #left有right没有
                    self.data[key]=l_simi[key]+min(r_simi.values())+1
                elif key in r_simi.keys():
                    self.data[key]=r_simi[key]+min(l_simi.values())+1
                else:
                    continue
            return self.data
    
    # 从父节点推断自己的取值
    def eva_data(self,up):
        if(isinstance(self.data,str)):
            return
        else:
            if up.keys()[0] in self.data.keys():                   # 与父节点相同
                key=up.keys()[0]
            else:                                                  # 最优节点
                key=min_key(self.data)
            self.data={key:self.data[key]}
            self.left.eva_data(self.data)
            self.right.eva_data(self.data)
                
"""
         N0
        /  \
       /    \
      /      N1
     /      /  \
    /      /    \
   /       N2    \  
  /       / \     \
  N3     /  N4    N5
 / \    /  / \   / \
L0 L1  L2 L3 L4 L5 L6
"""

"""
发生树类
"""
class Tree(object):
    def __init__(self,blas):
        self.leaves=[Node(data=ls,left=None,right=None) for ls in blas]
        node3=Node(data=None,left=self.leaves[0],right=self.leaves[1])
        node4=Node(data=None,left=self.leaves[3],right=self.leaves[4])
        node5=Node(data=None,left=self.leaves[5],right=self.leaves[6])
        node2=Node(data=None,left=self.leaves[2],right=node4)
        node1=Node(data=None,left=node2,right=node5)
        node0=Node(data=None,left=node3,right=node1)
        self.nodes=[node0,node1,node2,node3,node4,node5]
        self.root=node0

    def __str__(self):
        return self.root.__str__()
          
    def tree_print(self):
        format="""
         %s
        /  \\
       /    \\
      /      %s
     /      /  \\
    /      /    \\
   /      %s     \\ 
  /       / \\     \\
  %s     /  %s    %s
 / \\    /   / \\   / \\
%s  %s %s  %s %s %s %s
"""
        strs=tuple([str(node.data.keys()[0]) for node in self.nodes]+[str(leaf.data) for leaf in self.leaves])
        print format % strs
         
    # 最优情况时的根节点
    def __get_best_root(self):
        simi_root=self.root.simi_data()
        key=min_key(simi_root)
        return {key:simi_root[key]}

    # 将最优情况推行至全树
    def take_eva(self):
        best_root=self.__get_best_root()
        self.root.eva_data(best_root)
        return best_root.values()[0]


                
if __name__=="__main__":
    snps=getsnps()
    total=0
    for id in snps.keys():
        [blas,rs]=snps[id]
        tree=Tree(blas)
        va=tree.take_eva()
        total=total+va
        print rs,":",va
        tree.tree_print()
        print "========================="

    print total
