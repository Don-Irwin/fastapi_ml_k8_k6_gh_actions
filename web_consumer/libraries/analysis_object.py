from codecs import iterdecode
from copyreg import pickle
from itertools import count
import os
import sys
import json
from datetime import datetime
from os import system, name
from time import sleep
import copy
import threading
import imp
#from tkinter import S
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandasql as psql
from  libraries.utility import Utility
import pickle
import statsmodels.api as sm
import statsmodels.graphics.tsaplots as tsap
from statsmodels.compat import lzip
from statsmodels.stats.diagnostic import het_white


class analysis_object(Utility):



    def __init__(self,county_key,is_county=True):
        super().__init__()

        self.NO_OF_MO_ANALYSIS = 6
        self.COUNTY_FILE_DF = None
        self.COUNTY_SUMMARY_FILE = None
        self.COUNTY_PICKLE_FILE = None

        self.MODEL_USED = None

        self.NO_MO_PRICE_UP = None
        self.NO_MO_PRICE_DOWN = None
        self.PRICE_SIGNAL   = None

        self.PRICE_SIGNAL_DF = None

        self.NO_MO_INV_UP   = None
        self.NO_MO_INV_DOWN = None
        self.INV_SIGNAL     = None
        self.INV_SIGNAL_DF  = None

        self.NO_MO_INT_UP   = None
        self.NO_MO_INT_DOWN = None
        self.INT_SIGNAL     = None

        self.INT_SIGNAL_DF  = None

        self.NO_MO_DOM_UP   = None
        self.NO_MO_DOM_DOWN = None
        self.DOM_SIGNAL     = None

        self.DOM_SIGNAL_DF  = None
        
        self.INTEREST_RATE_PCT_YOY = None

        self.MODEL_SMAPE = None
        self.MODEL_DF = None
        self.MODEL_SIGNAL = None
        self.MODEL_USED = None

        self.INITIAL_HPARAMS = None
        self.TUNED_HPARAMS = None

        ###print(county_key)

        self.COUNTY_KEY = county_key
        self.COUNTY_FILE_DF, self.COUNTY_SUMMARY_FILE, self.MODEL_SMAPE, self.MODEL_DF,self.MODEL_USED  = self.load_county_data(county_key,is_county)

    def get_county_df(self):
        COUNTY_FILE_DF = self.COUNTY_FILE_DF

        my_return_df = COUNTY_FILE_DF
        my_return_df = COUNTY_FILE_DF[['county_name','date', 'median_listing_price','thirty_year_interest_rate','thirty_year_interest_rate_five','active_listing_count','median_days_on_market']]

        #my_return_df.insert(0,"id",range(0,0+len(my_return_df)))

        return my_return_df

    def get_df_as_json(self):
        COUNTY_FILE_DF = self.COUNTY_FILE_DF

        my_return_df = COUNTY_FILE_DF
        my_return_df = COUNTY_FILE_DF[['county_name','date', 'median_listing_price','thirty_year_interest_rate_five','active_listing_count']]

        #my_return_df.insert(0,"id",range(0,0+len(my_return_df)))

        return my_return_df.to_json(orient="records")
        

    def get_feature_signal(self,mo_up,mo_down,this_year_count, last_year_count,this_year_higher,pct_change,feature_name,latest_mo_pct_change,this_year_higher_latest_month):
        INTEREST_RATE_PCT_YOY = self.INTEREST_RATE_PCT_YOY
        INT_SIGNAL = self.INT_SIGNAL
        response_text = None
        signal = "up"
        print(mo_up,mo_down,this_year_count, last_year_count,this_year_higher,pct_change,feature_name)
        #days on market:
        last_month_string = "higher" if this_year_higher_latest_month else "lower"
        if feature_name == 'm_active_listing_count':
            if mo_up > mo_down and this_year_higher:
                signal="down"
                response_text = "Inventory has risen for {0} of the past 6 months,<br/> and is on average {1} % higher, than the same months last year,<br/>and is {2}% {3} for the latest month.".format(mo_up,round(pct_change,2),round(latest_mo_pct_change,2),last_month_string)
            if mo_up == mo_down and this_year_higher:
                signal="down"
                response_text = "Has increased and decreased an equal number of months,<br/> but is on average {1} % higher, than the same months last year,<br/>and is {2}% {3} for the latest month.".format(mo_up,round(pct_change,2),round(latest_mo_pct_change,2),last_month_string)
            if mo_up > mo_down and not this_year_higher:
                signal="neutral"
                response_text = "Inventory has risen for {0} of the past 6 months,<br/> but is on average {1} % lower, than the same months last year,<br/>and is {2}% {3} for the latest month.".format(mo_up,round(pct_change,2),round(latest_mo_pct_change,2),last_month_string)
            if mo_down > mo_up and this_year_higher and round(pct_change,2) > 27:
                signal="down"
                response_text = "Inventory has increased for {0} of the past 6 months,<br/> but is on average {1} % higher, than the same months last year,<br/>and is {2}% {3} for the latest month.".format(mo_up,round(pct_change,2),round(latest_mo_pct_change,2),last_month_string)

            # if mo_up > mo_down and (not this_year_higher):
            #     signal="neutral"
        
        if feature_name == 'thirty_year_interest_rate':
            if mo_up > mo_down and this_year_higher:
                signal="down"
                response_text = "The thirty year fixe rate has risen {0} out of the past 6 months.<br/> It is on average {1} % higher month over month.<br/>This is going to have downward pressure on prices.".format(mo_up,round(INTEREST_RATE_PCT_YOY,2))                
            if mo_up > mo_down and (not this_year_higher):
                signal="neutral"
            
        
        if feature_name == 'median_listing_price':
            ##print("******")
            #print(feature_name)
            #print("mo_down=",mo_down)
            #print("******")
            if mo_down >= mo_up:
                if pct_change <= INTEREST_RATE_PCT_YOY:
                    signal="down"
                    response_text = "The 30 year fixed interest is up an average of {0}%, <br/>per month, over the past 6 months. It is higher than this time last year.<br/>Prices have yet to respond to higher interest rates.".format(round(INTEREST_RATE_PCT_YOY,2))
                else:
                    signal="neutral"
            else:
                signal="neutral"
            if mo_up > mo_down:
                if pct_change <= INTEREST_RATE_PCT_YOY:
                    response_text = "Prices have risen {0} out of the past 6 months.<br/> This indicates demand is still strong. <br/> But prices haven't adjusted to the {1} % average monthly increase in interest rates.".format(mo_up,round(INTEREST_RATE_PCT_YOY,2))                
                    signal="neutral"
            else:
                if pct_change <= 2 and pct_change <= INTEREST_RATE_PCT_YOY:
                    signal = "down"
                    response_text = "Prices have fallen {0} out of the past 6 months.<br> However they are only down {1} % from the same period last year, month-over-month.<br/>They haven't responded to the {2} % average monthly interest rate increases.".format(mo_down,round(pct_change,2),round(INTEREST_RATE_PCT_YOY,2))
            #print(feature_name,mo_down,mo_up,INTEREST_RATE_PCT_YOY,pct_change)

        if feature_name == 'median_days_on_market':
            if mo_up > mo_down and this_year_higher:
                response_text = "Days on market have risen {0} of the past 6 months.<br/>Days on market is {1}% higher than the same months last year,<br/>and is {2}% {3} for the latest month.".format(mo_up,round(pct_change,2),round(latest_mo_pct_change,2),last_month_string)
            if mo_up > mo_down and (not this_year_higher):
                response_text = "Days on market have risen {0} of the past 6 months.<br/>However, days on market is {1}% lower  than the same months last year,<br/>and is {2}% {3} for the latest month.".format(mo_up,round(pct_change,2),round(latest_mo_pct_change,2),last_month_string)
                signal="neutral"
            if mo_down > mo_up and (not this_year_higher):
                signal="up"
            if mo_down > mo_up and (this_year_higher):
                signal="down"
                response_text = "Days on market are higher than the same period last year."
                signal="down"
            if mo_down == mo_up and (this_year_higher):
                response_text = "Days on market are higher than the same period last year."
                signal="down"


        return signal, response_text


    def do_int_analysis(self):

        COUNTY_FILE_DF = self.COUNTY_FILE_DF

        NO_MO_INT_UP  = self.NO_MO_INT_UP  
        NO_MO_INT_DOWN = self.NO_MO_INT_DOWN

        INT_SIGNAL_DF = self.INT_SIGNAL_DF

        NO_OF_MO_ANALYSIS = self.NO_OF_MO_ANALYSIS

        self.INT_SIGNAL_DF,this_year_count, last_year_count,this_year_higher,pct_change,latest_mo_pct_change,this_year_higher_latest_month = self.get_year_over_year_comp(COUNTY_FILE_DF,'thirty_year_interest_rate')
        self.NO_MO_INT_UP, self.NO_MO_INT_DOWN = self.evaluate_feature('thirty_year_interest_rate',COUNTY_FILE_DF)

        self.INT_SIGNAL ,int_response_text = self.get_feature_signal(self.NO_MO_INT_UP,self.NO_MO_INT_DOWN,this_year_count,last_year_count,this_year_higher,pct_change,"thirty_year_interest_rate",latest_mo_pct_change,this_year_higher_latest_month)

        self.INT_SIGNAL_GRAPH = self.get_signal_graph(self.INT_SIGNAL_DF,'thirty_year_interest_rate','last_yr_thirty_year_interest_rate','Year over year interest rate')

        return self.INT_SIGNAL_DF,self.NO_MO_INT_UP,self.NO_MO_INT_DOWN,self.INT_SIGNAL_GRAPH,self.INT_SIGNAL,this_year_count, last_year_count,this_year_higher,pct_change,int_response_text


    def do_inv_analysis(self):

        COUNTY_FILE_DF = self.COUNTY_FILE_DF

        # global NO_MO_INV_UP  
        # global NO_MO_INV_DOWN
        # global INV_SIGNAL    

        # global INV_SIGNAL_DF 

        # global NO_OF_MO_ANALYSIS

        self.INV_SIGNAL_DF,this_year_count, last_year_count,this_year_higher,pct_change,latest_mo_pct_change,this_year_higher_latest_month = self.get_year_over_year_comp(COUNTY_FILE_DF,'m_active_listing_count')

        self.NO_MO_INV_UP, self.NO_MO_INV_DOWN = self.evaluate_feature('m_active_listing_count',COUNTY_FILE_DF)

        self.INV_SIGNAL_GRAPH = self.get_signal_graph(self.INV_SIGNAL_DF,'m_active_listing_count','last_yr_m_active_listing_count','Year over year inventory rate')

        self.INV_SIGNAL,inv_response_text = self.get_feature_signal(self.NO_MO_INV_UP,self.NO_MO_INV_DOWN,this_year_count,last_year_count,this_year_higher,pct_change,'m_active_listing_count',latest_mo_pct_change,this_year_higher_latest_month)

        return self.INV_SIGNAL_DF,self.NO_MO_INV_UP,self.NO_MO_INV_DOWN,self.INV_SIGNAL_GRAPH,self.INV_SIGNAL,this_year_count, last_year_count,this_year_higher,pct_change,inv_response_text




    def do_price_analysis(self):

        COUNTY_FILE_DF = self.COUNTY_FILE_DF

        NO_OF_MO_ANALYSIS = self.NO_OF_MO_ANALYSIS

        self.PRICE_SIGNAL_DF,this_year_count, last_year_count,this_year_higher,pct_change,latest_mo_pct_change,this_year_higher_latest_month = self.get_year_over_year_comp(COUNTY_FILE_DF,'median_listing_price')
        self.NO_MO_PRICE_UP, self.NO_MO_PRICE_DOWN = self.evaluate_feature('median_listing_price',COUNTY_FILE_DF)

        #print("median_listing_price",NO_MO_PRICE_UP,NO_MO_PRICE_UP)

        self.PRICE_SIGNAL_GRAPH = self.get_signal_graph(self.PRICE_SIGNAL_DF,'median_listing_price','last_yr_median_listing_price','Year over year price')

        self.PRICE_SIGNAL,price_response_text = self.get_feature_signal(self.NO_MO_PRICE_UP,self.NO_MO_PRICE_DOWN,this_year_count,last_year_count,this_year_higher,pct_change,'median_listing_price',latest_mo_pct_change,this_year_higher_latest_month)

        return self.PRICE_SIGNAL_DF,self.NO_MO_PRICE_UP,self.NO_MO_PRICE_DOWN,self.PRICE_SIGNAL_GRAPH,self.PRICE_SIGNAL,this_year_count, last_year_count,this_year_higher,pct_change,price_response_text


    def do_dom_analysis(self):

        COUNTY_FILE_DF = self.COUNTY_FILE_DF

        self.DOM_SIGNAL_DF,this_year_count, last_year_count,this_year_higher,pct_change,latest_mo_pct_change,this_year_higher_latest_month = self.get_year_over_year_comp(COUNTY_FILE_DF,'median_days_on_market')
        self.NO_MO_DOM_UP, self.NO_MO_DOM_DOWN = self.evaluate_feature('median_days_on_market',COUNTY_FILE_DF)

        self.DOM_SIGNAL_GRAPH = self.get_signal_graph(self.DOM_SIGNAL_DF,'median_days_on_market','last_yr_median_days_on_market','Year over year days on market')

        self.DOM_SIGNAL,dom_response_text = self.get_feature_signal(self.NO_MO_DOM_UP,self.NO_MO_DOM_DOWN,this_year_count,last_year_count,this_year_higher,pct_change,'median_days_on_market',latest_mo_pct_change,this_year_higher_latest_month)

        return self.DOM_SIGNAL_DF,self.NO_MO_DOM_UP,self.NO_MO_DOM_DOWN,self.DOM_SIGNAL_GRAPH,self.DOM_SIGNAL,this_year_count, last_year_count,this_year_higher,pct_change,dom_response_text



    def get_signal_graph(self,df,this_year_column,last_year_column,label="Year over year comparison of "):

        #df['date'] = pd.to_datetime(df['date'])

        COUNTY_KEY = self.COUNTY_KEY
        state = COUNTY_KEY.split("_")[len(COUNTY_KEY.split("_"))-1].upper()
        county_nm =""
        for part in COUNTY_KEY.split("_"):
            if part.upper() == state:
                continue
            county_nm = county_nm + " " + part.capitalize()

        county_nm = county_nm + ", " + state

        base = alt.Chart(df).transform_fold([this_year_column,last_year_column])
        #print(df)
        #print(df.describe())
        #print(df.dtypes)

        title2 = label + " in " + county_nm

        line = base.mark_line().encode(

        x=alt.X('date:O',axis=alt.Axis(title='Month and Year:',labelAngle=-15)),
        y=alt.Y('value:Q',axis=alt.Axis(title='Value:')),
        

        color=alt.Color(field="key", type="nominal",
                        scale = alt.Scale(range = ['#265499', '#A8DDA4']),
                        legend = alt.Legend(title="Key")),
        strokeWidth = alt.value(3)
        )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000,
        ).encode(
            x=alt.X('date:O',axis=alt.Axis(title='')),
            y=alt.Y('value:Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip("date"),
                     alt.Tooltip(this_year_column,format=",.0f" ),
                     alt.Tooltip(last_year_column,format=",.0f")
                     ]
        )

        return_chart = alt.layer(line,points).properties(
            width=340,
            height=220,
            title=title2
        )

        return return_chart




    def get_year_over_year_comp(self,df,s_column_name):
        NO_OF_MO_ANALYSIS = self.NO_OF_MO_ANALYSIS
        sql = '''
        select
                date,
                ''' + str(s_column_name) + ''',                
                date(date,'-1 years') as last_yr_date
        from df 
                order by date desc
        limit \'''' + str(NO_OF_MO_ANALYSIS+1) + '''\' ''' 

        this_year = psql.sqldf(sql)

        this_year_and_last = pd.merge(this_year,df,how='inner', left_on='last_yr_date',right_on='date',suffixes=('_right','_left') )
        print(s_column_name)
        #print(this_year_and_last["date_right","last_yr_date",s_column_name+'_right',s_column_name+'_left'])

        sql = '''
        select
            date_right as date,
            date_left as last_yr_date,
            ''' + str(s_column_name) + '''_left as last_yr_''' + str(s_column_name) + ''',
            ''' + str(s_column_name) + '''_right as ''' + str(s_column_name) + '''
        from this_year_and_last 
                order by date desc
        limit \'''' + str(NO_OF_MO_ANALYSIS+1) + '''\' ''' 

        this_and_last_parsed = psql.sqldf(sql)
        print(this_and_last_parsed)
        
        this_year_count = this_and_last_parsed[s_column_name].sum()
        last_year_count = this_and_last_parsed['last_yr_'+s_column_name].sum()

        this_year_latest_month_count = this_and_last_parsed[s_column_name].head(1).sum()
        last_year_latest_month_count = this_and_last_parsed['last_yr_'+s_column_name].head(1).sum()        

        print("this_year_count : {}".format(this_year_count))
        print("last_year_count : {}".format(last_year_count))
        print("this_year_latest_month_count : {}".format(this_year_latest_month_count))
        print("last_year_latest_month_count : {}".format(last_year_latest_month_count))

        this_year_higher = True if this_year_count > last_year_count else False

        this_year_higher_latest_month = True if this_year_latest_month_count > last_year_latest_month_count else False

        #global INTEREST_RATE_PCT_YOY

        if this_year_higher_latest_month:
            latest_mo_pct_change = ((this_year_latest_month_count - last_year_latest_month_count) * 100) / last_year_latest_month_count
        else:
            latest_mo_pct_change = ((last_year_latest_month_count - this_year_latest_month_count) * 100) / this_year_latest_month_count

        if this_year_higher:
            pct_change = ((this_year_count - last_year_count) * 100) / last_year_count
        else:
            pct_change = ((last_year_count - this_year_count) * 100) / this_year_count            

        if s_column_name == "thirty_year_interest_rate":
            self.INTEREST_RATE_PCT_YOY = pct_change

        return this_and_last_parsed, this_year_count, last_year_count,this_year_higher,pct_change,latest_mo_pct_change,this_year_higher_latest_month




    def evaluate_feature(self,s_column_name,df):

        mo_up, mo_down = self.get_months_up_or_down(s_column_name,df)

        #year_over_year_comp = self.get_year_over_year_comp(df,s_column_name)

        ##print("mo_up =",mo_up)
        ##print("mo_down =",mo_down)

        #df = self.get_year_over_year_comp(df,s_column_name)

        return mo_up, mo_down


    def get_months_up_or_down(self,s_column_name,df):

        NO_OF_MO_ANALYSIS = self.NO_OF_MO_ANALYSIS

        sql = '''
        select
        ''' + str(s_column_name) + '''
        from df
        order by date desc
        limit \'''' + str(NO_OF_MO_ANALYSIS+1) + '''\' ''' 

        output = psql.sqldf(sql)

        ##print(output)

        mo_up       = 0
        mo_down     = 0
        last_val    = 0
        m_counter   = 0

        for i, j in output[::-1].iterrows():
            cv = int(j)
            ##print(int(j))
            if last_val == 0:
                last_val = int(j)
                continue
            else:
                if cv >= last_val:
                    mo_up = mo_up + 1
                else:
                    mo_down = mo_down + 1
            m_counter = m_counter + 1
            last_val = int(j)

            #print("*"*80)

        #print(str(s_column_name))
        #print("mo_up=",mo_up)
        #print("mo_down=",mo_down)
        #print("last_val=",last_val)
        #print("m_counter=",m_counter)


        #print("*"*80)


        return mo_up, mo_down




    def print_internal_directory(self):

        for k,v in self.__dict__.items():
            print("{} is \"{}\"".format(k,v))

    def load_best_county_model(self,county_key,is_county=True):
     
        if is_county:
            initial_mean_losses_path     = os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_files",county_key.lower() + "_initial","mean_losses.txt")
            tuned_mean_losses_path       = os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_files",county_key.lower() + "_tuned","mean_losses.txt")
            initial_mean_losses     = self.get_data_from_file(initial_mean_losses_path)
            tuned_mean_losses       = self.get_data_from_file(tuned_mean_losses_path)           
            initial_hparams         = self.get_data_from_file(os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_files",county_key.lower() + "_initial","hparams.txt")).replace("\n","\n<br/>") + "SMAPE Score: " + initial_mean_losses + "<br/>"
            tuned_hparams           = self.get_data_from_file(os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_files",county_key.lower() + "_tuned","hparams.txt")).replace("\n","\n<br/>") + "SMAPE Score: " + tuned_mean_losses + "<br/>"
        else: 
            initial_mean_losses_path     = os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_msa",county_key.lower() + "_initial","mean_losses.txt")
            tuned_mean_losses_path       = os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_msa",county_key.lower() + "_tuned","mean_losses.txt")
            initial_mean_losses     = self.get_data_from_file(initial_mean_losses_path)
            tuned_mean_losses       = self.get_data_from_file(tuned_mean_losses_path)            
            initial_hparams         = self.get_data_from_file(os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_msa",county_key.lower() + "_initial","hparams.txt")).replace("\n","\n<br/>") + "SMAPE Score: " + initial_mean_losses + "<br/>"
            tuned_hparams           = self.get_data_from_file(os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_msa",county_key.lower() + "_tuned","hparams.txt")).replace("\n","\n<br/>") + "SMAPE Score: " + tuned_mean_losses + "<br/>"


        print("*"*60)
        print("initial_mean_losses_path=",initial_mean_losses_path)


        #get out if it errored out
        if not os.path.exists(initial_mean_losses_path):
                return None,None,None,None,None

        #implicit else
        initial_mean_losses     = float(initial_mean_losses)
        tuned_mean_losses       = float(tuned_mean_losses)

        print("tuned_mean_losses=",tuned_mean_losses)
        print("initial_mean_losses=",initial_mean_losses)

        model_to_use = None
        model_smape = None
        if initial_mean_losses > tuned_mean_losses:
            # model_to_use = "tuned"
            # if initial_mean_losses <= float(0.15):
            #     model_to_use = "initial"
            #     model_smape = initial_mean_losses
            #     if is_county:
            #         model_dir = os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_files",county_key.lower() + "_initial")
            #     else:
            #         model_dir = os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_msa",county_key.lower() + "_initial")
            # else:
            if is_county:
                model_dir = os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_files",county_key.lower() + "_tuned")
            else:
                model_dir = os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_msa",county_key.lower() + "_tuned")
            model_to_use = "tuned"
            model_smape = tuned_mean_losses
        else:
            if is_county:
                model_dir = os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_files",county_key.lower() + "_initial")
            else:
                model_dir = os.path.join(self.get_this_dir(),"data","ml_predictions","pytorch_msa",county_key.lower() + "_initial")
            model_to_use = "initial"
            model_smape = initial_mean_losses

        #global MODEL_USED
        self.MODEL_USED = model_to_use

        model_df = pd.read_csv(os.path.join(model_dir,county_key.lower() + ".csv"))
        print("model_smape=",model_smape)
        print("model_smape=",model_smape)
        return model_smape, model_df, model_to_use, initial_hparams, tuned_hparams

    def load_county_data(self,county_key,is_county):

        data_directory      = "data"
        ml_pred_dir         = "ml_predictions"
        cdf                 = "county_data_files"
        mdf                 = "msa_data_files"
        county_file         = county_key + ".csv"
        olsmfd              = "ols_model_files"
        olsd                = "ols_models_by_county"
        mfd                 = "model_files"
        mfn                 = county_key + "_OLS.pickle"
        ired                = "interest_rate_effect"
        ird                 = "thirty_year_interest_rate_three"
        sd                  = "summary"
        sf                  = county_key + "_summary.txt"

        #print("is_county=",is_county)

        if is_county:
            cf = pd.read_csv(os.path.join(self.get_this_dir(),data_directory,ml_pred_dir,cdf,county_file))
        else:
            cf = pd.read_csv(os.path.join(self.get_this_dir(),data_directory,ml_pred_dir,mdf,county_file.lower()))

        # print("*"*68)
        # print(os.path.join(self.get_this_dir(),data_directory,ml_pred_dir,mdf,county_file.lower()))
        # print("*"*68)


        cf["m_active_listing_count"] = cf["active_listing_count"]

        # pf = open(os.path.join(self.get_this_dir(),data_directory,ml_pred_dir,olsmfd,ired,olsd,ird,mfd,mfn),"rb")

        # po = pickle.load(pf)

        sf = os.path.join(self.get_this_dir(),data_directory,ml_pred_dir,olsmfd,ired,olsd,ird,sd,sf)
        print("About to load best object")
        print("*"*60)
        model_smape, model_df, model_to_use, initial_hparams, tuned_hparams = self.load_best_county_model(county_key=county_key,is_county=is_county)

        self.INITIAL_HPARAMS = initial_hparams
        self.TUNED_HPARAMS = tuned_hparams

        return cf,sf,model_smape, model_df, model_to_use

    def get_models_hparams(self):
        # global INITIAL_HPARAMS
        # global TUNED_HPARAMS
        # global MODEL_USED
        return self.INITIAL_HPARAMS, self.TUNED_HPARAMS, self.MODEL_USED


    def analyze_model_df(self):
        MODEL_DF = self.MODEL_DF
        MODEL_SMAPE = self.MODEL_SMAPE
        #Get the last two months:
        working_df = copy.deepcopy(MODEL_DF)

        working_df = working_df.tail(2)

        additional_text = None

        actual_count    = working_df["median_listing_price"].sum()
        predict_count   = working_df["pred_median_listing_price"].sum()
        predict_higher  = True if predict_count > actual_count else False

        if predict_higher:
            pct_change = ((predict_count - actual_count) * 100) / predict_count
        else:
            pct_change = ((actual_count - predict_count) * 100) / actual_count

        #look at inventory
        #this_month = MODEL_DF.tail(1)["date"]
        this_month                          = int(MODEL_DF.tail(1)["month"])
        this_months_actual_listing_count    = float(MODEL_DF.tail(1)["active_listing_count"])
        this_months_average_listings        = MODEL_DF.groupby("month")["active_listing_count"].mean()[this_month]

        #print(this_months_actual_listing_count)
        #print(this_months_average_listings)

        this_month_higher = True if this_months_actual_listing_count > this_months_average_listings else False

        if this_month_higher:
            l_pct_change = ((this_months_actual_listing_count - this_months_average_listings) * 100) / this_months_average_listings
        else:
            l_pct_change = ((this_months_average_listings - this_months_actual_listing_count) * 100) / this_months_actual_listing_count

        this_months_days_on_market               = float(MODEL_DF.tail(1)["median_days_on_market"])
        this_month_average_days_on_market        = MODEL_DF.groupby("month")["median_days_on_market"].mean()[this_month]

        #print(this_months_actual_listing_count)
        #print(this_months_average_listings)

        this_month_higher_dom = True if this_months_days_on_market > this_month_average_days_on_market else False

        if this_month_higher_dom:
            l_pct_change_dom = ((this_months_days_on_market - this_month_average_days_on_market) * 100) / this_month_average_days_on_market
        else:
            l_pct_change_dom = ((this_month_average_days_on_market - this_months_days_on_market) * 100) / this_months_days_on_market

        # if not this_month_higher_dom:
        #     additional_text_dom = "<br/>NOTE: The model looks at interest rates and inventory. At the present time <b>inventory is {0} % lower</b>, at {1} units on market.<br/> The average listing count is {2}, for the entirety of the same months the model was trained on.".format(round(l_pct_change,2),round(this_months_days_on_market),round(this_month_average_days_on_market))

        # if this_month_higher_dom:
        #     additional_text_dom = "<br/>NOTE: The model looks at interest rates and inventory. At the present time <b>inventory is {0} % higher</b>, at {1} units on market.<br/> The average listing count is {2}, for the entirety of the same months the model was trained on.".format(round(l_pct_change,2),round(this_months_days_on_market),round(this_month_average_days_on_market))

        if not this_month_higher:
            additional_text = "<br/>NOTE: The model looks at interest rates, days on market, and inventory. At the present time <b>inventory is {0} % lower</b>, at {1} units on market.<br/> The average listing count is {2}, for the entirety of the same months the model was trained on.".format(round(l_pct_change,2),round(this_months_actual_listing_count),round(this_months_average_listings))

        if this_month_higher:
            additional_text = "<br/>NOTE: The model looks at interest rates, days on market, and inventory. At the present time <b>inventory is {0} % higher</b>, at {1} units on market.<br/> The average listing count is {2}, for the entirety of the same months the model was trained on.".format(round(l_pct_change,2),round(this_months_actual_listing_count),round(this_months_average_listings))

        if this_month_higher_dom:
            additional_text = additional_text + "<br/>At the present time <b>days on market is {0} % higher</b>, at {1} average days on market.<br/> The average days on market is {2}, for the entirety of the same months the model was trained on.".format(round(l_pct_change_dom,2),round(this_months_days_on_market),round(this_month_average_days_on_market))
        else: 
            additional_text = additional_text + "<br/>At the present time <b>days on market is {0} % lower</b>, at {1} average days on market.<br/> The average days on market is {2}, for the entirety of the same months the model was trained on.".format(round(l_pct_change_dom,2),round(this_months_days_on_market),round(this_month_average_days_on_market))


        #print("MODEL_SMAPE=",MODEL_SMAPE)
        if additional_text is None:
            additional_text = ""
        additional_text = additional_text + "<br/>The Model's mean SMAPE score is <b>{0}</b>.".format(MODEL_SMAPE)

        this_month_inv_higher = this_month_higher

        return predict_higher, pct_change, additional_text, this_month_inv_higher, l_pct_change


    def get_model_signal(self):
        MODEL_SMAPE = self.MODEL_SMAPE
        MODEL_DF = self.MODEL_DF
        MODEL_USED = self.MODEL_USED
        #global MODEL_SIGNAL
        return_text = None
        signal = "up"

        if MODEL_SMAPE is None:
            signal = "neutral"
            return_text = "The LSTM Neural Net Model errored out and cound not converge. <br/>As such, it is not a reliable component of our composite model.".format(MODEL_SMAPE)
            self.MODEL_SIGNAL = signal
            return signal, return_text, MODEL_USED,MODEL_DF

        if MODEL_SMAPE > 0.15:
            signal = "neutral"
            return_text = "The LSTM Neural Net Model has a <b>SMAPE score of {0}</b>. <br/>As such, it is not a reliable component of our composite model.".format(MODEL_SMAPE)
            self.MODEL_SIGNAL = signal
            return signal, return_text, MODEL_USED,MODEL_DF

        
        #implicit else
        predict_higher, pct_change , additional_text, this_mont_inv_higher, inv_pct_change = self.analyze_model_df()


        print("pct_change=",pct_change)

        if predict_higher and pct_change < 0.5:
            signal="neutral"
            return_text = "The neural net believes that the listing price should be <b>{0} % higher</b> than the actual listing price.".format(round(pct_change,2))
            return_text = return_text + "<br/>Since this increase is so little, we give the neural net a \"neutral\" rating."
            if additional_text is not None:
                return_text = return_text + additional_text
                self.MODEL_SIGNAL = signal
            return signal,return_text,MODEL_USED,MODEL_DF


        if predict_higher:
            print("got in here",this_mont_inv_higher,inv_pct_change)
            signal="up"
            return_text = "The neural net believes that the listing price should be <b>{0} % higher</b> than the actual listing price.".format(round(pct_change,0))
            if this_mont_inv_higher and inv_pct_change > 25.0 :
                signal="neutral"
                self.MODEL_SIGNAL = signal
                return_text = return_text + "<br/> <b>However inventory high and rising</b>, indicating that prices may not have support."                
            if additional_text is not None:
                return_text = return_text + additional_text
                self.MODEL_SIGNAL = signal                
            return signal,return_text,MODEL_USED,MODEL_DF

        if not predict_higher:
            signal="down"
            return_text = "The neural net believes that the listing price should be <b>{0} % lower</b> than the actual listing price.".format(round(pct_change,0))
            #If it's predicting down, but, inventory is very low
            #cancel its vote, and tell the user.
            if not this_mont_inv_higher and inv_pct_change > 40.0 :
                signal="down"
                return_text = return_text + "<br/> <b>However inventory is at historic lows in this market</b>, indicating that prices may have support."
            if additional_text is not None:
                return_text = return_text + additional_text

            self.MODEL_SIGNAL = signal

        return signal, return_text, MODEL_USED, MODEL_DF


    def load_state_drop_down_data(self):

        data_directory      = "data"
        sub_dir             = "ml_predictions"
        sub_dir1            = "files_for_drop_downs"
        state_file          = "state_file.csv"
        unique_counties     = "unique_counties.csv"

        dir = os.path.join(self.get_this_dir(),data_directory,sub_dir,sub_dir1)

        state_file = pd.read_csv(os.path.join(dir,state_file))

        unique_counties = pd.read_csv(os.path.join(dir,unique_counties))

        return state_file, unique_counties

    def convert_signal_to_int(self,signal):
        if signal == "neutral":
            return 0
        if signal == "up":
            return 1
        if signal == "down":
            return -1

    def get_smape_multiplier(self,smape_score):
        if smape_score in np.arange(0.15,0.16,0.01):
            return 1
        if smape_score in np.arange(0.14,0.15,0.01):
            return 1.1
        if smape_score in np.arange(0.13,0.14,0.01):
            return 1.2
        if smape_score in np.arange(0.12,0.13,0.01):
            return 1.3
        if smape_score in np.arange(0.11,0.12,0.01):
            return 1.4           
        if smape_score in np.arange(0.10,0.11,0.01):
            return 1.5
        if smape_score in np.arange(0.09,0.10,0.01):            
            return 1.6
        if smape_score in np.arange(0.08,0.09,0.01):
            return 1.7           
        if smape_score in np.arange(0.07,0.08,0.01):
            return 1.8            
        if smape_score in np.arange(0.06,0.07,0.01):
            return 1.9            
        if smape_score in np.arange(0.05,0.06,0.01):
            return 2.0
        if smape_score in np.arange(0.04,0.05,0.01):
            return 2.1
        if smape_score in np.arange(0.03,0.04,0.01):
            return 2.2           
        if smape_score in np.arange(0.02,0.03,0.01):
            return 2.3           
        if smape_score in np.arange(0.01,0.02,0.01):
            return 2.4           



    def get_aggregate_signal(self):
        INV_SIGNAL = self.INV_SIGNAL
        INT_SIGNAL = self.INT_SIGNAL
        DOM_SIGNAL = self.DOM_SIGNAL
        PRICE_SIGNAL = self.PRICE_SIGNAL
        MODEL_SIGNAL = self.MODEL_SIGNAL
        MODEL_SMAPE = self.MODEL_SMAPE
        #global OVERALL_SIGNAL

        i_inv_signal = self.convert_signal_to_int(INV_SIGNAL)
        i_int_signal = self.convert_signal_to_int(INT_SIGNAL)
        i_dom_signal = self.convert_signal_to_int(DOM_SIGNAL)
        i_price_signal = self.convert_signal_to_int(PRICE_SIGNAL)
        i_model_signal = self.convert_signal_to_int(MODEL_SIGNAL)

        print(i_inv_signal,i_int_signal,i_dom_signal,i_price_signal)
        print(MODEL_SMAPE)

        smape_multiplier = self.get_smape_multiplier(MODEL_SMAPE)

        print(self.get_smape_multiplier(MODEL_SMAPE))

        if MODEL_SIGNAL == 'neutral':
            smape_multiplier = 1

        if MODEL_SMAPE is not None and MODEL_SMAPE<=0.15:
            print("dealio")
            print(i_inv_signal,i_int_signal,i_dom_signal,i_price_signal,i_model_signal,smape_multiplier)
            print("dealio")

            aggregate_signal = (i_inv_signal+i_dom_signal+i_price_signal+round((i_model_signal*smape_multiplier)))
            #exceptions.
            #netrual across the board, but weak neural net.
            if i_inv_signal == 0 and i_dom_signal == 0 and i_price_signal ==0 and self.get_smape_multiplier(MODEL_SMAPE) == 1:
                aggregate_signal =0

        else:
            aggregate_signal = (i_inv_signal+i_dom_signal+i_price_signal+i_int_signal)

        if aggregate_signal ==0:
            self.OVERALL_SIGNAL = "neutral"
        if aggregate_signal <0:
            self.OVERALL_SIGNAL = "down"
        if aggregate_signal >0:
            self.OVERALL_SIGNAL = "up"            
        #print("OVERALL_SIGNAL=",OVERALL_SIGNAL)

        return self.OVERALL_SIGNAL







    def get_world_event_data(self) :

        data_directory = "data"
        trade_balance_sub_dir = "econ_concepts"
        file_name = "econ_concepts.txt"

        return_file_name = os.path.join(self.get_this_dir(),data_directory,trade_balance_sub_dir,file_name)

        return pd.read_csv(return_file_name,sep='\t').replace(np.nan,'',regex=True)



    def get_model_graph(self,label="Temporal Neural Net Predictions vs Actuals for: "):

        #df['date'] = pd.to_datetime(df['date'])

        #global COUNTY_KEY
        COUNTY_KEY = self.COUNTY_KEY
        state = COUNTY_KEY.split("_")[len(COUNTY_KEY.split("_"))-1].upper()
        county_nm =""
        for part in COUNTY_KEY.split("_"):
            if part.upper() == state:
                continue
            county_nm = county_nm + " " + part.capitalize()

        county_nm = county_nm + ", " + state

        MODEL_DF = self.MODEL_DF
        df = copy.deepcopy(MODEL_DF).tail(11)

        base = alt.Chart(df).transform_fold(["median_listing_price","pred_median_listing_price"])
        #print(df)
        #print(df.describe())
        #print(df.dtypes)

        title2 = label + county_nm

        line = base.mark_line().encode(

        x=alt.X('date:O',axis=alt.Axis(title='Month and Year:')),
        y=alt.Y('value:Q',axis=alt.Axis(title='Value:')),
        

        color=alt.Color(field="key", type="nominal",
                        scale = alt.Scale(range = ['#265499', '#A8DDA4']),
                        legend = alt.Legend(title="Key")),
        strokeWidth = alt.value(3)
        )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000,
        ).encode(
            x=alt.X('date:O',axis=alt.Axis(title='',labelAngle=-15)),
            y=alt.Y('value:Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip("date"),
                     alt.Tooltip("median_listing_price",title="Actual Median Listing Price",format=",.0f" ),
                     alt.Tooltip("pred_median_listing_price",title="Model's Opinion:",format=",.0f")
                     ]
        )

        return_chart = alt.layer(line,points).properties(
            width=800,
            height=220,
            title=title2
        )

        return return_chart


