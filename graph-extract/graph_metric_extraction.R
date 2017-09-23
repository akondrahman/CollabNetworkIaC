cat("\014") 
library('igraph')
options(max.print=1000000)
t1 <- Sys.time()

# dirs2search <- list.dirs('/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/MOZILLA/', recursive=FALSE)
# the_name_  <- 'MOZILLA'

# dirs2search <- list.dirs('/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/OPENSTACK/', recursive=FALSE)
# the_name_  <- 'OPENSTACK'

# dirs2search <- list.dirs('/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dataset/WIKIMEDIA/', recursive=FALSE)
# the_name_  <- 'WIKIMEDIA'


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
    file_vec    <- c()
    defect_vec  <- c()
    ds_name_    <- c()

    node_cnt_vec <- c()
    edge_cnt_vec <- c()
    
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
    
    med_bet_vec <- c()
    avg_bet_vec <- c()
    
    med_close_vec <- c()
    avg_close_vec <- c()              
    modularity_vec <- c()             
    
    ##track which files ahve been processed ... 
    file_tracker <- c()
    
    for(row_ind in 1:row_cnt)
    {
      file_name  <- all_file_names[row_ind]
      node_file  <- node_file_names[row_ind]
      edge_file  <- edge_file_names[row_ind]   
      defect_    <- defect_statuses[row_ind]

      print(file_name)
      if(file_name %in% file_tracker)
      {
          print('Already processed ... skipping ...')
      }
      else
      {
        ## add current file to tracker 
        file_tracker <- append(file_tracker, file_name)    
        
        if((file.exists(edge_file)) & (file.exists(node_file)))
        {
          #construct the network        
          print(edge_file)
          nodes <- read.csv(node_file, header=T, as.is=T)
          edges <- read.csv(edge_file, header=T, as.is=T)      
          net <- graph_from_data_frame(d=edges, vertices=nodes, directed=F) 
          
          ### GET THE DEFECT STATUS AND FILE NAME
          file_vec    <- append(file_vec, file_name)
          defect_vec  <- append(defect_vec, defect_)
          ds_name_    <- append(ds_name_, the_name_)
          
          
          # # GET THE METRICS 
          edge_cnt     <- length(E(net))
          node_cnt     <- length(V(net)) 
          node_cnt_vec <- append(node_cnt_vec, node_cnt)
          edge_cnt_vec <- append(edge_cnt_vec, edge_cnt)
          
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
          
          
          edge_dens_vec  <- append(edge_dens_vec, edg_dens)
          clus_coeff_vec <- append(clus_coeff_vec, clust_coeff)                      
          
          edge_betw    <- edge.betweenness(net, e=E(net))
          med_e_bet    <- median(edge_betw)
          avg_e_bet    <- mean(edge_betw)
          
          med_bet_vec  <- append(med_bet_vec, med_e_bet)       
          avg_bet_vec  <- append(avg_bet_vec, avg_e_bet)       
          
          
          closeness   <- closeness(net, vids=V(net))
          avg_close   <- mean(closeness)
          med_close   <- median(closeness)
          
          med_close_vec <- append(med_close_vec, med_close)
          avg_close_vec <- append(avg_close_vec, avg_close)              
          
          clust_edge_bet <- cluster_edge_betweenness(net) # first create clsuters using Newman's algorithm 
          modula_        <- modularity(clust_edge_bet)    # now calculate modularity 
          modularity_vec <- append(modularity_vec, modula_)      
        }        
      }
    }
    
    #### NOW APPEND !!! 
    print(dir2search)
#     graph.metric.data <- data.frame(ds_name_, file_vec, node_cnt_vec, edge_cnt_vec, 
#                                               med_in_deg_vec, avg_in_deg_vec, 
#                                               med_out_deg_vec, avg_out_deg_vec, 
#                                               med_all_deg_vec, avg_all_deg_vec, 
#                                               dia_vec, 
#                                               med_ecce_vec, avg_ecce_vec,
#                                               edge_dens_vec, 
#                                               med_bet_vec, avg_bet_vec, 
#                                               med_close_vec, avg_close_vec, modularity_vec, 
#                                               defect_vec)

    graph.metric.data <- data.frame(ds_name_, file_vec, node_cnt_vec, edge_cnt_vec, 
                                med_all_deg_vec,  
                                edge_dens_vec, 
                                med_close_vec, 
                                defect_vec)

    print(head(graph.metric.data))
#     col_headers <- c( 'repo_name', 'file_name', 'v_count', 'e_count', 'med_indeg', 'avg_indeg', 'med_outdeg', 'avg_outdeg', 
#                                                               'med_alldeg', 'avg_alldeg', 'dia', 
#                                                               'med_ecc', 'avg_ecc', 'e_density', 
#                                                               'med_bet', 'avg_bet', 'med_closeness', 'avg_closeness', 
#                                                               'modu', 'defect_status'
#                     )
    col_headers <- c( 'repo_name', 'file_name', 'v_count', 'e_count', 'med_alldeg', 'e_density', 
                      'med_closeness', 'defect_status'
    )
    colnames(graph.metric.data) <- col_headers
    output_file                 <- paste0(dir2search, 'FINAL.GRAPH.METRIC.csv', sep='')
    write.table(graph.metric.data, file=output_file, col.names = T, sep = ",", row.names = F, quote = FALSE)
    print("================================================")
  }
}


t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))