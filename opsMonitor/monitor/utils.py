#!/usr/bin/env python
# coding: utf-8
from collections import Counter

def get_models_obj(obj,**kwargs):
    try:
        obj = obj.objects.get(**kwargs)
        return obj
    except Exception as e:
        print ('obj is None %s' % e)
        return False


def get_list_percent(result_list, para):
    '''
    获得一个list中某个元素出现的频率，
    :param result_list: [1,1,1,0,0,1,1]
    :param para: 计算出现频率的那个元素名 0
    :return: 0出现2次，list长度为7，0出现的评率为2/7*100
    '''
    result = Counter(result_list)
    return '%.1f' % (result[para]/len(result_list)*100)


def process_time_data(param):
    '''

    :param param: 5 days, 0:00:33
    :return:
    '''
    if ',' in param:
        return (param.split(',')[0])
    else:
        if param.split(':')[0] == '0':
            if param.split(':')[1] == '00':
                return ("{}秒".format(param.split(':')[2]))
            else:
                return ("{}分{}秒".format(param.split(':')[1],param.split(':')[2]))
        else:
            return ("{}小时{}分{}秒".format(param.split(':')[0],param.split(':')[1],param.split(':')[2]))


