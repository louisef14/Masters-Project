#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import linregress 

#method for preparing and collating the data
sample_map=pd.read_csv('projectname_platenumber_wells.csv',header=None)
sample_map
rfu_cq_data=pd.read_csv('projectname_platenumber_RFU_Cq.csv')
rfu_cq_data=rfu_cq_data.filter(['Well','End RFU','Cq'])
list_of_samples= sample_map.values.tolist()
flattened_samples = [val for sublist in list_of_samples for val in sublist]
locations = ['A01','A02','A03','A04','A05','A06','A07','A08','A09','A10','A11','A12',
            'B01','B02','B03','B04','B05','B06','B07','B08','B09','B10','B11','B12',
            'C01','C02','C03','C04','C05','C06','C07','C08','C09','C10','C11','C12',
            'D01','D02','D03','D04','D05','D06','D07','D08','D09','D10','D11','D12',
            'E01','E02','E03','E04','E05','E06','E07','E08','E09','E10','E11','E12',
            'F01','F02','F03','F04','F05','F06','F07','F08','F09','F10','F11','F12',
            'G01','G02','G03','G04','G05','G06','G07','G08','G09','G10','G11','G12',
            'H01','H02','H03','H04','H05','H06','H07','H08','H09','H10','H11','H12']
mapped_data= pd.DataFrame(list(zip(locations, flattened_samples)), 
               columns =['Well', 'Sample_id']) 
combined_data= mapped_data.merge(rfu_cq_data, left_on='Well', right_on='Well')
mapping_data=pd.read_csv('project_mapped_unmapped_reads_data.csv',header=None)
mapping_data= mapping_data.T
mapping_data.columns = ['Sample_id', 'Unmapped', 'Mapped','TotalReads','PercentMapped']
mapping_data = mapping_data.iloc[1:]
mapping_data['Sample_id'] = mapping_data['Sample_id'].str[2:]
final_data=combined_data.merge(mapping_data, on='Sample_id', how='right') 
final_data.to_csv('combineddata_projectname_platenumber.csv')


#method for creating linear regression between PCR-related metrics and between sequencing performance indicators
plt.style.use('seaborn')
data=pd.read_csv('controlgroupname.csv') '
Data= data.where(data['controlgroupname']=="variableonXaxis, variableonYaxis")
Data=Data.dropna()
X=Data["variableonXaxis"]
Y=Data["variableonYaxis"]
Regressdata=linregress(X,Y)

ax = sns.regplot(x="", y="", data=data, color='purple')
sns.set_style("white")
plt.xlabel('', weight='bold', fontsize=14)
plt.ylabel('',weight='bold',fontsize=14)
plt.title('control group name and what variables are being regressed ',weight='bold', fontsize=14)
plt.suptitle('p=, r=-',weight='bold')
plt.subplots_adjust(top=1.0)
fig = ax.get_figure()
fig.savefig('Control group name and what variables are being regressed.jpg')


#method for creating FacetGrids 
plate1= pd.read_csv('combineddata_projectname_platenumber.csv') 
plate1=plate1.filter(['Well','Sample_id','End RFU','Cq','Unmapped','TotalReads','PercentMapped']) 
plate2= pd.read_csv('combineddata_projectname_platenumber.csv') 
plate2= plate2.filter(['Well','Sample_id','End RFU','Cq','Unmapped','TotalReads','PercentMapped']) 
plate3= pd.read_csv('combineddata_projectname_platenumber.csv') 
plate3=plate3.filter(['Well','Sample_id','End RFU','Cq','Unmapped','TotalReads','PercentMapped']) 
plate4= pd.read_csv('combineddata_projectname_platenumber.csv') 
plate4=plate4.filter(['Well','Sample_id','End RFU','Cq','Unmapped','TotalReads','PercentMapped']) 
plate1['projectname']= 'Plate 1' 
plate2['projectname']= 'Plate 2'
plate3['projectname']= 'Plate 3' 
plate4['projectname']= 'Plate 4'
data=pd.concat([plate1,plate2,plate3,plate4]) 

Dataplate1= data.where(data['projectname']=="Plate 1")
Dataplate1=Dataplate1.dropna()
X=Dataplate1["variableonXaxis"]
Y=Dataplate1["variableonYaxis"]
Regressplate1=linregress(X,Y)
plate1['projectname']= 'Plate 1, p=, r=' 
#repeat linear regression for plates 2-4

g= sns.FacetGrid(data, col="projectname",col_wrap=2)
g= (g.map(sns.regplot, "variableonXaxis", "variableonYaxis",scatter_kws={'s':2, "color": "black"}))
g.set_titles(col_template="{col_name}", fontsize=18,) 
g.set_axis_labels(x_var="", y_var="")
plt.subplots_adjust(top=0.85)
g.fig.suptitle('Project name and variables being regressed',fontweight='bold', fontsize=12)
g.fig.set_size_inches(8,8)
g.savefig('Project name and variables being regressed.jpg')

