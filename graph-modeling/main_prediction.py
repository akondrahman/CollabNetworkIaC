'''
main prediction
Akond Rahman
Sep 23, 2017
Saturday
'''
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import decomposition
import numpy as np , pandas as pd, os
from itertools import combinations
import utility, sklearn_modeling
glimpseIndex=10

def getPCAInsights(pcaParamObj, no_of_pca_comp_to_see):
    print '+'*25
    print 'PCA metric importance zone  ...'
    print '+'*25
    for comp_index in xrange(no_of_pca_comp_to_see):
        all_metric_value_in_one_component =  np.abs(pcaParamObj.components_[comp_index])
        non_zero_metric_cnt = len([x_ for x_ in all_metric_value_in_one_component if x_ > 0])
        print 'Number of non-zero metrics:{}, of {}'.format(non_zero_metric_cnt, len(all_metric_value_in_one_component))
        print '$'*15
        sorted_all_metric_index_in_one_component = all_metric_value_in_one_component.argsort()[::-1]
        for met_index in sorted_all_metric_index_in_one_component:
            print 'Metric index:{}, metric score:{}'.format(met_index, all_metric_value_in_one_component[met_index])
            print '~'*10
        # top_components_index = sorted_all_metric_value_in_one_component[:how_many_metrics]
        # print top_components_index
        print '$'*15
    print "+"*25

def constructCombos(ds_param):
        ds_lists, output_list  = [], []
        for dir_ in os.listdir(ds_param):
            if (dir_!='.DS_Store'):
               dir2look = ds_param + dir_ + '/'
               file2look = dir2look + 'FINAL.GRAPH.METRIC.csv'
               if(os.path.exists(file2look)):
                 ds_lists.append(file2look)
        ds_lists =  list(combinations(ds_lists, 2))
        for combo in ds_lists:
            train_file, test_file = combo
            train_path, test_path = os.path.dirname(train_file), os.path.dirname(test_file)
            train_year_value, test_year_value =  int(train_path.split('/')[-1]), int(test_path.split('/')[-1])
            #print train_year_value, test_year_value
            if((test_year_value > train_year_value) and ((test_year_value - train_year_value)==1)):
                output_list.append(combo)
        return output_list



if __name__=='__main__':
   ds_dir   = "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/MOZILLA/"
   folder_to_save = "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/output/MOZILLA_TIME_PRED_RES/"

   # ds_dir = "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/OPENSTACK/"
   # ds_dir = "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/"

   train_test_combos = constructCombos(ds_dir)
   #print train_test_combos
   for index_ in xrange(len(train_test_combos)):
       train_file, test_file = train_test_combos[index_]
       '''
       training dataset zone
       '''
       train_log_features, train_labels = utility.getFeaturesAndLabels(train_file)
       '''
       test dataset zone
       '''
       test_log_features, test_labels = utility.getFeaturesAndLabels(test_file)
       '''
       do prediction: 10 times iteration
       '''
       folder2write = folder_to_save +  str(index_) + '/'
       if((os.path.exists(folder2write))==False):
           os.makedirs(folder2write)
       sklearn_modeling.performIterativeModeling(train_log_features, test_log_features, train_labels, test_labels, folder2write, 10)
       print '='*100
