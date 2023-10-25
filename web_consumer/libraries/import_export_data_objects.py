import os
import sys
import json
from datetime import datetime
from os import system, name
from time import sleep
import copy
import threading
import imp
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandasql as psql
from  libraries.utility import Utility



class import_export_data(Utility):
    
    ALL_COUNTRIES_DATA_FRAME = None
    ALL_COUNTRIES_BY_TYPE_DF = None
    ALL_COUNTRIES_GDP_DATA = None
    EXCHANGE_RATE_DATA = None


    def __init__(self,load_data_from_url=False):
        super().__init__()
        global ALL_COUNTRIES_DATA_FRAME
        global ALL_COUNTRIES_BY_TYPE_DF
        global ALL_COUNTRIES_GDP_DATA
        global EXCHANGE_RATE_DATA
        if load_data_from_url == False:
            EXCHANGE_RATE_DATA = self.load_exchange_rate_data()
            ALL_COUNTRIES_DATA_FRAME = self.load_and_clean_up_top_20_file()
            ALL_COUNTRIES_BY_TYPE_DF = self.load_and_clean_up_WTO_file()
            ALL_COUNTRIES_GDP_DATA = self.load_and_clean_up_GDP_file()
            
        else:
            ALL_COUNTRIES_DATA_FRAME = self.load_and_clean_up_top_20_file_fromurl()
            ALL_COUNTRIES_BY_TYPE_DF = self.load_and_clean_up_WTO_file_fromurl()


    def print_internal_directory(self):

        for k,v in self.__dict__.items():
            print("{} is \"{}\"".format(k,v))


    def get_world_event_data(self) :

        data_directory = "data"
        trade_balance_sub_dir = "world_events"
        file_name = "world_events.txt"

        return_file_name = os.path.join(self.get_this_dir(),data_directory,trade_balance_sub_dir,file_name)

        return pd.read_csv(return_file_name,sep='\t').replace(np.nan,'',regex=True)


    def get_world_event_data_json(self):
        return self.get_world_event_data().to_json(orient='records')

    def get_top_20_full_file_name(self) :

        data_directory = "data"
        trade_balance_sub_dir = "trade_balance_datasets"
        top_20_file_name = "top20_2014-2020_all.csv"

        return_file_name = os.path.join(self.get_this_dir(),data_directory,trade_balance_sub_dir,top_20_file_name)

        return return_file_name
    def get_GDP_full_file_name(self):
        data_directory = "data"
        trade_balance_sub_dir = "trade_balance_datasets"
        GDP_file_name = "wb_econind_gdp_data.csv"
        return_file_name = os.path.join(self.get_this_dir(),data_directory,trade_balance_sub_dir,GDP_file_name)

        return return_file_name

    def get_WTO_individual_file_name(self) :
        
        file_names = ['WtoData_services_imports.csv','WtoData_services_imports.csv','WtoData_merchandise_imports.csv','WtoData_merchandise_exports.csv']

        data_directory = "data"
        trade_balance_sub_dir = "trade_balance_datasets"
        return_file_path_list = []

        for file_name in file_names:
            return_file_path_list.append(os.path.join(self.get_this_dir(),data_directory,trade_balance_sub_dir,file_name))

        return return_file_path_list


    def get_WTO_full_file_name(self) :

        data_directory = "data"
        trade_balance_sub_dir = "trade_balance_datasets"
        WTO_file_name = "WtoData_all.csv"

        return_file_name = os.path.join(self.get_this_dir(),data_directory,trade_balance_sub_dir,WTO_file_name)

        return return_file_name


    def get_world_countries_by_iso_label(self):
        data_directory = "data"
        file_name = "countries.tsv"

        load_file_name = os.path.join(self.get_this_dir(),data_directory,file_name)

        my_data = pd.read_csv(load_file_name,sep='\t')
        return my_data

    def get_exchange_rate_files(self) :

        data_directory = "data"
        exchange_rate_dir = "exchange_rates"
        exchange_rate = "exchange_rates_from_oecd_website.csv"
        country_codes = "wikipedia-iso-country-codes.csv"

        exchange_rate_file = os.path.join(self.get_this_dir(),data_directory,exchange_rate_dir,exchange_rate)

        country_code_file = os.path.join(self.get_this_dir(),data_directory,exchange_rate_dir,country_codes)

        return exchange_rate_file, country_code_file

    def load_exchange_rate_data(self):

        exchange_rate_file, country_code_file = self.get_exchange_rate_files()

        exchange_rates = pd.read_csv(exchange_rate_file)

        country_codes = pd.read_csv(country_code_file)

        mysql = '''
            select 
                country_codes.[English short name lower case] as Country,
                exchange_rates.TIME as year,
                exchange_rates.Value as rate
            from 
                exchange_rates
            join country_codes
                on
                country_codes.[Alpha-3 code] = exchange_rates.LOCATION

        '''

        return psql.sqldf(mysql)
        


    def load_and_clean_up_top_20_file_fromurl(self):

        #url = "https://tuneman7.github.io/WtoData_all.csv"
        url = "https://tuneman7.github.io/top20_2014-2020_all.csv"

        my_data = pd.read_csv(url)
        
        return my_data


    def load_and_clean_up_top_20_file(self):

        global EXCHANGE_RATE_DATA

        file_to_load = self.get_top_20_full_file_name()

        my_data = pd.read_csv(file_to_load)

        sql = '''
            select 
                my_data.*,
                EXCHANGE_RATE_DATA_1.rate as country_exchange_rate,
                EXCHANGE_RATE_DATA_2.rate as trading_partner_exchange_rate
            from my_data
            left join EXCHANGE_RATE_DATA as EXCHANGE_RATE_DATA_1
                on
                    EXCHANGE_RATE_DATA_1.year = my_data.year
                and
                    EXCHANGE_RATE_DATA_1.Country = my_data.Country
            left join EXCHANGE_RATE_DATA as EXCHANGE_RATE_DATA_2
                on
                    EXCHANGE_RATE_DATA_2.year = my_data.year
                and
                    EXCHANGE_RATE_DATA_2.Country = my_data.[Trading Partner]

        '''
        my_data = psql.sqldf(sql)
        
        return my_data

    def load_and_clean_up_GDP_file(self):

        file_to_load = self.get_GDP_full_file_name()

        my_data = pd.read_csv(file_to_load)

        global EXCHANGE_RATE_DATA

        sql = '''
        select 
            my_data.*,
            EXCHANGE_RATE_DATA.rate as exchange_rate
        from my_data
        left join EXCHANGE_RATE_DATA
            on 
                EXCHANGE_RATE_DATA.Country = my_data.Country
            and
                EXCHANGE_RATE_DATA.year = my_data.Year


        '''
        
        return psql.sqldf(sql)

    def load_and_clean_up_EU_files(self):

        #file_to_load = self.get_WTO_individual_file_name()
        file_to_load = self.load_and_clean_up_top_20_file()

        eu_countries=['Austria','Belgium','Croatia','Czech Republic','Denmark','Finland','France','Germany','Greece','Hungary',
            'Italy','Netherlands','Poland','Portugal','Spain','Sweden','United Kingdom']

        eu_df = file_to_load.loc[(file_to_load['Trading Partner'].isin(eu_countries)) & (file_to_load['country'].isin(eu_countries))]
        eu_df_filtered = eu_df[['Trading Partner','country','Total Trade ($M)','year']].reset_index()
        #df_concat = eu_df_filtered.pivot_table('Total Trade ($M)', ['Trading Partner','country'], 'year').reset_index()
        
        return eu_df_filtered


    def load_and_clean_up_WTO_file(self):

        file_to_load = self.get_WTO_full_file_name()

        my_data = pd.read_csv(file_to_load)

        global EXCHANGE_RATE_DATA

        # sql = '''
        #     select 
        #         my_data.*,
        #         EXCHANGE_RATE_DATA_1.rate as reporting_economy_exchange_rate,
        #         EXCHANGE_RATE_DATA_2.rate as partner_economy_exchange_rate
        #     from my_data
        #     left join EXCHANGE_RATE_DATA as EXCHANGE_RATE_DATA_1
        #         on
        #         EXCHANGE_RATE_DATA_1.Country = my_data.[Reporting Economy]
        #     left join EXCHANGE_RATE_DATA as EXCHANGE_RATE_DATA_2
        #         on
        #         EXCHANGE_RATE_DATA_2.Country = my_data.[Partner Economy]

        # '''

        sql = '''
            select 
                my_data.*,
                EXCHANGE_RATE_DATA_1.rate as reporting_economy_exchange_rate
            from my_data
            left join EXCHANGE_RATE_DATA as EXCHANGE_RATE_DATA_1
                on
                EXCHANGE_RATE_DATA_1.Country = my_data.[Reporting Economy]
                and EXCHANGE_RATE_DATA_1.year = my_data.Year

        '''
        
        return psql.sqldf(sql)

    def load_and_clean_up_WTO_file_fromurl(self):

        url = "https://tuneman7.github.io/WtoData_all.csv"
        #url = "https://tuneman7.github.io/top20_2014-2020_all.csv"

        my_data = pd.read_csv(url)
        
        return my_data

    def get_sql_for_world_or_region(self, source_country):
        my_sql = '''
        SELECT
            'World' [Trading Partner],
            sum([Total Trade ($M)])  [Total Trade ($M) ],
            avg([RtW (%)])  [RtW (%)],
            sum([Exports ($M)] )[Exports ($M)],
            avg([RtW (%).1])  [RtW (%).1],
            sum([Imports ($M)])  [Imports ($M)],
            avg([RtW (%).2])  [RtW (%).2],
            sum([Net Exports ($M)])  [Net Exports ($M)],
            ''  [Exports Ticker],
            ''  [Imports Ticker],
            country,
            year
        FROM 
            my_data_frame
        WHERE 
            country =  \'''' + source_country + '''\'
        and
            [Trading Partner] <> \'''' + source_country + '''\'
        GROUP BY
            country, year
        '''
        #print(my_sql)
        return my_sql

    def get_sql_for_world_or_region(self, source_country):
        my_sql = '''
        SELECT
            'World' [Trading Partner],
            sum([Total Trade ($M)])  [Total Trade ($M)],
            avg([RtW (%)])  [RtW (%)],
            sum([Exports ($M)] )[Exports ($M)],
            avg([RtW (%).1])  [RtW (%).1],
            sum([Imports ($M)])  [Imports ($M)],
            avg([RtW (%).2])  [RtW (%).2],
            sum([Net Exports ($M)])  [Net Exports ($M)],
            ''  [Exports Ticker],
            ''  [Imports Ticker],
            country,
            year
        FROM 
            my_data_frame
        WHERE 
            country =  \'''' + source_country + '''\'
        and
            [Trading Partner] <> \'''' + source_country + '''\'
        GROUP BY
            country, year
        '''
        #print(my_sql)
        return my_sql

    def get_data_by_source_and_target_country(self,source_country,target_country):

        global ALL_COUNTRIES_DATA_FRAME

        my_data_frame = ALL_COUNTRIES_DATA_FRAME

        if target_country.lower() == "world":
            my_sql = self.get_sql_for_world_or_region(source_country)
        else:
            my_sql = "SELECT * FROM my_data_frame WHERE country = '" +  source_country + "' and [Trading Partner] = '" + target_country + "' "

        my_return_data = psql.sqldf(my_sql)

        return my_return_data

    def get_top5data_by_source_country(self,source_country):

        global ALL_COUNTRIES_DATA_FRAME

        my_data_frame = ALL_COUNTRIES_DATA_FRAME

        if source_country.lower() == 'world':
            my_sql = '''
            SELECT * 
            FROM (
                SELECT *,
                    RANK() OVER(PARTITION BY year ORDER BY [Total Trade ($M)] DESC) AS rnk
                FROM my_data_frame
                where country in (select distinct country from my_data_frame)
            ) t
            WHERE rnk <= 5
            '''
        else:

            my_sql = '''
            SELECT * 
            FROM (
                SELECT *,
                    RANK() OVER(PARTITION BY year ORDER BY [Total Trade ($M)] DESC) AS rnk
                FROM my_data_frame
                WHERE country = ''' + "'" + source_country + '''\'
            ) t
            WHERE rnk <= 5
            '''

        my_return_data = psql.sqldf(my_sql)

        return my_return_data

    def get_top5data_by_imports_exports(self,source_country, direction):

        global ALL_COUNTRIES_BY_TYPE_DF

        my_data_frame = ALL_COUNTRIES_BY_TYPE_DF
        if source_country.lower() != "world":
            my_sql = '''
            SELECT *
            FROM (
                SELECT 
                    Year, Value,
                    [Product/Sector-reformatted],
                    RANK() OVER(
                        PARTITION BY Year 
                        ORDER BY Value DESC) AS rnk
                FROM my_data_frame
                WHERE      
                    [Reporting Economy] =  \'''' + source_country + '''\'
                and
                    Direction = \'''' + direction + '''\'
                and
                    [Product/Sector-reformatted] NOT LIKE '%Total%'
            ) t
            WHERE rnk <= 5
            '''
        else:
            my_sql = '''
            SELECT *
            FROM (
                SELECT 
                    Year, Value,
                    [Product/Sector-reformatted],
                    RANK() OVER(
                        PARTITION BY Year 
                        ORDER BY Value DESC) AS rnk
                FROM my_data_frame
                WHERE      
                    [Reporting Economy] in (select distinct [Reporting Economy] from my_data_frame)
                and
                    Direction = \'''' + direction + '''\'
                and
                    [Product/Sector-reformatted] NOT LIKE '%Total%'
            ) t
            WHERE rnk <= 5
            '''


        my_return_data = psql.sqldf(my_sql)

        return my_return_data

    def imports_exports_by_sectors(self,source_country, target_country, direction):

        global ALL_COUNTRIES_BY_TYPE_DF

        my_data_frame = ALL_COUNTRIES_BY_TYPE_DF
        if source_country.lower() != "world":
            my_sql = '''
            SELECT 
                Year, Value,
                [Product/Sector-reformatted],
                [Reporting Economy]
            FROM my_data_frame
            WHERE      
                ([Reporting Economy] =  \'''' + source_country + '''\'
                or
                [Reporting Economy] =  \'''' + target_country + '''\'
                )
            and
                Direction = \'''' + direction + '''\'
            and
                [Product/Sector-reformatted] NOT LIKE '%Total%'
            '''
        else:
            my_sql = '''
            SELECT 
                Year, Value,
                [Product/Sector-reformatted],
                [Reporting Economy]
            FROM my_data_frame
            WHERE      
                [Reporting Economy] in (select distinct [Reporting Economy] from my_data_frame)
            and
                Direction = \'''' + direction + '''\'
            and
                [Product/Sector-reformatted] NOT LIKE '%Total%'
            '''


        my_return_data = psql.sqldf(my_sql)

        return my_return_data

    def imports_exports_by_sectors_source(self):

        global ALL_COUNTRIES_BY_TYPE_DF

        my_data_frame = ALL_COUNTRIES_BY_TYPE_DF
        my_sql = '''
        SELECT 
            distinct
            Year, Value,
            [Product/Sector-reformatted],
            [Direction],
            [Type],
            [Reporting Economy]
        FROM my_data_frame
        WHERE [Product/Sector-reformatted] NOT LIKE '%Total%'
        '''
        ## and [Reporting Economy] =  \'''' + source_country + '''\'

        my_return_data = psql.sqldf(my_sql)

        return my_return_data

    def get_top_trading_and_net_value(self,source_country):

        global ALL_COUNTRIES_DATA_FRAME

        my_data_frame = ALL_COUNTRIES_DATA_FRAME
        if source_country.lower() != "world":
            my_sql = '''
            SELECT 
            [Trading Partner],
            [year],
            [Total Trade ($M)],
            [Exports ($M)]-[Imports ($M)] as net_trade,
            'Net: ' || '$' || printf("%,d",cast([Exports ($M)]-[Imports ($M)] as text)) as net_trade_text,
            [Exports ($M)],
            [Imports ($M)],
            ''' + "'" + source_country + "'" + ''' as 'source_country'
            FROM (
                SELECT *,
                    RANK() OVER(PARTITION BY year ORDER BY [Total Trade ($M)] DESC) AS rnk
                FROM my_data_frame
                WHERE country = ''' + "'" + source_country + '''\'
            ) t
            WHERE rnk <= 5
            '''
        else:
            my_sql = '''
            SELECT 
            distinct
            [Trading Partner],
            [year],
            [Total Trade ($M)],
            [Exports ($M)]-[Imports ($M)] as net_trade,
            'Net: ' || '$' || printf("%,d",cast([Exports ($M)]-[Imports ($M)] as text)) as net_trade_text,
            [Exports ($M)],
            [Imports ($M)],
            'World' as source_country
            FROM (
                SELECT 
                    [Trading Partner],
                    sum([Total Trade ($M)]) as [Total Trade ($M)],
                    sum([Exports ($M)]) as [Exports ($M)],
                    sum([Imports ($M)]) as [Imports ($M)],
                    year,
                    RANK() OVER(PARTITION BY year ORDER BY sum([Total Trade ($M)]) DESC) AS rnk
                FROM my_data_frame
                WHERE country in (select distinct country from my_data_frame )
                --and [Trading Partner] <> 'European Union'
                group by [Trading Partner],year
            ) t
            WHERE rnk <= 5
            group by [Trading Partner], [year]            
            '''            

        my_return_data = psql.sqldf(my_sql)

        return my_return_data

    
    def get_eu_trade_data(self):
        
        global ALL_COUNTRIES_DATA_FRAME

        my_data_frame = ALL_COUNTRIES_DATA_FRAME

        eu_countries=['Austria','Belgium','Croatia','Czech Republic','Denmark','Finland','France','Germany','Greece','Hungary',
        'Italy','Netherlands','Poland','Portugal','Spain','Sweden']
        eu_countries=pd.DataFrame(eu_countries)
        eu_countries.columns=['Country']
        eu_countries

        my_sql = '''
            SELECT t.*,
            t.Exports*-1 ExportsN
            FROM 
            (
            select
            [country],
            [year],
            case 
            WHEN [Trading Partner] in (select distinct Country from eu_countries) then 'EU'
            WHEN [Trading Partner] not in (select distinct Country from eu_countries) then 'World'
            ELSE 'World'
            END  [Trade Group],
            sum([Imports ($M)]) Imports,
            sum([Exports ($M)]) Exports,
            sum([Total Trade ($M)]) TotalTrade,
            sum([Net Exports ($M)]) NetTrade,
            sum(case WHEN [Total Trade ($M)] > 0 then 1 else 0 end) as [Trade Partners]
            from my_data_frame
            group by [country],[year],[Trade Group]
            ) t
        '''
        
        my_return_data = psql.sqldf(my_sql)

        return my_return_data

    def get_eu_trade_data_pcts(self):
        
        global ALL_COUNTRIES_DATA_FRAME

        eu_countries=['Austria','Belgium','Croatia','Czech Republic','Denmark','Finland','France','Germany','Greece','Hungary',
        'Italy','Netherlands','Poland','Portugal','Spain','Sweden']
        eu_countries=pd.DataFrame(eu_countries)
        eu_countries.columns=['Country']
        eu_countries

        my_data_frame = ALL_COUNTRIES_DATA_FRAME
        
        eu_data_frame=self.get_eu_trade_data()
        
        my_sql = '''
                    SELECT 
                    t.*,
                    g.[Imports] TotalTop20Imports,
                    g.[Exports] TotalTop20Exports,
                    g.[TotalTrade] TotalTop20Trade,
                    g.[NetTrade] TotalTop20NetTrade,
                    t.[Imports]/g.[Imports] EUvWorld_Imports_tradepct,
                    t.[Exports]/g.[Exports] EUvWorld_Exports_tradepct,
                    t.[TotalTrade]/g.[TotalTrade] EUvWorld_TotalTrade_tradepct
                    FROM 
                    (
                    select
                    case 
                    WHEN [country] in ('United States') then 'US'
                    WHEN [country] in ('China') then [country]
                    WHEN [country] in (select distinct Country from eu_countries) then 'EU'
                    WHEN [country] not in (select distinct Country from eu_countries) then 'RoW'
                    ELSE 'RoW'
                    END [Top20group],
                    [year],
                    [Trade Group],
                    sum([Imports]) Imports,
                    sum([Exports]) Exports,
                    sum([TotalTrade]) TotalTrade,
                    sum([NetTrade]) NetTrade
                    from eu_data_frame
                    group by [Top20group],[year],[Trade Group]
                    ) t
                    left join
                    (
                    SELECT
                    [year],
                    case 
                    WHEN [country] in ('United States') then 'US'
                    WHEN [country] in ('China') then [country]
                    WHEN [country] in (select distinct Country from eu_countries) then 'EU'
                    WHEN [country] not in (select distinct Country from eu_countries) then 'RoW'
                    ELSE 'RoW'
                    END [Top20group],
                    sum([Imports]) Imports,
                    sum([Exports]) Exports,
                    sum([TotalTrade]) TotalTrade,
                    sum([NetTrade]) NetTrade
                    from eu_data_frame
                    group by [year],[Top20group]
                    ) g
                    ON
                    t.[Top20group]=g.[Top20group]
                    and 
                    t.[year]=g.[year]
                '''

        my_return_data = psql.sqldf(my_sql)

        my_return_data['EUvsWorld Imports %']=(my_return_data['EUvWorld_Imports_tradepct']*100).round(2)
        my_return_data['EUvsWorld Exports %']=(my_return_data['EUvWorld_Exports_tradepct']*100).round(2)
        my_return_data['EUvsWorld Total Trade %']=(my_return_data['EUvWorld_TotalTrade_tradepct']*100).round(2)
        return my_return_data

    def get_data_nafta_trade_continent_tool(self):
        nafta_return_top5=self.get_top20_trade_continental_cont_data()
        my_return_data_top5_continent=nafta_return_top5[nafta_return_top5['Continent Trade Rank']<=5]
        my_return_data_top5_continent

        my_dataframe=self.get_top20_trade_nafta_continental_cont_data()
        my_dataframe

        my_sql = '''
                    SELECT 
                    country as [Trade Group],
                    [Continent TP] as [Continent],
                    [year] as [Year],
                    [Exports ($M)],
                    [Imports ($M)],
                    [Net Exports ($M)],
                    [Total Trade ($M)],
                    [Continent Trade Rank]
                    FROM my_return_data_top5_continent
                    UNION
                    SELECT
                    [group] as [Trade Group],
                    [Continent TP] as [Continent],
                    [year] [Year],
                    [Exports ($M)],
                    [Imports ($M)],
                    [Net Exports ($M)],
                    [Total Trade ($M)],
                    [Continent Trade Rank]
                    from my_dataframe
                '''

        my_return_data = psql.sqldf(my_sql)
        return my_return_data

    def get_nafta_trade_data(self):
        
        global ALL_COUNTRIES_DATA_FRAME

        my_data_frame = ALL_COUNTRIES_DATA_FRAME

        nafta_countries=['United States','Mexico','Canada']
        nafta_countries=pd.DataFrame(nafta_countries)
        nafta_countries.columns=['Country']
        nafta_countries

        my_sql = '''
            SELECT t.*,
            t.Exports*-1 ExportsN
            FROM 
            (
            select
            [country],
            [year],
            case 
            WHEN [Trading Partner] in (select distinct Country from nafta_countries) then 'NAFTA'
            WHEN [Trading Partner] not in (select distinct Country from nafta_countries) then 'World'
            ELSE 'World'
            END  [Trade Group],
            sum([Imports ($M)]) Imports,
            sum([Exports ($M)]) Exports,
            sum([Total Trade ($M)]) TotalTrade,
            sum([Net Exports ($M)]) NetTrade,
            sum(case WHEN [Total Trade ($M)] > 0 then 1 else 0 end) as [Trade Partners]
            from my_data_frame
            where [Trading Partner]<>'European Union'
            group by [country],[year],[Trade Group]
            ) t
        '''
        
        my_return_data = psql.sqldf(my_sql)

        return my_return_data

    def get_nafta_trade_data_pcts(self):
        
        global ALL_COUNTRIES_DATA_FRAME

        nafta_countries=['United States','Mexico','Canada']
        nafta_countries=pd.DataFrame(nafta_countries)
        nafta_countries.columns=['Country']
        nafta_countries

        my_data_frame = ALL_COUNTRIES_DATA_FRAME
        
        nafta_data_frame=self.get_nafta_trade_data()
        
        my_sql = '''
                    SELECT 
                    t.*,
                    g.[Imports] TotalTop20Imports,
                    g.[Exports] TotalTop20Exports,
                    g.[TotalTrade] TotalTop20Trade,
                    g.[NetTrade] TotalTop20NetTrade,
                    t.[Imports]/g.[Imports] NAFTA_Imports_tradepct,
                    t.[Exports]/g.[Exports] NAFTA_Exports_tradepct,
                    t.[TotalTrade]/g.[TotalTrade] NAFTA_TotalTrade_tradepct
                    FROM 
                    (
                    select
                    case
                    WHEN [country] in ('China') then [country]
                    WHEN [country] in (select distinct Country from nafta_countries) then 'NAFTA'
                    WHEN [country] not in (select distinct Country from nafta_countries) then 'RoW'
                    ELSE 'RoW'
                    END [Top20group],
                    [year],
                    [Trade Group],
                    sum([Imports]) Imports,
                    sum([Exports]) Exports,
                    sum([TotalTrade]) TotalTrade,
                    sum([NetTrade]) NetTrade
                    from nafta_data_frame
                    group by [Top20group],[year],[Trade Group]
                    ) t
                    left join
                    (
                    SELECT
                    [year],
                    case
                    WHEN [country] in ('China') then [country]
                    WHEN [country] in (select distinct Country from nafta_countries) then 'NAFTA'
                    WHEN [country] not in (select distinct Country from nafta_countries) then 'RoW'
                    ELSE 'RoW'
                    END [Top20group],
                    sum([Imports]) Imports,
                    sum([Exports]) Exports,
                    sum([TotalTrade]) TotalTrade,
                    sum([NetTrade]) NetTrade
                    from nafta_data_frame
                    group by [year],[Top20group]
                    ) g
                    ON
                    t.[Top20group]=g.[Top20group]
                    and 
                    t.[year]=g.[year]
                '''

        my_return_data = psql.sqldf(my_sql)

        my_return_data['NAFTA Imports %']=(my_return_data['NAFTA_Imports_tradepct']*100).round(2)
        my_return_data['NAFTA Exports %']=(my_return_data['NAFTA_Exports_tradepct']*100).round(2)
        my_return_data['NAFTA Total Trade %']=(my_return_data['NAFTA_TotalTrade_tradepct']*100).round(2)
        return my_return_data

        
    def get_top20_trade_continental_data(self):
        
        country_mapping=pd.read_csv('data/trade_balance_datasets/country_mapping_2.csv')
        country_mapping

        top20_dataframe=self.load_and_clean_up_top_20_file()

        my_sql = '''

                    SELECT 
                    'Country' as [Level],
                    t.[country],
                    g2.[TradeGroup] as [TradeGroup country],
                    g2.[Top20] as [Top20 country],
                    t.[Trading Partner],
                    --g.[Continent] as [Continent TP],
                    CASE
                    when g.[Continent] in ('Australia', 'Oceania') then 'Oceania'
                    when g.[Continent] in ('null') then 'Other'
                    else g.[Continent]
                    end as [Continent TP],
                    t.[year],
                    t.[Total Trade ($M)],
                    t.[Exports ($M)],
                    t.[Imports ($M)],
                    t.[Net Exports ($M)]
                    FROM top20_dataframe t
                    left join
                    country_mapping g
                    ON
                    t.[Trading Partner]=g.[Country]
                    left join
                    country_mapping g2
                    ON
                    t.[country]=g2.[Country]
                    where t.[country] in ('United States','Mexico','Canada')
                    and g.[Continent] not in ('Geo Group','','')

                    UNION

                    SELECT 
                    'Trade Group' as [Level],
                    g2.[TradeGroup] as [TradeGroup country],
                    g2.[TradeGroup] as [TradeGroup country],
                    g2.[Top20] as [Top20 country],
                    t.[Trading Partner],
                    CASE
                    when g.[Continent] in ('Australia', 'Oceania') then 'Oceania'
                    when g.[Continent] in ('null') then 'Other'
                    else g.[Continent]
                    end as [Continent TP],
                    t.[year],
                    sum(t.[Total Trade ($M)]) [Total Trade ($M)],
                    sum(t.[Exports ($M)]) [Exports ($M)],
                    sum(t.[Imports ($M)]) [Imports ($M)],
                    sum(t.[Net Exports ($M)]) [Net Exports ($M)]
                    FROM top20_dataframe t
                    left join
                    country_mapping g
                    ON
                    t.[Trading Partner]=g.[Country]
                    left join
                    country_mapping g2
                    ON
                    t.[country]=g2.[Country]
                    where g2.[TradeGroup] in ('NAFTA')
                    and g.[Continent] not in ('Geo Group','','')
                    group by g2.[TradeGroup],g2.[TradeGroup],g2.[Top20],t.[Trading Partner],g.[Continent],t.[year]

                '''

        my_return_data = psql.sqldf(my_sql)
        my_return_data['Continent Trade Rank']=my_return_data.groupby(['Level','country','Continent TP','year'])['Total Trade ($M)'].rank(ascending=False)
        return my_return_data


    def get_top20_trade_continental_cont_data(self):
      
        country_mapping=pd.read_csv('data/trade_balance_datasets/country_mapping_2.csv')
        country_mapping

        top20_dataframe=self.load_and_clean_up_top_20_file()

        my_sql = '''
                    SELECT 
                    'Country Continent' as [Level],
                    t.[country],
                    CASE
                    when g.[Continent] in ('Arab World', 'Africa', 'Latin America', 'Australia', 'Oceania','null') then 'Other'
                    else g.[Continent]
                    end as [Continent TP],
                    t.[year],
                    sum(t.[Total Trade ($M)]) [Total Trade ($M)],
                    sum(t.[Exports ($M)]) [Exports ($M)],
                    sum(t.[Imports ($M)]) [Imports ($M)],
                    sum(t.[Net Exports ($M)]) [Net Exports ($M)] 
                    FROM top20_dataframe t
                    left join
                    country_mapping g
                    ON
                    t.[Trading Partner]=g.[Country]
                    left join
                    country_mapping g2
                    ON
                    t.[country]=g2.[Country]
                    where t.[country] in ('United States','Mexico','Canada') and
                    g.[Continent] not in ('Geo Group','','')
                    group by [Level],t.[country],[Continent TP],[year]
                '''

        my_return_data = psql.sqldf(my_sql)
        my_return_data['Continent Trade Rank']=my_return_data.groupby(['Level','country','Continent TP','year'])['Total Trade ($M)'].rank(ascending=False)
        return my_return_data

    def get_top20_trade_nafta_continental_cont_data(self):

        country_mapping=pd.read_csv('data/trade_balance_datasets/country_mapping_2.csv')
        country_mapping

        top20_dataframe=self.load_and_clean_up_top_20_file()

        my_sql = '''
                    SELECT 
                    'Trade Group' as [Level],
                    'NAFTA' as [group],
                    CASE
                    when g.[Continent] in ('Arab World', 'Africa', 'Latin America', 'Australia', 'Oceania','null') then 'Other'
                    else g.[Continent]
                    end as [Continent TP],
                    t.[year],
                    sum(t.[Total Trade ($M)]) [Total Trade ($M)],
                    sum(t.[Exports ($M)]) [Exports ($M)],
                    sum(t.[Imports ($M)]) [Imports ($M)],
                    sum(t.[Net Exports ($M)]) [Net Exports ($M)] 
                    FROM top20_dataframe t
                    left join
                    country_mapping g
                    ON
                    t.[Trading Partner]=g.[Country]
                    left join
                    country_mapping g2
                    ON
                    t.[country]=g2.[Country]
                    where t.[country] in ('United States','Mexico','Canada') and
                    g.[Continent] not in ('Geo Group','','')
                    group by [Level],[group],[Continent TP],[year]
                '''

        my_return_data = psql.sqldf(my_sql)
        my_return_data['Continent Trade Rank']=my_return_data.groupby(['group','year'])['Total Trade ($M)'].rank(ascending=False)
        return my_return_data


    def get_nafta_world_trade_data(self):
 
        global ALL_COUNTRIES_DATA_FRAME

        nafta_countries=['United States','Mexico','Canada']
        nafta_countries=pd.DataFrame(nafta_countries)
        nafta_countries.columns=['Country']
        nafta_countries

        my_data_frame = ALL_COUNTRIES_DATA_FRAME

        my_sql = '''
                select
                t.*
                from
                (
                select
                    Country,
                    Year,
                    'World' [Trading Group],
                    sum([Imports ($M)]*-1) Imports,
                    sum([Exports ($M)]) Exports,
                    sum([Net Exports ($M)]) Net_Exports
                    from my_data_frame
                    where Country in (select Country from nafta_countries)
                    group by [Country], [Year], [Trading Group]
                union
                select
                    Country,
                    Year,
                    'NAFTA' [Trading Group],
                    sum(case WHEN [Trading Partner] in (select Country from nafta_countries) then [Imports ($M)]*-1 else 0 end) Imports,
                    sum(case WHEN [Trading Partner] in (select Country from nafta_countries) then [Exports ($M)] else 0 end) Exports,
                    sum(case WHEN [Trading Partner] in (select Country from nafta_countries) then [Net Exports ($M)] else 0 end) Net_Exports
                    from my_data_frame
                    where Country in (select Country from nafta_countries)
                    group by [Country], [Year], [Trading Group]
                ) t
                '''

        my_return_data = psql.sqldf(my_sql)

        return my_return_data
    

    def get_distinct_country_list(self,add_world=False,as_data_frame=False):

        global ALL_COUNTRIES_DATA_FRAME

        my_data_frame = ALL_COUNTRIES_DATA_FRAME

        my_sql = "SELECT distinct country from my_data_frame"

        my_return_data = psql.sqldf(my_sql)
        if as_data_frame==True:
            return my_return_data

        return_data = [ str(value).strip("[]'") for value in my_return_data.values.tolist()]
        if add_world == True:
            return_data.append("World")
    
        return return_data

    def get_distinct_country_tuples(self,add_world=False):

        return [(value,value) for value in self.get_distinct_country_list(add_world=add_world)]

    def get_gdp_data_by_country(self,source_country):

        global ALL_COUNTRIES_GDP_DATA

        my_data = ALL_COUNTRIES_GDP_DATA

        sql = "select * from my_data where Country = '" + source_country + "'"

        my_return = psql.sqldf(sql)

        return my_return
    
    def get_gdp_data_compare(self,source_country,target_country):

        global ALL_COUNTRIES_GDP_DATA

        my_data = ALL_COUNTRIES_GDP_DATA

        sql = "SELECT * FROM my_data WHERE Country = '" +  source_country + "' or Country = '" + target_country + "' "

        my_return = psql.sqldf(sql)

        return my_return

    def get_eu_gdp_data_growth_rate(self,source_country):
        #eu or #nafta
        global ALL_COUNTRIES_GDP_DATA
        
        my_data_frame=ALL_COUNTRIES_GDP_DATA

        eu_countries=['Austria','Belgium','Croatia','Czech Republic','Denmark','Finland','France','Germany','Greece','Hungary',
        'Italy','Netherlands','Poland','Portugal','Spain','Sweden','United Kingdom']
        eu_countries=pd.DataFrame(eu_countries)
        eu_countries.columns=['Country']
        eu_top_20=['France','Germany','Italy','Spain','United Kingdom','Netherlands']
        eu_top_20=pd.DataFrame(eu_top_20)
        eu_top_20.columns=['Country']


        my_sql = '''
                select
                case 
                WHEN Country in (select distinct Country from eu_top_20) then 'Top 20 EU'
                WHEN Country in (select distinct Country from eu_countries) then 'Non Top 20 EU'
                WHEN Country not in (select distinct Country from eu_countries) then [Country]
                ELSE 'Other' END [Continental],
                [Year],
                avg([GDP Pct Growth]) [GDP Pct Growth]
                from my_data_frame
                where Continental in ('China','Top 20 EU','Non Top 20 EU','United States')
                group by [Continental],[Year]
                
                UNION
                
                select
                Country as [Continental],
                [Year],
                avg([GDP Pct Growth]) [GDP Pct Growth]
                from my_data_frame
                where Country='Denmark'
                --Country ==source country
                group by [Continental],[Year]
                '''

        my_return_data = psql.sqldf(my_sql)
        
        return my_return_data
    
    def get_nafta_gdp_data_growth_rate(self):
        global ALL_COUNTRIES_GDP_DATA
        
        my_data_frame=ALL_COUNTRIES_GDP_DATA

        eu_countries=['Austria','Belgium','Croatia','Czech Republic','Denmark','Finland','France','Germany','Greece','Hungary',
        'Italy','Netherlands','Poland','Portugal','Spain','Sweden','United Kingdom']
        eu_countries=pd.DataFrame(eu_countries)
        eu_countries.columns=['Country']

        nafta_countries=['United States','Mexico','Canada']
        nafta_countries=pd.DataFrame(nafta_countries)
        nafta_countries.columns=['Country']
        nafta_countries

        my_sql = '''
                select
                case 
                WHEN Country in (select distinct Country from nafta_countries) then 'NAFTA'
                WHEN Country in (select distinct Country from eu_countries) then 'European Union'
                WHEN Country in ('China') then [Country]
                ELSE 'Other' END [Continental],
                [Year],
                avg([GDP Pct Growth]) [GDP Pct Growth]
                from my_data_frame
                where Continental in ('NAFTA')
                group by [Continental],[Year]
                
                UNION
                
                select
                Country as [Continental],
                [Year],
                [GDP Pct Growth] [GDP Pct Growth]
                from my_data_frame
                where Continental in ('United States','Mexico','Canada')
                group by [Continental],[Year]
                '''

        my_return_data = psql.sqldf(my_sql)
        return my_return_data

    def get_gdp_all_data(self):

        global ALL_COUNTRIES_GDP_DATA

        my_data = ALL_COUNTRIES_GDP_DATA

        sql = "SELECT * FROM my_data"

        my_return = psql.sqldf(sql)

        return my_return

    def get_gdp_all_data_2(self):

        global ALL_COUNTRIES_GDP_DATA

        my_data=pd.read_csv('data/trade_balance_datasets/wb_econind_gdp_data_2.csv')

        sql = "SELECT * FROM my_data"

        my_return = psql.sqldf(sql)   

        return my_return

    def get_trade_region_map_data(self):

        top_20_trading_nations = self.get_distinct_country_list(as_data_frame=True)

        nafta_countries=['United States','Mexico','Canada']
        nafta_countries=pd.DataFrame(nafta_countries)
        nafta_countries.columns=['Country']
        nafta_countries
        
        eu_countries=['Austria','Belgium','Croatia','Czech Republic','Denmark','Finland','France','Germany','Greece','Hungary',
        'Italy','Netherlands','Poland','Portugal','Spain','Sweden','United Kingdom']
        eu_countries=pd.DataFrame(eu_countries)
        eu_countries.columns=['Country']
        eu_top_20=['France','Germany','Italy','Spain','United Kingdom','Netherlands']
        eu_top_20=pd.DataFrame(eu_top_20)
        eu_top_20.columns=['Country']

        global ALL_COUNTRIES_GDP_DATA

        my_data = ALL_COUNTRIES_GDP_DATA

        sql = '''
        SELECT 
        Country,
        Year,
        [GDP per capita],
        [Population],
        [GDP],
        [GDP $B],
        case
        WHEN Country in (select distinct Country from eu_countries) then 'European Union'
        WHEN Country in (select distinct Country from nafta_countries) then 'NAFTA'
        WHEN Country in ('China') then [Country]
        ELSE 'Other'
        END [Trade Group Map],
        case
        WHEN Country in (select distinct Country from top_20_trading_nations) then 'Top 20'
        WHEN Country in (select distinct Country from top_20_trading_nations) then 'Non Top 20'
        END [Top 20]
        FROM my_data
        where (Country in (select distinct Country from eu_countries)
        or Country in (select distinct Country from nafta_countries)
        or Country in ('China'))
        and Year==2020
        '''

        my_return = psql.sqldf(sql)

        return my_return

    def get_Chinadata_by_country(self):

        global ALL_COUNTRIES_DATA_FRAME
        global ALL_COUNTRIES_GDP_DATA

        trade_data = ALL_COUNTRIES_DATA_FRAME
        gdp_df = ALL_COUNTRIES_GDP_DATA

        country_sql = "SELECT DISTINCT country FROM trade_data"
        
        country_set = psql.sqldf(country_sql)['country'].values.tolist()

        my_sql = '''
        SELECT
            gdp_data.*,
            trade_subset.*
        FROM (
            SELECT 
                Country,
                Year,
                [GDP Growth Pct],
                [Trade Pct GDP],
                [Trade Pct GDP] - LAG([Trade Pct GDP], 1) OVER (
                PARTITION BY country ORDER BY year) AS TradePctGDPChange
            FROM gdp_df
        ) gdp_data
        LEFT JOIN (
            SELECT *,
                total_trade / total_toWorld_trade - 
                LAG(total_trade / total_toWorld_trade, 1) OVER (
                PARTITION BY country ORDER BY year) AS china_target_pct_chg

            FROM (
                SELECT *,
                    SUM(total_trade) OVER (PARTITION BY country, year) as total_toWorld_trade,
                    SUM(exports) OVER (PARTITION BY country, year) as total_toWorld_exports,
                    SUM(imports) OVER (PARTITION BY country, year) as total_toWorld_imports,
                    SUM(net_exports) OVER (PARTITION BY country, year) as total_toWorld_net_exports
                FROM (
                    SELECT
                        country,
                        year,
                        SUM([Total Trade ($M)]) as total_trade,
                        SUM([Exports ($M)]) as exports,
                        SUM([Net Exports ($M)]) as net_exports,
                        SUM([Imports ($M)]) as imports,
                        CASE
                            WHEN [Trading Partner] = "China" THEN "Trades with China"
                            ELSE "Trades with Others"
                        END as isChinaPartner
                    FROM trade_data
                    GROUP BY isChinaPartner, country, year) t
                ) s
        ) AS trade_subset
        ON (gdp_data.Country = trade_subset.country
            and gdp_data.Year = trade_subset.year)
        WHERE gdp_data.Country in (''' +  str(country_set)[1:-1] + ''')
        '''
        my_return_data = psql.sqldf(my_sql)

        return my_return_data

    #am here
    def get_nafta_by_country(self):

        global ALL_COUNTRIES_DATA_FRAME
        global ALL_COUNTRIES_GDP_DATA

        trade_data = ALL_COUNTRIES_DATA_FRAME
        gdp_df = ALL_COUNTRIES_GDP_DATA

        country_sql = "SELECT DISTINCT country FROM trade_data where ltrim(rtrim(country)) not in ('United States','Canada','Mexico')"
        
        country_set = psql.sqldf(country_sql)['country'].values.tolist()

        my_sql = '''
        SELECT
            gdp_data.*,
            trade_subset.*
        FROM (
            SELECT 
                Country,
                Year,
                [GDP Growth Pct],
                [Trade Pct GDP],
                [Trade Pct GDP] - LAG([Trade Pct GDP], 1) OVER (
                PARTITION BY country ORDER BY year) AS TradePctGDPChange
            FROM gdp_df
        ) gdp_data
        LEFT JOIN (
            SELECT *,
                total_trade / total_toWorld_trade - 
                LAG(total_trade / total_toWorld_trade, 1) OVER (
                PARTITION BY country ORDER BY year) AS china_target_pct_chg

            FROM (
                SELECT *,
                    SUM(total_trade) OVER (PARTITION BY country, year) as total_toWorld_trade,
                    SUM(exports) OVER (PARTITION BY country, year) as total_toWorld_exports,
                    SUM(imports) OVER (PARTITION BY country, year) as total_toWorld_imports,
                    SUM(net_exports) OVER (PARTITION BY country, year) as total_toWorld_net_exports
                FROM (
                    SELECT
                        country,
                        year,
                        SUM([Total Trade ($M)]) as total_trade,
                        SUM([Exports ($M)]) as exports,
                        SUM([Net Exports ($M)]) as net_exports,
                        SUM([Imports ($M)]) as imports,
                        CASE
                            WHEN [Trading Partner] in ("United States", "Mexico", "Canada") THEN "Trades with NAFTA"
                            ELSE "Trades with Others"
                        END as isChinaPartner
                    FROM trade_data
                    GROUP BY isChinaPartner, country, year) t
                ) s
        ) AS trade_subset
        ON (gdp_data.Country = trade_subset.country
            and gdp_data.Year = trade_subset.year)
        WHERE gdp_data.Country in (''' +  str(country_set)[1:-1] + ''')
        '''
        my_return_data = psql.sqldf(my_sql)

        return my_return_data



    def get_EUdata_by_country(self):

        global ALL_COUNTRIES_DATA_FRAME
        global ALL_COUNTRIES_GDP_DATA

        trade_data = ALL_COUNTRIES_DATA_FRAME
        gdp_df = ALL_COUNTRIES_GDP_DATA

        country_sql = "SELECT DISTINCT country FROM trade_data"
        
        country_set = psql.sqldf(country_sql)['country'].values.tolist()

        my_sql = '''
        SELECT
            gdp_data.*,
            trade_subset.*
        FROM (
            SELECT 
                Country,
                Year,
                [GDP Growth Pct],
                [Trade Pct GDP],
                [Trade Pct GDP] - LAG([Trade Pct GDP], 1) OVER (
                PARTITION BY country ORDER BY year) AS TradePctGDPChange
            FROM gdp_df
        ) gdp_data
        LEFT JOIN (
            SELECT *,
                total_trade / total_toWorld_trade - 
                LAG(total_trade / total_toWorld_trade, 1) OVER (
                PARTITION BY country ORDER BY year) AS eu_target_pct_chg

            FROM (
                SELECT *,
                    SUM(total_trade) OVER (PARTITION BY country, year) as total_toWorld_trade,
                    SUM(exports) OVER (PARTITION BY country, year) as total_toWorld_exports,
                    SUM(imports) OVER (PARTITION BY country, year) as total_toWorld_imports,
                    SUM(net_exports) OVER (PARTITION BY country, year) as total_toWorld_net_exports
                FROM (
                    SELECT
                        country,
                        year,
                        SUM([Total Trade ($M)]) as total_trade,
                        SUM([Exports ($M)]) as exports,
                        SUM([Net Exports ($M)]) as net_exports,
                        SUM([Imports ($M)]) as imports,
                        CASE
                            WHEN [Trading Partner] = "European Union" THEN "Trades with EU"
                            WHEN [Trading Partner] not in ("European Union","Austria","Belgium","Croatia","Czech Republic","Denmark","Finland","France","Germany","Greece","Hungary","Italy","Netherlands","Poland","Portugal","Spain","Sweden","United Kingdom") THEN "Trades with Others"
                        END as isEuPartner
                    FROM trade_data
                    GROUP BY isEuPartner, country, year) t
                ) s
        ) AS trade_subset
        ON (gdp_data.Country = trade_subset.country
            and gdp_data.Year = trade_subset.year)
        WHERE gdp_data.Country in (''' +  str(country_set)[1:-1] + ''')
        '''
        my_return_data = psql.sqldf(my_sql)

        return my_return_data



    def get_top_20_gdp_data_for_map(self):
        country_source = self.get_world_countries_by_iso_label()
        country_source.loc[84,'Country'] = 'South Korea'
        country_source = country_source.drop(4)

        all_gdp=self.get_gdp_all_data()
        year2020 = psql.sqldf("select * from all_gdp where Year = 2020") #all_gdp[all_gdp['Year'] == 2020]

        #We are not dealing with top 20 GDP, we're dealing with top 20 nations.
        top_20_trading_nations = self.get_distinct_country_list(as_data_frame=True)
        sql = '''
            select 
                distinct
                year2020.Country as Country,
                year2020.GDP as GDP
            from year2020
            join top_20_trading_nations
                on 
                top_20_trading_nations.Country = year2020.Country

        '''
        return psql.sqldf(sql)



    #def get_gdp_data_by_country(self):

    #    global ALL_COUNTRIES_GDP_DATA

    #    trade_data = get_Chinadata_by_country()

    #    gdp_data = ALL_COUNTRIES_GDP_DATA

    #    sql = '''
    #    SELECT
    #        gdp_data.Country,
    #        gdp_data.Year,
    #        gdp_data.[GDP Growth Pct],
    #        gdp_data.[Trade Pct GDP],
    #        trade_subset.isChinaPartner,
    #        trade_subset.Total
    #        trade_subset.total_toWorld_trade,
    #        trade_subset.total_toWorld_exports,
    #        trade_subset.total_toWorld_imports,
    #        trade_subset.total_toWorld_net_exports,
    #        trade_subset.total_toWorld_net_exports,
    #    FROM gdp_data
    #    LEFT JOIN (

    #    ) AS trade_subset
    #    ON (gdp_data.Country = trade_subset.country
    #        and gdp_data.Year = trade_subset.year)
    #    '''

    #    my_return = psql.sqldf(sql)

    #    return my_return

    def get_top20_2020_gdp(self):

        global ALL_COUNTRIES_DATA_FRAME
        global ALL_COUNTRIES_GDP_DATA

        trade_data = ALL_COUNTRIES_DATA_FRAME
        gdp_df = ALL_COUNTRIES_GDP_DATA

        country_sql = "SELECT DISTINCT country FROM trade_data"
        
        country_set = psql.sqldf(country_sql)['country'].values.tolist()

        my_sql = '''
        SELECT
            Country,
            [GDP Pct Growth],
            [Inflation, consumer prices],
            [Trade Total Change %]
        FROM gdp_df
        WHERE Year = 2020 and Country in (''' +  str(country_set)[1:-1] + ''')
        '''
        my_return_data = psql.sqldf(my_sql)
        return my_return_data

    
    def imports_exports_GDP_by_sectors(self,source_country, target_country):
        global ALL_COUNTRIES_BY_TYPE_DF
        global ALL_COUNTRIES_GDP_DATA

        df_by_type = ALL_COUNTRIES_BY_TYPE_DF
        df_gdp = ALL_COUNTRIES_GDP_DATA

        my_sql = '''
        SELECT
            Year, Country, sector,
            export_to_GDP_ratio - LAG(export_to_GDP_ratio, 1) OVER (
            PARTITION BY Country, sector ORDER BY Year) as yoy_export_GDP_change
        FROM (
            SELECT
                df_sector_country.Year,
                df_gdp.Country,
                df_sector_country.Value / df_gdp.GDP *1000000 AS export_to_GDP_ratio,
                [Product/Sector-reformatted] AS sector

            FROM (
                SELECT 
                    Year, Value,
                    [Product/Sector-reformatted],
                    [Reporting Economy]
                FROM df_by_type
                WHERE      
                    ([Reporting Economy] =  \'''' + source_country + '''\'
                    or
                    [Reporting Economy] =  \'''' + target_country + '''\'
                    )
                and
                    Direction = 'exports'
                and
                    [Product/Sector-reformatted] NOT LIKE '%Total%'
             ) AS df_sector_country
            INNER JOIN df_gdp
            ON df_sector_country.Year = df_gdp.Year AND df_gdp.Country = df_sector_country.[Reporting Economy]
        )
        '''
        my_return_data = psql.sqldf(my_sql)
        return my_return_data