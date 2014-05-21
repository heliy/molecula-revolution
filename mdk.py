# coding:utf-8

from data import sample_infos, snps_samples

def sample_group(head, info):
    """
    将head根据info分类
    """
    groups = {}
    for key in head:
        g_id = info[key]
        if groups.has_key(g_id):
            groups[g_id].append(key)
        else:
            groups[g_id]=[key]
    return groups

def sets_group():
    [heads, infos] = sample_infos()
    """
    取前三类数目最大的
    返回{"Group_ID":[样本下标,],}
    """
    all_groups = sample_group(heads, infos)
    lens = [ len(all_groups[group]) for group in all_groups]   #数目
    lens.sort()
    lens.reverse()
    max3 = lens[:3]                       #前三
    max3group = {}
    for group in all_groups:
        if len(all_groups[group]) in max3:
            max3group[group] = [ heads.index(item) for item in all_groups[group]]
    del all_groups, lens, infos, heads
    return max3group

def snp_groups(snps, groups):
    """
    样本分类
    返回[[snp-rs,group-1,group-2,group-3],]
    """
    formats = []
    snps = snps_samples()
    for [snp, samples] in snps:
        snp_cons = [snp]
        for group in groups:
            snp_cons.append("".join([samples[index] for index in groups[group]]))
        formats.append(snp_cons)
    return formats

def run():
    snps = snps_samples()
    groups = sets_group()
    formats = snp_groups(snps, groups)
    return formats
        


