'''
Akond Rahman
Sep 21, 2017
Thursday
Generate graph dataset
'''
import os, csv
import graph_utils

if __name__=='__main__':
   # dataset_file   = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mozilla.Final.Categ.csv'
   # dataset_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.Final.Categ.csv'
   dataset_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Final.Categ.csv'
   threshold    = 10

   all_months_in_ds, file_per_mon_dict, file_defect_dict, repo_dict = graph_utils.getAllMonthsFromDataset(dataset_file)

   for mon_, file_per_mon in file_per_mon_dict.iteritems():
       all_files, all_nodes, all_edges = [], [], []
       #print 'Month:{}, file:{}'.format(mon_, len(file_per_mon))
       if (len(file_per_mon)>= threshold):
          for each_file in file_per_mon:
              '''
              get per month raw data
              '''
              defect_status = file_defect_dict[each_file]
              repo_of_file  = repo_dict[each_file]

              prog_names=graph_utils.getUniqueDevsForGit(each_file, repo_of_file)
              nodes_, edges_ =graph_utils.constructGraph(prog_names)
              if (len(edges_) > 0):
                 graph_utils.dumpTempGraphForFile(nodes_, edges_, mon_, 'WIKIMEDIA', each_file)
                 print 'File:{}, repo:{}, defect:{}, nodes:{}, edges:{}'.format(each_file, repo_of_file, defect_status, len(nodes_), len(edges_))
                 print '-'*100
