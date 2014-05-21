# coding:utf-8

"""
文件数据处理
"""

filename1="data/1-data"
filename2="data/2-data"
head_file = "data/3-head"
info_file = "data/3-info"

keys=['00','01','10','11']

"""
判断该位点是否有信息
"""
def is_sig(blas):
    elems = {}
    for key in keys:
        elems[key] = 0
    for i in blas:
        elems[i] += 1
    count = elems.values()
    count.sort()
    if 2 <= count[2] :                 #有两个2以上的位点
        return True
    else:
        return False

"""
从文件里得到显著的位点
返回{id:[blas,rs],}
"""
def getsnps(f=filename1):
   snps = {}
   for line in open(f,'r').read().replace("|","").splitlines():
       cons = line.split("\t")
       id = cons[0]
       rs = cons[3]
       blas = cons[6:]
       if is_sig(blas):
           snps[id] = [blas,rs]
   return snps

"""
将文件打包为单体型字符串
返回[[rs,][str(haplos),]]
"""
def get_haplo(f=filename2):
    snps = []
    haplos = []
    for line in open(f,"r").read().replace("|","").splitlines():
        cons = line.split("\t")
        snp = cons[2]                     #SNPrs号
        locs = "".join(cons[5:])
        total_len = len(locs)             #样本单体型数目
        if len(haplos) < total_len:
            haplos = ['']*total_len
        zero_no = locs.count("0")         #‘0’数目
        if zero_no < 2 or zero_no > total_len-2:   #不符合条件
            continue
        snps.append(snp)
        for loc in range(total_len):
            haplos[loc] += locs[loc]
    return [snps,haplos]

def sample_infos(head_file=head_file,info_file=info_file):
    """
    提取样本编号和分类信息
    """
    heads = open(head_file, "r").read().splitlines()[0].split("\t")
    infos = {}
    for line in open(info_file, "r").read().splitlines():
        cons = line.split("\t")
        if len(cons) < 3:
            continue
        infos[cons[0]]=cons[2]
    return [heads, infos]

def snps_samples(f=filename2):
    """
    提取每行snp的位点
    样本之间分割
    """
    snps = []
    for line in open(f,"r").read().replace("|","").splitlines():
        cons = line.split("\t")
        snps.append(cons[2:])
    return snps
