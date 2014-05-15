# coding:utf-8

"""
进化iHS
"""
from data import get_haplo
from math import log
from numpy import std,mean

"""
返回snp位点信息
"""
def get_loc_snp(haplos,loc):
    return [haplo[loc] for haplo in haplos]

"""
根据snp_type将haplo_type分为['0-type','1-type']
"""
def split_class(snp_type,haplo_type):
    zero_type = []
    one_type = []
    for ht in haplo_type:
        if snp_type[ht]=='0':
            zero_type.append(ht)
        else:
            one_type.append(ht)
    return zero_type,one_type

def c2(c):
    return c*(c-1)/2

"""
计算ehh值
ehhs为已算好的ehh值
haplos为背景信息
types为已有的单体型分类
loc为本次分类的位点
denominator为总类分母
down=True/False为向上或向下
"""
def ehh_marks(ehhs,haplos,types,loc,denominator,down):
    if loc<0 or loc >= len(haplos[0]): # 已无snp
        return
    new_types = []
    snp_type = get_loc_snp(haplos,loc) # 该位点的snp信息
    for t in types:                         # 对已知的haplo小类
        zero_type,one_type = split_class(snp_type,t)
        if len(zero_type) > 1:  #两个及以上
            new_types.append(zero_type)
        if len(one_type) > 1:
            new_types.append(one_type)
    if len(new_types)==0:          # 已无可分类的单体型
        return
    numerator = 0
    for ty in new_types:
        numerator += c2( int( len(ty) ) )
    ehhs.append(numerator/denominator)
    del types
    if down:
        next_loc = loc + 1
    else:
        next_loc = loc - 1
    ehh_marks(ehhs, haplos, new_types, next_loc, denominator, down)
    

"""
计算haplos中loc位点的EHH值
向上向下均计算
默认`0`为祖先等位,`1`为衍生等位
返回[[祖先等位向上EHH扩展值],[祖先等位向下EHH扩展值],[衍生等位向上EHH扩展值],[衍生等位向上EHH扩展值]]
"""
def ehh(haplos,loc):
    core_type = get_loc_snp(haplos,loc) # 改位点coresnp的分类
    core_haplos = [[],[]]                        # 将haplos分为两类
    for core in range(len(core_type)):
        core_haplos[int(core_type[core])].append(core)
    # core_haplos[0]为coresnp是祖先等位的haplo的序号 
    # core_haplos[1]为coresnp是衍生等位的haplo的序号
    ancestral_haplos = [core_haplos[0][:]] # 祖先等位最初分类
    ances_deno = float(c2(len(ancestral_haplos[0])))
    derived_haplos = [core_haplos[1][:]]   # 衍生等位最初分类
    deriv_deno = float(c2(len(derived_haplos[0])))
    up_ancestral,down_ancestral,up_derived,down_derived = [],[],[],[]
    ehh_marks(up_ancestral, haplos, ancestral_haplos, loc-1, ances_deno, False)
    ehh_marks(up_derived, haplos, derived_haplos, loc-1, deriv_deno, False)
    ehh_marks(down_ancestral, haplos, ancestral_haplos, loc+1, ances_deno, True)
    ehh_marks(down_derived, haplos, derived_haplos, loc+1, deriv_deno, True)
    if loc==0:
        print down_ancestral
    return [up_ancestral,down_ancestral,up_derived,down_derived]    

"""
获得未标准化的iHS值
"""
def unstand_ihs(haplos,snp_len):
    ihss=[]
    for snp_no in range(snp_len):
        [up_ance,down_ance,up_deri,down_deri] = ehh(haplos,snp_no)
        # 积分为求和
        ihss.append(
            log(
                ( sum(up_deri)+ sum(down_deri) ) /
                ( sum(up_ance)+ sum(down_ance) )
                )
            )
    return ihss
"""
标准化后的iHS值
"""
def ihs():
    [snps,haplos] = get_haplo()
    snp_len = len(snps)    
    marks = unstand_ihs(haplos, snp_len)
    ep = mean(marks)
    sd = std(marks)
    for m in range(snp_len):
        print snps[m]+":"+str((marks[m]-ep)/sd)

if __name__=="__main__":
    ihs()
