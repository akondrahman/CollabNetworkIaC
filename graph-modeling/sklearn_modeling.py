from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np, pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation, svm
from sklearn.linear_model import RandomizedLogisticRegression, LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, mean_absolute_error, accuracy_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
import utility

def dumpPredPerfValuesToFile(iterations, predPerfVector, fileName):
   str2write=''
   headerStr='AUC,PRECISION,RECALL,FMEASURE,'
   for cnt in xrange(iterations):
     auc_   = predPerfVector[0][cnt]
     prec_  = predPerfVector[1][cnt]
     recal  = predPerfVector[2][cnt]
     fmeas  = predPerfVector[3][cnt]
     str2write = str2write + str(auc_) + ',' + str(prec_) + ',' + str(recal) + ',' + str(fmeas) + ',' + '\n'
   str2write = headerStr + '\n' + str2write
   bytes_ = Utility.dumpContentIntoFile(str2write, fileName)
   print "Created {} of {} bytes".format(fileName, bytes_)




def evalClassifier(actualLabels, predictedLabels):
  '''
    the way skelarn treats is the following: first index -> lower index -> 0 -> 'Low'
                                             next index after first  -> next lower index -> 1 -> 'high'
  '''
  target_labels =  ['N', 'Y']
  '''
    peeking into the labels of the dataset
  '''
  #print "Glimpse at  actual:{}, and predicted:{} labels(10th entry in label list)".format(actualLabels[10], predictedLabels[10])
  print classification_report(actualLabels, predictedLabels, target_names=target_labels)
  print">"*25
  '''
  getting the confusion matrix
  '''
  #conf_matr_output = confusion_matrix(actualLabels, predictedLabels)
  print "Confusion matrix start"
  #print conf_matr_output
  conf_matr_output = pd.crosstab(actualLabels, predictedLabels, rownames=['True'], colnames=['Predicted'], margins=True)
  print conf_matr_output
  print "Confusion matrix end"
  # preserve the order first test(real values from dataset), then predcited (from the classifier )
  '''
  the precision score is computed as follows:
  '''
  prec_ = precision_score(actualLabels, predictedLabels, average='binary')
  #print "The precision score is:", prec_
  #print">"*25
  '''
  the recall score is computed as follows:
  '''
  recall_ = recall_score(actualLabels, predictedLabels, average='binary')
  #print">"*25
  '''
    are under the curve values .... reff: http://gim.unmc.edu/dxtests/roc3.htm
    0.80~0.90 -> good, any thing less than 0.70 bad , 0.90~1.00 -> excellent
  '''
  #print predictedLabels
  area_roc_output = roc_auc_score(actualLabels, predictedLabels)
  # preserve the order first test(real values from dataset), then predcited (from the classifier )
  #print "Area under the ROC curve is ", area_roc_output
  #print">"*10
  f_measure_output = f1_score(actualLabels, predictedLabels, average='binary')
  '''
    mean absolute error (mae) values .... reff: http://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html
    the smaller the better , ideally expect 0.0
  '''
  #mae_output = mean_absolute_error(actualLabels, predictedLabels)
  # preserve the order first test(real values from dataset), then predcited (from the classifier )
  #print "Mean absolute errro output  is ", mae_output
  #print">"*25
  '''
  accuracy_score ... reff: http://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter .... percentage of correct predictions
  ideally 1.0, higher the better
  '''
  #accuracy_score_output = accuracy_score(actualLabels, predictedLabels)
  # preserve the order first test(real values from dataset), then predcited (from the classifier )
  #print "Accuracy output  is ", accuracy_score_output
  #print">"*10
  '''
    this function returns area under the curve , which will be used
    for D.E. and repated measurements
  '''
  return area_roc_output, prec_, recall_, f_measure_output


def perform_cross_validation(classiferP, featuresP, labelsP, cross_vali_param, infoP):
  predicted_labels = cross_validation.cross_val_predict(classiferP, featuresP , labelsP, cv=cross_vali_param)
  area_roc_to_ret = evalClassifier(labelsP, predicted_labels)
  return area_roc_to_ret




