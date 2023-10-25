from libraries.import_export_data_objects import import_export_data as Import_Export_Data
from libraries.utility import Utility
import numpy as np

import altair as alt
from vega_datasets import data
import os
import pandas as pd
import pandasql as psql
import math


class AltairRenderings:


    def __init__(self,load_data_from_url=False):
        if load_data_from_url == True:
            self.my_data_object = Import_Export_Data()
        else:
            self.my_data_object = Import_Export_Data(load_data_from_url=load_data_from_url)

    def get_altaire_line_char_json_county_trade(self,source_country,target_country):

        my_data = self.my_data_object

        title = "Trade between " + source_country + " and " + target_country + " for the years 2014 through 2020"

        source_and_target_data = my_data.get_data_by_source_and_target_country(source_country,target_country)

        base = alt.Chart(source_and_target_data).transform_fold(['Total Trade ($M)','Exports ($M)','Imports ($M)'])

        line = base.mark_line().encode(
            x=alt.X('year:O',axis=alt.Axis(title='Year')),
            y=alt.Y('value:Q',axis=alt.Axis(title='Total Trade In Millions of USD:')),
            color="key:N",
            strokeWidth = alt.value(2)
        ).properties(
            width=700,
            height=350,
            title=title
            )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('year:O',axis=alt.Axis(title='')),
            y=alt.Y('value:Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip("Total Trade ($M)",format="$,.0f"),
                     alt.Tooltip("Exports ($M)",format="$,.0f" ),
                     alt.Tooltip("Imports ($M)",format="$,.0f")]
        ).properties(width=700)

        
        return_chart = alt.layer(line,points)
        return return_chart

    def get_altaire_line_chart_county_trade_for_matrix(self,source_country,target_country,width=340,height=200):

        my_data = self.my_data_object

        title = "Trade between " + source_country + " and " + target_country + " 2014 - 2020"

        source_and_target_data = my_data.get_data_by_source_and_target_country(source_country,target_country)

        base = alt.Chart(source_and_target_data).transform_fold(['Total Trade ($M)','Exports ($M)','Imports ($M)'])

        line = base.mark_line().encode(
            x=alt.X('year:O',axis=alt.Axis(title='Year')),
            y=alt.Y('value:Q',axis=alt.Axis(title='Total Trade In Millions of USD:')),
            color=alt.Color(field="key", type="nominal",
                            scale = alt.Scale(range = ['#265499', '#A8DDA4', '#EEBC59']),
                            legend = alt.Legend(title="Key")),
            strokeWidth = alt.value(3)

            
        ).properties(
            width=width,
            height=height,
            title=title
            )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('year:O',axis=alt.Axis(title='')),
            y=alt.Y('value:Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip("Total Trade ($M)",format="$,.0f"),
                     alt.Tooltip("Exports ($M)",format="$,.0f" ),
                     alt.Tooltip("Imports ($M)",format="$,.0f")]
        ).properties(width=width)

        
        return_chart = alt.layer(line,points)
        return return_chart

    def get_altaire_bar_top5_partners_for_matrix(self,source_country,width=320,height=130):

        my_data = self.my_data_object

        title = source_country + "'s Top 5 Trading Partners"


        source_data = my_data.get_top5data_by_source_country(source_country)

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        base = alt.Chart(source_data)

        bars = base.mark_bar(color = '#9CBAD5').encode(
            x=alt.X('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            y=alt.Y('Trading Partner:N',axis=alt.Axis(title='Trading Partner'), sort='-x'),
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        )

        text = base.mark_text(align='left', dx=5, dy=-5).encode(
            x=alt.X('Total Trade ($M):Q'),
            y=alt.Y('Trading Partner:N', sort='-x',axis=None),
            text=alt.Text('Total Trade ($M):Q', format='$,.0f')
        )

        return_chart = alt.layer(bars, text).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).resolve_scale(
            y = 'independent'
        ).properties(
            title=title,
            width=width,
            height=height
        )
        return return_chart


    def get_altaire_bar_top5_partners(self,source_country):

        my_data = self.my_data_object

        title = source_country + "'s Top 5 Trading Partners by Total Trade Values ($M in USD)"

        source_data = my_data.get_top5data_by_source_country(source_country)

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        base = alt.Chart(source_data)

        bars = base.mark_bar(color = '#aec7e8').encode(
            x=alt.X('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            y=alt.Y('Trading Partner:N',axis=alt.Axis(title='Trading Partner'), sort='-x'),
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        )

        text = base.mark_text(align='left', dx=5, dy=-5).encode(
            x=alt.X('Total Trade ($M):Q'),
            y=alt.Y('Trading Partner:N', sort='-x',axis=None),
            text=alt.Text('Total Trade ($M):Q', format='$,.0f')
        )

        return_chart = alt.layer(bars, text).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).resolve_scale(
            y = 'independent'
        ).configure_axis(
            grid=False
        ).configure_view(
            strokeWidth=0
        ).properties(
            width=700,
            height=350,
            title=title
        )
        return return_chart



    def get_import_export_balance_top_five(self,source_country,year=None,for_matrix=False,height=200,width=300):

        my_data = self.my_data_object

        title = source_country + "'s Imports, Exports, and Net Trade"
        if source_country.lower() == "world":
            source_country = "world"

        source_data = my_data.get_top_trading_and_net_value(source_country)

        if year is not None:
            sql = "select '$' || printf(\"%,d\",cast(sum(net_trade) as text)) as total_net_trade from source_data where year = '" + str(year) + "'"
            my_result= psql.sqldf(sql)
            total_net_trade=my_result["total_net_trade"][0]
            title += ", Net Trade: "+ total_net_trade +" for Year: " + str(year)
            sql = "select * from source_data where year = '" + str(year) + "'"
            source_data = psql.sqldf(sql)


        # A slider filter
        if year is None:
            year_slider = alt.binding_range(min=2014, max=2020, step=1)
            slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        base = alt.Chart(source_data).transform_fold(
                                                    ["Exports ($M)","Imports ($M)"],
                                                    as_ = ['column','value']
                                                    )

        bars = base.mark_bar(opacity=0.6).encode(
            y=alt.Y('value:Q',axis=alt.Axis(title='Total Trade ($M)')),
            x=alt.X('Trading Partner',  sort=alt.SortField('value', order='descending')),
            tooltip=[alt.Tooltip("Total Trade ($M)",format="$,.0f"),alt.Tooltip("net_trade",format="$,.0f", title="Net Trade"),alt.Tooltip("Exports ($M)",format="$,.0f" ),alt.Tooltip("Imports ($M)",format="$,.0f"),alt.Tooltip("Imports ($M)",format="$,.0f")],
            color=alt.Color(field="column", type="nominal",
                            scale = alt.Scale(range = ['#265499', '#A8DDA4']),
                            legend = alt.Legend(title="column"))

        )
        
        line = bars.mark_line(color='#5E5EFF').encode(
            x=alt.X('Trading Partner'),
            y=alt.Y('net_trade:Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip("Total Trade ($M)",format="$,.0f"),alt.Tooltip("net_trade",format="$,.0f", title="Net Trade"),alt.Tooltip("Exports ($M)",format="$,.0f" ),alt.Tooltip("Imports ($M)",format="$,.0f"),alt.Tooltip("Imports ($M)",format="$,.0f")],
            color=alt.Color(scale = alt.Scale(range = ['#5E5EFF']))               
        )
 

        invisible_dots = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Trading Partner'),
            y=alt.Y('net_trade:Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip("Total Trade ($M)",format="$,.0f"),alt.Tooltip("net_trade",format="$,.0f", title="Net Trade"),alt.Tooltip("Exports ($M)",format="$,.0f" ),alt.Tooltip("Imports ($M)",format="$,.0f"),alt.Tooltip("Imports ($M)",format="$,.0f")]
        )

        visible_dots = base.mark_circle(
            color='#5E5EFF',#'#EEBC59'
            opacity=1.0,
            size=60
        ).encode(
            x=alt.X('Trading Partner'),
            y=alt.Y('net_trade:Q',axis=alt.Axis(title=''))
        )

        line_text = base.mark_text(
            color="black",
            opacity=1,
            fontSize=13,
            dy=-14
        ).encode(
            x=alt.X('Trading Partner'),
            y=alt.Y('net_trade:Q',axis=alt.Axis(title='')),
            text=alt.Text('net_trade_text')
        )

        if for_matrix==False:
            return  alt.layer(bars + invisible_dots+line+line_text+visible_dots).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).resolve_scale(
                y = 'independent'
            ).configure_axis(
                grid=False
            ).configure_view(
                strokeWidth=0
            ).properties(
                width=700,
                height=350,
                title=title
            )
        else:

            return  alt.layer(bars + invisible_dots+line+line_text+visible_dots).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).resolve_scale(
                y = 'independent'
            ).properties(
                width=width,
                height=height,
                title=title
            )


    def get_altaire_dual_axis_bar_top5(self,source_country):

        my_data = self.my_data_object

        title = "Top 5 Trading Product Types by Values ($M in USD)"

        exports_data = my_data.get_top5data_by_imports_exports(source_country, 'exports')
        exports_data['Value'] = exports_data['Value'] * -1.0
        exports_data = exports_data.rename(columns={'Value': 'Export_Value', 'Product/Sector-reformatted': 'Export_Product'})
        imports_data = my_data.get_top5data_by_imports_exports(source_country, 'imports')
        imports_data = imports_data.rename(columns={'Value': 'Import_Value', 'Product/Sector-reformatted': 'Import_Product'})
        df = pd.merge(exports_data, imports_data, 
                      how = 'inner', on = ['rnk', 'Year'], 
                     left_index = False, right_index = False)
        domain_x = max(max(abs(df['Export_Value'])), max(df['Import_Value']))
        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        base = alt.Chart(df).encode(x='Export_Value:Q')

        export_bars = base.mark_bar(color = '#aec7e8').encode(
            x=alt.X('Export_Value:Q',axis=alt.Axis(title='Trade Value ($M in USD)'), scale=alt.Scale(domain=[-domain_x,domain_x])),
        
            y=alt.Y('Export_Product:N',axis=alt.Axis(title='Export Product'), sort='x'),
            tooltip=alt.Tooltip('Export_Value', format="$,.0f")
        )
        import_bars = base.mark_bar(color = '#e7969c').encode( 
            x=alt.X('Import_Value:Q',axis=alt.Axis(title='Trade Value ($M in USD)'), scale=alt.Scale(domain=[-domain_x,domain_x])),
            y=alt.Y('Import_Product:N',axis=alt.Axis(title='Import Product'), sort='-x'),
            tooltip=alt.Tooltip('Import_Value', format="$,.0f")
        )

        text_import = base.mark_text(align='left', dx=5, dy=-5).encode(
            x=alt.X('Import_Value:Q'),
            y=alt.Y('Import_Product:N', sort='-x', axis=None),
            text=alt.Text('Import_Value:Q', format='$,.0f')
        )
        text_export = base.mark_text(align='right', dx=-5, dy=-5).encode(
            x=alt.X('Export_Value:Q'),
            y=alt.Y('Export_Product:N', sort='x', axis=None),
            text=alt.Text('Export_Value:Q', format='$,.0f')
        )

        return_chart = alt.layer(export_bars, import_bars, text_export, text_import).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).resolve_scale(
            y = 'independent'
        ).configure_axis(
            grid=False
        ).configure_view(
            strokeWidth=0
        ).properties(
            width=700,
            height=350,
            title=title
        )
        return return_chart

    def get_altaire_dual_pie_chart_by_types(self,source_country,target_country, direction):

        my_data = self.my_data_object
        title = source_country + " vs. "+ target_country + " Trade Type Distribution"
        
        df = my_data.imports_exports_by_sectors(source_country, target_country, direction)
        country_data = df.rename(columns={'Product/Sector-reformatted': 'Product_Type'})
        #source_country_data = df[df['Reporting Economy']==source_country].rename(
        #    columns={'Product/Sector-reformatted': 'Product_Type'})
        #target_country_data = df[df['Reporting Economy']==target_country].rename(
        #    columns={'Product/Sector-reformatted': 'Product_Type'})

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        # radio button for export/import option
        #direction = ["exports", "imports"]
        #direction_radio = alt.binding_radio(options=direction)

        #direction_select = alt.selection_single(fields=['Direction'], bind=direction_radio, name="Direction", init = {'Direction': 'exports'})


        base = alt.Chart(country_data).encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color(field="Product_Type", type="nominal", scale=alt.Scale(scheme='tableau20')),
            tooltip=alt.Tooltip('Product_Type')
        )

        source_pie_chart = base.transform_filter(
            alt.FieldEqualPredicate(field='Reporting Economy', equal=source_country)
        ).mark_arc(outerRadius=120).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).properties(title=source_country)

        #source_pie_chart_direction = source_pie_chart.add_selection(
        #    direction_select
        #).transform_filter(
        #    direction_select
        #)
        base_target = alt.Chart(country_data).encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color(field="Product_Type", type="nominal"),
            tooltip=alt.Tooltip('Product_Type')
        ).transform_filter(
            alt.FieldEqualPredicate(field='Reporting Economy', equal=target_country)
        )

        target_pie_chart = base.mark_arc(outerRadius=120).transform_filter(
            alt.FieldEqualPredicate(field='Reporting Economy', equal=target_country)
        ).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).properties(title=target_country)

        return_chart = alt.hconcat(source_pie_chart, target_pie_chart)

        return return_chart

    def get_top_20_countries(self):

        return self.my_data_object.get_distinct_country_list()

    def get_world_map(self):

        world_map_source = alt.topo_feature(data.world_110m.url, 'countries')
        
        my_data = self.my_data_object

        country_source = my_data.get_world_countries_by_iso_label()
        country_source.loc[84,'Country'] = 'South Korea'
        country_source = country_source.drop(4)

        top20_2020 = my_data.get_top_20_gdp_data_for_map()
        country_gdp = pd.merge(country_source, top20_2020, on='Country', how = 'outer')
        country_gdp['GDP'] = country_gdp['GDP'].fillna(0)


        foreground = (
            alt.Chart(world_map_source)
            .mark_geoshape(stroke="black", strokeWidth=1)
            .encode(
                color = alt.condition('datum.GDP > 0', 
                                    alt.Color('GDP:Q',legend=alt.Legend(title="County GDP in $MM")),
                                    alt.value('#f3f3f3')),
                tooltip=[alt.Tooltip("Country:N", title="Country"),
                         alt.Tooltip("GDP:Q", title="GDP", format="$,.0f")]
            )
            .transform_lookup(
                lookup="id",
                from_=alt.LookupData(country_gdp, "id", ["Country",'GDP']),
            )
        )

        my_map = (
            (foreground)
            .configure_view(strokeWidth=0)
            .properties(width=900, height=550)
            .project("mercator", scale=185,center=np.array([24,12]))
        )
        #my_map = alt.concat(my_map,scale=160)
        
        utility = Utility()
        this_dir = utility.get_this_dir()
        file_name = os.path.join(this_dir,"libraries","world.json")
        my_json = utility.get_data_from_file(file_name)
        return my_json,my_map


    # def my_new_map(self):
    #     source = alt.topo_feature(data.world_110m.url, 'countries')
    #     my_map=alt.Chart(source).mark_geoshape(
    #     fill='blue',
    #     stroke='grey',).encode(tooltip='id:N').project('naturalEarth1').properties(width=800, height=600).configure_view(stroke=None)

    #     return my_map

    def my_new_map(self):
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        interested_countries = ['Australia','Brazil','Canada','China','France','Germany','India','Indonesia','Iran','Italy','Japan',
                       'Mexico','Netherlands','Russia','Saudi Arabia','South Korea','Spain','Switzerland','United Kingdom','United States of America']
        gdp = list(range(100,300,10))

        country_gdp = pd.DataFrame(
            {'name': interested_countries,
            'GDP': gdp
            })

        world_gdp = pd.merge(world, country_gdp, on='name', how = 'outer')
        world_gdp['GDP'] = world_gdp['GDP'].fillna(0)

        my_map = alt.Chart(world_gdp[world_gdp.continent!='Antarctica']).mark_geoshape(
                color = "#purpleblue"
            ).project(
            ).encode(
                color='GDP',
                tooltip='name' 
            ).properties(
                width=700,
                height=500
            )

        return my_map

    def get_time_series_gdp_chart_for_matrix(self,source_country,width=300,height=200):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_by_country(source_country)

        title = source_country + "'s GDP"

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data)

        line = base.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title="GDP $B",labelExpr='"$" + datum.value / 1E9 + "B"'))#,
            #color="Country:N"
            
        ).properties(
            width=width,
            height=height,
            title=title
            )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title='')),
            tooltip=['Country',
                     alt.Tooltip('GDP $B', format="$,.0f")]
        ).properties(width=width)

        
        return_chart = alt.layer(line,points).configure_axis(grid=False)
        return return_chart

    def get_lines_for_top5_countries(self,width=300,height=200):
        #time_s = self.get_altaire_line_chart_county_trade_for_matrix(source_country,"World",width=width,height=height)
        #get_import_export_balance_top_five(source_country,for_matrix=True,width=width,height=height)
        indo = self.get_import_export_balance_top_five("Indonesia",for_matrix=True,width=width,height=height)
        aus = self.get_import_export_balance_top_five("Australia",for_matrix=True,width=width,height=height)
        sk = self.get_import_export_balance_top_five("South Korea",for_matrix=True,width=width,height=height)
        jap = self.get_import_export_balance_top_five("Japan",for_matrix=True,width=width,height=height)

        space_data = pd.DataFrame({'a': list('CCCDDDEEE'),
                            'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})

        space_chart = alt.Chart(space_data).mark_point(opacity=0.0)   

        row_1  = (sk | jap )
        row_3  = (indo | aus )
        my_chart = (space_chart & row_1 & row_3).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                ).resolve_scale(color='independent')

        return my_chart


    def get_charts_for_click_from_world_map(self,source_country,width=300,height=200):
        top_5  = self.get_altaire_bar_top5_partners_for_matrix(source_country,width=width,height=height)
        trade  = self.get_import_export_balance_top_five(source_country,for_matrix=True,width=width,height=height)
        time_s = self.get_altaire_line_chart_county_trade_for_matrix(source_country,"World",width=width,height=height)
        #gdp = self.get_time_series_gdp_chart_for_matrix(source_country,width=width,height=height)
        gdp = self.get_time_series_gdp_trade_for_matrix(source_country,width=width,height=height)

        row_1 = (time_s | top_5).resolve_scale(
            color='independent')
        row_2 = (trade | gdp).resolve_scale(
            color='independent')


        my_chart = (row_1 & row_2 ).configure_axis(
        grid=False
        ).configure_view(
        strokeWidth=0
        )

        return my_chart

    def get_time_series_gdp_chart(self,source_country):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_by_country(source_country)

        title = "GDP " + source_country

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data)

        line = base.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title="GDP $B",labelExpr='"$" + datum.value / 1E9 + "B"'))#,
            #color="Country:N"
            
        ).properties(
            width=700,
            height=350,
            title=title
            )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title='')),
            tooltip=['Country',
                     alt.Tooltip('GDP $B', format="$,.0f")]
        ).properties(width=700)

        
        return_chart = alt.layer(line,points).configure_axis(grid=False)
        return return_chart


    def get_time_series_gdp_compare_chart(self,source_country,target_country):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_compare(source_country,target_country)

        title = "GDP Growth " + source_country + " and " + target_country + "2014 to 2020"

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data)

        line = base.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('GDP Pct Growth:Q',axis=alt.Axis(title="GDP Growth %",labelExpr='datum.value + "%"')),
            color=alt.Color(field="Country", type="nominal",
                            scale = alt.Scale(range = ['#3E7B7B', '#CBD9BF']),
                            legend = alt.Legend(title="Country"))
            
        ).properties(
            width=700,
            height=350,
            title=title
            )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('GDP Pct Growth:Q',scale=alt.Scale(domain=(-10, 10)),axis=alt.Axis(title='')),
            tooltip=['Country',
                     alt.Tooltip('GDP Pct Growth', format=".2f")]
        ).properties(width=700)

        
        return_chart = alt.layer(line,points).configure_axis(grid=False)
        return return_chart

    def get_time_series_gdp_chart_for_matrix(self,source_country,width=300,height=150):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_by_country(source_country)

        title = "GDP " + source_country

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data)

        line = base.mark_line().encode(
            x=alt.X('Year',axis=alt.Axis(title='Year')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title="GDP $B",labelExpr='"$" + datum.value / 1E9 + "B"'))#,
            #color="Country:N"
            
        ).properties(
            width=width,
            height=height,
            title=title
            )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year',axis=alt.Axis(title='')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title='')),
            tooltip=['Country',
                     alt.Tooltip('GDP $B', format="$,.0f")]
        ).properties(width=width)

        
        return_chart = alt.layer(line,points)
        return return_chart

    def get_time_series_gdp_trade_trend_chart(self,source_country):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_by_country(source_country)

        title = "GDP & Trade Growth Compare " + source_country

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data).transform_fold(['GDP Pct Growth','Trade Total Change %'])

        line = base.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('value:Q',axis=alt.Axis(title="GDP and Trade % Change",labelExpr='datum.value + "%"')),
            color="key:N"
        ).properties(
            width=700,
            height=350,
            title=title
            )

                #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('value:Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip('GDP Growth Pct', format=".2f"),
                     alt.Tooltip('Trade Total Change %', format=".2f")]
        ).properties(width=700)

        return_chart = alt.layer(line,points).configure_axis(grid=False)
        return return_chart
    
    def get_time_series_gdp_trade_for_matrix(self,source_country,width=300,height=200):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_by_country(source_country)

        title = "GDP & Trade Growth Compare " + source_country

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data).transform_fold(['GDP Pct Growth','Trade Total Change %'])

        line = base.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('value:Q',axis=alt.Axis(title="GDP and Trade % Change",labelExpr='datum.value + "%"')),
            color=alt.Color(field="key", type="nominal",
                            scale = alt.Scale(range = ['#799D5E', '#E4AB65']),
                            legend = alt.Legend(title="key"))
        ).properties(
            width=width,
            height=height,
            title=title
            )

                #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('value:Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip('GDP Growth Pct', format=".2f"),
                     alt.Tooltip('Trade Total Change %', format=".2f")]
        ).properties(
            width=width)

        return_chart = alt.layer(line,points)
        return return_chart


    def get_charts_for_country_dill_down(self,source_country,target_country,width=300,height=200):
        time_s  = self.get_altaire_line_chart_county_trade_for_matrix(source_country,target_country)
        pie     = self.get_altaire_dual_pie_chart_by_types_for_matrix(source_country,target_country, "exports")
        gdp     = self.get_time_series_gdp_compare_chart_form_matrix(source_country,target_country)
        yoy_chg = self.get_altaire_yoy_trade_per_GDP_for_matrix(source_country,target_country)

        row_1 = (time_s | pie).resolve_scale(
            color='independent')
        row_2 = (gdp | yoy_chg).resolve_scale(
            color='independent')


        my_chart = (row_1 & row_2 ).configure_axis(
        grid=False
        ).configure_view(
        strokeWidth=0
        ).configure_view(
            stroke=None
        )

        return my_chart

    def get_altaire_dual_pie_chart_by_types_for_matrix(self,source_country,target_country, direction,width=300,height=200):

        my_data = self.my_data_object
        title =  source_country + " vs. "+ target_country + " " + direction + " breakdown"
        
        df = my_data.imports_exports_by_sectors(source_country, target_country, direction)
        country_data = df.rename(columns={'Product/Sector-reformatted': 'Product_Type'})
        #source_country_data = df[df['Reporting Economy']==source_country].rename(
        #    columns={'Product/Sector-reformatted': 'Product_Type'})
        #target_country_data = df[df['Reporting Economy']==target_country].rename(
        #    columns={'Product/Sector-reformatted': 'Product_Type'})

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        # radio button for export/import option
        #direction = ["exports", "imports"]
        #direction_radio = alt.binding_radio(options=direction)

        #direction_select = alt.selection_single(fields=['Direction'], bind=direction_radio, name="Direction", init = {'Direction': 'exports'})


        base = alt.Chart(country_data).encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color(field="Product_Type", type="nominal", scale=alt.Scale(scheme='tableau20')),
            tooltip=alt.Tooltip('Product_Type')
        )

        source_pie_chart = base.transform_filter(
            alt.FieldEqualPredicate(field='Reporting Economy', equal=source_country)
        ).mark_arc(outerRadius=(width/4)).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).properties(title=source_country,width=(width/2),height=height)

        base_target = alt.Chart(country_data).encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color(field="Product_Type", type="nominal"),
            tooltip=alt.Tooltip('Product_Type')
        ).transform_filter(
            alt.FieldEqualPredicate(field='Reporting Economy', equal=target_country)
        )

        target_pie_chart = base.mark_arc(outerRadius=(width/4)).transform_filter(
            alt.FieldEqualPredicate(field='Reporting Economy', equal=target_country)
        ).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).properties(title=target_country,width=(width/2),height=height)

        return_chart = alt.hconcat(source_pie_chart, target_pie_chart).properties(
            title=alt.TitleParams(text=title,align="left"))

        return return_chart

    def get_time_series_gdp_compare_chart_form_matrix(self,source_country,target_country,width=300,height=200):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_compare(source_country,target_country)

        title = "GDP Growth " + source_country + " and " + target_country + " 2014 to 2020"

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data)

        line = base.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('GDP Pct Growth:Q',axis=alt.Axis(title="GDP Growth %",labelExpr='datum.value + "%"')),
            color=alt.Color(field="Country", type="nominal",
                            scale = alt.Scale(range = ['#3E7B7B', '#CBD9BF']),
                            legend = alt.Legend(title="Country"))
            
        ).properties(
            width=width,
            height=height,
            title=title
            )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('GDP Pct Growth:Q',scale=alt.Scale(domain=(-10, 10)),axis=alt.Axis(title='')),
            tooltip=['Country',
                     alt.Tooltip('GDP Pct Growth', format=".2f")]
        ).properties(width=width)

        
        return_chart = alt.layer(line,points)
        return return_chart


    def get_time_series_gdp_chart_for_matrix(self,source_country,width=300,height=150):

        my_data = self.my_data_object

        my_data_to_graph = my_data.get_gdp_data_by_country(source_country)

        title = "GDP " + source_country

        source_and_target_data = my_data_to_graph

        base = alt.Chart(source_and_target_data)

        line = base.mark_line().encode(
            x=alt.X('Year',axis=alt.Axis(title='Year')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title="GDP $B",labelExpr='"$" + datum.value / 1E9 + "B"'))#,
            #color="Country:N"
            
        ).properties(
            width=width,
            height=height,
            title=title
            )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year',axis=alt.Axis(title='')),
            y=alt.Y('GDP:Q',axis=alt.Axis(title='')),
            tooltip=['Country',
                     alt.Tooltip('GDP $B', format="$,.0f")]
        ).properties(width=width)

        return_chart = alt.layer(line,points)
        return return_chart

    def get_net_trade_chart(self,source_country):

        my_data = self.my_data_object
        
        title = "" + source_country + "Trade Imports, Exports, Net Trade"
        #title="Trade Imports, Exports, Net Trade"

        df_set=my_data.get_data_by_source_and_target_country(source_country,'China')
        df_set['Exports']=df_set['Exports ($M)']
        df_set['Imports']=df_set['Imports ($M)']*-1
        df_set['Net Exports']=df_set['Net Exports ($M)']
        df_set[df_set['country']==source_country]

        #from altair.vegalite.v4.schema.core import Color
        base = alt.Chart(df_set).transform_fold(['Imports','Exports'])
        base2= alt.Chart(df_set)

        bar = base.mark_bar(size=(35)).encode(
            x=alt.X('year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('value:Q',axis=alt.Axis(title="Trade",labelExpr='"$" + datum.value / 1E3 + "B"')),#,
            #strokeWidth=alt.value(3)
            color=alt.Color("key:N",scale=alt.Scale(scheme='blues'))
        ).properties(
            width=500,
            height=250,
            title=title
            )

        line = base2.mark_line(color='green').encode(
            x=alt.X('year:N'),#,axis=alt.Axis(title='Year')),
            y=alt.Y('Net Exports:Q'),#,axis=alt.Axis(title="Trade")),#,
            strokeWidth=alt.value(3)
            #color=alt.Color()
            #strokeWidth=alt.value(3)
            #color=alt.Color("key:N",scale=alt.Scale(scheme='blues'))
        ).properties(
            width=500,
            height=250
            )

        return_chart=alt.layer(bar,line).configure_axis(grid=False)
        return return_chart
    
    def get_nafta_net_trade_chart(self,source_country,trade_group):
        #NOT SET-UP YET
        #CAN CHANGE TO NAFTA & EU

        my_data = self.my_data_object
        
        title = "" + source_country + "Trade Imports, Exports, Net Trade"
        #title="Trade Imports, Exports, Net Trade"

        source_country=source_country
        trade_group=trade_group

        df_set=my_data.get_data_by_source_and_target_country()
        df_set['Exports']=df_set['Exports ($M)']
        df_set['Imports']=df_set['Imports ($M)']*-1
        df_set['Net Exports']=df_set['Net Exports ($M)']
        df_set[df_set['country']==source_country]

        #from altair.vegalite.v4.schema.core import Color
        base = alt.Chart(df_set).transform_fold(['Imports','Exports'])
        base2= alt.Chart(df_set)

        bar = base.mark_bar(size=(35)).encode(
            x=alt.X('year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('value:Q',axis=alt.Axis(title="Trade",labelExpr='"$" + datum.value / 1E3 + "B"')),#,
            #strokeWidth=alt.value(3)
            color=alt.Color("key:N",scale=alt.Scale(scheme='blues'))
        ).properties(
            width=500,
            height=250,
            title=title
            )

        line = base2.mark_line(color='green').encode(
            x=alt.X('year:N'),#,axis=alt.Axis(title='Year')),
            y=alt.Y('Net Exports:Q'),#,axis=alt.Axis(title="Trade")),#,
            strokeWidth=alt.value(3)
            #color=alt.Color()
            #strokeWidth=alt.value(3)
            #color=alt.Color("key:N",scale=alt.Scale(scheme='blues'))
        ).properties(
            width=500,
            height=250
            )

        return_chart=alt.layer(bar,line).configure_axis(grid=False)
        return return_chart

    def get_exchange_rate_chart(self,source_country,width=500,height=250):
        
        my_data = self.my_data_object
        gdp=my_data.get_gdp_all_data()
        #gdp_c=gdp[gdp.Country==source_country]
        base=alt.Chart(gdp_c)

        nafta_list=['Mexico','United States','Canada']
        nafta_dropdown = alt.binding_select(options= nafta_list,name="Country")
        nafta_select = alt.selection_single(fields=['Country'], bind=nafta_dropdown, init={'Country': nafta_list[0]})

        exchange_rate=base.mark_line().encode(
            x=alt.X('Year:N'),
            y=alt.Y('exchange_rate:Q',axis=alt.Axis(title='Local Currency to $USD Exchange Rate',format='.2f')),
            color='Country:N'
            ).properties(height=height,width=width)
        
        return_chart=exchange_rate
        return return_chart

    def get_import_export_type_chart(self,source_country,height=250,width=350):
        
        my_data = self.my_data_object
        direction_list=['imports','exports']
        source_country=source_country

        direction_dropdown = alt.binding_select(options= direction_list,name="Direction")
        direction_select = alt.selection_single(fields=['Direction'], bind=direction_dropdown, init={'Direction': direction_list[0]})

        #direction_input=direction
        #dataframe_ie=my_data.imports_exports_by_sectors_source(source_country)
        #Hard coded Canada / Need to get dual drop down to work
        dataframe_ie=my_data.imports_exports_by_sectors_source()
        dataframe_ie=dataframe_ie[dataframe_ie['Reporting Economy']=='Canada']
        dataframe_ie_grp=dataframe_ie.groupby(['Year','Direction','Reporting Economy','Type']).sum().reset_index()

        dataframe_ie['Year Trade Rank']=dataframe_ie.groupby(['Year','Direction'])['Value'].rank(ascending=False)
        dataframe_ie_top5=dataframe_ie[dataframe_ie['Year Trade Rank']<=5]
        dataframe_ie_top5

        baseexp=alt.Chart(dataframe_ie_grp)

        title='Import and Exports Type'

        exp_chart=baseexp.mark_bar().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('Value:Q'),
            color='Type:N'
        ).add_selection(
            direction_select
        ).transform_filter(
            direction_select).properties(title=title,height=height,width=width)

        title2='Import and Exports Product/Sector'

        baseexp_t5=alt.Chart(dataframe_ie_top5)

        exp_top5=baseexp_t5.mark_bar().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('Value:Q'),
            color='Product/Sector-reformatted:N'
        ).add_selection(
            direction_select
        ).transform_filter(
            direction_select).properties(title=title2,height=height,width=width)

        return_chart=alt.hconcat(exp_chart,exp_top5).resolve_scale(color='independent')
        return return_chart


    def get_import_export_prod_type_chart(self,height=250,width=350):

        my_data = self.my_data_object

        direction_list=['imports','exports']
        direction_dropdown = alt.binding_select(options= direction_list,name="Direction")
        direction_select = alt.selection_single(fields=['Direction'], bind=direction_dropdown, init={'Direction': direction_list[0]})

        nafta_list=['Mexico','United States','Canada']
        nafta_dropdown = alt.binding_select(options= nafta_list,name="Country")
        nafta_select = alt.selection_single(fields=['Country'], bind=nafta_dropdown, init={'Country': nafta_list[0]})

        dataframe_ie=my_data.imports_exports_by_sectors_source()
        dataframe_ie=dataframe_ie[dataframe_ie['Reporting Economy'].isin(['Canada','United States','Mexico'])]
        dataframe_ie['Country']=dataframe_ie['Reporting Economy']
        dataframe_ie_grp=dataframe_ie.groupby(['Year','Direction','Reporting Economy','Type']).sum().reset_index()
        dataframe_ie_grp['Country']=dataframe_ie_grp['Reporting Economy']

        dataframe_ie['Year Trade Rank']=dataframe_ie.groupby(['Country','Year','Direction'])['Value'].rank(ascending=False)
        dataframe_ie_top5=dataframe_ie[dataframe_ie['Year Trade Rank']<=5]

        title2='Import and Exports Product/Sector'

        baseexp_t5=alt.Chart(dataframe_ie_top5)

        exp_top5=baseexp_t5.mark_bar().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('Value:Q'),
            color='Product/Sector-reformatted:N'
        ).properties(title=title2,height=height,width=width).add_selection(
            nafta_select).transform_filter(
            nafta_select).add_selection(
            direction_select).transform_filter(
            direction_select)

        return_chart=exp_top5

        return return_chart


    def get_eu_domestic_trading_chart(self, height=250, width=350):
        my_data = self.my_data_object
        df=my_data.load_and_clean_up_EU_files().copy()

        df['year'] = df.year.astype(str)
        df['ordered-cols'] = df.apply(lambda x: '-'.join(sorted([x['Trading Partner'],x['country'],x['year']])), axis=1)
        df = df.drop_duplicates(['ordered-cols'])
        df['year'] = df.year.astype(int)

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        base= alt.Chart(df)
        block = base.mark_rect(color='green').encode(
            x=alt.X("Trading Partner:N"),
            y=alt.Y("country:N"),
            color='Total Trade ($M):Q',
            tooltip = alt.Tooltip('Total Trade ($M):Q', format="$,.0f")
        ).properties(title='EU Domestic Service Trading Gross Volume',width=width,height=height)

        return_chart = block.add_selection(
                slider_selection
                ).transform_filter(
                slider_selection).resolve_scale(
                y='independent')

        return return_chart


    def get_eu_versus_noneu_trading_chart(self, height=250, width=350):
        my_data = self.my_data_object
        df = my_data.load_and_clean_up_top_20_file().copy()
        eu_countries=['Austria','Belgium','Croatia','Czech Republic','Denmark','Finland','France','Germany','Greece','Hungary',
        'Italy','Netherlands','Poland','Portugal','Spain','Sweden','United Kingdom','European Union']

        title = 'EU Internal vs. Non-EU Countries Trade Volume'

        #EU Country as source contries
        eu_df = df.loc[df['country'].isin(eu_countries)][['Trading Partner','Total Trade ($M)','Exports ($M)','Imports ($M)','country','year']]
        
        #Non EU as trading stats
        non_eu = eu_df.loc[~eu_df['Trading Partner'].isin(eu_countries)]
        non_eu = eu_df.loc[~eu_df['Trading Partner'].isin(eu_countries)]
        non_eu = non_eu.groupby(by=['country','year'])['Total Trade ($M)','Exports ($M)','Imports ($M)'].sum()
        non_eu = non_eu.reset_index()
        non_eu['Trading Partner'] = 'Non-EU'
        #non_eu[non_eu['year']==2020]

        eu_filtered_df = eu_df.loc[eu_df['Trading Partner']== 'European Union']
        complete_df = pd.concat([non_eu, eu_filtered_df], axis = 0).reset_index()

        #complete_df['Imports ($M)'] = 0 - complete_df['Imports ($M)']
        complete_df = complete_df.sort_values(by=['Trading Partner'], ascending=False)

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        return_chart_1 = alt.Chart(complete_df).mark_area(opacity=1).encode(
            x='country',
            y='Exports ($M)',
            color = 'Trading Partner',
            tooltip = alt.Tooltip('Exports ($M)', format="$,.0f"),
            order=alt.Order(
            # Sort the segments of the bars by this field
            'Trading Partner',
            sort='ascending'
            )
        ).properties(width=width,height=height,title='EU Internal vs. Non-EU Countries Exports Trading Volume').add_selection(
                slider_selection
                ).transform_filter(
                slider_selection).resolve_scale(
                y='independent')

        return_chart_2 = alt.Chart(complete_df).mark_area(opacity=0.75).encode(
            x='country',
            y='Imports ($M)',
            color = 'Trading Partner',
            tooltip = alt.Tooltip('Imports ($M)', format="$,.0f"),
            order=alt.Order(
            # Sort the segments of the bars by this field
            'Trading Partner',
            sort='ascending'
            )
        ).properties(width=width,height=height, title ='EU Internal vs. Non-EU Countries Imports Trading Volume').add_selection(
                slider_selection
                ).transform_filter(
                slider_selection).resolve_scale(
                y='independent')

        return_chart=return_chart_1 | return_chart_2
        
        return return_chart

    def get_altaire_multi_charts_for_EU(self,width=1000,height=600):
        my_data = self.my_data_object
        title = "Percentage of Total Trades Done with EU"
        background = '#f9f9f9'

        eu_countries=['Austria','Belgium','Croatia','Czech Republic','Denmark','Finland','France','Germany','Greece','Hungary','Italy','Netherlands','Poland','Portugal','Spain','Sweden','United Kingdom','European Union']
 
        df = my_data.get_EUdata_by_country()
        df = df.rename(columns={'TradePctGDPChange': 'Trade/GDP ratio change'})

        df = df[df['isEuPartner'].isin(['Trades with EU','Trades with Others'])]

        df_new_total = df.groupby(by=['Country','year'])['total_trade'].sum()
        df_new_total = df_new_total.reset_index()
        new_df = pd.merge(df, df_new_total,  how='left', left_on=['Country','year'], right_on=['Country','year'])

        new_df = new_df.drop(columns=['total_toWorld_trade'])
        df = new_df.rename(columns={'total_trade_x': 'total_trade', 'total_trade_y': 'total_toWorld_trade'})

        #country_list = df['Country'].unique().tolist()
        country_list = ['Spain', 'France', 'Netherlands', 'Germany', 'Italy', 'United Kingdom', 'Switzerland',
                        'Russia', 'United States', 'China', 'Saudi Arabia', 'Brazil', 'Iran', 'India','Japan',
                        'South Korea', 'Australia', 'Canada', 'Indonesia', 'Mexico']
        test = df[(df['year']==2020)&(df['country']=='Australia')]
        print(df['isEuPartner'].unique())
        print(country_list)

        # Slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        # Pie charts
        base = alt.Chart(df).encode(
            theta=alt.Theta(field="total_trade", type="quantitative"),
            color=alt.Color(field="isEuPartner", type="nominal",
                            scale = alt.Scale(domain = ['Trades with EU', 'Trades with Others'],
                                              range = ['#156296', '#B9CDDB']), 
                            legend = alt.Legend(title="Key")),
            
            tooltip=alt.Tooltip('total_trade', format="$,.0f")
        )

        base2 = alt.Chart(df).encode(
            theta=alt.Theta(field="total_trade", type="quantitative"),
            color=alt.Color(field="isEuPartner", type="nominal",
                            scale = alt.Scale(domain = ['Trades with EU', 'Trades with Others'],
                                              range = ['#156296', '#B9CDDB']),
                            legend = None),
            tooltip=alt.Tooltip('total_trade', format="$,.0f")
        )

        chart1 = alt.hconcat()
        for country in country_list[0:7]: 
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+10), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            
            if country in eu_countries:
                EU_tag = country + ' (EU)'
            else:
                EU_tag = country 

            chart1 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=EU_tag,width=(width/8),height=(height/10+30))
        
        chart2 = alt.hconcat()
        for country in country_list[7:7*2]:
            base_pie = base2.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base2.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+10), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            chart2 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+30))

        chart3 = alt.hconcat()
        for country in country_list[14:]:
            base_pie = base2.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base2.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+10), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )

            chart3 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+30))


        return_chart = (chart1 & chart2 & chart3 ).configure_title(
            baseline="line-top",
            dy = -5
        ).configure_legend(orient='right')
        return return_chart


    def get_eu_trade_overall_chart(self):
        
        my_data = self.my_data_object
        #Net Trade with EU for China, EU Top 20, US, Rest of World Top 20
        df=my_data.get_eu_trade_data_pcts()
        base1=alt.Chart(df[df["Top20group"]=='EU'])
        title1='Top 20 EU Net Trade'
        pct12=base1.mark_line().encode(
            x=alt.X('year:N',axis=alt.Axis(title='')),
            y=alt.Y('NetTrade',axis=alt.Axis(title='T20 EU',labelExpr='"$" + datum.value / 1E6 + "U"'),scale=alt.Scale(domain=[-1000000, 1000000])),
            color='Trade Group:N'
        ).properties(title=title1,height=150,width=300)

        df=my_data.get_eu_trade_data_pcts()
        base2=alt.Chart(df[df["Top20group"]=='US'])
        title2='US & EU Net Trade'
        pct22=base2.mark_line().encode(
            x=alt.X('year:N',axis=alt.Axis(title='')),
            y=alt.Y('NetTrade',axis=alt.Axis(title='US',labelExpr='"$" + datum.value / 1E6 + "U"'),scale=alt.Scale(domain=[-1000000, 1000000])),
            color='Trade Group:N'
        ).properties(title=title2,height=150,width=300)

        df=my_data.get_eu_trade_data_pcts()
        base3=alt.Chart(df[df["Top20group"]=='China'])
        title3='China Net Trade'
        pct32=base3.mark_line().encode(
            x=alt.X('year:N',axis=alt.Axis(title='')),
            y=alt.Y('NetTrade',axis=alt.Axis(title='China',labelExpr='"$" + datum.value / 1E6 + "U"'),scale=alt.Scale(domain=[-1000000, 1000000])),
            color='Trade Group:N'
        ).properties(title=title3,height=150,width=300)

        df=my_data.get_eu_trade_data_pcts()
        base4=alt.Chart(df[df["Top20group"]=='RoW'])
        title4='Rest of World Net Trade'
        pct42=base4.mark_line().encode(
            x=alt.X('year:N',axis=alt.Axis(title='')),
            y=alt.Y('NetTrade',axis=alt.Axis(title='RoW',labelExpr='"$" + datum.value / 1E6 + "U"'),scale=alt.Scale(domain=[-1000000, 1000000])),
            color='Trade Group:N'
        ).properties(title=title4,height=150,width=300)


        pct12.configure_axis(grid=False)
        pct22.configure_axis(grid=False)
        pct32.configure_axis(grid=False)
        pct42.configure_axis(grid=False)

        ntrade1=alt.vconcat(pct12,pct22)
        ntrade2=alt.vconcat(pct32,pct42)

        nettrade=alt.hconcat(ntrade1,ntrade2).configure_axis(grid=False)
        return nettrade


    def get_gdp_per_cap_lcu_chart(self,source_country,height=250,width=350):
        
        my_data = self.my_data_object

        #Function Ready to Go        
        nafta_list=['Mexico','United States','Canada']
        nafta_dropdown = alt.binding_select(options= nafta_list,name="Country")
        nafta_select = alt.selection_single(fields=['Country'], bind=nafta_dropdown, init={'Country': nafta_list[0]})

        #source_country=source_country
        df_gdp_nafta=my_data.get_gdp_all_data()

        base = alt.Chart(df_gdp_nafta)

        title='GDP per Capita Local Currency & USD Exchange Rate'

        bar = base.mark_bar().encode(
        x=alt.X('Year:N',axis=alt.Axis(title='Year')),
        #y=alt.Y('GDP per capita:Q',axis=alt.Axis(title="GDP Per Capita $"))#,
        y=alt.Y('GDP per capita constant LCU',axis=alt.Axis(title="GDP Per Capita LCU $"))#,
        #color="Country:N"
        ).properties(
        width=width,
        height=height,
        title=title
        )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
        color='red',
        opacity=0.0,
        size=1000
        ).encode(
        x=alt.X('Year:N',axis=alt.Axis(title='')),
        y=alt.Y('GDP per capita constant LCU',axis=alt.Axis(title='')),
        tooltip=['GDP per capita constant LCU']
        ).properties(width=700)

        base2= alt.Chart(df_gdp_nafta)
        line = base2.mark_line(color='green').encode(
            x=alt.X('Year:N'),#,axis=alt.Axis(title='Year')),
            y=alt.Y('exchange_rate:Q'),#,axis=alt.Axis(title="Trade")),#,
            #,scale=alt.Scale(domain=[-3000000, 2000000])
            strokeWidth=alt.value(3)
        ).properties(width=width,height=height)

        return_chart = alt.layer(bar,points)

        return_chart_2 = alt.layer(return_chart,line).add_selection(
                nafta_select
                ).transform_filter(
                nafta_select).resolve_scale(
                y='independent')

        return return_chart_2


    def get_gdp_unemployment(self,height=250,width=350):

        my_data = self.my_data_object

        #Function Ready to Go
        nafta_list=['Mexico','United States','Canada']
        nafta_dropdown = alt.binding_select(options= nafta_list,name="Country")
        nafta_select = alt.selection_single(fields=['Country'], bind=nafta_dropdown, init={'Country': nafta_list[0]})

        #source_country=source_country
        df_gdp_nafta=my_data.get_gdp_all_data_2()
        df_gdp_nafta=df_gdp_nafta[(df_gdp_nafta['Country'].isin(['Mexico','United States','Canada'])) & (df_gdp_nafta['Year']>=1994)]

        base = alt.Chart(df_gdp_nafta)

        highlight = alt.selection(type='single', on='mouseover',
                        fields=['Country'], nearest=True)

        title='NAFTA National Unemployment'

        bar = base.mark_bar().encode(
        x=alt.X('Year:N',axis=alt.Axis(title='Year')),
        #y=alt.Y('GDP per capita:Q',axis=alt.Axis(title="GDP Per Capita $"))#,
        y=alt.Y('Unemployment pct national est',axis=alt.Axis(title="Unemployment Pct"))#,
        #color="Country:N"
        #Alt Metric Unemployment pct national est
        ).properties(
        width=width,
        height=height,
        title=title
        )

        line = base.mark_line().encode(
        x=alt.X('Year:N',axis=alt.Axis(title='Year')),
        #y=alt.Y('GDP per capita:Q',axis=alt.Axis(title="GDP Per Capita $"))#,
        y=alt.Y('Unemployment pct ILO',axis=alt.Axis(title="Unemployment pct ILO")),
        #y=alt.Y('Unemployment pct national est',axis=alt.Axis(title="Unemployment Pct")),#,
        color=alt.Color("Country:N",
                    legend = alt.Legend(title=None,orient='right')),
        size=alt.condition(~highlight, alt.value(1), alt.value(3))
        ).properties(
        width=width,
        height=height,
        title=title
        )

        #Throw points on so that the tool tips will work better.
        points = base.mark_circle(
        color='red',
        opacity=0.0,
        size=1000
        ).encode(
        x=alt.X('Year:N',axis=alt.Axis(title='')),
        y=alt.Y('Unemployment pct ILO',axis=alt.Axis(title='')),
        tooltip=[alt.Tooltip('Unemployment pct ILO', format=".2f")]
        ).encode(
        opacity=alt.value(0)
        ).add_selection(
            highlight
        ).properties(width=350)

        return_chart=alt.layer(line,points)
        return return_chart


    def get_nafta_import_export_pie_chart(self,height=250,width=350):
    
        my_data = self.my_data_object

        title = "Exports Breakdown"

        imp_exp=my_data.imports_exports_by_sectors_source()
        nafta_imp_exp=imp_exp[imp_exp['Reporting Economy'].isin(['United States','Mexico','Canada'])]
        nafta_exp=nafta_imp_exp[nafta_imp_exp['Direction']=='exports']
        nafta_exp=nafta_exp.rename(columns={'Product/Sector-reformatted': 'Product_Type','Reporting Economy':'Country'})

        nafta_list=['Mexico','United States','Canada']
        nafta_dropdown = alt.binding_select(options= nafta_list,name="Country")
        nafta_select = alt.selection_single(fields=['Country'], bind=nafta_dropdown, init={'Country': nafta_list[0]})

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        base = alt.Chart(nafta_exp).encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color(field="Product_Type", type="nominal", scale=alt.Scale(scheme='tableau20')),
            tooltip=alt.Tooltip(['Product_Type',
                            'Value']
                            )
        )

        source_pie_chart = base.mark_arc(outerRadius=(width/4)).add_selection(nafta_select).transform_filter(nafta_select).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).properties(width=width,height=height)

        return_chart1=source_pie_chart.properties(
            title=alt.TitleParams(text=title))


        title2 = "Imports Breakdown"

        nafta_imp=nafta_imp_exp[nafta_imp_exp['Direction']=='imports']
        nafta_imp=nafta_imp.rename(columns={'Product/Sector-reformatted': 'Product_Type','Reporting Economy':'Country'})

        base_imp = alt.Chart(nafta_imp).encode(
            theta=alt.Theta(field="Value", type="quantitative"),
            color=alt.Color(field="Product_Type", type="nominal", scale=alt.Scale(scheme='tableau20')),
            tooltip=alt.Tooltip(['Product_Type',
                            'Value'])
        )

        source_pie_chart_imp = base_imp.mark_arc(outerRadius=(width/4)).add_selection(nafta_select).transform_filter(nafta_select).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).properties(width=width,height=height)

        return_chart2=source_pie_chart_imp.properties(
            title=alt.TitleParams(text=title2))

        return_chart = alt.hconcat(return_chart1, return_chart2).resolve_scale(y='independent')
        return return_chart


    def get_nafta_trade_data_pcts(self):
        
        my_data = self.my_data_object

        df_nafta=my_data.get_nafta_trade_data_pcts()
        df_nafta_n=df_nafta[df_nafta['Top20group']=='NAFTA']

        title="Inter NAFTA vs World Trade"

        base=alt.Chart(df_nafta_n)

        gnafta1=base.mark_bar().encode(
            alt.Column('year'),
            x=alt.X('Trade Group:N',axis=alt.Axis(title='')),
            y=alt.Y('TotalTrade:Q'),
            color='Trade Group:N'
        ).properties(title=title,height=250,width=40)

        return_chart=gnafta1
        return return_chart


    def get_nafta_world_inter_trade(self,height=250,width=350):
        
        my_data = self.my_data_object

        title="North America Trade - World vs Inter"

        #Tool Tips
        df_nafta=my_data.get_nafta_trade_data_pcts()
        df_nafta_n=df_nafta[df_nafta['Top20group']=='NAFTA']
        df_nafta_tt=df_nafta_n[['Top20group','year','Trade Group','Imports','Exports','TotalTrade','NetTrade','NAFTA Imports %','NAFTA Exports %','NAFTA Total Trade %']]
        df_nafta_tt=df_nafta_tt.rename(columns={'NAFTA Imports %': 'Imports %','NAFTA Exports %':'Exports %','NAFTA Total Trade %':'Total Trade %'})
        df_nafta_pivot=df_nafta_tt.pivot(index=['Top20group','year'], columns=['Trade Group'], values=['Imports %','Exports %','Total Trade %','Imports','Exports','TotalTrade']).reset_index()
        df_nafta_pivot.columns = df_nafta_pivot.columns.droplevel(1)
        df_colnames=['Top20group','year','NAFTA Imports %','World Imports %','NAFTA Exports %','World Exports %','NAFTA Total Trade %','World Total Trade %','NAFTA Imports','World Imports','NAFTA Exports','World Exports','NAFTA Total Trade','World Total Trade']
        df_nafta_pivot.columns=df_colnames

        base_tt = alt.Chart(df_nafta_pivot).transform_fold(
                                                            ['World Total Trade','NAFTA Total Trade'],
                                                            as_ = ['column','value']
                                                            )

        bars_tt = base_tt.mark_bar(
            size=(35)
        ).encode(
            y=alt.Y('value:Q',axis=alt.Axis(title='Total Trade ($B)',labelExpr='"$" + datum.value / 1E3 + "B"'),scale=alt.Scale(domain=[0, 6500000])),
            x=alt.X('year:N'),
            tooltip=[alt.Tooltip('NAFTA Total Trade',format="$,.0f"),alt.Tooltip('World Total Trade',format="$,.0f"),alt.Tooltip('NAFTA Total Trade %'),alt.Tooltip('World Total Trade %')],                
        color=alt.Color(
                'column:N',
                scale=alt.Scale(
                #domain=['NAFTA','World'],
                range=['#778ba5', '#02075d']),
                legend=alt.Legend(
                title=None,
                orient='none',
                legendX=85, legendY=-20,
                direction='horizontal',
                titleAnchor='middle')
                ),
            order=alt.Order('column:N', sort='ascending')
        ).properties(title=title,height=height,width=width)

        return_chart=bars_tt
        return return_chart

    def get_trade_group_gdp_growth_chart(self,trade_group,height=250,width=350):

        my_data = self.my_data_object

        if trade_group=='NAFTA':
            nafta_gdp_growth=my_data.get_nafta_gdp_data_growth_rate()
            nafta_gdp_growth=nafta_gdp_growth[nafta_gdp_growth['Continental'].isin(['Canada', 'Mexico','United States'])]
            base=alt.Chart(nafta_gdp_growth)
            title='NAFTA GDP Growth'

        else:# trade_group='EU':
            gdp_growth=my_data.get_eu_gdp_data_growth_rate('1')
            base=alt.Chart(gdp_growth)

            
        highlight = alt.selection(type='single', on='mouseover',
                                fields=['Continental'], nearest=True)    

        continent=base.mark_line().encode(
            x=alt.X('Year:N'),
            y=alt.Y('GDP Pct Growth:Q'),
            #color='Continental:N'
            color=alt.Color(
                            'Continental:N',
                            legend = alt.Legend(title=None,orient='right')#,
                            #legend=alt.Legend(
                            #title=None,
                            #orient='none',
                            #legendX=50, legendY=-20,
                            #direction='horizontal',
                            #titleAnchor='end')
                            ),
            size=alt.condition(~highlight, alt.value(1), alt.value(3))
            )#.properties(title=title,height=height,width=width)

        points = base.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('GDP Pct Growth:Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip("Continental:N"),
                    alt.Tooltip("GDP Pct Growth:Q",format=".2f" ),
                    alt.Tooltip("Year:N")]
        ).encode(
        opacity=alt.value(0)
        ).add_selection(
            highlight
        )

        #return_chart=continent
        return_chart=alt.layer(continent, points).properties(
                title=title,
                width=width,
                height=height
            )

        return return_chart

    def get_nafta_world_trade_chart(self,trade_group,height=250,width=350):

        my_data = self.my_data_object

        #source_country='Mexico'
        #trade_group='NAFTA'

        title="North America Net Trade - World vs Inter"

        #NAFTA COUNTRY DROPDOWN LIST
        nafta_list=['Mexico','United States','Canada']
        nafta_dropdown = alt.binding_select(options= nafta_list,name="Country")
        nafta_select = alt.selection_single(fields=['Country'], bind=nafta_dropdown, init={'Country': nafta_list[0]})

        #TRADE GROUP DROPDOWN LIST
        tg_list=['NAFTA','World']
        tg_dropdown = alt.binding_select(options= tg_list,name="Trading Group")
        tg_select = alt.selection_single(fields=['Trading Group'], bind=tg_dropdown, init={'Trading Group': tg_list[0]})

        df_set=my_data.get_nafta_world_trade_data()
        df_set_input=df_set

        #from altair.vegalite.v4.schema.core import Color
        base = alt.Chart(df_set_input).transform_fold(['Imports','Exports'])
        #base2= alt.Chart(df_set_input)

        bar = base.mark_bar(size=(35)).encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('value:Q',axis=alt.Axis(title="Trade",labelExpr='"$" + datum.value / 1E3 + "B"')),
            #,#strokeWidth=alt.value(3)
            #,scale=alt.Scale(domain=[-3000000, 2000000])
            tooltip=[alt.Tooltip('Year:N'),
                        alt.Tooltip('value:Q',title='Import/Export Amt' , format='$,.0f'),
                        alt.Tooltip('Trading Group'),
                        alt.Tooltip('Country')
                        ],
            color=alt.Color("key:N",scale=alt.Scale(scheme='blues'),legend=alt.Legend(
                title=None,
                orient='none',
                legendX=130, legendY=-40,
                direction='horizontal',
                titleAnchor='middle'))
        ).properties(
            title=title,
            width=width,
            height=height
            )
  
