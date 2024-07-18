# Weather-data-analysis
Parsing and analysing data from gismeteo

# Library stack
### requests - to execute HTTP requests
### BeautifulSoup - for HTML parsing
### datetime - for working with dates
### pandas - for working with data
### csv - for working with CSV files
### ast - for safe execution of strings as Python expressions
### re - for working with regular expressions
### matplotlib.pyplot, openpyxl(Alignment, Image, load_workbook), numpy - for working in Excel and visualising graphs

# Structure
### data - This file is created for correct parsing of data from Gismeteo site and obtaining and forming necessary data for further analysis.
### analyse - in which I collect all data by cities and form dataframes for further analysis
### vis - represents calculation, visualisation and parsing of data in excel

# Objective:
### To identify key differences in weather patterns relative to their location in the north central and southern regions

### The main hypothesis was that temperature, humidity and wind speed were likely to be the main variations in terms of temperature, humidity and wind speed relative to the central region

# Result:
### The result of these files is the file results_part2.xslx in which the data and graphs of the urban weather analyses are displayed on several tabs. The last tab in the file is the output of the result of the data analysis, which generally coincides with the hypothesis and reflects the characteristic features of each region. 

## Speaking about the future of the project, we can say with certainty that it is definitely possible to develop this project. For example, the most obvious extension is to include more cities in the analysis. Moreover, in the future it will be possible to divide cities into specific regions or areas to which they belong and analyse weather climate changes in each region separately, which could be useful for farming and various agro crops. 