def performCART(featureParam, labelParam, foldParam, infoP):
  theCARTModel = DecisionTreeClassifier()

  cart_area_under_roc = perform_cross_validation(theCARTModel, featureParam, labelParam, foldParam, infoP)
  print "For {}, area under ROC is: {}".format(infoP, cart_area_under_roc[0])
  return cart_area_under_roc



def performRF(featureParam, labelParam, foldParam, infoP):
  theRndForestModel = RandomForestClassifier()

  rf_area_under_roc = perform_cross_validation(theRndForestModel, featureParam, labelParam, foldParam, infoP)
  print "For {} area under ROC is: {}".format(infoP, rf_area_under_roc[0])
  return rf_area_under_roc

def performSVC(featureParam, labelParam, foldParam, infoP):
  theSVMModel = svm.SVC(kernel='rbf').fit(featureParam, labelParam)

  svc_area_under_roc = perform_cross_validation(theSVMModel, featureParam, labelParam, foldParam, infoP)
  print "For {} area under ROC is: {}".format(infoP, svc_area_under_roc[0])
  return svc_area_under_roc


def performLogiReg(featureParam, labelParam, foldParam, infoP):
  theLogisticModel = LogisticRegression()

  theLogisticModel.fit(featureParam, labelParam)
  logireg_area_under_roc = perform_cross_validation(theLogisticModel, featureParam, labelParam, foldParam, infoP)
  print "For {} area under ROC is: {}".format(infoP, logireg_area_under_roc[0])
  return logireg_area_under_roc



def performNaiveBayes(featureParam, labelParam, foldParam, infoP):
  theNBModel = GaussianNB()
  #######theNBModel = MultinomialNB() : not used : throws weird error
  #theNBModel = BernoulliNB()
  '''
  with optimized parameters
  first is mozilla then wiki
  '''
  theNBModel.fit(featureParam, labelParam)
  gnb_area_under_roc = perform_cross_validation(theNBModel, featureParam, labelParam, foldParam, infoP)
  print "For {} area under ROC is: {}".format(infoP, gnb_area_under_roc[0])
  return gnb_area_under_roc


def performModeling(features, labels, foldsParam):
  #r_, c_ = np.shape(features)
  ### lets do CART (decision tree)
  performCART(features, labels, foldsParam, "CART")
  print "="*100
  ### lets do RF (ensemble method: random forest)
  performRF(features, labels, foldsParam, "RF")
  print "="*100
  ### lets do SVC (support vector: support-vector classification)
  performSVC(features, labels, foldsParam, "SVC")
  print "="*100
  ### lets do Logistic regession
  performLogiReg(features, labels, foldsParam, "LogiRegr")
  print "="*100
  ### lets do naive bayes
  performNaiveBayes(features, labels, foldsParam, "Naive-Bayes")
  print "="*100


def dumpPredPerfValuesToFile(iterations, predPerfVector, fileName):
   str2write=''
   headerStr='AUC,PRECISION,RECALL,FMEASURE,'
   for cnt in xrange(iterations):
     auc_   = predPerfVector[0][cnt]
     prec_  = predPerfVector[1][cnt]
     recal  = predPerfVector[2][cnt]
     fmeas  = predPerfVector[3][cnt]
     str2write = str2write + str(auc_) + ',' + str(prec_) + ',' + str(recal) + ',' + str(fmeas) + ',' +  '\n'
   str2write = headerStr + '\n' + str2write
   bytes_ = Utility.dumpContentIntoFile(str2write, fileName)
   print "Created {} of {} bytes".format(fileName, bytes_)



