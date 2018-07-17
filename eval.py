# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

p = pd.read_excel('file:///C:/Users/12157/Desktop/totalDataPredit.xlsx', sheetname='data_predit')
p_gbdt = pd.read_excel('file:///C:/Users/12157/Desktop/totalDataPredit_GBDT.xlsx', sheetname='data_predit')

#predict data
pt = p['2018-01-31 00:00:00':'2018-12-31 00:00:00']
pt_gbdt = p_gbdt['2018-01-31 00:00:00':'2018-12-31 00:00:00']

#real data
eco=pd.read_excel('file:///C:/Users/12157/Desktop/data.xls', sheetname='宏观经济指标')
car=pd.read_excel('file:///C:/Users/12157/Desktop/data.xls', sheetname="汽车行业指标")
eng=pd.read_excel('file:///C:/Users/12157/Desktop/data.xls', sheetname="发动机产量与销量")
complement=pd.read_excel('file:///C:/Users/12157/Desktop/data.xls', sheetname="补充指标")

def extraction(df):
    df = df['2018-01-01 00:00:00':'2018-12-31 00:00:00']
    return df
    
eco=extraction(eco)
car=extraction(car)
eng=extraction(eng)
complement=extraction(complement)

#a=list(r.columns)
#a[1][-1]
#len(r)

def getMonthValue(df):
    cols=list(df.columns)
    #fullIndex=pd.date_range(min(df.index),max(df.index),closed="right",freq='M')
    #df=df.reindex(fullIndex)
    df.fillna(0.0,inplace=True) #补足所有缺失日期(fill all nan with 0)
    df['year']=df.index.year
    df['month']=df.index.month
    df['season']=(df.index.month-1)//3+1
    tot=len(df)
    #按照指标的粒度，平滑到月(convert to monthly data)
    for i in range(len(cols)):#遍历列col (traversal column)
        freq=cols[i][-1] #列名标记s,m,y(Using s,m,y mark the data type at the end of column name  )
        if freq=='d' or freq=='m':
            dico=dict(df.groupby(["year","month"])[cols[i]].mean()) #求每月对应的各个指标均值(for every attribute calculate mean of monthly data)
            for j in  range(tot): #遍历行row (traversal row)
                e=df.iloc[j,:]
                df.ix[j,[cols[i]]]=dico[(e["year"],e["month"])] 
        elif freq=='s':
            dico=dict(df.groupby(["year","season"])[cols[i]].sum().apply(lambda x:x/3))
            for j in  range(tot):
                e=df.iloc[j,:]
                df.ix[j,[cols[i]]]=dico[(e["year"],e["season"])]
        elif freq=='y':
            dico=dict(df.groupby(["year"])[cols[i]].sum().apply(lambda x:x/12))
            for j in  range(tot):
                e=df.iloc[j,:]
                df.ix[j,[cols[i]]]=dico[(e["year"])]
    return df

eco=eco.resample('M').mean() #把半月整并到月(convert half month to month) 
eco=getMonthValue(eco)


eng=eng.resample('M').mean() 
eng=getMonthValue(eng)

car=car.resample('M').mean()
car=getMonthValue(car)
 
complement=complement.resample('M').mean() 
complement=getMonthValue(complement)


def evaluation(real,pred):
    cols_r=list(real.columns)
    pred=pred[cols_r]
    pred=pred.ix[0:len(real),cols_r]
    for j in range(len(cols_r)-3):
        e=[]
        for i in range(len(real)):
            if real.iloc[i][j]!=0:
                e.append(np.abs(pred.iloc[i][j]-real.iloc[i][j])*100/real.iloc[i][j])
        print(np.mean(e))

#mape for eco
evaluation(eco,pt)
evaluation(eco,pt_gbdt)

#mape for car
evaluation(car,pt)
evaluation(car,pt_gbdt)

#mape for eng
evaluation(eng,pt)
evaluation(eng,pt_gbdt)

#mape for complement
evaluation(complement,pt)
evaluation(complement,pt_gbdt)
