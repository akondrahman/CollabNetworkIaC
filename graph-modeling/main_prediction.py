'''
main prediction
Akond Rahman
Sep 23, 2017
Saturday
'''
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import decomposition
import process_metric_utility , numpy as np , pandas as pd, sklearn_utility
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

if __name__=='__main__':
