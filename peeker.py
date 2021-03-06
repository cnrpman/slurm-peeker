#!/bin/python

from __future__ import print_function

import re
import collections
import os
import time

# edit here to add more resource
res_list = ["cpu", "gres/gpu"]

pattern_strings = ["{}=(\d+)".format(res) for res in res_list]
patterns = [re.compile(pattern_string) for pattern_string in pattern_strings]

# Platform type
plats = [['Bigvideo', 'P100', 'TITANXP', 'GTX1080'], ['Test']]
plat_types = ['O', '~', 'X'] # with permission, temporary, without permission

def plat_classify(platform):
    for idx, plat in enumerate(plats):
        if platform in plat:
            return plat_types[idx]
    return plat_types[-1] # other type

def main():
    print('Executing peeker.sh...')
    starttime = time.time()
    os.chdir(os.path.dirname(__file__))
    os.system('[ -e output.txt ] && rm output.txt\n'
              'sh peeker.sh > output.txt')
    print('Finished at {}'.format(time.strftime("%H:%M:%S")))
    print('Cost time {:.5}s'.format(time.time() - starttime))
    print('='*40)

    with open('output.txt', 'r') as f:
        for line in f:
            unrolled = line.strip().split('|')
            id, name, platform, res = [item.strip() for item in unrolled]
            
            search_ress = [pattern.search(res) for pattern in patterns]

            the_list = []
            for search_res in search_ress:
                the_ele = search_res.groups()[0] if search_res is not None else 0
                the_list.append(int(the_ele))

            # edit here to add more regist dict
            regist_dict(name_dict, "[{:^1}] {}".format(plat_classify(platform), name), the_list)
            regist_dict(platform_dict, "[{:^1}] {}".format(plat_classify(platform), platform), the_list)
    
    # edit here to add more output dict
    output_dict(name_dict, "Aggregate by User Name and platform type")
    print('='*40)
    output_dict(platform_dict, "Aggregate by Platform")

def list_str(the_list):
    return ("{:>4},"*len(the_list)).format(*the_list)[:-1]

def output_dict(the_dict, annotate):
    print("{}, output in order of {} and job".format(annotate, list_str(res_list)))
    for key, value in sorted(the_dict.iteritems()):
        print("{:<22}{}".format(key, list_str(value)))

content_len = len(res_list) + 1 # content + job
def default_caller():
    return [0] * content_len

# edit here to add more dict
name_dict = collections.defaultdict(default_caller)
platform_dict = collections.defaultdict(default_caller)

def regist_dict(the_dict, key, content):
    content += [1] # job counter
    val = the_dict[key]
    for idx in range(content_len):
        val[idx] += content[idx]

if __name__ == "__main__":
    main()
