'''
graph utility file for Sep 21, 2017
Thursday
Akond Rahman
'''
import os, csv, numpy as np
import pandas as pd
import subprocess
from itertools import combinations
def getYear(single_date):
    dt2ret = single_date.split('-')[0]
    return dt2ret

def getMonth(single_date):
    dt2ret =  single_date.split('-')[0] + '-' + single_date.split('-')[1]
    return dt2ret

def getTimeInfo(id_param, repo_param):
    dict2see = {}
    if repo_param.endswith('/'):
       repo_param = repo_param
    else:
       repo_param = repo_param + '/'
    file2read = repo_param + 'fullThrottle_msg_file_map.csv'
    with open(file2read, 'rU') as f:
         reader_ = csv.reader(f)
         for row in reader_:
             id_       = row[0]
             ts_    = row[2]
             dict2see[id_] = ts_
    return dict2see[id_param]

def getMonthFileCount(df_param):
    _df = pd.DataFrame(df_param, columns=['ID', 'REPO', 'FILE', 'TIME', 'DEFECTSTATUS'])
    _df['YEAR']  = _df['TIME'].apply(getYear)
    _df['MONTH'] = _df['TIME'].apply(getMonth)
    #print _df.head()
    _df         = _df.sort(['MONTH'])
    _df_mon_cnt = _df.groupby(['MONTH'])[['FILE']].count()

    m_list     = _df_mon_cnt.index.get_level_values('MONTH').tolist()
    m_c_list       = _df_mon_cnt['FILE'].tolist()
    return m_list, m_c_list

def getYearFileCount(df_param):
    _df = pd.DataFrame(df_param, columns=['ID', 'REPO', 'FILE', 'TIME', 'DEFECTSTATUS'])
    _df['YEAR']  = _df['TIME'].apply(getYear)
    _df         = _df.sort(['YEAR'])
    _df_year_cnt = _df.groupby(['YEAR'])[['FILE']].count()

    y_list         = _df_year_cnt.index.get_level_values('YEAR').tolist()
    y_c_list       = _df_year_cnt['FILE'].tolist()
    return y_list, y_c_list

def getAllMonthsFromDataset(categ_file_param):
       str2write = ''
       df_list = []
       '''
       dicionary to hold files for each month
       '''
       month_file_dict, defect_file_dict, repo_file_dict = {}, {}, {}
       with open(categ_file_param, 'rU') as f:
         reader_ = csv.reader(f)
         next(reader_, None)
         for row in reader_:
             id_       = row[0]
             repo_     = row[1]
             categ_    = row[3]
             if categ_=='N':
                 defect_status = '0'
             else:
                 defect_status = '1'
             filepath_ = row[4]
             time_ = getTimeInfo(id_, repo_)
             time2write = time_.split(' ')[0]
             df_list.append((id_, repo_, filepath_, time2write, defect_status))
             '''
             dictionary month
             '''
             month2write = getMonth(time2write)
             if month2write not in month_file_dict:
                 month_file_dict[month2write] = [filepath_]
             else:
                 month_file_dict[month2write] = month_file_dict[month2write] + [filepath_]
             '''
             dictionary files
             '''
             if filepath_ not in defect_file_dict:
                 defect_file_dict[filepath_] = defect_status
             '''
             dictionary repos
             '''
             if filepath_ not in repo_file_dict:
                 repo_file_dict[filepath_] = repo_
       # get all months, and files in the month for the dataset
       m_list, m_c_list = getMonthFileCount(df_list)
       return m_list, month_file_dict, defect_file_dict, repo_file_dict

