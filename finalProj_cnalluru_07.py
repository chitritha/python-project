"""
Program: Commodity Data Filtering Final
Author: Nalluru Chitritha Chowdary
Description: This program is used to filter and represent data based on user inputs
Revisions:
00 - Importing CSV, datetime and plotly modules
01 - Printing announcement
02 - Import data from CSV file and change into required format
03 - Compiling list of all Commodities, dates and locations in dictionaries
04 - Asking user input on the commodities, dates and locations required
05 - Filtering out the records based on the user criteria
06 - Creating a dict with commodities and locations as key and average of the prices as values
07 - Plotting the data using plotly
"""
### Step 1 - Importing CSV, datetime and plotly modules
import csv
import itertools
import sys
from _datetime import datetime
import plotly.offline as py
import plotly.graph_objs as go

### Step 2 - Printing announcement
print('=' * 26, '\nAnalysis of Commodity Data\n', '=' * 26, '\n', sep='')

### Step 3 - Import data from CSV file and change into required format
data = []
csvfile = open('produce_csv.csv', 'r')
reader = csv.reader(csvfile)
for row in reader:
    if reader.line_num == 1:
        locations = row[2:]
    else:
        for location, value in zip(locations, row[2:]):  # iterate through locations and values
            row_num = len(data)  # index for the data row
            data.append(row[:1])  # new data row: commodity
            data[row_num].append(datetime.strptime(row[1], '%m/%d/%Y'))  # append date
            data[row_num].append(location)  # append location
            data[row_num].append(float(value.replace('$', '')))  # append price value
csvfile.close()

### Step 4 - Compiling list of all Commodities, dates and locations in dictionaries
commList = dict()
for num, commodity in enumerate(sorted(set(x[0] for x in data))):
    commList[num] = commodity  # Creating dict with index as keys and commodity as values
dateList = dict()
for num, date in enumerate(sorted(set(x[1] for x in data))):
    dateList[num] = date.strftime('%Y-%m-%d')
    # Creating dict with index as keys and dates in string format as values
locList = dict()
for num, location in enumerate(sorted(locations)):
    locList[num] = location
    # Creating dict with index as keys and locations as values

### Step 5 - Asking user input on the commodities, dates and locations required
print("SELECT PRODUCTS BY NUMBER ...")
for i in commList:
    # Printing all commodities 3 a line
    if (i + 1) % 3 == 0:
        print(f"<{i:2}> {commList[i]:20}")
    else:
        print(f"<{i:2}> {commList[i]:20}", end='')
try:
    products = [commList[int(p.replace('<> ', ''))] for p in
                input("\nEnter product numbers separated by spaces: ").split()]
    # Taking and validation user inputs
except TypeError as t:
    print("\nInvalid input. Please enter a valid number from 0 to 21.")
    sys.exit()
print("\nSelected products: ", end='')
print(*products, sep=" ")

print("\nSELECT DATE RANGE BY NUMBER ...")
for i in dateList:
    # Printing all dates 5 a line
    if (i + 1) % 5 == 0:
        print(f"<{i:2}> {dateList[i]:<10}")
    else:
        print(f"<{i:2}> {dateList[i]:<10}", end='\t')
print(f"\nEarliest available date is: {min(dateList.values())}"
      f"\nLatest available date is: {max(dateList.values())}\n")
try:
    # Validating date input
    startDate, endDate = map(
        int, input("Enter start/end date numbers separated by a space: ").split())
except TypeError as t:
    print('Invalid input. Please try again')
    sys.exit()
except ValueError as v:
    print("Please enter only 2 values: Start date and End Date")
    sys.exit()
if not (not (endDate < startDate) and not (endDate < 0) and not (endDate > 52) and not (startDate < 0) and not (
        endDate > 52) and not (startDate == '')) or endDate == '':
    raise Exception("The start date cannot be greater than end date. Please enter a valid number between 0 and 52")
print(f"\nDates from {dateList[startDate]} to {dateList[endDate]}\n")
dates = [datetime.strptime(dateList[n], '%Y-%m-%d') for n in range(startDate, endDate + 1)]
# print(dates)

print("SELECT LOCATIONS BY NUMBER ...")
for i in locList:
    # Printing all locations
    print(f"<{i}> {locList[i]}")
try:
    selLocations = [locList[int(l)] for l in input("\nEnter location numbers separated by spaces: ").split()]
    # Taking and validation user inputs
except TypeError as t:
    print("Please enter a valid number between 0 and 4")
    sys.exit()
print("\nSelected locations: ", end='')
print(*selLocations, sep=" ")

### Step 6 - Filtering out the records based on the user criteria
select = list(filter(lambda a: a[0] in products and a[1] in dates and a[2] in selLocations, data))
print(len(select), "records have been selected.")

### Step 7 - Creating a dict with commodities and locations as key and average of the prices as values
pltData = dict()
for x in itertools.product(products, selLocations):
    priceList = [i[3] for i in select if i[0] == x[0] and i[2] == x[1]]
    if len(priceList) > 0:
        pltData[x] = sum(priceList) / len(priceList)

### Step 8 - Plotting the data using plotly
plt = [None] * len(selLocations)
for i, loc in enumerate(selLocations):
    # Creating list of lists with the required information
    plt[i] = go.Bar(
        x=products,
        y=[pltData[y] for y in pltData.keys() if y[1] == loc],
        name=loc
    )
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=plt, layout=layout)
# Adding a title to the x axis, y axis and chart
fig.update_layout(title_text=f'Produce Prices from {dateList[startDate]} through {dateList[endDate]}',
                  xaxis=dict(title='Product'),
                  yaxis=dict(title='Average Price',
                             tickformat="$.2f")) # formatting the y axis values
py.plot(fig, filename='final-proj.html')
