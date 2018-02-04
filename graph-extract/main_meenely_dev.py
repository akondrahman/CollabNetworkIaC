'''
Akond Rahman
Feb 04, 2018
Meenely's Dev Network
'''

if __name__=='__main__':
    ### INPUT
    theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Cisco_Categ_For_DB.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mirantis_Categ_For_DB.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Mozilla.Final.Categ.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Openstack.WithoutBadBoys.Final.Categ.csv'
    # theCompleteCategFile='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Defect-Categ-Project/output/Wikimedia.Final.Categ.csv'



    ### OUTPUT
    datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dev-ds/CIS.PKL'
    # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dev-ds/MIR.PKL'
    # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dev-ds/MOZ.PKL'
    # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dev-ds/OST.PKL'
    # datasetFile2Save='/Users/akond/Documents/AkondOneDrive/OneDrive/IaC-Graph/dev-ds/WIK.PKL'

    final_dict = getEdgeForFiles(theCompleteCategFile)
    # pickle.dump(final_dict, open(datasetFile2Save, 'wb'))
