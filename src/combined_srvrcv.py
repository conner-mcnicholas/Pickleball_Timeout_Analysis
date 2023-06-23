import pandas as pd
pd.set_option('mode.chained_assignment', None)
from collections import Counter
import numpy as np
import psycopg2
from matplotlib import pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.style as mplstyle
import matplotlib.patches as mpatches
from matplotlib.ticker import (PercentFormatter,MultipleLocator, AutoMinorLocator)
import seaborn as sns

conn = psycopg2.connect(database="postgres",
                        host="pklmartdb.ckkvdwandqoa.us-east-1.rds.amazonaws.com",
                        user="cmcnicholas",
                        password="momentum101",
                        port="5432")
conn.autocommit = True

def pullawsdata(tablename):
    with conn,conn.cursor() as cursor:
        try:
            cursor.execute(f"SELECT column_name FROM information_schema.columns where table_name='{tablename}';")
            cols=cursor.fetchall()
            cols = [cols[x][0] for x in range(len(cols))]
            cursor.execute(f"SELECT * FROM pklm_prd.{tablename}")
            data=cursor.fetchall()
            return(pd.DataFrame(data,columns=cols))
        except Exception as inst:
            print(type(inst))    
            print(inst.args)     
            print(inst)

rally=pullawsdata('rally')

rally = rally[['game_id', 'rally_id', 'rally_nbr', 'srv_team_id', 'w_team_id', 'to_team_id']]
rally['game_id'] = [int(x[1:]) for x in rally.game_id]
rally['rally_id'] = [int(x[1:]) for x in rally.rally_id]
rally = rally.sort_values(['game_id', 'rally_id', 'rally_nbr']).reset_index(drop=True)


game=pullawsdata('game')[['match_id','game_id','game_nbr','score_w','score_l','w_team_id','l_team_id','skill_lvl']]
game['game_id'] = [int(x[1:]) for x in game.game_id]
game['match_id'] = [int(x[1:]) for x in game.match_id]
game.skill_lvl.iloc[game.skill_lvl == '4'] = '4.0'
game.skill_lvl.iloc[game.skill_lvl == '5'] = '5.0'
game = game.sort_values(['match_id','game_id']).reset_index(drop=True)


glist = list(rally.game_id.unique())
dlist = []

for i in range(len(glist)):
    gi = rally[rally.game_id==glist[i]].reset_index(drop=True)
    gi = gi[gi.loc[gi.to_team_id != 'N/A'].to_team_id.ne(gi.to_team_id.shift())]
    to_game = glist[i]
    to_inds = list(gi.index[gi.to_team_id != 'N/A'])
    to_teams = list(gi.to_team_id[gi.to_team_id != 'N/A'])
    skill_lvl = list(game.skill_lvl[game.game_id == glist[i]])[0]
    if (len(to_inds) > 0):
        for j in range(len(to_inds)):
            if j == 0:
                pre = list(range(to_inds[j]))
            else:
                pre = list(range(to_inds[j-1]+1,to_inds[j]))
            if j == len(to_inds)-1:
                post = list(range(to_inds[j]+1,len(gi)))
            else:
                post = list(range(to_inds[j]+1,to_inds[j+1]))
            toteam = to_teams[j]
            rallynbr = gi.rally_nbr.iloc[to_inds[j]]
            
            winpre = round(100*len(gi.iloc[pre][lambda x:x.w_team_id == toteam])/len(pre),1)
            winpost = round(100*len(gi.iloc[post][lambda x:x.w_team_id == toteam])/len(post),1)
            windelta = round(winpost-winpre,1)
            
            srvpre = gi.iloc[pre][lambda x:x.srv_team_id == toteam]
            rcvpre = gi.iloc[pre][lambda x:x.srv_team_id != toteam]

            srvlenpre=len(srvpre)
            rcvlenpre=len(rcvpre)
            
            srvpost = gi.iloc[post][lambda x:x.srv_team_id == toteam]
            rcvpost = gi.iloc[post][lambda x:x.srv_team_id != toteam]

            srvlenpost=len(srvpost)
            rcvlenpost=len(rcvpost)
            
            if srvlenpre > 0:
                srvwinpre = round(100*len(srvpre.loc[lambda x:x.w_team_id == toteam])/srvlenpre,1)
            else:
                srvwinpre = None
            if srvlenpost > 0:
                srvwinpost = round(100*len(srvpost.loc[lambda x:x.w_team_id == toteam])/srvlenpost,1)
            else:
                srvwinpost = None
            if srvlenpre > 0 and srvlenpost > 0:
                srvwindelta = round(srvwinpost-srvwinpre,1)
            else:
                srvwindelta = None
                
            
            if rcvlenpre > 0:
                rcvwinpre = round(100*len(rcvpre.loc[lambda x:x.w_team_id == toteam])/rcvlenpre,1)
            else:
                rcvwinpre = None
            if rcvlenpost > 0:
                rcvwinpost = round(100*len(rcvpost.loc[lambda x:x.w_team_id == toteam])/rcvlenpost,1)
            else:
                rcvwinpost = None
            if rcvlenpre > 0 and rcvlenpost > 0:
                rcvwindelta = round(rcvwinpost-rcvwinpre,1)
            else:
                rcvwindelta = None
        
            
            dlist.append([to_game,skill_lvl,j+1,toteam,rallynbr,winpre,winpost,windelta,srvwinpre,srvwinpost,srvwindelta,rcvwinpre,rcvwinpost,rcvwindelta])

