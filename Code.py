import numpy as np
import pandas as pd
import re
import xlsxwriter
from sklearn import linear_model
spotify = pd.read_excel('Spotify.xlsx')
g = spotify['Genre']
#g has just one column
#this is for writing in excell
writer = pd.ExcelWriter('cis_project.xlsx', engine='xlsxwriter')
for i in range(len(g)):
    shelp=g[i].lower()
    if re.match('.*pop$', shelp):
        spotify.loc[i,'Genre']="Pop"
    elif re.match('.*hip hop$', shelp):
        spotify.loc[i,'Genre']="Hip Hop"
    elif re.match('.*rock$', shelp):
        spotify.loc[i,'Genre']="Rock"
    elif re.match('.*rap$', shelp):
        spotify.loc[i,'Genre']="Rap"
    elif re.match('.*\w\s\w.*', shelp):
        spotify.loc[i,'Genre']="Other"
    else :
        spotify.loc[i,'Genre']=g[i].capitalize()

output1=spotify["Genre"]
#print(spotify['Genre'].head(20))
#print(spotify['Genre'][106])

#second Quesion
#first part: dealing with feat. in artists
for i in range(-1,602):
    j=i+1
    if "feat" in spotify.loc[j,'Artist']:
        names=spotify.loc[j,'Artist']
        names=names.replace('feat.','+')
        spotify.loc[j,'Artist']=names
#second Question
#second part: dealing with feat. in Title
for i in range(-1,602):
    if type(spotify.loc[i+1,'Title'])==str:
        if "feat" in spotify.loc[i+1,'Title']:
            names=spotify.loc[i+1,'Title']
            names=names.split(' (feat. ')
            spotify.loc[i+1,'Title']=names[0]#title column
            feat_artist=names[1][:-1]#artist column
            spotify.loc[i+1,'Artist']=spotify.loc[i+1,'Artist']+' + '+ str(feat_artist)
            
output2=spotify["Artist"]
#print(output2)
#Third Question
output3=spotify.describe(include='all')
output3.to_excel(writer,sheet_name="Describe")

#fourth Question
q4=spotify.loc[spotify.bpm>0.9*206]
q4=q4.sort_values(by=['bpm'],ascending=False)
output4=q4[['Title','Artist','Genre','bpm','Popularity']]
output4.to_excel(writer,sheet_name="bpm")

#fifth Question
#first part
db=[0,0,0,0,0,0,0,0,0,0]
dbt=[0,0,0,0,0,0,0,0,0,0]
for i in range(len(spotify)):
    if spotify["Year"][i]==2010:
        db[0]=db[0]+spotify["dB"][i]
        dbt[0]=dbt[0]+1
    elif spotify["Year"][i]==2011:
        db[1]=db[1]+spotify["dB"][i]
        dbt[1]=dbt[1]+1
    elif spotify["Year"][i]==2012:
        db[2]=db[2]+spotify["dB"][i]
        dbt[2]=dbt[2]+1
    elif spotify["Year"][i]==2013:
        db[3]=db[3]+spotify["dB"][i]
        dbt[3]=dbt[3]+1
    elif spotify["Year"][i]==2014:
        db[4]=db[4]+spotify["dB"][i]
        dbt[4]=dbt[4]+1
    elif spotify["Year"][i]==2015:
        db[5]=db[5]+spotify["dB"][i]
        dbt[5]=dbt[5]+1
    elif spotify["Year"][i]==2016:
        db[6]=db[6]+spotify["dB"][i]
        dbt[6]=dbt[6]+1
    elif spotify["Year"][i]==2017:
        db[7]=db[7]+spotify["dB"][i]
        dbt[7]=dbt[7]+1
    elif spotify["Year"][i]==2018:
        db[8]=db[8]+spotify["dB"][i]
        dbt[8]=dbt[8]+1
    elif spotify["Year"][i]==2019:
        db[9]=db[9]+spotify["dB"][i]
        dbt[9]=dbt[9]+1
        
d = {'Year': [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019], 'db_mean': [db[0]/dbt[0],db[1]/dbt[1],db[2]/dbt[2],db[3]/dbt[3],db[4]/dbt[4],db[5]/dbt[5],db[6]/dbt[6],db[7]/dbt[7],db[8]/dbt[8],db[9]/dbt[9]]}
db_mean = pd.DataFrame(data=d)
output5=db_mean.sort_values(by=['db_mean'],ascending=False)
output5.to_excel(writer,sheet_name="db_mean")    

#sixth Question
#first: we create a list of all artists in songs(it has all song's artists)
artists_list=[]
for i in range(603):
  if('+' in spotify.loc[i,'Artist']):
    artists=spotify.loc[i,'Artist']
    artists=artists.split(" + ")
    artists_list=artists_list+artists

  else:
    artists=spotify.loc[i,'Artist']
    artists_list.append(artists)

#now we creat a dictionary of this list, keys are artists and values are the number of their songs in spotify dataset!
artists_dict={}
for c in range(len(artists_list)):
    artists_dict[artists_list[c]] = artists_list.count(
        artists_list[c]
        )
#now, we create data frame with two columns: Artist and number of presence in songs
df=pd.DataFrame(artists_dict.items(),columns=["Artist",'#no'])

#Question 6 continue
Best_artists=df.loc[df['#no']>2]
Best_artists=Best_artists.sort_values(by="#no")
Best_artists
output6=Best_artists.copy()
output6.to_excel(writer,sheet_name="Best_Artists")    

#seventh Question
#first part: Hit_Songs
Hit_Songs=spotify.loc[spotify['Popularity']>=80]
Hit_Songs.to_excel(writer,sheet_name="Hit_Songs")
#Question 7 continue
Hit_Songs_Count=Hit_Songs.groupby(by='Year').Year.count()
Hit_Songs_Count.to_excel(writer,sheet_name="Hit_Songs_Count")



#eighth Question
lm = linear_model.LinearRegression()
y=np.array(spotify["Popularity"])
x=np.array(spotify["Accousticness"])

model1 = lm.fit(x.reshape(-1, 1),y)
coef=list(model1.coef_)
print("{0:.4f}*x+{1:.4f}=y".format(coef[0],model1.intercept_))
spotify.to_excel(writer,sheet_name="data")
writer.save()    
    
