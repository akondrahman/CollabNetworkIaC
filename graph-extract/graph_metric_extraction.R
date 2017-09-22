cat("\014") 
library('igraph')
options(max.print=1000000)
t1 <- Sys.time()

dirs2search <- list.dirs('/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/', recursive=FALSE)
#print(dir2search)
for(dir2search in dirs2search)
{
  dir2search <- paste0(dir2search, '/', sep='')  
  files_     <- list.files(dir2search)
  fil_cnt    <- length(files_)
  if(fil_cnt > 1)
  {
    mapping_file_name <- paste0(dir2search, 'temp.mapping.csv', sep='')
    #print(mapping_file_name)
    mapping_file_df   <- read.csv(mapping_file_name, header=T, sep=',', stringsAsFactors=F) 
    #print(head(mapping_file_df))
    row_cnt <- nrow(mapping_file_df)
    #print(row_cnt)
    
    
    all_file_names  <- mapping_file_df$FILE
    node_file_names <- mapping_file_df$NODE_FILE  
    edge_file_names <- mapping_file_df$EDGE_FILE    
    for(row_ind in 1:row_cnt)
    {
      file_name  <- all_file_names[row_ind]
      node_file  <- node_file_names[row_ind]
      edge_file  <- edge_file_names[row_ind]    
      #print((file_name))
      #print(node_file)
      #construct the network        
      nodes <- read.csv(node_file, header=T, as.is=T)
      edges <- read.csv(edge_file, header=T, as.is=T)
      
      net <- graph_from_data_frame(d=edges, vertices=nodes, directed=T) 
      
      # # Compute node degrees (#links) and use that to set node size:
      print("Degree ...")
      degree_ <- degree(net, mode="in")
      print(degree_)
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
      print(edge_density(net, loops=T))
      print("Transitivity")
      print(transitivity(net))
      # gives the clustering coefficient of the whole network            
      # Betweenness is the number of shortest paths between two nodes that go through each node of interest
      print("Betweenness")
      #print(betweenness(net, v=V(net)))
      print(edge.betweenness(net, e=E(net)))
      # Closeness refers to how connected a node is to its neighbors
      print("Closeness")
      print(closeness(net, vids=V(net)))
      #print("Eigen centraility")
      #print(eigen_centrality(net))
      print("Closeness centraility")
      print(median(closeness(net)))
      print("Modularity")
      clust_edge_bet <- cluster_edge_betweenness(net)
      #wtc <- cluster_walktrap(net)
      print(modularity(clust_edge_bet))
      print("================================================")
    }   
  }
}




t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))

# transitivity(test.graph,type="local")
# # gives the clustering coefficient of each node



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



# for(filename_ in filenames)
# {
#   #TODO read from file : get node file name and get edge file name 
#   
#   nodes <- read.csv("/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/2012-10/node.Users.akond.PUPP_REPOS.wikimedia-downloads.cdh4.manifests.hadoop.pp.csv", header=T, as.is=T)
#   edges <- read.csv("/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/2012-10/edge.Users.akond.PUPP_REPOS.wikimedia-downloads.cdh4.manifests.hadoop.pp.csv", header=T, as.is=T)
#   
#   net <- graph_from_data_frame(d=edges, vertices=nodes, directed=T) 
#   
#   # # Compute node degrees (#links) and use that to set node size:
#   print("Degree ...")
#   degree_ <- degree(net, mode="all")
#   degree_
#   V(net)$size <- degree_ * 2
#   
#   # Set edge width based on weight:
#   E(net)$width <- E(net)$weight/6
#   
#   #change arrow size and edge color:
#   E(net)$arrow.size <- .2
#   E(net)$edge.color <- "blue"
#   E(net)$width <- 1 + E(net)$weight / 12
#   
#   # plot(net, edge.arrow.size=.5,  edge.curved=.1, vertex.shape="square" )
#   
#   print("Assortivity")
#   print(assortativity_degree(net))
#   print("Diameter")
#   print(diameter(net, directed=F))
#   print("Eccentricity")
#   print(eccentricity(net))
#   print("Page rank")
#   page_rank(net)$vector
#   print("Edge density")
#   edge_density(net, loops=T)
#   
# }