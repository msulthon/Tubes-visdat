#!/usr/bin/env python
# coding: utf-8

# import library
import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.models import Legend
from bokeh.palettes import Spectral6, Turbo256
import colorcet as cc
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import Slider, Select

# import dataset
data = pd.read_csv("./covid.csv")

# drop nan value
df2=data.dropna(how='all')

# format years
df2['Year'] = pd.DatetimeIndex(df2['Date']).year
df2.set_index('Year', inplace=True)

# rename column
df2.rename(columns = {'New Cases':'newcases', 'New Deaths':'newdeaths', 'New Recovered':'newrecovered', 'New Active Cases':'newactivecases', 'Total Cases':'totalcases', 'Total Deaths':'totaldeaths', 'Total Recovered':'totalrecovered'}, inplace = True)

# location list for categorical color
df2 = df2[df2["Location"] != "Indonesia"]
locations_list = df2.Location.unique().tolist()

# make color mapper from location list
color_mapper = CategoricalColorMapper(factors=locations_list, palette=cc.glasbey)


# Make the ColumnDataSource: source
source = ColumnDataSource(data={
    'x'       : df2.loc[2020].totalcases,
    'y'       : df2.loc[2020].totaldeaths,
    'country' : df2.loc[2020].Island,
    'pop'     : (df2.loc[2020].Population / 20000000) + 2,
    'region'  : df2.loc[2020].Location,
})


# Create the figure: plot
plot = figure(title='Persebaran kasus covid 19 di tiap provinsi tahun 2020', x_axis_label='Total Cases', y_axis_label='Total Deaths',
           plot_height=750, plot_width=1000,
             title_location='above', tools = ['pan, wheel_zoom, box_zoom, reset','tap'])

# adding hover tools to plot
plot.add_tools(HoverTool(tooltips = [('Location','@region'),
                                  ('x', '@x'),
                                  ('y', '@y'),]))

# add legend to right side the layout
plot.add_layout(Legend(), 'right')

# Add a circle glyph to the plot
plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
           color=dict(field='region', transform=color_mapper), legend_group='region')

# Set the legend text and align
plot.legend.label_text_font_size = '6pt'
plot.title.align = 'center'


# Define the callback function: update_plot
def update_plot(attr, old, new):
    # set the `yr` name to `slider.value` and `source.data = new_data`
    yr = slider.value
    x = x_select.value
    y = y_select.value
    
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    
    # new data
    new_data = {
    'x'       : df2.loc[yr][x],
    'y'       : df2.loc[yr][y],
    'country' : df2.loc[yr].Island,
    'pop'     : (df2.loc[yr].Population / 20000000) + 2,
    'region'  : df2.loc[yr].Location,
    }
    source.data = new_data
    
    # Add title to figure: plot.title.text
    plot.title.text = 'Covid Cases data of Indonesia for %d per province' % yr

    
# Make a slider object: slider
slider = Slider(start=2020, end=2021, step=1, value=2020, title='Year')
slider.on_change('value',update_plot)

# Make dropdown menu for x and y axis
# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['totalcases', 'totaldeaths', 'totalrecovered', 'newcases', 'newdeaths', 'newrecovered', 'newactivecases'],
    value='totalcases',
    title='x-axis data'
)
# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['totalcases', 'totaldeaths', 'totalrecovered', 'newcases', 'newdeaths', 'newrecovered', 'newactivecases'],
    value='totaldeaths',
    title='y-axis data'
)
# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot)
    
# Create layout and add to current document
layout = row(plot, widgetbox(slider, x_select, y_select))
curdoc().add_root(layout)
