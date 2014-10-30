# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 15:53:06 2014

@author: andmas
"""

import os
import numpy as np 
import numpy.ma as ma
from subprocess import call



path_to_GTIS = "/mnt/4tbdata/xmm_reduce_results/old_results_ntt_100"
path_to_tbin_data = "/mnt/4tbdata/xmm_reduce_results/old_results_ntt_FASPER" 

excess_tbins = True



def read_tbin_in():
    timing_results_file = os.listdir(path_to_tbin_data)
    for results in timing_results_file:
            test_string = str(results)
            test_tbin = test_string[-8:-4]
            print test_tbin
            if test_tbin == 'tbin':
                tbin_file = path_to_tbin_data + '/' + test_string
                print tbin_file
    tbin_contents=[]
    with open(tbin_file,'r') as f: 
        file_data = f.readlines()
        for line in file_data[0:]:
            data = line.split('\n')
            tbin_contents.append(float(data[-1]))
    return tbin_contents


def compare_gtis(gti_array, tbin_array, number_of_elements_in_tbin):
    
    a = []
    b= []
    good = np.zeros
    num_gtis = len(gti_array)
    num_dims = gti_array.ndim
    if num_gtis == 2 and num_dims == 1:
        start = gti_array[0:1]
        stop = gti_array[1:2]
        indices = zip(*np.where(np.logical_and(tbin_array>=start,tbin_array<=stop)))
        a.extend(indices)
    else:
        for x in range(0,num_gtis):
            both = gti_array[x]
            start = both[0:1]
            stop = both[1:2]
            indices = zip(*np.where(np.logical_and(tbin_array>=start,tbin_array<=stop)))
            a.extend(indices)
            
    number_of_elements_found_after_GTIS = len(a)    
    print "number_of_elements_in_tbin:          " + str(number_of_elements_in_tbin)
    print "number_of_elements_found_after_GTIS: " + str(number_of_elements_found_after_GTIS)
    if number_of_elements_found_after_GTIS != number_of_elements_in_tbin: 
        return False        
    

   
        
results = os.listdir(path_to_GTIS)
for dir_list in results:
    #pull_obs.execute("DELETE FROM not_reduced WHERE obs_id = %s", (dir_list,))
    dir_string = str(dir_list)
    dir_list = dir_string.strip('\'(),')
    move_to_dir = path_to_GTIS + "/" + dir_list
    sub_dir = os.listdir(move_to_dir)
    for subs in sub_dir:
        if subs == 'processed':
            sub_dir_name = path_to_GTIS + "/" + dir_list + "/" + subs
            sub_sub_dir = os.listdir(sub_dir_name)
            for subs_subs in sub_sub_dir:
                if subs_subs == 'test': 
                    path_for_test = sub_dir_name + "/" + subs_subs
                    print path_for_test
#    Open and readin GTIs 
                    file_listing = os.listdir(path_for_test)
                    for files in file_listing: 
                         gti_front_filename, gti_filename_ext = os.path.splitext(files)
                         gti_file = gti_front_filename[0:3]
                         
                         if gti_file == 'GTI':
                             gti_to_use = path_to_GTIS + "/" + dir_list + "/" + subs +"/" + subs_subs + "/" + gti_front_filename + gti_filename_ext
                             print gti_to_use
                             gti_array = np.loadtxt(gti_to_use,dtype=np.float)
                             break
                   
# read each tbin file and compare with relevant GTIs
                    tbin_file_listing = os.listdir(path_to_tbin_data)
                    for files in tbin_file_listing: 
                        find_obsID = files[0:10]
                        detID = files[11:17]
                        tbin_filename = path_to_tbin_data + "/" + files
                        if find_obsID == dir_list:
                            end_filename = files[-8:-4]
                            if end_filename == 'tbin':
                                print "obsId : " + find_obsID + " detID: " + detID  
                                tbin_array = np.loadtxt(tbin_filename, dtype=np.float)
                                number_of_elements_in_tbin = len(tbin_array)
                                excess_tbins = compare_gtis(gti_array, tbin_array, number_of_elements_in_tbin)

                                if excess_tbins == False: 
                                    print "!!!!!!!!!!! PROBLEM !!!!!!!" +  "obsID: " + find_obsID + "detID: " + detID
                    print "end"
                







                    
                    
                    
                    
                    
                     
                                 