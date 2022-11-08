import pandas as pd
import datetime as dt
from datetime import timedelta
import holidays
import numpy as np



def ricalendarizzatore(dfAnnoX,anno,dateAnnoFinale,Paese="IT"):
    '''
     dfAnnoX deve essere ricalendarizzato rispetto all'anno anno
     dfAnnoX è un dataframe e ha come colonne < Date , [Valore] > 
             - la colonna Date deve avere questo nome
             - la colonna [Valore] può avere qualsiasi nome
     anno è un intero ed è l'anno su cui devo ricalendarizzare
     dateAnnoFinale = lista di date 
     Paese stringa che può essere IT,FR,DE

     Restituisce : un dataframe con le colonne < Date , [Valore] >
    '''
    #riempio eventuali buchi presenti nella curva mettendo il valore precedente 
    colonnaTarget = dfAnnoX.columns[1] 
    indiciBucati = dfAnnoX[dfAnnoX[colonnaTarget].isnull()].index

    for indice in indiciBucati:
        dfAnnoX[colonnaTarget].iloc[indice] = dfAnnoX[colonnaTarget].iloc[indice-1] 
    if Paese == "IT":
        ferieY = holidays.Italy(years=anno)
        ferieX = holidays.Italy(years=dfAnnoX["Date"].loc[0].year)
    if Paese == "FR":
        ferieY = holidays.France(years=anno)
        ferieX = holidays.France(years=dfAnnoX["Date"].loc[0].year)
    if Paese == "DE":
        ferieY = holidays.Germany(years=anno)
        ferieX = holidays.Germany(years=dfAnnoX["Date"].loc[0].year)

    dfDate = pd.DataFrame(columns=["Date"])
    dfDate["Date"] = dfAnnoX["Date"].apply(lambda x: x.date())

    # CREO DATA FRAME FINALE
    dfFinale = pd.DataFrame(columns=["Date"])
    dfFinale["Date"] = dateAnnoFinale
    dfFinale = dfFinale.reset_index()
    # ESTRAGGO DATE E NOMI DELLE FERIE
    dateX = []
    nomiFerie = []
    for data in ferieY.items():
        nomiFerie.append(data[1])

    
    for item in ferieX.items():
        if dfAnnoX["Date"].loc[0].year == 2038:
            if len(item[1].split(","))>1:
                dateX.append(item[0])
                dateX.append(item[0])
            elif item[1] in nomiFerie:
                dateX.append(item[0])
        else:    
            if item[1] in nomiFerie:   
                    dateX.append(item[0])
            
       

    dateY = []
    for date in ferieY.items():
        dateY.append(date[0])
       
    #------------------------------------------------------
    #
    # traslazione di x al primo giorno dell'anno y
    dowY = dateY[0].weekday()
    # trovo l'indice del primo giorno della settimana uguale dowY
    index = 0
    for i in range(len(dfAnnoX)):
        if dfAnnoX["Date"].loc[i].weekday() == dowY:
            index = i
            break
    subsetX = dfAnnoX.loc[index:]
    subsetX = subsetX.reset_index()

    # FINE TRASLAZIONE
    # ---------------------------------
    # INIZIO ASSOCIAZIONE FESTE
    dfFinale = dfFinale.merge(subsetX,how='outer',left_index=True,right_index=True)
    

    for i in range(len(nomiFerie)):
        dataFerieY = dateY[i]
        dataFerieX = dateX[i]

        
        # esclusa la prima e la seconda festività
            # prendi il giorno della settimana precedente rispetto alla festività nell'anno x
            # e mettilo al posto della festività
        if i > 1 and not (dfFinale['Date_x'][dfFinale["Date_y"].dt.date == dataFerieX].iloc[0] in dateY): 
            dataFerieX_temp = dataFerieX + dt.timedelta(days=-7)
            #dfValoriX_Sett = dfAnnoX[colonnaTarget][dfAnnoX["Date"].dt.date == dataFerieX_temp ]
            if (len(dfFinale[colonnaTarget][dfFinale["Date_y"].dt.date == dataFerieX]) < len(dfFinale[colonnaTarget][dfFinale["Date_y"].dt.date == dataFerieX_temp])):
                # togli ora 3 
                valori = dfFinale[colonnaTarget][dfFinale["Date_y"].dt.date == dataFerieX_temp].values
                valori = np.delete(valori,2)
                dfFinale[colonnaTarget][dfFinale["Date_y"].dt.date == dataFerieX] = valori
            elif (len(dfFinale[colonnaTarget][dfFinale["Date_y"].dt.date == dataFerieX]) > len(dfFinale[colonnaTarget][dfFinale["Date_y"].dt.date == dataFerieX_temp])):
                # copia ora 3
                valore = dfFinale[colonnaTarget][dfFinale["Date_y"].dt.date == dataFerieX_temp].values[2]
                valori = dfFinale[colonnaTarget][dfFinale["Date_y"].dt.date == dataFerieX_temp].values[0:2]
                valori = np.append(valori,valore)
                valori = np.append(valori,dfFinale[colonnaTarget][dfFinale["Date_y"].dt.date == dataFerieX_temp].values[2:])
                dfFinale[colonnaTarget][dfFinale["Date_y"].dt.date == dataFerieX] = valori
            else:
                dfFinale[colonnaTarget][dfFinale["Date_y"].dt.date == dataFerieX] = dfFinale[colonnaTarget][dfFinale["Date_y"].dt.date == dataFerieX_temp].values 

        # COPIARE IL VALORE DEL PUN DA DATAX A DATAY
        # VALORI DA X
        dfValoriX = dfAnnoX[colonnaTarget][dfAnnoX["Date"].dt.date == dataFerieX ]
        
        '''
        if (len(dfFinale[colonnaTarget][dfFinale["Date_x"].dt.date == dataFerieY ]) < len(dfValoriX)):
            # togli l'ora 3 
            valori = dfValoriX.values
            valori = np.delete(valori,2)
            dfFinale[colonnaTarget][dfFinale["Date_x"].dt.date == dataFerieY ] = valori
        elif (len(dfFinale[colonnaTarget][dfFinale["Date_x"].dt.date == dataFerieY]) > len(dfValoriX)):
            # copia l'ora 3 
            valore = dfValoriX.values[2]
            valori = dfValoriX.values[0:2]
            valori = np.append(valori,valore)
            valori = np.append(valori,dfValoriX.values[2:])
            dfFinale[colonnaTarget][dfFinale["Date_x"].dt.date == dataFerieY ] = valori
        else:
            dfFinale[colonnaTarget][dfFinale["Date_x"].dt.date == dataFerieY ] = dfValoriX.values
        '''
      
    
    # CICLO PER RIEMPIRE I VALORI NAN 
    listaDateNulle = dfFinale["Date_x"][dfFinale[colonnaTarget].isnull()].dt.date.unique()
    for date in listaDateNulle:
        # se il weekday precedente sull'anno vecchio non è un festivo 
        weekday_Y = date.weekday()
        ultimoWeekDayX = dfAnnoX["Date"][(dfAnnoX["Date"].dt.month == 12) & (dfAnnoX["Date"].dt.dayofweek == weekday_Y)].dt.date.unique()
        
        if ultimoWeekDayX[-1] in dateX :
            # se l'ultimo non è disponibile scelgo il penultimo per valorizzare la data nulla
            dataRiserva = ultimoWeekDayX[-2]
            dfFinale[colonnaTarget][dfFinale["Date_x"].dt.date == date] = dfAnnoX[colonnaTarget][dfAnnoX["Date"].dt.date == dataRiserva].values
        else:
            dfFinale[colonnaTarget][dfFinale["Date_x"].dt.date == date] = dfAnnoX[colonnaTarget][dfAnnoX["Date"].dt.date == ultimoWeekDayX[-1]].values

    
    dfFinale = dfFinale.drop(columns=["Date_y","index_x","index_y"],axis = 0)
    dfFinale["Date_x"] = pd.to_datetime(dfFinale["Date_x"].dt.tz_localize(None))
    dfFinale = dfFinale.rename(columns={"Date_x":"Date"})
    return dfFinale


