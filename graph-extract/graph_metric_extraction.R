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
    mapping_file_df   <- read.csv(mapping_file_name, header=T, sep=',', stringsAsFactors=F) 
    row_cnt <- nrow(mapping_file_df)

    all_file_names  <- mapping_file_df$FILE
    node_file_names <- mapping_file_df$NODE_FILE  
    edge_file_names <- mapping_file_df$EDGE_FILE    
    defect_statuses <- mapping_file_df$DEFECT_STATUS
    ### INITIALIZATION OF VECTORS 
    file_vec   <- c()
    defect_vec <- c()
    
    med_in_deg_vec <- c()
    avg_in_deg_vec <- c()      
    
    med_out_deg_vec <- c()
    avg_out_deg_vec <- c()          
    
    med_all_deg_vec <- c()
    avg_all_deg_vec <- c()              

    assort_vec <- c()
    dia_vec    <- c()                  
    
    med_ecce_vec <- c()
    avg_ecce_vec <- c()                
    
    edge_dens_vec  <- c()
    clus_coeff_vec <- c()                      
    between_vec    <- c()    
    
    med_close_vec <- c()
    avg_close_vec <- c()              
    modularity_vec <- c()             
    
    for(row_ind in 1:row_cnt)
    {
      file_name  <- all_file_names[row_ind]
      node_file  <- node_file_names[row_ind]
      edge_file  <- edge_file_names[row_ind]   
      defect_    <- defect_statuses[row_ind]

      #construct the network        
      nodes <- read.csv(node_file, header=T, as.is=T)
      edges <- read.csv(edge_file, header=T, as.is=T)      
      net <- graph_from_data_frame(d=edges, vertices=nodes, directed=F) 
      
      ### GET THE DEFECT STATUS AND FILE NAME
      file_vec    <- append(file_vec, file_name)
      defect_vec  <- append(defect_vec, defect_)

      # # GET THE METRICS 
      in_degree_  <- degree(net, mode="in")
      med_in_deg  <- median(in_degree_)
      avg_in_deg  <- mean(in_degree_)
      
      med_in_deg_vec <- append(med_in_deg_vec, med_in_deg)
      avg_in_deg_vec <- append(avg_in_deg_vec, avg_in_deg)      

      out_degree_  <- degree(net, mode="out")
      med_out_deg  <- median(out_degree_)
      avg_out_deg  <- mean(out_degree_)

      med_out_deg_vec <- append(med_out_deg_vec, med_out_deg)
      avg_out_deg_vec <- append(avg_out_deg_vec, avg_out_deg)            
      
      all_degree_  <- degree(net, mode="all")
      med_all_deg  <- median(all_degree_)
      avg_all_deg  <- mean(all_degree_)      

      med_all_deg_vec <- append(med_all_deg_vec, med_all_deg)
      avg_all_deg_vec <- append(avg_all_deg_vec, avg_all_deg)                  
      
      assort_val_  <- assortativity_degree(net)
      diam_val_    <- diameter(net, directed=F)
      
      assort_vec <- append(assort_vec, assort_val_)
      dia_vec    <- append(dia_vec, diam_val_)                  
      
      eceentric_   <- eccentricity(net)
      med_ecentric <- median(eceentric_)
      avg_ecentric <- mean(eceentric_)
      
      med_ecce_vec <- append(med_ecce_vec, med_ecentric)
      avg_ecce_vec <- append(avg_ecce_vec, avg_ecentric)                      

      edg_dens     <- edge_density(net, loops=T)
      clust_coeff  <- transitivity(net)
      edge_betw    <- edge.betweenness(net, e=E(net))
      
      edge_dens_vec  <- append(edge_dens_vec, edg_dens)
      clus_coeff_vec <- append(clus_coeff_vec, clust_coeff)                      
      between_vec    <- append(between_vec, edge_betw)       

      closeness   <- closeness(net, vids=V(net))
      avg_close   <- mean(closeness)
      med_close   <- median(closeness)
      
      med_close_vec <- append(med_close_vec, med_close)
      avg_close_vec <- append(avg_close_vec, avg_close)              

      clust_edge_bet <- cluster_edge_betweenness(net) # first create clsuters using Newman's algorithm 
      modula_        <- modularity(clust_edge_bet)    # now calculate modularity 
      modularity_vec <- append(modularity_vec, modula_)    
      
    }
    #### NOW APPEND !!! 
    graph.metric.data <- data.frame(file_vec, med_in_deg_vec, avg_in_deg_vec, 
                                              med_out_deg_vec, avg_out_deg_vec, 
                                              med_all_deg_vec, avg_all_deg_vec, 
                                              assort_vec, dia_vec, 
                                              med_ecce_vec, avg_ecce_vec,
                                              edge_dens_vec, clus_coeff_vec, between_vec, 
                                              med_close_vec, avg_close_vec, modularity_vec, 
                                              defect_vec)
    print(head(graph.metric.data))
    print("================================================")
  }
}




t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))

# transitivity(test.graph,type="local")
# # gives the clustering coefficient of each node

#       print(degree_)
#       V(net)$size <- degree_ * 2
#       
#       # Set edge width based on weight:
#       E(net)$width <- E(net)$weight/6
#       
#       #change arrow size and edge color:
#       E(net)$arrow.size <- .2
#       E(net)$edge.color <- "blue"
#       E(net)$width <- 1 + E(net)$weight / 12
#       
#       # plot(net, edge.arrow.size=.5,  edge.curved=.1, vertex.shape="square" )


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