#           color=alt.Color(
 #           'Trade Group:N',
    #         scale=alt.Scale(
  #            domain=['NAFTA','World'],
   #            range=['#778ba5', '#02075d']),)

        base2= alt.Chart(df_set_input)
        line = base2.mark_line(color='green').encode(
            x=alt.X('Year:N'),#,axis=alt.Axis(title='Year')),
            y=alt.Y('Net_Exports:Q'),#,axis=alt.Axis(title="Trade")),#,
            #,scale=alt.Scale(domain=[-3000000, 2000000])
            strokeWidth=alt.value(4)
        ).properties(width=width,height=height)

        line_text = base2.mark_text(
            color="black",
            opacity=1,
            fontSize=9,
            dy=-14
        ).encode(
            x=alt.X('Year:N'),
            y=alt.Y('Net_Exports:Q',axis=alt.Axis(title='')),
            text=alt.Text('Net_Exports:Q', format='$,.0f')
        )

        return_chart=alt.layer(bar,line,line_text).add_selection(
                nafta_select
                ).transform_filter(
                nafta_select).add_selection(
                tg_select
                ).transform_filter(
                tg_select)
        
        return return_chart

    def nafta_continental_trade_partners_top5(self,height=250,width=350):
        
        my_data = self.my_data_object

        #NAFTA Top 5 Trade Partner by Continent
        my_dataframe=my_data.get_top20_trade_continental_data()
        my_return_data_top5_continent=my_dataframe[my_dataframe['Continent Trade Rank']<=5]
        nafta_return_top5=my_return_data_top5_continent[my_return_data_top5_continent['country']=='NAFTA']

        #NAFTA COUNTRY DROPDOWN LIST
        nafta_list=['Arab World', 'Africa', 'South America', 'Australia', 'Europe','Asia', 'Latin America', 'Geo Group', 'North America', 'Oceania']
        nafta_dropdown = alt.binding_select(options= nafta_list,name="country")
        nafta_select = alt.selection_single(fields=['Continent TP'], bind=nafta_dropdown, init={'Continent TP': nafta_list[0]})

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        #CHART 1
        title = "NAFTA Top Continental Trade Partners Rank"
        base = alt.Chart(nafta_return_top5)

        bars = base.mark_bar(color = '#9CBAD5').encode(
            x=alt.X('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            y=alt.Y('Trading Partner:N',axis=alt.Axis(title='Trading Partner'), sort='-x'),
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        )

        text = base.mark_text(align='left', dx=5, dy=-5).encode(
            x=alt.X('Total Trade ($M):Q'),
            y=alt.Y('Trading Partner:N', sort='-x',axis=None),
            text=alt.Text('Total Trade ($M):Q', format='$,.0f')
        )

        return_chart_1 = alt.layer(bars, text).add_selection(
        nafta_select
        ).transform_filter(
        nafta_select
        ).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).resolve_scale(
            y = 'independent'
        ).properties(
            title=title,
            width=width,
            height=height
        )

        base2 = alt.Chart(nafta_return_top5)

        line = base2.mark_line().encode(
            x=alt.X('year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            color='Trading Partner',
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        )

        return_chart_2=line.add_selection(
            nafta_select
            ).transform_filter(
            nafta_select
            ).properties(
                title=title,
                width=width,
                height=height
            )

        return_chart=return_chart_1 | return_chart_2
        return return_chart

    def nafta_continental_trade_partners_top5_country(self,height=250,width=350):
        
        my_data = self.my_data_object
        
        #NAFTA Top 5 Trade Partner by Continent
        my_dataframe=my_data.get_top20_trade_continental_data()
        nafta_return_top5=my_dataframe[(my_dataframe['Level']=='Country') & (my_dataframe['TradeGroup country']=='NAFTA')]
        nafta_return_top5=nafta_return_top5.rename(columns={'year':'Year','country': 'Country','Continent TP':'Continent'})
        my_return_data_top5_continent=nafta_return_top5[nafta_return_top5['Continent Trade Rank']<=5]
        my_return_data_top5_continent

        #my_dataframe=my_data.get_top20_trade_continental_data()
        #nafta_return_top5=my_dataframe[(my_dataframe['Level']=='Country') & (my_dataframe['TradeGroup country']=='NAFTA')]
        #nafta_return_top5=nafta_return_top5.rename(columns={'year':'Year','country': 'Country','Continent TP':'Continent'})
        #my_return_data_top5_continent=nafta_return_top5[nafta_return_top5['Continent Trade Rank']<=5]
        #my_return_data_top5_continent

        #CONTINENT COUNTRY DROPDOWN LIST
        continent_list=['Arab World', 'Africa', 'South America', 'Europe','Asia', 'Latin America',  'North America', 'Oceania']
        continent_dropdown = alt.binding_select(options= continent_list,name="Continent")
        continent_select = alt.selection_single(fields=['Continent'], bind=continent_dropdown, init={'Continent': continent_list[0]})

        #NAFTA COUNTRY LIST
        nafta_list=['Mexico','United States','Canada']
        nafta_dropdown = alt.binding_select(options= nafta_list,name="Country")
        nafta_select = alt.selection_single(fields=['Country'], bind=nafta_dropdown, init={'Country': nafta_list[0]})

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        #CHART 1
        title = "NAFTA Top Continental Trade Partners Rank"
        base = alt.Chart(my_return_data_top5_continent)

        bars = base.mark_bar(color = '#02075d').encode(
            x=alt.X('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            y=alt.Y('Trading Partner:N',axis=alt.Axis(title='Trading Partner'), sort='-x'),
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        )

        text = base.mark_text(align='left', dx=5, dy=-5).encode(
            x=alt.X('Total Trade ($M):Q'),
            y=alt.Y('Trading Partner:N', sort='-x',axis=None),
            text=alt.Text('Total Trade ($M):Q', format='$,.0f')
        )

        return_chart_1 = alt.layer(bars, text).add_selection(
            nafta_select
            ).transform_filter(
            nafta_select
            ).add_selection(
        continent_select
        ).transform_filter(
        continent_select
        ).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).resolve_scale(
            y = 'independent'
        ).properties(
            title=title,
            width=width,
            height=height
        )

        base2 = alt.Chart(my_return_data_top5_continent)

        line = base2.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            color='Trading Partner',
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        )
        #.add_selection(
         #   nafta_select
          #  ).transform_filter(
           # nafta_select
            #).add_selection(
        #    continent_select
        #    ).transform_filter(
        #    continent_select
        #    ).properties(
        #        title=title,
        #        width=width,
        #        height=height
        #    )

        points = base2.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('Total Trade ($M):Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip("Trading Partner"),
                     alt.Tooltip("Total Trade ($M):Q",format="$,.0f" ),
                     alt.Tooltip("year:N")]
        )#.properties(width=700)

        return_chart_2 = alt.layer(line, points).add_selection(
            nafta_select
            ).transform_filter(
            nafta_select
            ).add_selection(
        continent_select
        ).transform_filter(
        continent_select
        #).resolve_scale(
         #   y = 'independent'
        ).properties(
            title=title,
            width=width,
            height=height
        )

        #return_chart_2=line

        return_chart=return_chart_1 | return_chart_2
        return return_chart


    def nafta_continental_trade_partners_top5_country_cont(self,height=250,width=350):

        my_data = self.my_data_object
        #NAFTA Top 5 Trade Partner by Continent
        #nafta_return_top5=my_data.get_top20_trade_continental_cont_data()
        nafta_return_top5=my_data.get_data_nafta_trade_continent_tool()
        my_return_data_top5_continent=nafta_return_top5

        #CONTINENT COUNTRY DROPDOWN LIST
        continent_list=['Arab World', 'Africa', 'South America', 'Australia', 'Europe','Asia', 'Latin America', 'Geo Group', 'North America', 'Oceania']
        continent_dropdown = alt.binding_select(options= continent_list,name="Continent")
        continent_select = alt.selection_single(fields=['Continent'], bind=continent_dropdown, init={'Continent': continent_list[0]})

        #NAFTA COUNTRY LIST
        nafta_list=['Mexico','United States','Canada','NAFTA']
        nafta_dropdown = alt.binding_select(options= nafta_list,name="Trade Group")
        nafta_select = alt.selection_single(fields=['Trade Group'], bind=nafta_dropdown, init={'Trade Group': nafta_list[0]})

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        #CHART 1
        title = "NAFTA Trade by Continent"
        base = alt.Chart(my_return_data_top5_continent)

        bars = base.mark_bar(color = '#02075d').encode(
            x=alt.X('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            y=alt.Y('Continent:N',axis=alt.Axis(title='Continent'), sort='-x'),
            color=alt.Color(
                'Continent:N',
                scale=alt.Scale(
                domain=['North America','Asia','Europe','Other','South America'],
                range=['#778ba5', '#02075d','#02075d','#02075d','#02075d']),
                legend=None
                ),
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
            )

        text = base.mark_text(align='left', dx=5, dy=-5).encode(
            x=alt.X('Total Trade ($M):Q'),
            y=alt.Y('Continent:N', sort='-x',axis=None),
            text=alt.Text('Total Trade ($M):Q', format='$,.0f')
        )

        return_chart_1 = alt.layer(bars, text).add_selection(
            nafta_select
            ).transform_filter(
            nafta_select
            #).add_selection(
        #continent_select
        #).transform_filter(
        #continent_select
        ).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).resolve_scale(
            y = 'independent'
        ).properties(
            title=title,
            width=width,
            height=height
        )

        base2 = alt.Chart(my_return_data_top5_continent)

        title2 = "NAFTA Trade by Continent 2014 to 2020"

        line = base2.mark_line().encode(
            x=alt.X('Year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade ($B)',labelExpr='"$" + datum.value / 1E3 + "B"')),
            color='Continent',
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        ).add_selection(
            nafta_select
            ).transform_filter(
            nafta_select
            ).properties(
                title=title2,
                width=width,
                height=height
            )

        points = base2.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('Year:N',axis=alt.Axis(title='')),
            y=alt.Y('Total Trade ($M):Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip("Continent"),
                    alt.Tooltip("Total Trade ($M):Q",format="$,.0f" ),
                    alt.Tooltip("Year:N")]
        )

        return_chart_2 = alt.layer(line, points).add_selection(
            nafta_select
            ).transform_filter(
            nafta_select
            #).resolve_scale(
            #y = 'independent'
        ).properties(
            title=title,
            width=width,
            height=height
        )

        return_chart=alt.hconcat(return_chart_1,return_chart_2).resolve_scale(color='independent')
        return return_chart_2

    def nafta_continental_trade(self,height=250,width=350):

        my_data = self.my_data_object

        #NAFTA Top 5 Trade Partner by Continent
        my_dataframe=my_data.get_top20_trade_nafta_continental_cont_data()
        nafta_return_top5=my_dataframe

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        #CHART 1
        title = "North America Trade by Continent"
        base = alt.Chart(nafta_return_top5)

        bars = base.mark_bar(color = '#9CBAD5').encode(
            x=alt.X('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            y=alt.Y('Continent TP:N',axis=alt.Axis(title='Continent TP'), sort='-x'),
            color=alt.Color(
                'Continent TP:N',
                scale=alt.Scale(
                domain=['North America','Asia','Europe','Other','South America'],
                range=['#778ba5', '#02075d','#02075d','#02075d','#02075d']),
                legend=None
                ),
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        )

        text = base.mark_text(align='left', dx=5, dy=-5).encode(
            x=alt.X('Total Trade ($M):Q'),
            y=alt.Y('Continent TP:N', sort='-x',axis=None),
            text=alt.Text('Total Trade ($M):Q', format='$,.0f')
        )

        return_chart_1 = alt.layer(bars, text).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).resolve_scale(
            y = 'independent'
        ).properties(
            title=title,
            width=width,
            height=height
        )

        base2 = alt.Chart(nafta_return_top5)

        title2 = "North America Trade by Continent 2014 to 2020"

        line = base2.mark_line().encode(
            x=alt.X('year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            color='Continent TP',
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        ).properties(
                title=title2,
                width=width,
                height=height
            )

        points = base2.mark_circle(
            color='red',
            opacity=0.0,
            size=1000
        ).encode(
            x=alt.X('year:N',axis=alt.Axis(title='')),
            y=alt.Y('Total Trade ($M):Q',axis=alt.Axis(title='')),
            tooltip=[alt.Tooltip("Continent TP"),
                     alt.Tooltip("Total Trade ($M):Q",format="$,.0f" ),
                     alt.Tooltip("year:N")]
        )

        return_chart_2 = alt.layer(line, points).properties(
                title=title2,
                width=width,
                height=height
            )

        return_chart=alt.hconcat(return_chart_1,return_chart_2)
        return_chart.configure_title(anchor='middle')
        return return_chart

    def nafta_continental_trade_partners_trend(self,height=250,width=350):
        #CHART 2
        title = "NAFTA Top Continental Trade Partners Trend"

        my_data = self.my_data_object

        #NAFTA Top 5 Trade Partner by Continent
        my_dataframe=my_data.get_top20_trade_continental_data()
        my_return_data_top5_continent=my_dataframe[my_dataframe['Continent Trade Rank']<=5]
        nafta_return_top5=my_return_data_top5_continent[my_return_data_top5_continent['country']=='NAFTA']

        #NAFTA COUNTRY DROPDOWN LIST
        nafta_list=['Arab World', 'Africa', 'South America', 'Australia', 'Europe','Asia', 'Latin America', 'Geo Group', 'North America', 'Oceania']
        nafta_dropdown = alt.binding_select(options= nafta_list,name="country")
        nafta_select = alt.selection_single(fields=['Continent TP'], bind=nafta_dropdown, init={'Continent TP': nafta_list[0]})

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['year'], name="Year", init={'year': 2020})

        base2 = alt.Chart(nafta_return_top5)

        line = base2.mark_line().encode(
            x=alt.X('year:N',axis=alt.Axis(title='Year')),
            y=alt.Y('Total Trade ($M):Q',axis=alt.Axis(title='Total Trade Value ($M in USD)')),
            color='Trading Partner',
            tooltip=alt.Tooltip('Total Trade ($M)', format="$,.0f")
        )

        return_chart=line.add_selection(
            nafta_select
            ).transform_filter(
            nafta_select
            ).properties(
                title=title,
                width=width,
                height=height
            )
        return return_chart

    def get_altaire_multi_charts_for_China(self,width=1000,height=600):

        my_data = self.my_data_object
        title = "Percentage of Total Trades Done with China"
        
        df = my_data.get_Chinadata_by_country()
        df = df.rename(columns={'TradePctGDPChange': 'Trade/GDP ratio change'})
        # GDP growth correlation
        china_gdp_df = df[df['Country'] == 'China'][['Country', 'GDP Growth Pct']].reset_index(drop = True)
        other_gdp_df = df[df['Country'] != 'China'][['Country', 'GDP Growth Pct']]
        other_gdp_df = other_gdp_df.drop_duplicates().reset_index(drop = True)
        country_list = df[df['Country'] !='China']['Country'].unique()
        num_country_per_line = math.ceil(len(country_list)/3.0)
        
        gdp_correl = {}
        for country in country_list:
            gdp_correl[country] = china_gdp_df['GDP Growth Pct'].corr(
                other_gdp_df[other_gdp_df['Country']==country]['GDP Growth Pct'].reset_index(drop = True))
        gdp_correl_df = pd.DataFrame(gdp_correl.items(), columns=['Country', 'GDPcorrel_w_China'])
        
        df = df.merge(gdp_correl_df, on = 'Country', how = 'left')
        # Slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        # Pie charts
        base = alt.Chart(df).encode(
            theta=alt.Theta(field="total_trade", type="quantitative"),
            color=alt.Color(field="isChinaPartner", type="nominal",
                            scale = alt.Scale(domain = ['Trades with China', 'GDP Growth Pct', 
                                                        'Trades with Others', 'Trade/GDP ratio change'],
                                              range = ['#265499', '#AFD097', '#2899CC', '#EEBC59']), #'#2f6684', '#ff7c43', '#acc8df', '#665191'
                            legend = alt.Legend(title="Key")),
            
            tooltip=alt.Tooltip('total_trade', format="$,.0f")
        )

        chart1 = alt.hconcat()
        for country in country_list[0:num_country_per_line]: 
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+10), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            chart1 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+30))
        
        chart2 = alt.hconcat()
        for country in country_list[num_country_per_line:num_country_per_line*2]:
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+10), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            chart2 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+30))

        chart3 = alt.hconcat()
        for country in country_list[num_country_per_line*2:]:
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+10), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )

            chart3 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+30))

        # brush selection
        brush_selection = alt.selection_single(fields=['Country'], empty='none')

        # line charts
        dependency_bars = alt.Chart(df).mark_bar(opacity = 0.9, color = '#265499', size = 30).encode(
            x = alt.Y('Country:N', sort='-y',
                      axis=alt.Axis(labelAngle=-30, 
                                    labelOverlap=False,
                                    labelFontSize=12,
                                    labelFontWeight = 'bold')),
            y = 'PercentOfTotal:Q'
        ).transform_calculate(
            PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
        )
        dependency_text = dependency_bars.mark_text(dy = -10).encode(
            x = alt.Y('Country:N', sort='-y', axis = None),
            y = 'PercentOfTotal:Q',
            text=alt.Text("PercentOfTotal:Q", format='.1%')
        )

        dependency_chart = alt.layer(dependency_bars, dependency_text).transform_filter(
            alt.FieldEqualPredicate(field='Year', equal=2020)
        ).transform_filter(
            alt.FieldEqualPredicate(field='isChinaPartner', equal='Trades with China')
        ).resolve_scale(
            x = 'independent'
        ).add_selection(
            brush_selection
        ).properties(
            title="Trade Reliance on China",
            width=(width*0.75),height=(height/10)
        )

        # Correlation fact 
        corr_text = alt.Chart(df).mark_text(size = 40).encode(
            text=alt.Text("GDPcorrel_w_China:Q", format='.1%')
        ).transform_filter(
            brush_selection
        ).transform_filter(
            alt.FieldEqualPredicate(field='Year', equal=2020)
        ).properties(
            title="GDP Growth Correlation with China",
            width=(width*0.25),height=(height/10)
        )

        # ruler selection
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['Year'], empty='none')

        gdp_base = alt.Chart(df).transform_fold(
            ['Trade/GDP ratio change', 'GDP Growth Pct']
        )

        gdp_line = gdp_base.mark_line().encode(
            x = alt.X('Year:O',axis=alt.Axis(labelAngle=0)),
            y = alt.Y('value:Q',axis=alt.Axis(title = 'YoY Growth %', format='.1f')),
            color = 'key:N',
            tooltip=[alt.Tooltip('Year'),
                     alt.Tooltip('Trade/GDP ratio change', format=".2f"),
                     alt.Tooltip('GDP Growth Pct', format=".2f")]
        ).transform_filter(
            brush_selection
        )

        selectors = gdp_base.mark_point().encode(
            x=alt.X('Year:O',axis=alt.Axis(labelAngle=0)),
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        #points = gdp_line.mark_point().encode(
        #    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        #)

        points = gdp_line.mark_point(
            opacity=0.0,
            size=3000
        ).encode(
            x=alt.X('year:O',axis=None),
            y=alt.Y('value:Q',axis=None),
            tooltip=[alt.Tooltip('year'),
                     alt.Tooltip('Trade/GDP ratio change', format=".2f"),
                     alt.Tooltip('GDP Growth Pct', format=".2f")]
        )

        # Draw text labels near the points, and highlight based on selection
        #text = gdp_line.mark_text(align='left', dx=5, dy=-5).encode(
        #    text=alt.condition(nearest, 'value:Q', alt.value(' '))
        #)
        #text = gdp_base.mark_text(align='center', dx=5, dy=-5).encode(
        #    x=alt.X('year:O',axis=None),
        #    y=alt.Y('value:Q',axis=None),
        #    text=alt.Text('value:Q', format='.1f'),
        #    color = 'key:N'
        #).transform_filter(
        #    brush_selection
        #)

        # Draw a rule at the location of the selection
        rules = gdp_base.mark_rule(color='gray').encode(
            x='Year:Q',
        ).transform_filter(
            nearest
        )

        gdp_combine = alt.layer(
            gdp_line#, text #points, selectors,rules,
        ).properties(
            title="GDP and Trade/GDP ratio YoY Growth Percentage" ,width=width,height=(height*3/5-140)
        )

        return_chart = (chart1 & chart2 & chart3 & (dependency_chart | corr_text) & gdp_combine).configure_title(
            baseline="line-top",
            dy = -5
        )
        ## https://stackoverflow.com/questions/67997825/python-altair-generate-a-table-on-selection
        ## https://altair-viz.github.io/user_guide/transform/filter.html?highlight=filter
        ## https://vega.github.io/vega/docs/schemes/
        return return_chart

    def get_asian_trading_partners(self):

        

        indo = self.get_altaire_bar_top5_partners_for_matrix("Indonesia")
        aus = self.get_altaire_bar_top5_partners_for_matrix("Australia")
        sk = self.get_altaire_bar_top5_partners_for_matrix("South Korea")
        jap = self.get_altaire_bar_top5_partners_for_matrix("Japan")

        space_data = pd.DataFrame({'a': list('CCCDDDEEE'),
                                    'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})
        
        space_chart = alt.Chart(space_data).mark_point(opacity=0.0)   

        row_1  = (sk | jap )
        row_3  = (indo | aus )
        my_chart = (space_chart & row_1 & row_3).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                ).resolve_scale(
            color='independent')

        return my_chart

    def get_iran_trade_deal_line_charts(self,width=340,height=200):

        sk = self.get_altaire_line_chart_county_trade_for_matrix("Iran","South Korea",width=width,height=height)
        spain = self.get_altaire_line_chart_county_trade_for_matrix("Iran","Spain",width=width,height=height)
        usa = self.get_altaire_line_chart_county_trade_for_matrix("Iran","United States",width=width,height=height)
        jap = self.get_altaire_line_chart_county_trade_for_matrix("Iran","United Kingdom",width=width,height=height)


        row_1 = (sk | spain )
        row_2  = (usa | jap )
        my_chart = (row_1 & row_2).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                )

        return my_chart

    #am here
    def get_third_page_jcpoa_charts(self,width=340,height=200):
        top_five_partners = self.get_altaire_bar_top5_partners_for_matrix("Iran",width=width,height=height)

        trade  = self.get_import_export_balance_top_five("Iran",for_matrix=True,width=width,height=height)

        t_data = pd.DataFrame({'a': list('CCCDDDEEE'),
                            'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})

        m_dealio = alt.Chart(t_data).mark_point(opacity=0.0)
        
        #am here
        row_1 = (trade | top_five_partners ).resolve_scale(
            color='independent')
        my_chart = (m_dealio & row_1).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                )

        return my_chart

    def get_china_trade_with_us_pie_chart(self,height=200, width=200):
        title = "Percentage of Total Trades Done with China"
        my_data = self.my_data_object
        df = my_data.get_Chinadata_by_country()
        df = df.rename(columns={'TradePctGDPChange': 'Trade/GDP ratio change'})
        # GDP growth correlation
        china_gdp_df = df[df['Country'] == 'China'][['Country', 'GDP Growth Pct']].reset_index(drop = True)
        other_gdp_df = df[df['Country'] != 'China'][['Country', 'GDP Growth Pct']]
        other_gdp_df = other_gdp_df.drop_duplicates().reset_index(drop = True)
        country_list = df[df['Country'] !='China']['Country'].unique()

        country_list = df[df['Country'] =='United States']['Country'].unique()

        num_country_per_line = math.ceil(len(country_list)/3.0)

        gdp_correl = {}
        for country in country_list:
            gdp_correl[country] = china_gdp_df['GDP Growth Pct'].corr(
                other_gdp_df[other_gdp_df['Country']==country]['GDP Growth Pct'].reset_index(drop = True))
        gdp_correl_df = pd.DataFrame(gdp_correl.items(), columns=['Country', 'GDPcorrel_w_China'])

        df = df.merge(gdp_correl_df, on = 'Country', how = 'left')
        # Slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        # Pie charts
        base = alt.Chart(df).encode(
            theta=alt.Theta(field="total_trade", type="quantitative"),
            color=alt.Color(field="isChinaPartner", type="nominal",
                            scale = alt.Scale(domain = ['Trades with China', 'GDP Growth Pct', 
                                                        'Trades with Others', 'Trade/GDP ratio change'],
                                            range = ['#265499', '#AFD097', '#B9CDDB', '#EEBC59']),
                            legend = alt.Legend(title="Key")),

            tooltip=alt.Tooltip('total_trade', format="$,.0f")
        )
        chart1 = alt.hconcat()
        base_pie = base.transform_filter(
            alt.FieldEqualPredicate(field='Country', equal='United States')
        ).mark_arc(outerRadius=(width))

        base_text = base.transform_calculate(
            PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
        ).transform_filter(
            alt.FieldEqualPredicate(field='Country', equal=country)
        ).mark_text(radius=(width+15), size=12).encode(
            text=alt.Text("PercentOfTotal:Q", format='.1%')
        )
        chart1 |= (base_pie+base_text).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).properties(title=country,width=(width),height=(height))

        return chart1


    def china_trade_war_slide_three(self,width=250,height=180):
        china_world = self.get_altaire_line_chart_county_trade_for_matrix("China","World",width=width,height=height)
        united_states_world = self.get_altaire_line_chart_county_trade_for_matrix("United States","World",width=width,height=height)

        row_1 = (china_world | united_states_world ).resolve_scale(
            color='independent')
        my_chart = (row_1).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                )

        return my_chart

    def china_trade_war_slide_four(self,width=250,height=180):
        brazil  = self.get_altaire_line_chart_county_trade_for_matrix("China","Brazil",width=width,height=height)
        brazil_b    = self.get_altaire_dual_pie_chart_by_types_for_matrix("China","Brazil", "exports",width=width,height=height)
        australia  = self.get_altaire_line_chart_county_trade_for_matrix("China","Australia",width=width,height=height)
        australia_b    = self.get_altaire_dual_pie_chart_by_types_for_matrix("China","Australia", "exports",width=width,height=height)
        row_1  = (brazil | brazil_b ).resolve_scale(
            color='independent')
        row_3  = (australia | australia_b ).resolve_scale(
            color='independent')
        my_chart = (row_1 & row_3).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                )

        return my_chart

    def china_trade_war_slide_five(self,width=250,height=180):
        brazil  = self.get_altaire_line_chart_county_trade_for_matrix("United States","Vietnam",width=width,height=height)
        australia  = self.get_altaire_line_chart_county_trade_for_matrix("United States","Malaysia",width=width,height=height)
        row_1  = (brazil | australia ).resolve_scale(
            color='independent')
        my_chart = row_1.configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                )

        return my_chart
        
    def get_altaire_scatter_Covid(self,width=300,height=200):

        my_data = self.my_data_object
        title = "World economy growth in 2020"
        
        df = my_data.get_top20_2020_gdp()
        
        # scatter plot
        base = alt.Chart(df).mark_point().encode(
            x = "GDP Pct Growth:Q",
            y = "Trade Total Change %:Q",
            size = "Inflation, consumer prices",
            color = alt.Color(field="Country", type="nominal", scale=alt.Scale(scheme='tableau20'), legend=None),
            tooltip=[alt.Tooltip('GDP Pct Growth', format=".2f"),
                     alt.Tooltip('Trade Total Change %', format=".2f"),
                     alt.Tooltip('Inflation, consumer prices', format=".2f")]
        )

        text = alt.Chart(df).mark_text(align='center', dy=13).encode(
            x = "GDP Pct Growth:Q",
            y = "Trade Total Change %:Q",
            text="Country:N",
            color = alt.Color(field="Country", type="nominal", scale=alt.Scale(scheme='tableau20'), legend=None)
        )
        xrule = alt.Chart().mark_rule(
            strokeWidth=1
        ).encode(x=alt.datum(0))

        yrule = alt.Chart().mark_rule(
            strokeWidth=1
        ).encode(y=alt.datum(0))
        return (base + text + xrule + yrule)
    
    def get_fourt_page_of_jcpoa_chart(self,width=340,height=200):

        gdp_impact = self.get_time_series_gdp_trade_for_matrix("Iran",width=width,height=height)
        russia  = self.get_altaire_line_chart_county_trade_for_matrix("Iran","Russia",width=width,height=height)


        row_1 = (gdp_impact & russia ).resolve_scale(
            color='independent')
        my_chart = (row_1).configure_axis(
                    grid=False
                ).configure_view(
                    strokeWidth=0
                )

        return my_chart

    def get_china_section_1(self,width=950,height=600):

        my_data = self.my_data_object

        title = "Percentage of Total Trades Done with China"

        df = my_data.get_Chinadata_by_country()
        df = df.rename(columns={'TradePctGDPChange': 'Trade/GDP ratio change'})
        # GDP growth correlation
        china_gdp_df = df[df['Country'] == 'China'][['Country', 'GDP Growth Pct']].reset_index(drop = True)
        other_gdp_df = df[df['Country'] != 'China'][['Country', 'GDP Growth Pct']]
        other_gdp_df = other_gdp_df.drop_duplicates().reset_index(drop = True)
        country_list = df[df['Country'] !='China']['Country'].unique()
        #country_list = df[df['Country'] !='China']['Country'].unique()
        country_list = ['Australia', 'Iran', 'Brazil', 'South Korea', 'Japan', 'Indonesia', 'Saudi Arabia',
                        'Russia', 'United States', 'India', 'Mexico', 'Canada', 'Netherlands', 'United Kingdom',
                        'Germany', 'Italy', 'France', 'Switzerland', 'Spain']

        num_country_per_line = math.ceil(len(country_list)/3.0)

        gdp_correl = {}
        for country in country_list:
            gdp_correl[country] = china_gdp_df['GDP Growth Pct'].corr(
                other_gdp_df[other_gdp_df['Country']==country]['GDP Growth Pct'].reset_index(drop = True))
        gdp_correl_df = pd.DataFrame(gdp_correl.items(), columns=['Country', 'GDPcorrel_w_China'])

        df = df.merge(gdp_correl_df, on = 'Country', how = 'left')
        # Slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        # Pie charts
        base = alt.Chart(df).encode(
            theta=alt.Theta(field="total_trade", type="quantitative"),
            color=alt.Color(field="isChinaPartner", type="nominal",
                            scale = alt.Scale(domain = ['Trades with China', 'GDP Growth Pct', 
                                                        'Trades with Others', 'Trade/GDP ratio change'],
                                            range = ['#156296', '#799D5E', '#B9CDDB', '#E4AB65']),
                            legend = alt.Legend(title="Key")),

            tooltip=alt.Tooltip('total_trade', format="$,.0f")
        )


        chart1 = alt.hconcat()
        for country in country_list[0:num_country_per_line]: 
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+15), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            chart1 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+40))

        chart2 = alt.hconcat()
        for country in country_list[num_country_per_line:num_country_per_line*2]:
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+15), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            chart2 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+40))

        chart3 = alt.hconcat()
        for country in country_list[num_country_per_line*2:]:
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+15), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )

            chart3 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+40))

        # brush selection
        brush_selection = alt.selection_single(fields=['Country'], empty='none')

        # line charts
        dependency_bars = alt.Chart(df).mark_bar(opacity = 0.9, color = '#156296', size = 30).encode(
            x = alt.Y('Country:N', sort='-y',
                    axis=alt.Axis(labelAngle=-30, 
                                    labelOverlap=False,
                                    labelFontSize=12,
                                    labelFontWeight = 'bold')),
            y = 'PercentOfTotal:Q'
        ).transform_calculate(
            PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
        )
        dependency_text = dependency_bars.mark_text(dy = -10).encode(
            x = alt.Y('Country:N', sort='-y', axis = None),
            y = 'PercentOfTotal:Q',
            text=alt.Text("PercentOfTotal:Q", format='.1%')
        )

        dependency_chart = alt.layer(dependency_bars, dependency_text).transform_filter(
            alt.FieldEqualPredicate(field='Year', equal=2020)
        ).transform_filter(
            alt.FieldEqualPredicate(field='isChinaPartner', equal='Trades with China')
        ).resolve_scale(
            x = 'independent'
        ).add_selection(
            brush_selection
        ).properties(
            title="Trade Reliance on China",
            width=(width*0.75),height=(height/10+50)
        )

        # Correlation fact 
        corr_text = alt.Chart(df).mark_text(size = 40).encode(
            text=alt.Text("GDPcorrel_w_China:Q", format='.1%')
        ).transform_filter(
            brush_selection
        ).transform_filter(
            alt.FieldEqualPredicate(field='Year', equal=2020)
        ).properties(
            title="GDP Growth Correlation with China",
            width=(width*0.25),height=(height/10+50)
        )

        # ruler selection
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['Year'], empty='none')

        gdp_base = alt.Chart(df).transform_fold(
            ['Trade/GDP ratio change', 'GDP Growth Pct']
        )
        
        gdp_line = gdp_base.mark_line().encode(
            x = alt.X('Year:O',axis=alt.Axis(labelAngle=0)),
            y = alt.Y('value:Q',axis=alt.Axis(title = 'YoY Growth %', format='.1f')),
            color=alt.Color(field="key", type="nominal",
                            scale = alt.Scale(domain = ['GDP Growth Pct', 'Trade/GDP ratio change'],
                                            range = ['#799D5E', '#E4AB65']),
                            legend = alt.Legend(title="Key")),
            tooltip=[alt.Tooltip('Year'),
                    alt.Tooltip('Trade/GDP ratio change', format=".2f"),
                    alt.Tooltip('GDP Growth Pct', format=".2f")]
        ).transform_filter(
            brush_selection
        )

        selectors = gdp_base.mark_point().encode(
            x=alt.X('Year:O',axis=alt.Axis(labelAngle=0)),
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        #points = gdp_line.mark_point().encode(
        #    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        #)

        points = gdp_line.mark_point(
            opacity=0.0,
            size=3000
        ).encode(
            x=alt.X('year:O',axis=None),
            y=alt.Y('value:Q',axis=None),
            tooltip=[alt.Tooltip('year'),
                    alt.Tooltip('Trade/GDP ratio change', format=".2f"),
                    alt.Tooltip('GDP Growth Pct', format=".2f")]
        )

        # Draw text labels near the points, and highlight based on selection
        #text = gdp_line.mark_text(align='left', dx=5, dy=-5).encode(
        #    text=alt.condition(nearest, 'value:Q', alt.value(' '))
        #)
        #text = gdp_base.mark_text(align='center', dx=5, dy=-5).encode(
        #    x=alt.X('year:O',axis=None),
        #    y=alt.Y('value:Q',axis=None),
        #    text=alt.Text('value:Q', format='.1f'),
        #    color = 'key:N'
        #).transform_filter(
        #    brush_selection
        #)

        # Draw a rule at the location of the selection
        rules = gdp_base.mark_rule(color='gray').encode(
            x='Year:Q',
        ).transform_filter(
            nearest
        )

        gdp_combine = alt.layer(
            gdp_line#, text #points, selectors,rules,
        ).properties(
            title="GDP Growth and Trade/GDP Ratio Change YoY" ,width=width,height=(height*3/5-50)
        )

        return_chart = (chart1 & chart2 & chart3 ).configure_title(
            baseline="line-top",
            dy = -5
        )
        # return_chart = (chart1 & chart2 & chart3 & (dependency_chart | corr_text) & gdp_combine).configure_title(
        #     baseline="line-top",
        #     dy = -5
        # )

        ## https://stackoverflow.com/questions/67997825/python-altair-generate-a-table-on-selection
        ## https://altair-viz.github.io/user_guide/transform/filter.html?highlight=filter
        ## https://vega.github.io/vega/docs/schemes/        
        return return_chart

    def get_china_section_2(self,width=950,height=600):

        my_data = self.my_data_object

        title = "Percentage of Total Trades Done with China"

        df = my_data.get_Chinadata_by_country()
        df = df.rename(columns={'TradePctGDPChange': 'Trade/GDP ratio change'})
        # GDP growth correlation
        china_gdp_df = df[df['Country'] == 'China'][['Country', 'GDP Growth Pct']].reset_index(drop = True)
        other_gdp_df = df[df['Country'] != 'China'][['Country', 'GDP Growth Pct']]
        other_gdp_df = other_gdp_df.drop_duplicates().reset_index(drop = True)
        #country_list = df[df['Country'] !='China']['Country'].unique()
        country_list = ['Australia', 'Iran', 'Brazil', 'South Korea', 'Japan', 'Indonesia', 'Saudi Arabia',
                        'Russia', 'United States', 'India', 'Mexico', 'Canada', 'Netherlands', 'United Kingdom',
                        'Germany', 'Italy', 'France', 'Switzerland', 'Spain']

        num_country_per_line = math.ceil(len(country_list)/3.0)

        gdp_correl = {}
        for country in country_list:
            gdp_correl[country] = china_gdp_df['GDP Growth Pct'].corr(
                other_gdp_df[other_gdp_df['Country']==country]['GDP Growth Pct'].reset_index(drop = True))
        gdp_correl_df = pd.DataFrame(gdp_correl.items(), columns=['Country', 'GDPcorrel_w_China'])

        df = df.merge(gdp_correl_df, on = 'Country', how = 'left')
        # Slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        # Pie charts
        base = alt.Chart(df).encode(
            theta=alt.Theta(field="total_trade", type="quantitative"),
            color=alt.Color(field="isChinaPartner", type="nominal",
                            scale = alt.Scale(domain = ['Trades with China', 'GDP Growth Pct', 
                                                        'Trades with Others', 'Trade/GDP ratio change'],
                                            range = ['#156296', '#799D5E', '#B9CDDB', '#E4AB65']),
                            legend = alt.Legend(title="Key")),

            tooltip=alt.Tooltip('total_trade', format="$,.0f")
        )


        chart1 = alt.hconcat()
        for country in country_list[0:num_country_per_line]: 
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+15), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            chart1 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+40))

        chart2 = alt.hconcat()
        for country in country_list[num_country_per_line:num_country_per_line*2]:
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+15), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            chart2 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+40))

        chart3 = alt.hconcat()
        for country in country_list[num_country_per_line*2:]:
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+15), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )

            chart3 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+40))

        # brush selection
        brush_selection = alt.selection_single(fields=['Country'], empty='none', init={'Country': 'Australia'})

        # line charts
        dependency_bars = alt.Chart(df).mark_bar(opacity = 0.9, color = '#156296', size = 30).encode(
            x = alt.Y('Country:N', sort='-y',
                    axis=alt.Axis(labelAngle=-30, 
                                    labelOverlap=False,
                                    labelFontSize=12,
                                    labelFontWeight = 'bold')),
            y = 'PercentOfTotal:Q'
        ).transform_calculate(
            PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
        )
        dependency_text = dependency_bars.mark_text(dy = -10).encode(
            x = alt.Y('Country:N', sort='-y', axis = None),
            y = 'PercentOfTotal:Q',
            text=alt.Text("PercentOfTotal:Q", format='.1%')
        )

        dependency_chart = alt.layer(dependency_bars, dependency_text).transform_filter(
            alt.FieldEqualPredicate(field='Year', equal=2020)
        ).transform_filter(
            alt.FieldEqualPredicate(field='isChinaPartner', equal='Trades with China')
        ).resolve_scale(
            x = 'independent'
        ).add_selection(
            brush_selection
        ).properties(
            title="Trade Reliance on China",
            width=(width*0.75),height=(height/10+50)
        )

        # Correlation fact 
        corr_text = alt.Chart(df).mark_text(size = 40).encode(
            text=alt.Text("GDPcorrel_w_China:Q", format='.1%')
        ).transform_filter(
            brush_selection
        ).transform_filter(
            alt.FieldEqualPredicate(field='Year', equal=2020)
        ).properties(
            title="GDP Growth Correlation with China",
            width=(width*0.25),height=(height/10+50)
        )

        # ruler selection
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['Year'], empty='none')

        gdp_base = alt.Chart(df).transform_fold(
            ['Trade/GDP ratio change', 'GDP Growth Pct']
        )

        gdp_line = gdp_base.mark_line().encode(
            x = alt.X('Year:O',axis=alt.Axis(labelAngle=0)),
            y = alt.Y('value:Q',axis=alt.Axis(title = 'YoY Growth %', format='.1f')),
            color=alt.Color(field="key", type="nominal",
                            scale = alt.Scale(domain = ['GDP Growth Pct', 'Trade/GDP ratio change'],
                                            range = ['#799D5E', '#E4AB65']),
                            legend = alt.Legend(title="Key")),
            tooltip=[alt.Tooltip('Year'),
                    alt.Tooltip('Trade/GDP ratio change', format=".2f"),
                    alt.Tooltip('GDP Growth Pct', format=".2f")]
        ).transform_filter(
            brush_selection
        )

        selectors = gdp_base.mark_point().encode(
            x=alt.X('Year:O',axis=alt.Axis(labelAngle=0)),
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        #points = gdp_line.mark_point().encode(
        #    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        #)

        points = gdp_line.mark_point(
            opacity=0.0,
            size=3000
        ).encode(
            x=alt.X('year:O',axis=None),
            y=alt.Y('value:Q',axis=None),
            tooltip=[alt.Tooltip('year'),
                    alt.Tooltip('Trade/GDP ratio change', format=".2f"),
                    alt.Tooltip('GDP Growth Pct', format=".2f")]
        )

        # Draw text labels near the points, and highlight based on selection
        #text = gdp_line.mark_text(align='left', dx=5, dy=-5).encode(
        #    text=alt.condition(nearest, 'value:Q', alt.value(' '))
        #)
        #text = gdp_base.mark_text(align='center', dx=5, dy=-5).encode(
        #    x=alt.X('year:O',axis=None),
        #    y=alt.Y('value:Q',axis=None),
        #    text=alt.Text('value:Q', format='.1f'),
        #    color = 'key:N'
        #).transform_filter(
        #    brush_selection
        #)

        # Draw a rule at the location of the selection
        rules = gdp_base.mark_rule(color='gray').encode(
            x='Year:Q',
        ).transform_filter(
            nearest
        )

        gdp_combine = alt.layer(
            gdp_line#, text #points, selectors,rules,
        ).properties(
            title="GDP Growth and Trade/GDP Ratio Change YoY" ,width=width,height=(height*3/5-50)
        )

        return_chart = ((dependency_chart | corr_text) & gdp_combine).configure_title(
            baseline="line-top",
            dy = -5
        )

        ## https://stackoverflow.com/questions/67997825/python-altair-generate-a-table-on-selection
        ## https://altair-viz.github.io/user_guide/transform/filter.html?highlight=filter
        ## https://vega.github.io/vega/docs/schemes/        
        return return_chart        

    def get_nafta_section_1(self):
        chart1 = self.get_nafta_trade_data_pcts()
        chart2 = self.get_nafta_world_trade_chart('NAFTA')
        #US will Start NAFTA Charts tomorrow morning
        us=     self.get_altaire_bar_top5_partners_for_matrix('United States')
        mexico= self.get_altaire_bar_top5_partners_for_matrix('Mexico')
        canada= self.get_altaire_bar_top5_partners_for_matrix('Canada')
        
        row_1 = (chart1|chart2).resolve_scale(
            color='independent')
        row_2 = (us | mexico ).resolve_scale(
            color='independent')
        row_3 = (canada).resolve_scale(
            color='independent')
        return_chart = (row_1 & row_2 & row_3)
        return return_chart

    def get_nafta_section_2(self):
        nafta = self.get_trade_group_gdp_growth_chart('NAFTA')
        canada = self.get_import_export_type_chart('Canada')
        imports = self.get_gdp_per_cap_lcu_chart('Mexico')
        row_1 = (nafta | imports).resolve_scale(
            color='independent')
        row_2 = canada
        return_chart = (row_1 & row_2)
        return return_chart
        
    # def get_nafta_section_1_1(self):
    #     #CHARTS
    #     nafta1=self.get_nafta_world_inter_trade()
    #     nafta2=self.get_nafta_world_trade_chart('NAFTA')
    #     #continent=self.nafta_continental_trade_partners_top5(height=250,width=350)
    #     continent=self.nafta_continental_trade()

    #     space_data = pd.DataFrame({'a': list('CCCDDDEEE'),
    #                                 'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})
        
    #     space_chart = alt.Chart(space_data).mark_point(opacity=0.0)

    #     row_1 = (nafta1|nafta2).resolve_scale(
    #         color='independent')
    #     row_2 = (continent ).resolve_scale(
    #         color='independent')
    #     row_1_2 = (space_chart & row_1)
    #     return_chart = (row_1_2 & row_2)
    #     return return_chart
        
    def get_nafta_section_1_1(self):
        #CHARTS
        cont_cont=self.nafta_continental_trade_partners_top5_country_cont()
        #cont_tp_t5=self.nafta_continental_trade_partners_top5_country()
        inter=self.get_nafta_world_inter_trade()
        space_data = pd.DataFrame({'a': list('CCCDDDEEE'),
                                 'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})
        
        space_chart = alt.Chart(space_data).mark_point(opacity=0.0)

        row_1 = alt.hconcat(inter,cont_cont).resolve_scale(color='independent')
        return_chart = alt.vconcat(row_1)
        
        return return_chart

    def get_nafta_section_2_1(self):
        #CHARTS
        #cont_cont=self.nafta_continental_trade_partners_top5_country_cont()
        cont_tp_t5=self.nafta_continental_trade_partners_top5_country()
        row_1 = cont_tp_t5.resolve_scale(color='independent')

        space_data = pd.DataFrame({'a': list('CCCDDDEEE'),
                                 'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})
        
        space_chart = alt.Chart(space_data).mark_point(opacity=0.0)

        return_chart = alt.vconcat(space_chart,row_1)
        
        return return_chart

    def get_nafta_section_3_1(self):
        #CHARTS
        gdp_change=self.get_trade_group_gdp_growth_chart('NAFTA')
        #impexp=self.get_import_export_prod_type_chart()
        gdp=self.get_gdp_per_cap_lcu_chart('Canada')
        impexp=self.get_nafta_import_export_pie_chart()
        employ=self.get_gdp_unemployment()

        space_data = pd.DataFrame({'a': list('CCCDDDEEE'),
                            'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})
        
        space_chart = alt.Chart(space_data).mark_point(opacity=0.0)

        row_1 = (gdp_change | employ ).resolve_scale(color='independent')
        row_2 = (impexp).resolve_scale(color='independent')
        row_1_2 = (space_chart & row_1)
        return_chart = alt.vconcat(row_1_2,row_2)
        return return_chart

    def get_eu_section_1(self):

        #chart1 = self.get_eu_domestic_trading_chart()
        chart2 = self.get_eu_versus_noneu_trading_chart()
        #US will Start NAFTA Charts tomorrow morning
        
        # row_1 = (chart1).resolve_scale(
        #     color='independent')

        space_data = pd.DataFrame({'a': list('CCCDDDEEE'),
                                    'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})
        
        space_chart = alt.Chart(space_data).mark_point(opacity=0.0)


        row_2 = (chart2).resolve_scale(
            color='independent')


        my_chart = (space_chart & row_2 ).configure_axis(
        grid=False
        ).configure_view(
        strokeWidth=0
        )

        return my_chart

    def get_eu_section_1a(self):

        chart1 = self.get_eu_domestic_trading_chart()
        #chart2 = self.get_eu_versus_noneu_trading_chart()
        #US will Start NAFTA Charts tomorrow morning
        
        # row_1 = (chart1).resolve_scale(
        #     color='independent')

        space_data = pd.DataFrame({'a': list('CCCDDDEEE'),
                                    'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})
        
        space_chart = alt.Chart(space_data).mark_point(opacity=0.0)   

        row_2 = (space_chart & chart1).resolve_scale(
            color='independent')


        my_chart = (row_2 ).configure_axis(
        grid=False
        ).configure_view(
        strokeWidth=0
        )

        return my_chart


    def get_eu_section_2(self):

        chart1 = self.get_altaire_multi_charts_for_EU()
        
        row_1 = (chart1).resolve_scale(
            color='independent')
        return_chart = (row_1)
        return return_chart

    def get_altaire_yoy_trade_per_GDP_for_matrix(self,source_country,target_country,width=300,height=200):

        my_data = self.my_data_object
        title =  "Exports/GDP YoY Change by Sector Breakdown"
        
        df = my_data.imports_exports_GDP_by_sectors(source_country, target_country)
        domain_x = [min(df['yoy_export_GDP_change']), max(df['yoy_export_GDP_change'])]

        # A slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        base = alt.Chart(df)

        bars = base.mark_bar(size = 30).encode(
            x=alt.X('yoy_export_GDP_change:Q',axis=alt.Axis(title='Year Over Year Trade/GDP Change by Sector', format=".1%")),
            y=alt.Y('Country:N',axis=alt.Axis(title='Country')),
            color = alt.Color(field="sector", type="nominal", scale=alt.Scale(scheme='tableau20')),
            tooltip= [alt.Tooltip('sector'),
                      alt.Tooltip('yoy_export_GDP_change', format=".2%")]
        )

        xrule = base.mark_rule(
            strokeWidth=1
        ).encode(x=alt.datum(0))

        return_chart = alt.layer(bars, xrule).add_selection(
            slider_selection
        ).transform_filter(
            slider_selection
        ).properties(
            title=title,
            width=width,
            height=height
        )
        return return_chart

    def get_nafta_section_1a(self,width=950,height=600):

        my_data = self.my_data_object

        title = "Percentage of Total Trades Done with NAFTA"

        df = my_data.get_nafta_by_country()
        df = df.rename(columns={'TradePctGDPChange': 'Trade/GDP ratio change'})
        # GDP growth correlation
        china_gdp_df = df[df['Country'] == 'China'][['Country', 'GDP Growth Pct']].reset_index(drop = True)
        other_gdp_df = df[df['Country'] != 'China'][['Country', 'GDP Growth Pct']]
        other_gdp_df = other_gdp_df.drop_duplicates().reset_index(drop = True)
        country_list = df[df['Country'] !='China']['Country'].unique()
        #country_list = df[df['Country'] !='China']['Country'].unique()

        country_list = [ 'Japan','China','South Korea', 'Brazil','India',  'Switzerland', 'Indonesia', 'United Kingdom','Australia'
                        ,'Saudi Arabia', 'Italy', 'Netherlands', 'Germany',  'France','Russia',
                          'Spain','Iran']

        num_country_per_line = math.ceil(len(country_list)/3.0)

        gdp_correl = {}
        for country in country_list:
            gdp_correl[country] = china_gdp_df['GDP Growth Pct'].corr(
                other_gdp_df[other_gdp_df['Country']==country]['GDP Growth Pct'].reset_index(drop = True))
        gdp_correl_df = pd.DataFrame(gdp_correl.items(), columns=['Country', 'GDPcorrel_w_China'])

        df = df.merge(gdp_correl_df, on = 'Country', how = 'left')
        # Slider filter
        year_slider = alt.binding_range(min=2014, max=2020, step=1)
        slider_selection = alt.selection_single(bind=year_slider, fields=['Year'], name="Year", init={'Year': 2020})

        # Pie charts
        base = alt.Chart(df).encode(
            theta=alt.Theta(field="total_trade", type="quantitative"),
            color=alt.Color(field="isChinaPartner", type="nominal",
                            scale = alt.Scale(domain = ['Trades with NAFTA', 'GDP Growth Pct', 
                                                        'Trades with Others', 'Trade/GDP ratio change'],
                                            range = ['#156296', '#799D5E', '#B9CDDB', '#E4AB65']),
                            legend = alt.Legend(title="Key")),

            tooltip=alt.Tooltip('total_trade', format="$,.0f")
        )


        chart1 = alt.hconcat()
        for country in country_list[0:num_country_per_line]: 
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+15), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            chart1 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+40))

        chart2 = alt.hconcat()
        for country in country_list[num_country_per_line:num_country_per_line*2]:
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+15), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )
            chart2 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+40))

        chart3 = alt.hconcat()
        for country in country_list[num_country_per_line*2:]:
            base_pie = base.transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_arc(outerRadius=(width/35))

            base_text = base.transform_calculate(
                PercentOfTotal="datum.total_trade / datum.total_toWorld_trade"
            ).transform_filter(
                alt.FieldEqualPredicate(field='Country', equal=country)
            ).mark_text(radius=(width/30+15), size=12).encode(
                text=alt.Text("PercentOfTotal:Q", format='.1%')
            )

            chart3 |= (base_pie+base_text).add_selection(
                slider_selection
            ).transform_filter(
                slider_selection
            ).properties(title=country,width=(width/8),height=(height/10+40))


        return_chart = (chart1 & chart2 & chart3 ).configure_title(
            baseline="line-top",
            dy = -5
        )
        # return_chart = (chart1 & chart2 & chart3 & (dependency_chart | corr_text) & gdp_combine).configure_title(
        #     baseline="line-top",
        #     dy = -5
        # )

        ## https://stackoverflow.com/questions/67997825/python-altair-generate-a-table-on-selection
        ## https://altair-viz.github.io/user_guide/transform/filter.html?highlight=filter
        ## https://vega.github.io/vega/docs/schemes/        
        return return_chart
