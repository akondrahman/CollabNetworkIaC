'''
Akond Rahman
Feb 04, 2018
Meenely's Dev Network
'''
import os
import csv
import itertools
import subprocess
import numpy as np

def getGitProgrammerInfo(param_file_path, repo_path):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   commitCountCmd    = " git blame "+ theFile +"  | awk '{print $2}' | cut -d'(' -f2 "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   author_count_output = [x_ for x_ in author_count_output if x_!='']
   node_cnt            = len(np.unique(author_count_output)) ## get node count
   ## create edges using combinations
   ## get unique author names
   uni_aut_names = np.unique(author_count_output)
   temp_edge_list = list(itertools.permutations(uni_aut_names, 2))
   edge_list = [(x_[0], x_[1]) for x_ in temp_edge_list if x_[0] != x_[1]] ## used list comprehension to egenrate valid edges
   return (edge_list, node_cnt)

def getGraphData(file_path_p, repo_path_p):
    if 'moz' in file_path_p:
        graph_per_file = getHgProgrammerInfo(file_path_p, repo_path_p)
    else:
        graph_per_file = getGitProgrammerInfo(file_path_p, repo_path_p)
    ### now return value
    print 'File:{}, Graph:{}'.format(file_path_p, graph_per_file)
    # print 'Processing {} ...'.format(file_path_p)
    return graph_per_file

def getGraphForFiles(file_path_p):
    output_dict = {}
    with open(file_path_p, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
        repo_of_file       = row_[1]
        categ_of_file      = row_[3]
        full_path_of_file  = row_[4]
        if os.path.exists(full_path_of_file):
            if full_path_of_file not in output_dict:
                gr_for_file = getGraphData(full_path_of_file, repo_of_file)
                output_dict[full_path_of_file] = gr_for_file
    return output_dict

if __name__=='__main__':
    ### INPUT
    theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Cisco_Categ_For_DB.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mirantis_Categ_For_DB.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mozilla.Final.Categ.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.WithoutBadBoys.Final.Categ.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Final.Categ.csv'



    ### OUTPUT
    datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dev-ds/CIS.PKL'
    # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dev-ds/MIR.PKL'
    # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dev-ds/MOZ.PKL'
    # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dev-ds/OST.PKL'
    # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dev-ds/WIK.PKL'

    final_dict = getGraphForFiles(theCompleteCategFile)
    # pickle.dump(final_dict, open(datasetFile2Save, 'wb'))
