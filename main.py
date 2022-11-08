import pandas as pd
import datetime as dt
from datetime import timedelta
import holidays
import numpy as np
from ricalendarizzatore import *

if __name__ == "__main__":
    # INIZIALIZZO LE VARIABILI 
    listaColonne = []
    listaColonne.append("Date")
    listaColonne.append("Acquisti_Ric")
    dfAcquisti_Finale = pd.DataFrame(columns=listaColonne)

    # CARICO DATAFRAME 
    dfDati = pd.read_excel(r"C:\Users\G.Telloli\Documents\Progetti_Python\forecast_carico_rete\ANN\ENTSOE\load_nord\load_nord_entsoe_2021.xlsx",sheet_name="Dati")
    dfDateAnnoFinale = pd.DataFrame(columns=["Date"]) 
    dfDateAnnoFinale["Date"] = dfDati["Data"]
    # RICALENDARIZZO IL 2021 SUL 2022
    # LO FACCIO SUGLI ACQUISTI MGP DEL 2021
    
    # PREPARO I DATAFRAME DI INPUT 
    dfAnnoX_Acquisti = pd.DataFrame(columns=["Date","Acquisti"])

    dfAcquisti_Finale["Date"] = dfDateAnnoFinale["Date"]

    anno = 2021
    dfAnnoX_Acquisti["Date"] = dfDati["Data"][dfDati["Data"].dt.year == anno ]
    dfAnnoX_Acquisti["Acquisti"] = dfDati["Load"][dfDati["Data"].dt.year == anno ]

    dfAnnoX_Acquisti = dfAnnoX_Acquisti.reset_index(drop=True)
    risultato = ricalendarizzatore(dfAnnoX_Acquisti,2022,dfDateAnnoFinale)
    dfAcquisti_Finale["Load_Ric"] = risultato["Acquisti"]
    
    #SALVO I RISULTATI IN UN FILE EXCEL CON DUE FOGLI 
    dfAcquisti_Finale.to_excel("C:\\Users\\G.Telloli\\Documents\\Progetti_Python\\forecast_carico_rete\\ANN\\ENTSOE\\load_nord\\load_nord_hourly_2021_ricalendarizzato_2022.xlsx")