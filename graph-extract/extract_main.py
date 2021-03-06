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
   # ds_name = 'MOZILLA'

   # dataset_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.Final.Categ.csv'
   # ds_name = 'OPENSTACK'

   # dataset_file = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Final.Categ.csv'
   # ds_name = 'WIKIMEDIA'

   # all_months_in_ds, file_per_mon_dict, file_defect_dict, repo_dict = graph_utils.getAllMonthsFromDataset(dataset_file)
   '''
   FOR MONTH
   '''
   # threshold    = 10
   # all_time_vals, file_per_time_dict, file_defect_dict, repo_dict = graph_utils.getAllMonthsFromDataset(dataset_file)
   '''
   FOR YEARS
   '''
   threshold    = 50
   all_time_vals, file_per_time_dict, file_defect_dict, repo_dict = graph_utils.getAllYearsFromDataset(dataset_file)

   for time_unit, file_per_time in file_per_time_dict.iteritems():
       str2write = ''
       if (len(file_per_time)>= threshold):
          for each_file in file_per_time:
              '''
              get per month raw data
              '''
              defect_status = file_defect_dict[each_file]
              repo_of_file  = repo_dict[each_file]
              if('mozilla' in each_file):
                 prog_names = graph_utils.getUniqueDevsForHg(each_file, repo_of_file)
              else:
                 prog_names = graph_utils.getUniqueDevsForGit(each_file, repo_of_file)
              '''
              call method to construct graphs
              '''
              nodes_, edges_ =graph_utils.constructGraph(prog_names)
              if (len(edges_) > 0):
                 node_file_name, edge_file_name =graph_utils.dumpTempGraphForFile(nodes_, edges_, time_unit, ds_name, each_file)
                 print 'File:{}, repo:{}, defect:{}, nodes:{}, edges:{}'.format(each_file, repo_of_file, defect_status, len(nodes_), len(edges_))
                 print '-'*100
                 str2write = str2write + each_file + ',' + node_file_name + ',' + edge_file_name + ',' + defect_status + ',' + '\n'
       output_dir = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/' + ds_name + '/' + time_unit + '/'
       if(os.path.exists(output_dir)==False):
          os.makedirs(output_dir)
       file_dump  = output_dir + 'temp.mapping.csv'
       str2write  = 'FILE,NODE_FILE,EDGE_FILE,DEFECT_STATUS,' + '\n' + str2write
       byte_status=graph_utils.dumpContentIntoFile(str2write, file_dump)
       print 'Dumped the `temp mapping file` of {} bytes'.format(byte_status)
       print '='*100
