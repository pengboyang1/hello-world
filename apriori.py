# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 19:00:55 2018
apriori.py
@author: lenovo
Ck k候选项集
Lk K频繁项集
"""
def load_data_set():
    data_set=[['l1', 'l2', 'l5'], ['l2', 'l4'], ['l2', 'l3'],
            ['l1', 'l2', 'l4'], ['l1', 'l3'], ['l2', 'l3'],
            ['l1', 'l3'], ['l1', 'l2', 'l3', 'l5'], ['l1', 'l2', 'l3']]
    return data_set


def create_C1(data_set):
    '''创建第一个候选项集 只包含一个元素'''
    C1=set()
    for t in data_set:
        for item in t:
            item_set=frozenset([item])
            C1.add(item_set)
    return C1


def create_Ck(Lksub1,k):
    '''使用上一次发现的频繁k-1项集，产生新的候选k项集 '''
    Ck=set()
    len_Lksub1=len(Lksub1)
    list_Lksub1 = list(Lksub1)
    for i in range(len_Lksub1):
        l1 = list(list_Lksub1[i])
        for j in range(1, len_Lksub1):   
            l2 = list(list_Lksub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k-2] == l2[0:k-2]:
                Ck_item = list_Lksub1[i] | list_Lksub1[j]
                if is_apriori(Ck_item, Lksub1):
                    Ck.add(Ck_item)
    return Ck

def is_apriori(CK_item, Lksub1):
    '''检查构造的k候选项集是否满足所有子集是k-1频繁项集,如果满足条件则返回true'''
    for item in CK_item:
        sub_Ck=CK_item-frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True
    
def generate_Lk_by_Ck(data_set, Ck, min_support, support_data):
    """
    计算支持度和置信度，满足最小支持度的候选项集作为k频繁项集,support_data为满足条件的项集的支持度
    """
    Lk = set()
    item_count = {}#用字典对每个项集的频率进行统计 ，计算支持度
    for t in data_set:
        for item in Ck:
            if item.issubset(t):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
    t_num = float(len(data_set))
    for item in item_count:
        if (item_count[item] / t_num) >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item] / t_num
    return Lk


def generate_L(data_set, k, min_support):
    """
    产生L是所有频繁项集的一个列表,列表中每一个元素为集合形式frozenset
    """
    support_data = {}
    C1 = create_C1(data_set)
    L1 = generate_Lk_by_Ck(data_set, C1, min_support, support_data)
    Lksub1 = L1.copy()
    L = []
    L.append(Lksub1)
    for i in range(2, k+1):
        Ci = create_Ck(Lksub1, i)
        Li = generate_Lk_by_Ck(data_set, Ci, min_support, support_data)
        Lksub1 = Li.copy()
        L.append(Lksub1)
    return L, support_data


def generate_big_rules(L, support_data, min_conf):
    """
    根据置信度来选取规则，频繁项集的置信度大于最小置信度则产生新的规则模式
    """
    big_rule_list = []
    sub_set_list = []
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = support_data[freq_set] / support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= min_conf and big_rule not in big_rule_list:
                        # print freq_set-sub_set, " => ", sub_set, "conf: ", conf
                        big_rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    return big_rule_list


if __name__ == "__main__":
    """
    检验
    """
    data_set = load_data_set() #创建数据
    L, support_data = generate_L(data_set, k=3, min_support=0.2)
    big_rules_list = generate_big_rules(L, support_data, min_conf=0.7)
    for Lk in L:
        print("="*50)
        print("frequent " + str(len(list(Lk)[0])) + "-itemsets\t\tsupport")
        print("="*50)
        for freq_set in Lk:
            print(freq_set, support_data[freq_set])
    print
    print("Big Rules")
    for item in big_rules_list:
        print(item[0], "=>", item[1], "conf: ", item[2])
        
