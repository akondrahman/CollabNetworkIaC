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
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

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

def mapMinedDataToCommit(index_list, add_list, del_list, contrib_per_file, defect_status, date_, full_path_file_p):
    temp_add, temp_del = 0, 0
    perFileTuple = []
    for ind_ in index_list:
        if ((ind_ < len(add_list)) and (ind_ < len(del_list))):
           temp_add, temp_del = add_list[ind_], del_list[ind_]
        else:
           temp_add, temp_del = 0, 0
        comm_tot = temp_add + temp_del
        perFileTuple.append((date_, temp_add, temp_del, comm_tot, defect_status, contrib_per_file, full_path_file_p))
    return perFileTuple


def getContributorsForCommits(param_file_path, repo_path):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame " + theFile + "  | awk {'print $2 \" \" $4'} | cut -d'(' -f2 | sed -e 's/ /,/g' "
   command2Run       = cdCommand + blameCommand

   blame_output   = subprocess.check_output(['bash','-c', command2Run])
   blame_output   = blame_output.split('\n')
   blame_output   = [x_ for x_ in blame_output if x_!='']

   date_dict, mo_dict = {}, {}
   for val_ in blame_output:
       author_ = val_.split(',')[0]
       date_   = val_.split(',')[1]
       # print date_
       if '-' in date_:
           month_  = date_.split('-')[0] + '-' + date_.split('-')[1]
       else:
           month_  = '2012-01'
       if date_ not in date_dict:
          date_dict[date_] = author_
       if month_ not in mo_dict:
          mo_dict[date_] = author_
   return date_dict, mo_dict

def getContribCount(param_file_path, repo_path):
   minorList = []
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame " + theFile + "  | awk '{print $2}'  | cut -d'(' -f2"
   command2Run       = cdCommand + blameCommand

   blame_output   = subprocess.check_output(['bash','-c', command2Run])
   blame_output   = blame_output.split('\n')
   blame_output   = [x_ for x_ in blame_output if x_!='']
   author_contrib = dict(Counter(blame_output))
   # print author_contrib
   return author_contrib

def plotFeature(df_p):
    # fig, ax = plt.subplots()
    # for key, grp in df_p.groupby(['DEF_STA']):
    #     print key
    #     ax = grp.plot(ax=ax, kind='line', x='DATE', y='ADD', c=key, label=key)
    x_axis = [x_ for x_ in xrange(len(df_p['DATE'].tolist()))]
    y_axis = df_p['ADD'].tolist()
    colors = df_p['DEFECT'].tolist()
    # enable drawing of multiple graphs on one plot
    kcolors = ['red' if value_=='1' else 'green' for value_ in colors]
    plt.scatter(x_axis, y_axis, c = kcolors)
    plt.legend()
    plt.show()

def doAnalysis(full_df_p):
    all_files = np.unique(full_df_p['FILE_PATH'].tolist())
    for file_ in all_files:
        per_file_df =  full_df_p[full_df_p['FILE_PATH']==file_]
        sort_file_df = per_file_df.sort_values(by=['DATE'])
        # print sort_file_df
        plotFeature(sort_file_df)

def getCommitData(file_path_p):
    commitTimeDict=getCommitTimeData(file_path_p)
    perFileDFList = []
    for time_, value_ in commitTimeDict.iteritems():
        date_ = time_.split(' ')[0]
        full_path_of_file = value_.split('*')[-1]
        repo_of_file = value_.split('*')[0]
        defect_status = value_.split('*')[2]
        if os.path.exists(full_path_of_file):
               contrib_dict = getContribCount(full_path_of_file, repo_of_file)
               commit_dates = getDateofCommits(full_path_of_file, repo_of_file)
               # print full_path_of_file, date_, commit_dates
               if date_ in commit_dates:
                   indices = [i for i, x_ in enumerate(commit_dates) if x_ == date_]
                   # print indices
               else: ## find clossest matching date
                   month_ = date_.split('-')[0] + '-' + date_.split('-')[1]
                   commit_months = [x_.split('-')[0] + '-' + x_.split('-')[1] for x_ in commit_dates]
                   # print month_, commit_months
                   if month_ in commit_months:
                      indices = [i for i, x_ in enumerate(commit_months) if x_ == month_]
                      # print indices
               commit_additions = getAddedChurnMetrics(full_path_of_file, repo_of_file)
               commit_deletions = getDeletedChurnMetrics(full_path_of_file, repo_of_file)
               commit_contrib_dt, commit_contrib_mo = getContributorsForCommits(full_path_of_file, repo_of_file)
               if date_ in commit_contrib_dt:
                  author_ = commit_contrib_dt[date_]
                  if author_ in contrib_dict:
                      contrib_per_file = contrib_dict[author_]
               else:
                   month_ = date_.split('-')[0] + '-' + date_.split('-')[1]
                   if month_ in commit_contrib_mo:
                      author_ = commit_contrib_mo[month_]
                      if author_ in contrib_dict:
                         contrib_per_file = contrib_dict[author_]
               ### map teh data
               file_list = mapMinedDataToCommit(indices, commit_additions, commit_deletions, contrib_per_file, defect_status, date_, full_path_of_file) ##returns a df from all commits
               # print mined_data_for_commit, defect_status, date_, contrib_per_file
               # print file_list
               perFileDFList = perFileDFList + file_list

    labels = ['DATE', 'ADD', 'DEL', 'TOT', 'DEF_STA', 'CONTRIB_LOC', 'FILE_PATH']
    full_ds_df = pd.DataFrame.from_records(perFileDFList, columns=labels)
    print full_ds_df.head()
    doAnalysis(full_ds_df)

if __name__=='__main__':
    theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Cisco_Categ_For_DB.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mirantis_Categ_For_DB.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mozilla.Final.Categ.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.WithoutBadBoys.Final.Categ.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Final.Categ.csv'

    getCommitData(theCompleteCategFile)
