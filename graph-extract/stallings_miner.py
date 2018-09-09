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



def getAddedChurnMetrics(param_file_path, repo_path):
   totalAddedLinesForChurn = 0

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnAddedCommand = " git log --numstat --oneline "+ theFile +" | grep '" + theFile + "' | awk '{ print $1 }' "
   command2Run = cdCommand + churnAddedCommand

   add_churn_output = subprocess.check_output(['bash','-c', command2Run])
   add_churn_output = add_churn_output.split('\n')
   add_churn_output = [x_ for x_ in add_churn_output if x_!='']
   #print add_churn_output
   add_churn_output = [int(y_) for y_ in add_churn_output if y_.isdigit()]
   #print add_churn_output
   totalAddedLinesForChurn = sum(add_churn_output)
   #print totalAddedLinesForChurn
   return totalAddedLinesForChurn




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
   #print del_churn_output
   totalDeletedLinesForChurn = sum(del_churn_output)
   #print totalDeletedLinesForChurn
   return totalDeletedLinesForChurn




def getAverageAndTotalChangedLines(param_file_path, repo_path):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnDeletedCommand = " git log --numstat --oneline "+ theFile +" | grep '" + theFile + "' | awk '{ print $2 }' "
   command2Run = cdCommand + churnDeletedCommand

   del_churn_output = subprocess.check_output(['bash','-c', command2Run])
   del_churn_output = del_churn_output.split('\n')
   del_churn_output = [x_ for x_ in del_churn_output if x_!='']
   del_churn_output = [int(y_) for y_ in del_churn_output if y_.isdigit()]

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   churnAddedCommand = " git log --numstat --oneline "+ theFile +" | grep '" + theFile + "' | awk '{ print $1 }' "
   command2Run = cdCommand + churnAddedCommand

   add_churn_output = subprocess.check_output(['bash','-c', command2Run])
   add_churn_output = add_churn_output.split('\n')
   add_churn_output = [x_ for x_ in add_churn_output if x_!='']
   add_churn_output = [int(y_) for y_ in add_churn_output if y_.isdigit()]

   chanegHolder     = add_churn_output + del_churn_output
   #print chanegHolder
   avgChangeLOC     = np.mean(chanegHolder)
   sumChangeLOC     = sum(chanegHolder)
   #print avgChangeLOC
   return avgChangeLOC, sumChangeLOC

def getMinorContribCount(param_file_path, repo_path, sloc):
   minorList = []
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame " + theFile + "  | awk '{print $2}'  | cut -d'(' -f2"
   command2Run       = cdCommand + blameCommand

   blame_output   = subprocess.check_output(['bash','-c', command2Run])
   blame_output   = blame_output.split('\n')
   blame_output   = [x_ for x_ in blame_output if x_!='']
   author_contrib = dict(Counter(blame_output))
   #print author_contrib
   for author, contribs in author_contrib.items():
      if((float(contribs)/float(sloc)) < 0.05):
        minorList.append(author)
   return len(minorList)


# useful for task/responsibility switching as well

def getHighestContribsPerc(param_file_path, repo_path, sloc):
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame " + theFile + "  | awk '{print $2}'  | cut -d'(' -f2"
   command2Run       = cdCommand + blameCommand

   blame_output     = subprocess.check_output(['bash','-c', command2Run])
   blame_output     = blame_output.split('\n')
   blame_output     = [x_ for x_ in blame_output if x_!='']
   author_contrib   = dict(Counter(blame_output))
   #print author_contrib
   if (len(author_contrib) > 0):
     highest_author   = max(author_contrib.iteritems(), key=operator.itemgetter(1))[0]
     highest_contr    = author_contrib[highest_author]
     #print "LOC:{}, A:{}, C:{}, dict:{}".format(sloc, highest_author, highest_contr, author_contrib)
   else:
     highest_contr = 0
   if sloc <= 0 :
       sloc += 1
   return (round(float(highest_contr)/float(sloc), 5))*100

