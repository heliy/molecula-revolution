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
    返回{snp-rs:
            {"bases":[allele-one,allele-two],
             "group":[group-1,group-2,group-3],},
        }
    """
    formats = {}
    for cons in snps:
        snp = {}
        snp["bases"] = cons[1:3]
        snp["group"] = []
        samples = cons[3:]
        for group in groups:
            snp["group"].append("".join(
                [samples[index] for index in groups[group]]))
        formats[cons[0]]=snp
    return formats

def fix_poly(formats):
    fix = []
    poly = []
    for snp in formats:
        if sum([ len(set(locs)) for locs in formats[snp]["group"]]) == 3:
            fix.append(snp)
        else:
            poly.append(snp)
    return [fix, poly]
        

def run():
    snps = snps_samples()
    groups = sets_group()
    formats = snp_groups(snps, groups)
    [fix, poly] = fix_poly(formats)
    return fix,poly


