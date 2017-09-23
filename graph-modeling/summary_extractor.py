'''
get summary stats from datasets
Akond Rahman
Sep 23, 2017
'''
from scipy import stats
import pandas as pd
import numpy as np, os
import cliffsDelta

mozilla_dir   = "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/MOZILLA/"
openstack_dir = "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/OPENSTACK/"
wikimedia_dir = "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/"

dataset_dirs = [mozilla_dir, openstack_dir, wikimedia_dir]
for dataset_dir in dataset_dirs:
    for dir_ in os.listdir(dataset_dir):
        if (dir_!='.DS_Store'):
           dir2look = dataset_dir + dir_ + '/'
           file2look = dir2look + 'FINAL.GRAPH.METRIC.csv'
           if(os.path.exists(file2look)):
                df2read = pd.read_csv(file2look)
                print 'Analyzing:', file2look
                print '='*100
                # print df2read.head()
                features = df2read.columns
                for feature_ in features:
                    if ((feature_!='repo_name') and (feature_!='file_name') and (feature_!='defect_status')):
                       print 'Analyzing feature:', feature_
                       print '-'*25
                       defective_vals_for_feature     = df2read[df2read['defect_status']==1][feature_]
                       non_defective_vals_for_feature = df2read[df2read['defect_status']==0][feature_]
                       '''
                       summary time
                       '''
                       print "Defective values stats: \n", defective_vals_for_feature.describe()
                       print "Non defective values stats: \n", non_defective_vals_for_feature.describe()
                       TS, p = stats.mannwhitneyu(list(defective_vals_for_feature), list(non_defective_vals_for_feature), alternative='greater')
                       cliffs_delta = cliffsDelta.cliffsDelta(list(defective_vals_for_feature), list(non_defective_vals_for_feature))
                       print 'pee value:{}, cliffs:{}'.format( p, cliffs_delta)
                       print '='*50
                       '''
                       all data summary
                       '''
                       data_for_feature = df2read[feature_]
                       median_, mean_, total_ = np.median(data_for_feature), np.mean(data_for_feature), sum(data_for_feature)
                       print "Feature:{}, median:{}, mean:{}, sum:{}".format(feature_, median_, mean_, total_  )
                       print '='*100
