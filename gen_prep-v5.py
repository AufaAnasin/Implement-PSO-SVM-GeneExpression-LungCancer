#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import numpy as np
import GEOparse
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
# from sklearn.svm import SVC
# from sklearn.metrics import accuracy_score


# In[38]:
print("====================================================")
print("GEO Data Processing")
print("Program")
print("Created by: Isman Kurniawan (IKN)")
print("====================================================")


print("GSE code")
gse_code = input(":")

# In[19]:


gse = GEOparse.get_GEO(geo="{}".format(gse_code), destdir="./")


# In[20]:


pivot_data = gse.pivot_samples('VALUE')
flag = (pivot_data.values < 0).any()
if not flag:
    pivot_data = np.log2(pivot_data)
pivot_data = pivot_data.transpose()
pivot_data.head()


# In[24]:


# gse.phenotype_data


# In[25]:


experiments = {}
for i, (idx, row) in enumerate(gse.phenotype_data.iterrows()):
    tmp = {}
    tmp["Experiment"] = idx
#     tmp["Type"] = "control" if "Normal Lung" in row["title"].split('_')[0] else "tumor"
#    tmp["Type"] = row["title"].split('_')[0]
    tmp["Type"] = row["title"]
    experiments[i] = tmp
experiments = pd.DataFrame(experiments).T
experiments.set_index("Experiment", inplace=True)
experiments.head()


# In[26]:


data_set = pd.concat([pivot_data, experiments], axis=1)
data_set.head()


# In[28]:


best_gene = pd.read_csv("{}.top.table.tsv".format(gse_code), sep='\t')
# best_gene = best_gene.iloc[:,1:]
best_gene.head()


# In[32]:


# best_k = 100


# In[31]:


pick_gene = best_gene.iloc[:,0].values.tolist()


# In[32]:


sel_attr = pivot_data.loc[:,pick_gene]
sel_attr.head()


# In[33]:


data_set = pd.concat([sel_attr, experiments], axis=1)
data_set.head()


# In[34]:


data_set.to_csv("{}_data_set.csv".format(gse_code))

print("Processing Done...")


# In[ ]:
