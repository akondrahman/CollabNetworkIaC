cat("\014") 
library('igraph')
options(max.print=1000000)
t1 <- Sys.time()

dir2search <- list.dirs('/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/', recursive=FALSE)
#print(dir2search)
file_names <-c('/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/2012-10/Users.akond.PUPP_REPOS.wikimedia-downloads.cdh4.manifests.hadoop.pp')

for(filename_ in dir2search)
{
   #TODO read from file : get node file name and get edge file name 
  
  nodes <- read.csv("/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/2012-10/node.Users.akond.PUPP_REPOS.wikimedia-downloads.cdh4.manifests.hadoop.pp.csv", header=T, as.is=T)
  edges <- read.csv("/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/2012-10/edge.Users.akond.PUPP_REPOS.wikimedia-downloads.cdh4.manifests.hadoop.pp.csv", header=T, as.is=T)
  
  net <- graph_from_data_frame(d=edges, vertices=nodes, directed=T) 
  
  # # Compute node degrees (#links) and use that to set node size:
  print("Degree ...")
  degree_ <- degree(net, mode="all")
  degree_
  V(net)$size <- degree_ * 2
  
  # Set edge width based on weight:
  E(net)$width <- E(net)$weight/6
  
  #change arrow size and edge color:
  E(net)$arrow.size <- .2
  E(net)$edge.color <- "blue"
  E(net)$width <- 1 + E(net)$weight / 12
  
  # plot(net, edge.arrow.size=.5,  edge.curved=.1, vertex.shape="square" )
  
  print("Assortivity")
  print(assortativity_degree(net))
  print("Diameter")
  print(diameter(net, directed=F))
  print("Eccentricity")
  print(eccentricity(net))
  print("Page rank")
  page_rank(net)$vector
  print("Edge density")
  edge_density(net, loops=T)
  
}


t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))





# only_file_name=basename(file2search)
# if(substr(only_file_name, start=1, stop=4)=='node')
# {
#   node_file_vec <- append(node_file_vec, file2search)
# }
# if(substr(only_file_name, start=1, stop=4)=='edge')
# {
#   print(file2search)
#   edge_file_vec <- append(edge_file_vec, file2search)
# }
