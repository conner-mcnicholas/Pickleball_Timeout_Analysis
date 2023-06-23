#!/usr/bin/env python
# coding: utf-8

# In[149]:


import pandas as pd
pd.set_option('mode.chained_assignment', None)
pd.set_option('display.max_rows', 500)
import warnings
warnings.filterwarnings('ignore') # setting ignore as a parameter
import numpy as np 
import random
import psycopg2
import logging


# In[2]:


conn = psycopg2.connect(database="postgres",
                        host="pklmart.ckkvdwandqoa.us-east-1.rds.amazonaws.com",
                        user="cmcnicholas",
                        passworad="momentum101",
                        port="5432")
conn.autocommit = True


# In[155]:


#now we will Create and configure logger 
logging.basicConfig(filename="rallylog.log", format='%(message)s', filemode='w') 

#Let us Create an object 
logger=logging.getLogger() 

#Now we are going to Set the threshold of logger to DEBUG 
logger.setLevel(logging.WARNING) 


# In[3]:


def pullawsdata(tablename):
    with conn,conn.cursor() as cursor:
        try:
            cursor.execute(f"SELECT column_name FROM information_schema.columns where table_name=\'{tablename}\';")
            cols=cursor.fetchall()
            cols = [cols[x][0] for x in range(len(cols))]
            cursor.execute(f"SELECT * FROM pklm_prd.{tablename}")
            data=cursor.fetchall()
            return(pd.DataFrame(data,columns=cols))
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)


# In[4]:


rly = pullawsdata('rally')
numtos = sum(rly.to_team_id != 'N/A')
numrallies = sum(rly.to_team_id == 'N/A')
numsrvwin = sum(rly.srv_team_id == rly.w_team_id)
pctsrvwin = round(100*numsrvwin/numrallies,2)
print(f'total number of rallies in dataset: {numrallies} (ignores {numtos} timeouts)')
print(f'serving team won {pctsrvwin}% of rallies')


# In[5]:


df_coinsim = pd.DataFrame([],columns=['scoreA','scoreB','srv_team','win_team','to_ind','to_team_id'])
df_coinsim


# In[151]:


def coinsim(n,p,t):
    logging.info(f'simulating game:\n\tfirst to {n} points (win by 2)     #\n\twith odds of serving team winning rally: {p}% \
    #\n\twith {t} random timeouts')
    scoredict = {'A':0,'B':0}
    srvr,rcvr = list(np.random.choice(['A','B'],size=2,replace=False, p=[0.50,0.50]))
    global rallynum 
    rallynum = 0 
    
    #first to 11 wins
    while gameon(n,scoredict):
        logging.info(f'\nscore -> A:{scoredict["A"]} | B:{scoredict["B"]}')
        scoredict,srvr = serveround(scoredict,srvr,n,p) 
        
    logging.info(f'final score after {rallynum} rallies -- A:{scoredict["A"]}{(1-scoredict["A"]//10)*" "} | B:{scoredict["B"]}')
    logging.info(f'\n\n\t\t\tWINNER: {list(scoredict.keys())[list(scoredict.values()).index(max(scoredict.values()))]}')


# In[152]:


def gameon(n,scoredict):
    bothunderN = max(scoredict.values()) < n
    #if neither team has reached 11, continue playing
    if bothunderN:
        return True
    #if 11 has been reached, make sure winner has won by 2
    else:
        scorediff = abs(scoredict['A']-scoredict['B'])
        wonbytwo = scorediff >= 2
        #if either team has reached 11 but does not have 2 more points than the other, continue playing
        if wonbytwo == False:
            if scorediff == 0:
                logging.info('\t\tDEUCES!')
            else:
                logging.info(f'\t\tADVANTAGE: {list(scoredict.keys())[list(scoredict.values()).index(max(scoredict.values()))]}')
            return True
        #if either team has reached 11 and has 2 more points than the other, the game is over
        else:
            return False
        


# In[153]:


#simulates one full round of serving
def serveround(scoredict,srvr,n,p):
    rcvr = list({'A','B'}.symmetric_difference(srvr))[0]
    logging.info(f'server: {srvr} | receiver: {rcvr}')
    
    #start of 1st server
    srvnum = 1
    
    #serving team changes after losing 2 rallies
    while srvnum <= 2 and gameon(n,scoredict):
        global rallynum
        rallynum += 1
        logging.info(f'\n\tSTART OF RALLY SCORE -> A:{scoredict["A"]} | B:{scoredict["B"]}')
        logging.info(f'{srvr} #{srvnum} serving')
        #server has 45% chance of winning rally
        winr = list(random.choices([srvr,rcvr],cum_weights = (p,1.00),k=1))[0]
        #if server wins
        if srvr == winr:
            #add 1 to serving team's score
            logging.info(f'server({srvr}) won rally, still server #{srvnum}')
            scoredict[srvr] += 1
            
        #if serving team loses
        else:
            #add 1 to server number
            srvnum += 1
            logging.info(f'server({srvr}) lost rally, server # now {srvnum}')
        logging.info(f'\tEND OF RALLY SCORE -> A:{scoredict["A"]} | B:{scoredict["B"]}\n')
        
    #change server after losing rally on second server
    newserver = list({'A','B'}.symmetric_difference(srvr))[0]
    
    logging.info(f'serveround RETURNING ({scoredict},{newserver})\n')

    #return score and new serving team
    return (scoredict,newserver)


# In[158]:


n=11
listrlycnt  = []
for c in range(10001):
    rallynum = 0
    coinsim(n,.4204,3)
    listrlycnt.append(rallynum)
print(f'average number of rallies in {c} SIMULATED games to {n}: {round(np.mean(listrlycnt),1)}')


# In[159]:


n=15
listrlycnt  = []
for c in range(10001):
    rallynum = 0
    coinsim(n,.4204,3)
    listrlycnt.append(rallynum)
print(f'average number of rallies in {c} SIMULATED games to {n}: {round(np.mean(listrlycnt),1)}')


# In[88]:


rally = pullawsdata('rally')
rally = rally[['game_id', 'rally_id', 'rally_nbr', 'srv_team_id', 'w_team_id', 'to_team_id']]
rally['game_id'] = [int(x[1:]) for x in rally.game_id]
rally['rally_id'] = [int(x[1:]) for x in rally.rally_id]
rally = rally.sort_values(['game_id', 'rally_id', 'rally_nbr']).reset_index(drop=True)


# In[99]:


rlyst = [rs < 0 for rs in [y-x for x,y in list(zip(rally.rally_nbr[:-1],rally.rally_nbr[1:]))]]
rlyst.append(False)
avgrallies = round(np.mean(rally[rlyst].rally_nbr),2)
print(f'average number of rallies in {len(pullawsdata("game"))} REAL games: {avgrallies}')


# In[179]:


print(85/37)
print(37/11)
print(11/2)

