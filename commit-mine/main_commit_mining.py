'''
Akond Rahman
Commit Mining
Feb 05, 2018
Monday
'''
import cPickle as pickle
import os
import csv
import subprocess
import numpy as np

monthDict            = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
                         'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

def getDateofCommits(param_file_path, repo_path):
   totalCountForChurn   = 0

   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   commitCommand        = "git log  --format=%cd " + theFile + " | awk '{ print $2 $3 $5}' | sed -e 's/ /,/g'"
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   dt_churn_output = [x_ for x_ in dt_churn_output if x_!='']
   # print dt_churn_output
   date_output = [x_[-4:] + '-' + monthDict[x_[0:3]] + '-' + x_[3:5] for x_ in dt_churn_output ]
   # print len(date_output)
   return date_output

def getAddedChurnMetrics(param_file_path, repo_path):
   totalAddedLinesForChurn = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnAddedCommand = " git log --numstat --oneline "+ theFile +" | grep '" + theFile + "' | awk '{ print $1 }' "
   command2Run = cdCommand + churnAddedCommand
   # print command2Run

   add_churn_output = subprocess.check_output(['bash','-c', command2Run])
   add_churn_output = add_churn_output.split('\n')
   add_churn_output = [x_ for x_ in add_churn_output if x_!='']
   # print add_churn_output
   add_churn_output = [int(y_) for y_ in add_churn_output if y_.isdigit()]
   # print len(add_churn_output)

   return add_churn_output

def getDeletedChurnMetrics(param_file_path, repo_path):
   totalDeletedLinesForChurn = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnDeletedCommand = " git log --numstat --oneline "+ theFile +" | grep '" + theFile + "' | awk '{ print $2 }' "
   command2Run = cdCommand + churnDeletedCommand

   del_churn_output = subprocess.check_output(['bash','-c', command2Run])
   del_churn_output = del_churn_output.split('\n')
   del_churn_output = [x_ for x_ in del_churn_output if x_!='']
   del_churn_output = [int(y_) for y_ in del_churn_output if y_.isdigit()]
   # print len(del_churn_output)

   return del_churn_output

def getCommitTimeData(file_path_param):
    dict2ret = {}
    with open(file_path_param, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
         id_of_file     = row_[0]
         repo_of_file   = row_[1]
         categ_of_file  = row_[3]
         full_path_of_file  = row_[4]
         defect_status  = ''
         if categ_of_file=='N':
             defect_status = '0'
         else:
             defect_status = '1'
         if repo_of_file.endswith('/')==False:
            repo_of_file = repo_of_file + '/'
         file2read = repo_of_file + 'fullThrottle_id_msg_map.csv'
         dict_key = repo_of_file + '*' + str(id_of_file) + '*' + defect_status + '*' + full_path_of_file
         with open(file2read, 'rU') as file_:
              reader_ = csv.reader(file_)
              for row_ in reader_:
                  tstamp = row_[3]
                  if dict_key not in dict2ret:
                      dict2ret[tstamp] = dict_key
    return dict2ret

def getCommitData(file_path_p):
    commitTimeDict=getCommitTimeData(file_path_p)
    for time_, value_ in commitTimeDict.iteritems():
        date_ = time_.split(' ')[0]
        full_path_of_file = value_.split('*')[-1]
        if os.path.exists(full_path_of_file):
               print full_path_of_file, date_
               commit_dates = getDateofCommits(full_path_of_file, repo_of_file)
               commit_additions = getAddedChurnMetrics(full_path_of_file, repo_of_file)
               commit_deletions = getDeletedChurnMetrics(full_path_of_file, repo_of_file)


if __name__=='__main__':
    theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Cisco_Categ_For_DB.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mirantis_Categ_For_DB.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mozilla.Final.Categ.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.WithoutBadBoys.Final.Categ.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Final.Categ.csv'

    getCommitData(theCompleteCategFile)
