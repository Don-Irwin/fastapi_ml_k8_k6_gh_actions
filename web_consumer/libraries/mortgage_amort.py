from  libraries.AmortaPy.AmortaPy.core import _amortization  as ap
import os
import sys
import json
from datetime import datetime
from os import system, name
from time import sleep
import time
import copy
import threading
import imp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandasql as psql
import scipy.stats as st
import seaborn as sns
import glob
import string
import shutil
from  libraries.utility import Utility
import altair as alt
#from  utility import Utility
import pandas as pd


class Affordability(Utility):
    
    def __init__(self):
        super().__init__()

    def print_internal_directory(self):

        for k,v in self.__dict__.items():
            print("{} is \"{}\"".format(k,v)) 

    # Simple brute force mortgage allocation change. 
    def how_much_can_i_afford(self,monthly_allocation, interest_rate = 0.065, 
    repayment_freq = 12, down_payment_pct = 0.2, input_years = 30,
    input_loan = 500000,print_output=False,do_altair=True,recursive_call=False):


        loan_amt = input_loan - (input_loan * down_payment_pct)
        period_int_rate = interest_rate/repayment_freq
        periods = input_years * repayment_freq

        df = ap.generate_amortization_table(period_int_rate, loan_amt, periods)
        period_payment = df["period_payment"][0]
        amortization_schedule = df
        while period_payment > monthly_allocation:
            #print("monthly_allocation = ", monthly_allocation)
            #print("period_payment = ", period_payment)
            multiplier_ratio = period_payment/monthly_allocation
            input_loan = input_loan - 4000*multiplier_ratio
            #print("loan changes",input_loan)
            down_payment_amount = (input_loan * down_payment_pct)
            loan_amt = input_loan - down_payment_amount
            df = ap.generate_amortization_table(period_int_rate, loan_amt, periods)
            amortization_schedule = df
            period_payment = df["period_payment"][0]
            
            #print(period_payment)

        while period_payment < monthly_allocation:
            #print("monthly_allocation = ", monthly_allocation)
            #print("period_payment = ", period_payment)
            multiplier_ratio = monthly_allocation/period_payment
            input_loan = input_loan + 4000*multiplier_ratio
            #print("loan changes",input_loan)
            down_payment_amount = (input_loan * down_payment_pct)
            loan_amt = input_loan - down_payment_amount
            df = ap.generate_amortization_table(period_int_rate, loan_amt, periods)
            amortization_schedule = df
            period_payment = df["period_payment"][0]
            #print(period_payment)

        input_loan = round(input_loan)

        #print(amortization_schedule)

        output_string =  "With a monthly allocation of: $ {} ,".format(monthly_allocation) + "\r\n"
        output_string = output_string + "at an interest rate of {} % ,".format(interest_rate*100) + "\r\n"
        output_string = output_string + "and a down payment of {} %, or $ {} ,".format(down_payment_pct*100, down_payment_amount)  + "\r\n"
        output_string = output_string + "and a loan term of {} years; ".format(input_years)  + "\r\n"
        output_string = output_string + "You can afford a property priced $ {} .".format(input_loan) + "\r\n"
        if print_output:
            print(output_string)

        altair_object = None
        if do_altair:
            altair_object = self.create_altair_bar_graph(monthly_allocation,down_payment_amount,loan_amt,input_loan,input_years,interest_rate)
        line_graph = None
        if not recursive_call:
            line_graph = self.generate_steps_up_and_down_data(monthly_allocation=monthly_allocation, interest_rate = interest_rate, 
            repayment_freq = repayment_freq, down_payment_pct = down_payment_pct, 
            input_years = input_years, house_price = input_loan,print_output=print_output)

        return altair_object, line_graph, loan_amt, monthly_allocation, input_loan, down_payment_amount, down_payment_pct, interest_rate , amortization_schedule, output_string

    def generate_steps_up_and_down_data(self,monthly_allocation, interest_rate = 0.065, 
    repayment_freq = 12, down_payment_pct = 0.2, input_years = 30,house_price = 50000,print_output=False):
        
        list_of_interest_rates = self.get_five_points_each_way(interest_rate=interest_rate)
        if print_output:
            print(list_of_interest_rates)

        my_counter = 0
        output_df = None
        afford_list = []
        ir_list = []
        my_location = 0
        my_location1 = 0
        for ir in list_of_interest_rates:
            returner = self.how_much_can_i_afford(monthly_allocation=monthly_allocation, interest_rate = ir, 
            repayment_freq = repayment_freq, down_payment_pct = down_payment_pct, 
            input_years = input_years, input_loan = house_price,print_output=print_output,recursive_call=True)

            property_price = returner[4]
            afford_list.append(property_price)
            ir_list.append(ir*100)
            if ir == interest_rate:
                my_location=my_counter
            if property_price == house_price:
                my_location1=my_counter

            #findf = pd.DataFrame(data)
            my_counter = my_counter + 1    

        print("my_location=",ir_list[my_location])
        print("my_location=",afford_list[my_location])

        data = {"Interest Rate": ir_list,
        "What I Can Afford": afford_list}
        output_df = pd.DataFrame(data)
        print(output_df.head(2))
        print("*"*40)
        print(output_df.iloc[my_location:(my_location+1)])
        #print(output_df)
        create_line_graph = self.create_line_graph(output_df,monthly_allocation,my_location)
        #print(output_df)
        return create_line_graph


    def create_line_graph(self,df,monthly_allocation,my_location):

        mad = "${:,} ".format(monthly_allocation) 
        title2 = "What {} monthly buys at various intrest rates".format(mad)

        base = alt.Chart(df)
        line = base.mark_line().encode(
            x=alt.X('Interest Rate',axis=alt.Axis(title='Interest Rate')),
            y=alt.Y('What I Can Afford',axis=alt.Axis(title='What I Can Afford (USD):')),
            strokeWidth = alt.value(3)
            
        )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Interest Rate:Q',axis=alt.Axis(title='')),
            y=alt.Y('What I Can Afford:Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip("Interest Rate"),
                     alt.Tooltip("What I Can Afford",format="$,.0f" )]
        )

        callout = alt.Chart(df.iloc[my_location:(my_location+1)]).mark_point(
            color='red', size=500, tooltip="What I can Afford",opacity=1
                ).encode(
            x=alt.X('Interest Rate',axis=alt.Axis(title='')),
            y=alt.Y('What I Can Afford:Q',axis=alt.Axis(title='')),
                        tooltip=[
                            alt.Tooltip("Interest Rate"),
                            alt.Tooltip("What I Can Afford",format="$,.0f" )]
                )      
        #return_chart = alt.layer(line,points)
        return_chart = alt.layer(line,points,callout).properties(
            width=380,
            height=200,
            title=title2
        )
        return return_chart

        return return_chart



        

    def create_altair_bar_graph(self,monthly_allocation,down_payment_amount,loan_amt,home_price,loan_term,interest_rate):
        #create the title
        #monthly allocation dollars -- mad
        mad = "${:,} ".format(monthly_allocation) 

        #interest rate
        int_r = " {} % ".format(round(interest_rate*100, 2))
        
        #hp -- home price
        hp = "${:,} ".format(round(home_price,0))

        #dp
        dp = "${:,} ".format(round(down_payment_amount,2)).replace(".0","")

        title1 = "You can afford a house priced {}.".format(hp)
        title2 = "Your monthly housing budget of {} affords you a home priced {} ,".format(mad,hp)
        title3 = "given a {} interest rate, on a {} year mortgage, and a downpayment of {}.".format(int_r,loan_term,dp)

        #my_title = [title1,title2,title3]
        my_title = [title2,title3]


        data = {'Component': ["Monthly Pmt","Down Pmt","Loan Amt","Home Price"],
            'Value': [monthly_allocation,down_payment_amount,loan_amt,home_price]
        }
        findf = pd.DataFrame(data)

        hist = alt.Chart(findf).mark_bar().encode(x=alt.X('Component:N',axis=alt.Axis(title='Home Cost Component',labelAngle=-0), sort='y'),
                                                y=alt.Y('Value:Q',axis=alt.Axis(title='Dollar Amount')),
                                                tooltip=[alt.Tooltip('Component:N'),alt.Tooltip('Value:N',format="$,.0f"),],)

        return_chart = alt.layer(hist).properties(
            width=500,
            height=350,
            title=my_title
        )
        return return_chart


    def get_five_points_each_way(self,interest_rate):
            #go up three percentage points and go down three percentage points.
            lower_list = []
            upper_list = []
            upper_number = interest_rate + 0.05
            lower_number = interest_rate - 0.05
            working_number = interest_rate

            while working_number < upper_number:
                working_number = working_number + 0.0025
                upper_list.append(round(working_number,4))

            working_number = interest_rate

            while working_number > lower_number and (working_number - 0.00259) > 0:
                working_number = working_number - 0.0025
                lower_list.append(round(working_number,4))

            final_list = []
            for num in sorted(lower_list):
                final_list.append(num)
            final_list.append(interest_rate)

            for num in sorted(upper_list):
                final_list.append(num)
            
            return final_list