def performIterativeModeling(training_set_param, test_set_param, training_labels_param, actual_labels_param, folderP, iterationP):
  cart_prec_holder, cart_recall_holder, holder_cart = [], [], []
  rf_prec_holder,   rf_recall_holder,   holder_rf   = [], [], []
  svc_prec_holder,  svc_recall_holder,  holder_svc  = [], [], []
  logi_prec_holder, logi_recall_holder, holder_logi = [], [], []
  # Fu's feedback
  fscore_cart_holder, fscore_logi_holder, fscore_nb_holder, fscore_rf_holder, fscore_svc_holder = [], [], [], [], []
  for ind_ in xrange(iterationP):
    ## iterative modeling for CART
    cart_area_roc      = performCART(training_set_param, test_set_param, training_labels_param, actual_labels_param, "CART")[0]
    cart_prec_         = performCART(training_set_param, test_set_param, training_labels_param, actual_labels_param, "CART")[1]
    cart_recall_       = performCART(training_set_param, test_set_param, training_labels_param, actual_labels_param, "CART")[2]
    cart_fmeasu_       = performCART(training_set_param, test_set_param, training_labels_param, actual_labels_param, "CART")[3]
    holder_cart.append(cart_area_roc)
    cart_prec_holder.append(cart_prec_)
    cart_recall_holder.append(cart_recall_)
    fscore_cart_holder.append(cart_fmeasu_)
    cart_area_roc = float(0)
    cart_prec_    = float(0)
    cart_recall_  = float(0)
    cart_fmeasu_  = float(0)

    ## iterative modeling for RF
    rf_area_roc = performRF(training_set_param, test_set_param, training_labels_param, actual_labels_param, "Rand. Forest")[0]
    rf_prec_    = performRF(training_set_param, test_set_param, training_labels_param, actual_labels_param, "Rand. Forest")[1]
    rf_recall_  = performRF(training_set_param, test_set_param, training_labels_param, actual_labels_param, "Rand. Forest")[2]
    rf_fmeasu_  = performRF(training_set_param, test_set_param, training_labels_param, actual_labels_param, "Rand. Forest")[2]
    holder_rf.append(rf_area_roc)
    rf_prec_holder.append(rf_prec_)
    rf_recall_holder.append(rf_recall_)
    fscore_rf_holder.append(rf_fmeasu_)
    rf_area_roc = float(0)
    rf_prec_    = float(0)
    rf_recall_  = float(0)
    rf_fmeasu_  = float(0)

    ## iterative modeling for SVC
    svc_area_roc = performSVC(training_set_param, test_set_param, training_labels_param, actual_labels_param, "Supp. Vector Classi.")[0]
    svc_prec_    = performSVC(training_set_param, test_set_param, training_labels_param, actual_labels_param, "Supp. Vector Classi.")[1]
    svc_recall_  = performSVC(training_set_param, test_set_param, training_labels_param, actual_labels_param, "Supp. Vector Classi.")[2]
    svc_fscore_  = performSVC(training_set_param, test_set_param, training_labels_param, actual_labels_param, "Supp. Vector Classi.")[3]
    holder_svc.append(svc_area_roc)
    svc_prec_holder.append(svc_prec_)
    svc_recall_holder.append(svc_recall_)
    fscore_svc_holder.append(svc_fscore_)
    svc_area_roc = float(0)
    svc_prec_    = float(0)
    svc_recall_  = float(0)
    svc_fscore_  = float(0)

    ## iterative modeling for logistic regression
    logi_reg_area_roc = performLogiReg(training_set_param, test_set_param, training_labels_param, actual_labels_param, "Logi. Regression Classi.")[0]
    logi_reg_preci_   = performLogiReg(training_set_param, test_set_param, training_labels_param, actual_labels_param, "Logi. Regression Classi.")[1]
    logi_reg_recall   = performLogiReg(training_set_param, test_set_param, training_labels_param, actual_labels_param, "Logi. Regression Classi.")[2]
    logi_reg_fmeasu   = performLogiReg(training_set_param, test_set_param, training_labels_param, actual_labels_param, "Logi. Regression Classi.")[3]
    holder_logi.append(logi_reg_area_roc)
    logi_prec_holder.append(logi_reg_preci_)
    logi_recall_holder.append(logi_reg_recall)
    fscore_logi_holder.append(logi_reg_fmeasu)
    logi_reg_area_roc = float(0)
    logi_reg_preci_   = float(0)
    logi_reg_recall   = float(0)
    logi_reg_fmeasu   = float(0)

  print "-"*50
  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("CART", np.mean(holder_cart),
                                                                          np.median(holder_cart), max(holder_cart),
                                                                          min(holder_cart))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("CART", np.mean(cart_prec_holder),
                                                                          np.median(cart_prec_holder), max(cart_prec_holder),
                                                                          min(cart_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("CART", np.mean(cart_recall_holder),
                                                                          np.median(cart_recall_holder), max(cart_recall_holder),
                                                                          min(cart_recall_holder))
  print "*"*25
  print "Summary: F-Measure, for:{}, mean:{}, median:{}, max:{}, min:{}".format("CART", np.mean(fscore_cart_holder),
                                                                          np.median(fscore_cart_holder), max(fscore_cart_holder),
                                                                          min(fscore_cart_holder))
  print "*"*25

  cart_all_pred_perf_values = (holder_cart, cart_prec_holder, cart_recall_holder, fscore_cart_holder)
  dumpPredPerfValuesToFile(iterationP, cart_all_pred_perf_values, folderP+cart_output_file)
  print "-"*50

  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Rand. Forest", np.mean(holder_rf),
                                                                          np.median(holder_rf), max(holder_rf),
                                                                          min(holder_rf))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Rand. Forest", np.mean(rf_prec_holder),
                                                                          np.median(rf_prec_holder), max(rf_prec_holder),
                                                                          min(rf_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Rand. Forest", np.mean(rf_recall_holder),
                                                                          np.median(rf_recall_holder), max(rf_recall_holder),
                                                                          min(rf_recall_holder))
  print "*"*25
  print "Summary: F-Measure, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Rand. Forest", np.mean(fscore_rf_holder),
                                                                          np.median(fscore_rf_holder), max(fscore_rf_holder),
                                                                          min(fscore_rf_holder))
  print "*"*25
  rf_all_pred_perf_values = (holder_rf, rf_prec_holder, rf_recall_holder, fscore_rf_holder)
  dumpPredPerfValuesToFile(iterationP, rf_all_pred_perf_values, folderP+rf_output_file)
  print "-"*50

  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("S. Vec. Class.", np.mean(holder_svc),
                                                                          np.median(holder_svc), max(holder_svc),
                                                                          min(holder_svc))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("S. Vec. Class.", np.mean(svc_prec_holder),
                                                                            np.median(svc_prec_holder), max(svc_prec_holder),
                                                                            min(svc_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("S. Vec. Class.", np.mean(svc_recall_holder),
                                                                            np.median(svc_recall_holder), max(svc_recall_holder),
                                                                            min(svc_recall_holder))
  print "*"*25
  print "Summary: F-Measure, for:{}, mean:{}, median:{}, max:{}, min:{}".format("S. Vec. Class", np.mean(fscore_svc_holder),
                                                                          np.median(fscore_svc_holder), max(fscore_svc_holder),
                                                                          min(fscore_svc_holder))
  print "*"*25
  svc_all_pred_perf_values = (holder_svc, svc_prec_holder, svc_recall_holder, fscore_svc_holder)
  dumpPredPerfValuesToFile(iterationP, svc_all_pred_perf_values, folderP+svm_output_file)
  print "-"*50

  print "Summary: AUC, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Logi. Regression", np.mean(holder_logi),
                                                                          np.median(holder_logi), max(holder_logi),
                                                                          min(holder_logi))
  print "*"*25
  print "Summary: Precision, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Logi. Regression", np.mean(logi_prec_holder),
                                                                            np.median(logi_prec_holder), max(logi_prec_holder),
                                                                            min(logi_prec_holder))
  print "*"*25
  print "Summary: Recall, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Logi. Regression", np.mean(logi_recall_holder),
                                                                            np.median(logi_recall_holder), max(logi_recall_holder),
                                                                            min(logi_recall_holder))
  print "*"*25
  print "Summary: F-Measure, for:{}, mean:{}, median:{}, max:{}, min:{}".format("Logi. Regression", np.mean(fscore_logi_holder),
                                                                          np.median(fscore_logi_holder), max(fscore_logi_holder),
                                                                          min(fscore_logi_holder))
  print "*"*25
  logireg_all_pred_perf_values = (holder_logi, logi_prec_holder, logi_recall_holder, fscore_logi_holder)
  dumpPredPerfValuesToFile(iterationP, logireg_all_pred_perf_values, folderP+logi_output_file)
  print "-"*50
