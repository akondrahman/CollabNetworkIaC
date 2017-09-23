cat("\014") 
library(reshape2)  
library(FSelector)
options(max.print=1000000)
t1 <- Sys.time()
library(rpart)

#### MOZILLA
datasets <-c("/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/MOZILLA/2012/FINAL.GRAPH.METRIC.csv", 
             "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/MOZILLA/2013/FINAL.GRAPH.METRIC.csv", 
             "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/MOZILLA/2014/FINAL.GRAPH.METRIC.csv", 
             "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/MOZILLA/2015/FINAL.GRAPH.METRIC.csv",
             "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/MOZILLA/2016/FINAL.GRAPH.METRIC.csv"
)

# #### OPENSTACK
# datasets <-c("/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/OPENSTACK/2011/FINAL.GRAPH.METRIC.csv", 
#              "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/OPENSTACK/2012/FINAL.GRAPH.METRIC.csv", 
#              "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/OPENSTACK/2013/FINAL.GRAPH.METRIC.csv", 
#              "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/OPENSTACK/2014/FINAL.GRAPH.METRIC.csv", 
#              "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/OPENSTACK/2015/FINAL.GRAPH.METRIC.csv",
#              "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/OPENSTACK/2016/FINAL.GRAPH.METRIC.csv"
# )


# #### WIKIMEDIA
# datasets <-c("/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/2013/FINAL.GRAPH.METRIC.csv", 
#              "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/2014/FINAL.GRAPH.METRIC.csv", 
#              "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/2015/FINAL.GRAPH.METRIC.csv",
#              "/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/2016/FINAL.GRAPH.METRIC.csv"
# )

dep_var     <- "defect_status"

for(file_ in datasets)
{
  print(file_)
  dataset                  <- read.csv(file_)   
  dataset$defect_status    <- as.character(dataset$defect_status) ### keep an eye on the dependent variable 
  
  cols2drop                <- c(1, 2)
  dataset                  <- dataset[, -cols2drop]
  ds_row                   <- dim(dataset)[1]
  ds_col                   <- dim(dataset)[2]
  print('Specifying input for best first search feature selection ...')
  dataset_    <- dataset
  dep_var_ind <- ds_col  ## last olumn index is the dependent variable
  
  evaluator <- function(subset) 
  {
    #k-fold cross validation
    k <- 5
    splits <- runif(nrow(dataset_))
    results = sapply(1:k, function(i) 
    {
      test.idx <- (splits >= (i - 1) / k) & (splits < i / k)
      train.idx <- !test.idx
      test <- dataset_[test.idx, , drop=FALSE]
      train <- dataset_[train.idx, , drop=FALSE]
      
      tree <- rpart(as.simple.formula(subset, dep_var), train)
      test_def_stat <- test$defect_status
      #print("----------")
      #print(test_def_stat)
      pred_res <- predict(tree, test, type="c")
      #print(pred_res)
      error_rate = sum( test_def_stat != pred_res ) / nrow(test)  
      #print(error_rate)
      #print("----------")      
      return(1 - error_rate)
    })
    print("**********")
    print(subset)
    print(mean(results))
    print("**********")    
    return(mean(results))
  }
  
  #print(dataset_$defect_status)  
  features_ <- names(dataset_)[-dep_var_ind] 
  subset <- best.first.search(features_, evaluator)
  formula <- as.simple.formula(subset, dep_var)
  #print(features_) 
  print('=================================================================')
  print(file_)
  print(formula)
  
  
}

t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))