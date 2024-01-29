import panel as pn
import pandas as pd
import numpy as np
import hvplot.pandas as hvplot
pn.extension()

#imports the data of the file runners.tsv 
hardloop = pd.read_csv('runners.tsv', delimiter='\t')

#if sleep is empty replace it with 0
hardloop['SLEEP'] = hardloop['SLEEP'].fillna(0)
#adds the sleep of morning and evening together so you get the sleep of the past 24 hours.
hardloop['SLEEP'] = hardloop['SLEEP'] + hardloop['SLEEP'].shift(fill_value=0)
# sets sleep to 12 hours if it goes over 12
hardloop['SLEEP'] = np.where(hardloop['SLEEP'] > 12, 12, hardloop['SLEEP'])

#removes all the lines that dont have TQR or RPE data
hardloop = hardloop[hardloop['TQR'].notna() & hardloop['TQR'] != 0]
hardloop = hardloop[hardloop['RPE'].notna() & hardloop['RPE'] != 0]

#adds a time to the data so that there isn't two data points per date
hardloop['HOUR'] = np.where(hardloop['MOMENT'] == 'A', 0, 12)
hardloop['DATES'] = pd.to_datetime(hardloop['DATES'], format='%d-%b-%y')
hardloop['DATES'] = hardloop['DATES'] + pd.to_timedelta(hardloop['HOUR'], unit='h')

#changes moment to morning or evening
hardloop['MOMENT'] = np.where(hardloop['MOMENT'] == 'A', 'Evening', 'Morning')

#removes the hour and TQR_OF_RPE column because they are unnescecary
hardloop = hardloop.drop('HOUR', axis=1)
hardloop = hardloop.drop("TQR_OF_RPE", axis=1)

#read the data in the file injury.tsv
blessure = pd.read_csv('injury.tsv', delimiter="\t")

#create a collumn for the injury so that you can later select for it when creating the plots
hardloop['blessure'] = 'no injury'

#convert the dates in injury to usable dates
blessure['DATE_START'] = pd.to_datetime(blessure['DATE_START'], format='%d-%b-%y')
blessure['DATE_END'] = pd.to_datetime(blessure['DATE_END'], format='%d-%b-%y')

#fill the injury collumn with the suffered injuries
for i, row in blessure.iterrows():
    start_date = row['DATE_START']
    end_date = row['DATE_END']
    condition = (hardloop['PERSON_ID'] == row['PERSON_ID']) & (hardloop['DATES'] >= start_date) & (hardloop['DATES'] <= end_date)
    hardloop.loc[condition, 'blessure'] = row['DIAGNOSE']

#create a list of all the person ids
id_list = hardloop['PERSON_ID'].unique().tolist()

#convert the ids to integers
for i in range(len(id_list)):
    id_list[i] = int(id_list[i])

#sort the ids
id_list = sorted(id_list)

#the selectable metrics
metrics = ['RPE','TQR','DURATION']

#create the widgets
#create the select boxes to chose between the metrics
metric_select_1 = pn.widgets.Select(name='Select Metric', options=metrics)
metric_select_2 = pn.widgets.Select(name='Select Metric', options=metrics)

#create the select boxes to chose between the person ids
select_person_1 = pn.widgets.Select(name='Select Person', options=id_list)
select_person_2 = pn.widgets.Select(name='Select Person', options=id_list)

#this function creates the line plots for the metrics over time
def line_plot(id, metric):
    """
    Generate a line plot for a specific person and metric over time.

    Parameters:
    - id (int): Person ID.
    - metric (str):TQR, RPE or DURATION.

    Returns:
    A line plot showing a metric over change for a person.
    """
    person_data = hardloop[hardloop['PERSON_ID'] == id]

    plot = person_data.hvplot.line(
        x='DATES', y=metric, groupby='blessure',
        title=f'{metric} per day for person {id}',
        xlabel='Date', ylabel=metric,
        grid=True, width=700, height=300, rot=45
    )

    plot.opts(shared_axes=False)
    return plot