df_timeout = pd.DataFrame(dlist,columns=['game_id','skill_lvl','to_nbr','to_team','rally_nbr','prewin','postwin','deltawin','prewinsrv','postwinsrv','deltawinsrv','prewinrcv','postwinrcv','deltawinrcv'])

df_mix=pd.concat([df_timeout.skill_lvl.append(df_timeout.skill_lvl),df_timeout.deltawinsrv.append(df_timeout.deltawinrcv)],axis=1)
df_mix.columns = ['skill','chgwin']
df_mix.loc[df_mix.skill.isin(['Senior Pro','Pro']),'skill'] = 'Pro'

print('change in win percentage due to timeouts\n')
df_mix.groupby('skill').aggregate(func=['mean','median','std','count']).round(1)

df_mixnnull = df_mix.fillna(0.0).reset_index(drop=True)
dfm_pro=df_mixnnull[df_mixnnull.skill == 'Pro']
dfm_50=df_mixnnull[df_mixnnull.skill == '5.0']
dfm_45=df_mixnnull[df_mixnnull.skill == '4.5']
dfm_40=df_mixnnull[df_mixnnull.skill == '4.0']
skilldata=[list(x.chgwin) for x in [dfm_40,dfm_45,dfm_50,dfm_pro,df_mixnnull]]

fig, ax = plt.subplots(figsize=(14, 8))
meanlineprops = dict(linestyle='-', linewidth=2.0, color='black')
medianlineprops = dict(linestyle='--', linewidth=1.0, color='black')

box = plt.boxplot(skilldata,autorange=False,patch_artist=True,showmeans=True,medianprops=medianlineprops,meanline=True,meanprops=meanlineprops,labels=['4.0','4.5','5.0','Senior Pro','Pro','All'])

colors = ['red', 'orange', 'yellow', 'green', 'white']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
plt.show()
                                    
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams.update({'figure.figsize':(12,5), 'figure.dpi':100})
plt.hist(df_mix.chgwin, bins=19)
plt.gca().set(title='Change in Rally Win % After Timeout, srv status considered)', xlabel = 'win % change', ylabel='Frequency');

df_mix=df_mix.reset_index(drop=True)

fig, ax = plt.subplots(figsize=(14, 8))
HIST_BINS = np.linspace(-200/3, 100, 21)
p = sns.histplot(x="chgwin",data=df_mix[df_mix.skill != 'Senior Pro'],hue="skill",hue_order=['4.0','4.5','5.0','Pro'],palette='gist_heat_r',bins=HIST_BINS,stat="count",alpha=.53,discrete=False,fill=True,element='step',multiple='layer')
p.set_xlabel("Change in Rally Win % From Timeout, srv status considered",fontsize=10)
p.set_ylabel("Instances",fontsize=10)
plt.show()