'''
Core part of Stallings extractor
Akond Rahman
Sep 09, 2018
'''
import math
import os, subprocess, numpy as np, operator
from  collections import Counter
from  scipy.stats import entropy
import time
import datetime
import csv

monthDict            = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06',
                         'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}



def getAddedLines(param_file_path, repo_path):

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnAddedCommand = " git log --numstat --oneline "+ theFile +" | grep '" + theFile + "' | awk '{ print $1 }' "
   command2Run = cdCommand + churnAddedCommand

   add_churn_output = subprocess.check_output(['bash','-c', command2Run])
   add_churn_output = add_churn_output.split('\n')
   add_churn_output = [x_ for x_ in add_churn_output if x_!='']
   addition_output  = [int(y_) for y_ in add_churn_output if y_.isdigit()]

   return addition_output

def getDate(param_file_path, repo_path):
   dateList = []

   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   commitCommand        = "git log  --format=%cd " + theFile + " | awk '{ print $2 $3 $5}' | sed -e 's/ /,/g'"
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   dt_churn_output = [x_ for x_ in dt_churn_output if x_!='']

   formatDate = lambda x_ : '0' + x_ if (len(x_) < 2) else x_

   for dob in dt_churn_output:
       year = dob[-4:]
       mont = monthDict[dob[0:3]]
       if len(dob) > 8:
          day = dob[3:5]
       else:
          day = '0' + dob[3:4]
       # full_date = year + '-' + mont + '-' + day
       full_date = year + '-' + mont
       dateList.append(full_date)

   return dateList


def getDeletedLines(param_file_path, repo_path):
   totalDeletedLinesForChurn = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnDeletedCommand = " git log --numstat --oneline "+ theFile +" | grep '" + theFile + "' | awk '{ print $2 }' "
   command2Run = cdCommand + churnDeletedCommand

   del_churn_output = subprocess.check_output(['bash','-c', command2Run])
   del_churn_output = del_churn_output.split('\n')
   del_churn_output = [x_ for x_ in del_churn_output if x_!='']
   deletion_output  = [int(y_) for y_ in del_churn_output if y_.isdigit()]

   return deletion_output

def getMoziAddedLines(param_file_path, repo_path):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnAddedCommand = "hg churn --diffstat " + theFile + " | cut -d'+' -f2 | cut -d'/' -f1"
   command2Run = cdCommand + churnAddedCommand

   add_churn_output = subprocess.check_output(['bash','-c', command2Run])
   add_churn_output = add_churn_output.split('\n')
   add_churn_output = [x_ for x_ in add_churn_output if x_!='']
   add_churn_output = [x_ for x_ in add_churn_output if '@' not in x_]
   add_churn_output = [int(y_) for y_ in add_churn_output if (y_.isdigit())==True]

   return add_churn_output

def getMoziDeletedLines(param_file_path, repo_path):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnDeletedCommand = " hg churn --diffstat " + theFile + " | cut -d'+' -f2 | cut -d'/' -f2 | cut -d'-' -f2"
   command2Run = cdCommand + churnDeletedCommand

   del_churn_output = subprocess.check_output(['bash','-c', command2Run])
   del_churn_output = del_churn_output.split('\n')
   del_churn_output = [x_ for x_ in del_churn_output if x_!='']
   del_churn_output = [x_ for x_ in del_churn_output if '@' not in x_]
   del_churn_output = [int(y_) for y_ in del_churn_output]

   return del_churn_output

def getMoziDate(param_file_path, repo_path):
   cdCommand            = "cd " + repo_path + " ; "
   theFile              = os.path.relpath(param_file_path, repo_path)
   commitCommand        = " hg churn --dateformat '%Y-%m-%d' " +  theFile +    " | awk '{print $1 }' "
   command2Run          = cdCommand + commitCommand

   dt_churn_output = subprocess.check_output(['bash','-c', command2Run])
   dt_churn_output = dt_churn_output.split('\n')
   monthAndYeatList = [x_ for x_ in dt_churn_output if x_!='']
   print monthAndYeatList
   # formatDate = lambda x_ : '0' + x_ if (len(x_) < 2) else x_
   #
   # for dob in monthAndYeatList:
   #     year = dob[-4:]
   #     mont = monthDict[dob[0:3]]
   #     if len(dob) > 8:
   #        day = dob[3:5]
   #     else:
   #        day = '0' + dob[3:4]
   #     # full_date = year + '-' + mont + '-' + day
   #     full_date = year + '-' + mont
   #     dateList.append(full_date)

   return dateList

def createDataset(str2Dump, datasetNameParam):
   headerOfFile0='ORG,SCRIPT_PATH,'
   headerOfFile1='PREV_DEFECT_HISTORY,AVG_ADDPERLOC,'
   headerOfFile2='MED_ADDPERLOC,AVG_DELPERLOC,MED_DELPERLOC,'
   headerOfFile3='CURR_DEFECT_STATUS'

   headerStr = headerOfFile0 + headerOfFile1 + headerOfFile2  + headerOfFile3

   str2Write = headerStr + '\n' + str2Dump
   return dumpContentIntoFile(str2Write, datasetNameParam)

def giveTimeStamp():
  tsObj = time.time()
  strToret = datetime.datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP)
    fileToWrite.close()
    return str(os.stat(fileP).st_size)

