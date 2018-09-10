'''
Stallings exploration
Akond Rahman
Sep 09, 2018
'''
import stallings_miner
import pandas as pd
import os

def getAllProcessMetricsForSingleFile(full_path_param, repo_path_param, org_of_file, full_categ_df, window_size, mozi_flag):
      process_metrics =  stallings_miner.getStallingsMetrics(full_path_param, repo_path_param, org_of_file, full_categ_df, window_size, mozi_flag)
      print "-"*50
      print process_metrics
      print "Generated the process metrics ... "
      print "-"*50
      return process_metrics

def getAllProcessMetricForAllFiles(pupp_map_dict_param, datasetFile2Save, org_name, full_categ_df, window_size, mozi_flag ):
   str2ret=''
   fileCount = 0
   for file_, details_ in pupp_map_dict_param.items():
           repo_, defect_status = details_
           if (file_!= 'WTF') and (os.path.exists(file_)):
              fileCount = fileCount + 1
              all_metric_for_this_file = getAllProcessMetricsForSingleFile(file_, repo_, org_name, full_categ_df, window_size, mozi_flag)
              str2ret = str2ret + all_metric_for_this_file
              print "="*75
   dump_stats = stallings_miner.createDataset(str2ret, datasetFile2Save)
   print "Dumped a file of {} bytes".format(dump_stats)
   return str2ret

if __name__=='__main__':
  window_ = 5

  # org_name = '/Users/akond/PUPP_REPOS/wikimedia-downloads/'
  # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Categ.For.CSC712.csv'
  # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/output/exploration-stallings/WIKI.OUT.csv'
  # mozi_flag = False

  # org_name = '/Users/akond/PUPP_REPOS/openstack-downloads/'
  # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.Categ.For.CSC712.csv'
  # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/output/exploration-stallings/OSTK.OUT.csv'
  # mozi_flag = False

  org_name = '/Users/akond/PUPP_REPOS/mozilla-releng-downloads/'
  theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mozilla.Categ.For.CSC712.csv'
  datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/output/exploration-stallings/MOZI.OUT.csv'
  mozi_flag = True


  print "Started at:", stallings_miner.giveTimeStamp()
  fullPuppMap   = stallings_miner.getPuppetFileDetails(theCompleteCategFile, org_name)
  print "Loaded mapping of Puppet files ... "
  print "-"*100
  full_categ_df = pd.read_csv(theCompleteCategFile)
  str_ = getAllProcessMetricForAllFiles(fullPuppMap, datasetFile2Save, org_name, full_categ_df, window_, mozi_flag)
  print "-"*100
  print "We analyzed {} Puppet files".format(len(fullPuppMap))
  print "-"*100
  print "Ended at:", stallings_miner.giveTimeStamp()
  print "-"*100
