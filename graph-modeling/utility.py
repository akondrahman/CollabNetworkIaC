'''
Akond Rahman
Utility for graph prediction
Sep 23, 2017

'''
import numpy as np, math, os 


def createLogTransformedFeatures(allFeatureParam):
  log_transformed_feature_dataset_to_ret = []
  dataset_rows = len(allFeatureParam)
  print "-"*50
  print "Dataset rows:",dataset_rows
  print "-"*50
  for ind_ in xrange(dataset_rows):
    features_for_this_index = allFeatureParam[ind_, :]
    ## do the log tranform on the extracted index
    ## the following code handles the issue for zero values
    log_transformed_features_for_index = [math.log1p(x_) for x_ in features_for_this_index]
    log_transformed_feature_dataset_to_ret.append(log_transformed_features_for_index)
  ## convert to numpy  array
  log_transformed_feature_dataset_to_ret = np.array(log_transformed_feature_dataset_to_ret)
  return log_transformed_feature_dataset_to_ret


def getDatasetFromCSV(fileParam, dataTypeFlag=True):
  if dataTypeFlag:
    data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1, dtype='float')
  else:
        data_set_to_return = np.genfromtxt(fileParam, delimiter=',', skip_header=1,  dtype='str')
  return data_set_to_return


def getFeaturesAndLabels(file_name_param):
       training_dataset = getDatasetFromCSV(file_name_param)
       full_rows, full_cols = np.shape(training_dataset)
       feature_cols = full_cols - 1  ## the last column is defect status, so one column to skip
       training_features = training_dataset[:, 2:feature_cols]
       '''
       lets transform all the features via log transformation
       '''
       log_transformed_train_features = createLogTransformedFeatures(training_features)
       '''
       get labels
       '''
       dataset_for_labels = getDatasetFromCSV(file_name_param)
       label_cols = full_cols - 1
       all_labels  =  dataset_for_labels[:, label_cols]
       defected_file_count     = len([x_ for x_ in all_labels if x_==1.0])
       non_defected_file_count = len([x_ for x_ in all_labels if x_==0.0])
       print "No of. defects={}, non-defects={}".format(defected_file_count, non_defected_file_count)
       print "-"*50
       return log_transformed_train_features, all_labels





def dumpContentIntoFile(strP, fileP):
  fileToWrite = open( fileP, 'w')
  fileToWrite.write(strP )
  fileToWrite.close()
  return str(os.stat(fileP).st_size)