def getDeveloperScatternessOfFile(param_file_path, repo_path, sloc):
   '''
   output list
   '''
   lineNoProb        = []
   lineNoCnt         = []
   '''
   '''
   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   blameCommand      = " git blame -n " + theFile + " | awk '{print $2}' "
   command2Run       = cdCommand + blameCommand
   lineNoProb        = []

   blame_output      = subprocess.check_output(['bash','-c', command2Run])
   blame_output      = blame_output.split('\n')
   blame_output      = [x_ for x_ in blame_output if x_!='']
   line_chng_dict    = dict(Counter(blame_output))
   #print line_chng_dict
   for lineNo in xrange(sloc):
       line_key  = str(lineNo + 1)
       if (line_key in line_chng_dict):
          line_cnt  = line_chng_dict[line_key]
       else:
          line_cnt  = 0
       line_prob = float(line_cnt)/float(sloc)
       lineNoProb.append(line_prob) ### Version 1
       lineNoCnt.append(line_cnt)   ### Version 2
   #print "len:{}, list:{}, loc:{}".format(len(lineNoProb), lineNoProb, sloc)
   scatterness_prob = round(entropy(lineNoProb), 5)  ##Version 1
   scatterness_cnt  = round(entropy(lineNoCnt), 5)  ##Version 2
   '''
   handling -inf, inf, nan
   '''
   if((scatterness_cnt == float("-inf")) or (scatterness_cnt == float("inf")) or (scatterness_cnt == float("nan")) or math.isnan(scatterness_cnt)):
     scatterness_cnt = float(0)
   #print "list:{} ...\n prob->entropy:{}".format(lineNoProb, scatterness_prob)
   #print "list:{} ...\n count->entropy:{} ...sloc:{}".format(lineNoCnt, scatterness_cnt, sloc)
   #return scatterness_prob, scatterness_cnt
   return scatterness_cnt

'''
neew metric: non soliodity percentage per commit, normalized by number of commits
'''

def getNonSolPerc(param_file_path, repo_path):
    final_metric = 0.0
    cdCommand     = "cd " + repo_path + " ; "
    theFile       = os.path.relpath(param_file_path, repo_path)
    command       = " git log -p " + theFile + "  | grep 'diff' "
    command2Run   = cdCommand + command
    try:
        diff_lines    = subprocess.check_output(['bash','-c', command2Run])
        diff_lines    = diff_lines.split('\n')
        diff_lines    = [x_ for x_ in diff_lines if x_ != '\n' ]
        non_sol_per_lis = []
        for log_output in diff_lines:
            log_output    = log_output.split(' ')
            log_output    = [x_ for x_ in log_output if (('/' in x_) and ('.' in x_))]
            sol_files     = [x_ for x_ in log_output if x_.endswith('.sol')]
            non_sol_files = [x_ for x_ in log_output if x_.endswith('.sol')==False]
            #print sol_files, non_sol_files
            tot_files     = len(sol_files) + len(non_sol_files)
            if tot_files < 1:
               tot_files += 1
            if len(non_sol_files) < 1:
               non_sol_cnt  = 0
            else:
               non_sol_cnt = len(non_sol_files)
            non_sol_per   = float(non_sol_cnt)/float(tot_files)
            non_sol_per_lis.append(non_sol_per)
        if (len(non_sol_per_lis) > 0):
           final_metric = np.mean(non_sol_per_lis)
    except subprocess.CalledProcessError as e_:
        print 'Exception in Git mining ... skipping:' + e_.message

    return final_metric


def createDataset(str2Dump, datasetNameParam):
   headerOfFile0='ORG,SCRIPT_PATH,'
   headerOfFile1='PREV_DEFECT_HISTORY,AVG_ADDPERLOC,'
   headerOfFile2='MED_ADDPERLOC,AVG_DELPERLOC,MED_DELPERLOC,'
   headerOfFile3='CREATION_DATE,'
   headerOfFile4='CURR_DEFECT_STATUS'

   headerStr = headerOfFile0 + headerOfFile1 + headerOfFile2 + headerOfFile3  + headerOfFile4

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

def getStallingsMetrics(file_path_p, repo_path_p, org, full_ds_cat_df ):
   all_process_metrics = ''

   headerOfFile0='ORG,SCRIPT_PATH,'
   headerOfFile1='PREV_DEFECT_HISTORY,AVG_ADDPERLOC,'
   headerOfFile2='MED_ADDPERLOC,AVG_DELPERLOC,MED_DELPERLOC,'
   headerOfFile3='CREATION_DATE,'
   headerOfFile4='CURR_DEFECT_STATUS'

   # print full_ds_cat_df.head()

   file_df   = full_ds_cat_df[full_ds_cat_df['filepath']==file_path_p]
   sorted_df = file_df.sort('msgid', ascending=True)
   print sorted_df.head()

   all_process_metrics = all_process_metrics + org + ',' + repo_path_p + ',' + file_path_p + ','

   return all_process_metrics