def getPuppetFileDetails(theCompleteCategFile, org_dir):
    dict2Ret={}
    with open(theCompleteCategFile, 'rU') as file_:
      reader_ = csv.reader(file_)
      next(reader_, None)
      for row_ in reader_:
          commit_ID    = row_[1]
          repo_name_   = row_[2]
          categ_defect = row_[4]
          file_name_   = row_[5]
          commit_date  = row_[6]

          if categ_defect != 'N':
              defect_status = '1'
          else:
              defect_status  = '0'
          if commit_ID not in dict2Ret:
             dict2Ret[file_name_] = (repo_name_, defect_status)
    return dict2Ret

def getDateAddMap(date_list, added_lines):
    dict_ = {}
    for cnt in xrange(len(added_lines)):
        date_ = date_list[cnt]
        additions = added_lines[cnt]
        if date_ not in dict_:
           dict_[date_] = additions
    return dict_

def makeChunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def getIndiMetrics(defect_list, added_list, deleted_list, repo_p, file_p):
      prev_defect_status, curr_defect_status = '', ''
      #before calculation remove current data point
      if (len(defect_list) > 1):
         curr_defect_value = defect_list.pop()
         added_list.pop()
         deleted_list.pop()
      else:
         curr_defect_value = defect_list[0]
      if curr_defect_value != 'N':
          curr_defect_status = '1'
      else:
          curr_defect_status = '0'
      # now do calculation
      defects = np.unique(defect_list)
      if ((len(defects) == 1) and (defects[0]=='N')):
          prev_defect_status = '0'
      else:
          prev_defect_status = '1'
      str_to_ret =  repo_p + ',' + file_p + ',' + prev_defect_status + ',' + str(np.mean(added_list)) + ',' + str(np.median(added_list)) + ',' + str(np.mean(deleted_list)) + ',' + str(np.median(deleted_list))  + ',' + curr_defect_status + '\n'
      return str_to_ret

def getPrevMetricData(defect_list, added_list, deleted_list, window_p, repo_p, file_p):
    prev_defect_status = '0'
    str_to_ret = ''
    if(len(defect_list) > window_p):
      splitted_defect_list   = list(makeChunks(defect_list, window_p))
      splitted_addition_list = list(makeChunks(added_list, window_p))
      splitted_deletion_list = list(makeChunks(deleted_list, window_p))
      for ind_ in xrange(len(splitted_defect_list)):
         indi_defect_list, indi_added_list, indi_deleted_list = splitted_defect_list[ind_] , splitted_addition_list[ind_], splitted_deletion_list[ind_]
         str_ = getIndiMetrics(indi_defect_list, indi_added_list, indi_deleted_list, repo_p, file_p)
         str_to_ret = str_to_ret + str_
    else:
         str_to_ret = getIndiMetrics(defect_list, added_list, deleted_list, repo_p, file_p)

    return str_to_ret

def getStallingsMetrics(file_path_p, repo_path_p, org, full_ds_cat_df , window, mozi_flag):
   # print full_ds_cat_df.head()
   file_df   = full_ds_cat_df[full_ds_cat_df['filepath']==file_path_p]
   sorted_df = file_df.sort_values(by='msgid', ascending=True)
   # print sorted_df.head()

   if mozi_flag:
       file_added_lines   = getMoziAddedLines(file_path_p, repo_path_p)
       file_deleted_lines = getMoziDeletedLines(file_path_p, repo_path_p)
       file_date_list     = getMoziDate(file_path_p, repo_path_p)
   else:
       file_added_lines   = getAddedLines(file_path_p, repo_path_p)
       file_deleted_lines = getDeletedLines(file_path_p, repo_path_p)
       file_date_list     = getDate(file_path_p, repo_path_p)

   file_defect_stat   = sorted_df['categ'].tolist()


   # print file_added_lines
   # print file_date_list
   if (len(file_added_lines)==len(file_defect_stat)):
       # print file_defect_stat, file_added_lines, '='
       per_file_str = getPrevMetricData(file_defect_stat, file_added_lines, file_deleted_lines, window, repo_path_p, file_path_p)
   else:
       # date_to_add_map = getDateAddMap(file_date_list, file_added_lines)
       # # print date_to_add_map
       # dates_in_df  = sorted_df['date'].tolist()
       # months_in_df = [x_.split('-')[0] + '-' + x_.split('-')[1] for x_ in dates_in_df]
       # final_added_lines = []
       # for mont_ in months_in_df:
       #     if mont_ in date_to_add_map:
       #        final_added_lines.append(date_to_add_map[mont_])
       #
       # print file_defect_stat
       # print final_added_lines
       defect_list, addition_list, deletion_list = [], [], []

       rev_def_stat = list(reversed(file_defect_stat))
       rev_add_line = list(reversed(file_added_lines))
       rev_del_line = list(reversed(file_deleted_lines))

       for ind in xrange(len(rev_def_stat)):
           if (ind < len(rev_add_line)) and (ind < len(rev_del_line)):

              def_sta = rev_def_stat[ind]
              add_lin = rev_add_line[ind]
              del_lin = rev_del_line[ind]

              defect_list.append(def_sta)
              addition_list.append(add_lin)
              deletion_list.append(del_lin)

       # print defect_list, addition_list, '>'
       per_file_str = getPrevMetricData(defect_list, addition_list, deletion_list, window, repo_path_p, file_path_p)

   # print per_file_str

   return per_file_str
