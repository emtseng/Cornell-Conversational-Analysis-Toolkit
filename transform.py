#!/usr/bin/env python
# coding: utf-8

# # Creating Our Dataset and Applying Our Transformer
# 
# In this notebook, we:
# - download friends-corpus
# - apply our Transformer, Genderromantic, to it
# - analyze the resulting measures

# In[4]:


get_ipython().system('python3 -m pip install -r requirements.txt')


# In[5]:


import convokit
convokit


# In[6]:


from convokit import Corpus


# # Download locally stored corpus

# In[7]:


corpus = Corpus(filename='./datasets/friends-corpus/corpus')


# # Use locally defined Transformer

# In[8]:


from convokit import Genderromantic
Genderromantic


# In[9]:


grr = Genderromantic()


# In[10]:


transformed_corpus = grr.fit_transform(corpus)


# In[11]:


next(transformed_corpus.iter_utterances())


# In[12]:


transformed_corpus.get_utterance('s01_e01_c01_u001')


# # Running Statistics on Utterance-Level

# In[102]:


mf=[]
fm=[]
rom=[]
utt_count=0
utterance_ids = transformed_corpus.get_utterance_ids()
for uid in utterance_ids:
    utt=transformed_corpus.get_utterance(uid)
    utt_count=utt_count+1 
    mf2=utt.meta["male_about_female"]
    mf.append(mf2)
    fm2=utt.meta["female_about_male"]
    fm.append(fm2)
    rom2=utt.meta["contains_romantic"]
    rom.append(rom2)
print(utt_count)
counts=[]
x=mf.count(True)
counts.append(x)
xx=mf.count(False)
counts.append(xx)
y=fm.count(True)
counts.append(y)
yy=fm.count(False)
counts.append(yy)
z=rom.count(True)
counts.append(z)
zz=rom.count(False)
counts.append(zz)

print(counts)


# # Running Statistics on Conversation-Level

# In[197]:


convo={}
mf=[]
fm=[]
rom=[]
id2=[]
total_utt=0
utt_count=0
utterance_ids = transformed_corpus.get_utterance_ids()
current_scene=utterance_ids[0][:11]
current_scene2=1
for uid in utterance_ids:
    utt=transformed_corpus.get_utterance(uid)
    if uid[:11]==current_scene:
        total_utt=total_utt+1
        mf2=utt.meta["male_about_female"]
        if mf2==True:
            mf.append(mf2)
        fm2=utt.meta["female_about_male"]
        if fm2==True:
            fm.append(fm2)
        rom2=utt.meta["contains_romantic"]
        if rom2==True:    
            rom.append(rom2)
    else:
        current_scene=uid[:11]
        current_scene2=current_scene2+1
        mf=[]
        fm=[]
        rom=[]
        total_utt=0
    convo[current_scene2] = {'total utterances': total_utt, 'male-female': mf, 'female-male': fm, 'romantic': rom}
    


# In[185]:


#convo.keys()


# In[212]:


r= [(current_scene2, total_utt, len(convo[current_scene2]['romantic']), len(convo[current_scene2]['male-female']), len(convo[current_scene2]['female-male'])) for current_scene2 in convo.keys()]


# In[213]:


import pandas as pd
r=pd.DataFrame.from_dict(r)
r.columns=['scene', 'total_utterances', 'romantic', 'male-female', 'female-male']
print(r)


# # Average Number of Romantic Utterances

# In[214]:


def calculate_average(row):
    return ((row['romantic'])/(row['total_utterances']))*100

r.apply(calculate_average, axis=1)
r['avg_rom'] = r.apply(calculate_average, axis=1)

avg_rom=[]
x= r['avg_rom'].mean()
avg_rom.append(x)

y= r['avg_rom'].min()
avg_rom.append(y)

z= r['avg_rom'].max()
avg_rom.append(z)


print(avg_rom)


# In[215]:


#Female 

#Total number of female-male only conversations
f_all = len(r[(r['male-female']==0) & (r['female-male']>=1)]) # (255)
print(f_all)
#Total number of female-male only conversations with no romantic 
f_nr = len(r[(r['male-female']==0) & (r['female-male']>=1)] & (r['romantic']==0))
print(f_nr)
#Total number of female-male only conversations with some romantic
f_r = len(r[(r['male-female']==0) & (r['female-male']>=1)] & (r['romantic']>=1))
print(f_r)

#Male

#Total number of male-female only conversations
f_all = len(r[(r['female-male']==0) & (r['male-female']>=1)]) # (255)
print(f_all)
#Total number of male-female only conversations with no romantic 
f_nr = len(r[(r['female-male']==0) & (r['male-female']>=1)] & (r['romantic']==0))
print(f_nr)
#Total number of male-female only conversations with some romantic
f_r = len(r[(r['female-male']==0) & (r['male-female']>=1)] & (r['romantic']>=1))
print(f_r)


# In[ ]:




