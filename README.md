# Runners visualized

## What is runners visualized?
runners visualized is a dashboard that attempts to visualize data from people that recorded certain statistics about their runs for a long period of time. It also shows how these statistics change during injuries the runners have received. Runners visualized has three different plot types. The first plot type is a line graph of certain statistics over time, that also allows you to view the change in the statistic when injuries are suffered. The second plot type are two boxplots that show the difference in the range of the statistics between the morning and the evening. And the third plot is a scatter plot of how the statistics change for how many hours people have slept. The dashboard also contains an info page explaining the dashboard. And a tab that shows all of the injuries suffered.

## How to use runners visualized?
### With the provided data
Using runners visualized with the provided data is very simple. Download all the files from the git repository and place them in the same directory. Then open the file runners_visualied.py with a programme like visual studio code or pycharm. Then run runners_visualized.py with that programme. If everything went as it is supposed to go a new browser tab should open and the dashboard should appear. 

### With different data
Using runners visualized with your own data is certainly possible. The data you use has to have the same structure as the provided data. When you want to create the dashboard with your own data you can either replace the data in the runners.tsv and injuries.tsv files. If you want to use files with diferent names you will have to change the runners_visualized.py file. the easiest way to do this is to press Ctrl+f and search for runners.tsv and replace it with the name of your file containing the data of the runners. And you do the same for the injuries.tsv file.

## The data
The data in this git repository has been provided by Talko Dijkhuis. The data is represented in a tsv format and consists of two files: runners.tsv and injuries.tsv. runners.tsv is a diary of people that ran for a certain amount of time. It contains how long they ran for, at what time of the day they ran, how high their perceived rate of exertion is, how high their total quality of recovery is and how much they slept. injuries.tsv is a log of all the injuries that have been suffered by the runners