def getAllYearsFromDataset(categ_file_param):
       str2write = ''
       df_list = []
       '''
       dicionary to hold files for each year
       '''
       year_file_dict, defect_file_dict, repo_file_dict = {}, {}, {}
       with open(categ_file_param, 'rU') as f:
         reader_ = csv.reader(f)
         next(reader_, None)
         for row in reader_:
             id_       = row[0]
             repo_     = row[1]
             categ_    = row[3]
             if categ_=='N':
                 defect_status = '1'
             else:
                 defect_status = '0'
             filepath_ = row[4]
             time_ = getTimeInfo(id_, repo_)
             time2write = time_.split(' ')[0]
             df_list.append((id_, repo_, filepath_, time2write, defect_status))
             '''
             dictionary year
             '''
             y2write = getYear(time2write)
             if y2write not in year_file_dict:
                 year_file_dict[y2write] = [filepath_]
             else:
                 year_file_dict[y2write] = year_file_dict[y2write] + [filepath_]
             '''
             dictionary files
             '''
             if filepath_ not in defect_file_dict:
                 defect_file_dict[filepath_] = defect_status
             '''
             dictionary repos
             '''
             if filepath_ not in repo_file_dict:
                 repo_file_dict[filepath_] = repo_
       # get all years, and files in the year for the dataset
       y_list, y_c_list = getYearFileCount(df_list)
       return y_list, year_file_dict, defect_file_dict, repo_file_dict


def getUniqueDevsForGit(param_file_path, repo_path):

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   #print "full path: {}, repo path:{}, theFile:{}".format(param_file_path, repo_path, theFile)
   commitCountCmd    = " git blame "+ theFile +"  | awk '{print $2}' | cut -d'(' -f2 "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   author_count_output = [x_ for x_ in author_count_output if x_!='']

   return author_count_output

def getUniqueDevsForHg(param_file_path, repo_path):

   cdCommand         = "cd " + repo_path + " ; "
   theFile           = os.path.relpath(param_file_path, repo_path)
   commitCountCmd    = "hg churn --diffstat  " + theFile + " | awk '{print $1}'  "
   command2Run = cdCommand + commitCountCmd

   commit_count_output = subprocess.check_output(['bash','-c', command2Run])
   author_count_output = commit_count_output.split('\n')
   author_count_output = [x_ for x_ in author_count_output if x_!='']

   return author_count_output

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP)
    fileToWrite.close()
    return str(os.stat(fileP).st_size)


'''
Graph construction zone
'''
def getEdges(nodes_param):
    edges_list_to_ret, temp_holder_nodes = [], []
    if (len(nodes_param) > 1):
       edges_list_to_ret = list(combinations(nodes_param, 2))

    return edges_list_to_ret

def constructGraph(prog_list_param):
    nodes = np.unique(prog_list_param)
    edges = getEdges(nodes)
    return nodes, edges



def dumpTempGraphForFile(all_nodes_param, all_edges_param, mon_param, ds_name_param, file_name_param):
    node_str_to_write = ''
    edge_str_to_write = ''
    for node_index in xrange(len(all_nodes_param)):
        node_str_to_write = node_str_to_write + all_nodes_param[node_index] + ',' +  '\n'
    node_str_to_write = 'NODES' + ',' + '\n' + node_str_to_write
    for edge_ in all_edges_param:
        #print edge_
        edge_str_to_write = edge_str_to_write + edge_[0] + ',' + edge_[1] + ',' + '\n'

    edge_str_to_write = 'FROM' + ',' + 'TO' + ',' + '\n' + edge_str_to_write
    output_dir = '/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/' + ds_name_param + '/' + mon_param + '/'
    if(os.path.exists(output_dir)==False):
       os.makedirs(output_dir)
    file2write = file_name_param.replace('/', '.')
    node_output_file = output_dir  + 'node' + file2write + '.csv'
    edge_output_file = output_dir  + 'edge' + file2write + '.csv'
    print node_output_file
    bytes_ = dumpContentIntoFile(node_str_to_write, node_output_file)
    print 'Dumped a `NODE` file of {} bytes'.format(bytes_)
    bytes_ = dumpContentIntoFile(edge_str_to_write, edge_output_file)
    print 'Dumped a `EDGE` file of {} bytes'.format(bytes_)
    #TODO return the file name for nodes and edges
    return node_output_file, edge_output_file