def box_plot(id, metric):
    """
    Generate a box plot for a specific person and metric, comparing morning and evening data.

    Parameters:
    - id (int): Person ID.
    - metric (str): TQR, RPE or DURATION.

    Returns:
    A box plot showing the range of a metric per person for morning and evening
    """
    person_data = hardloop[hardloop['PERSON_ID'] == id]

    plot = person_data.hvplot.box(
        y=metric, by='MOMENT',
        title=f'{metric} difference between morning and evening for person {id}',
        grid=True, width=700, height=300, rot=45
    )

    plot.opts(shared_axes=False)
    return plot


def sleep_plot(id, metric):
    """
    Generate a line plot showing the average metric per hour of sleep for a specific person.

    Parameters:
    - id (int): Person ID.
    - metric (str): TQR, RPE or DURATION.

    Returns:
    A plot representing the average metric per hour slept.
    """
    person_data = hardloop[hardloop['PERSON_ID'] == id]

    plot = person_data.groupby('SLEEP')[metric].mean().hvplot.line(
        xlabel='Sleep(h)',
        ylabel=f'Average {metric}',
        title=f'Average {metric} per hour of sleep for person {id}',
        grid=True, width=700, height=500
    )

    plot.opts(shared_axes=False)

    return plot

#these depends are used to display the plots on the dashboard
@pn.depends(id=select_person_1.param.value, metric=metric_select_1.param.value)
def line1(id, metric):
    plot = line_plot(id, metric)
    return plot

@pn.depends(id=select_person_1.param.value, metric=metric_select_1.param.value)
def box1(id, metric):
    plot = box_plot(id, metric)
    return plot

@pn.depends(id=select_person_1.param.value, metric=metric_select_1.param.value)
def sleep1(id, metric):
    plot = sleep_plot(id, metric)
    return plot

@pn.depends(id=select_person_2.param.value, metric=metric_select_2.param.value)
def line2(id, metric):
    plot = line_plot(id, metric)
    return plot

@pn.depends(id=select_person_2.param.value, metric=metric_select_2.param.value)
def box2(id, metric):
    plot = box_plot(id, metric)
    return plot

@pn.depends(id=select_person_2.param.value, metric=metric_select_2.param.value)
def sleep2(id, metric):
    plot = sleep_plot(id, metric)
    return plot

#this makes the app consist out of tabs 
app = pn.Tabs()

#creates the header for the dashboard
header = '# Runners Visualized'

#this difines the layout for the dashboard by using rows and columns
layout = pn.Row(
   pn.Column(
      pn.Row(select_person_1),
      pn.Row(metric_select_1),
      pn.Row(line1),
      pn.Row(box1),
      pn.Row(sleep1)
   ),
   pn.Column(
      pn.Row(select_person_2),
      pn.Row(metric_select_2),
      pn.Row(line2),
      pn.Row(box2),
      pn.Row(sleep2)
   )
)


#combine header and layout to create the full dashboard
plot_layout = pn.Column(
    header,
    pn.Row(
        layout
    )
)

#content for the info tab
info = """# what is runners visualized?
 ### runners visualized is a dashboard that attempts to visualize data from people that recorded certain statistics about their runs for a long period of time.
 ### It also shows how these statistics change during injuries the runners have received. Runners visualized has three different plot types. The first plot type is a line
 ### graph of certain statistics over time, that also allows you to view the change in the statistic when injuries are suffered. The second plot type are two boxplots that
 ### show the difference in the range of the statistics between the morning and the evening. And the third plot is a scatter plot of how the statistics change for how many
 ### hours people have slept. The dashboard also contains an info page explaining the dashboard. And a tab that shows all of the injuries suffered.
 
 # What are the metrics?
 ## RPE
 ### RPE stands for the Rate of Perceived Exertion. It is a subjective scale of 1 to 20 where the runners wrote down how much they feel they exerted themselves.

 ## TQR
 ### TQR stands for the Total Quality of Recovery. It is a subjective scale of 1 to 20 where the runners wrote down how well they felt they had recovered since the last 
 ### time they ran.

 ## DURATION
 ### DURATION is how long the runners ran in minutes.
 """

#this creates the tabs with the correct content
app.append(('Plots', plot_layout))
app.append(('Info', info))
app.append(('Injuries', blessure))

#start the app
app.show()
