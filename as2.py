# Author: William Santos
# Date: 12/18/19
# Data Mining: Assignment 2
# Description: This code attempts to analyze crime data to form meaningful statistics for the user.

# IMPORTS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import statistics
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# CLASSES
# This central object handles all of the pandas data processing for the user, including orgnaization and display of information.
class DataAnalysis:
	def __init__(self,f):
		self.df = get_processed_df(f)
		self.crimeDict = self.initSelectionDict(self.df['Primary Type'].unique())
		self.years = self.initSelectionDict([str(x) for x in self.df.Year.unique()],default="None")
	

	# Gather all unique types of crime from the dataframe
	def initSelectionDict(self,myList,default="Exit"):
		idx = 1
		res = dict()
		for cType in myList:
			res[str(idx)] = cType
			idx = idx + 1
		res["0"] = default
		return res

	# Display all options gathered from the dataframe
	def displayCrimeOptions(self):
		for x, y in self.crimeDict.items():
			print(x + ") " + y)
		print("Please select the type of crime you wish to examine:")
		selection = str(input("Selection: "))
		if selection in self.crimeDict:
			res = self.crimeDict[selection]
			print("Selection: " + selection + " -> " + res + "\n\n")
			return res
		print("\n\n WARNING. Invalid Input: " + selection + ". Returning empty string.\n\n")
		return ""

	# Displays years and prompts user input for it	
	def displayYears(self):
		print("Please select the year to filter by: ")
		for x, y in self.years.items():
			print(x + ") " + y)
		selection = str(input("Selection: "))
		if selection in self.years:
			res = self.years[selection]
			print("Year Selected: " + selection + " -> " +res + "\n\n")
			return res
		print("\n\n WARNING. Invalid Input: " + selection + ". Defaulting to None.\n\n")
		return "None"
	
	# displays Histogram
	def plotHist(self,crimeType):
		cType = self.df['Primary Type'] == crimeType
		y14 = self.df[(self.df.Year == 2014) & cType]
		y15 = self.df[(self.df.Year == 2015) & cType]
		y16 = self.df[(self.df.Year == 2016) & cType]
		y17 = self.df[(self.df.Year == 2017) & cType]
		yrs = [ y14, y15, y16, y17 ]
		count = []
		c = ["red","blue","green","yellow"]
		legend = [str(y) for y in self.years.values()]
		p = 'Primary Type'
		
		for y in yrs:
			count.append(len(y.Year))
		
		print("\n\nGeneral Stats for Type: " + crimeType)
		print("Mean: ", (statistics.mean(count)))
		print("Std: ", (statistics.pstdev(count)))
		print("Var: ", (statistics.pvariance(count)))
		print("Generating histogram...")
		
		# Plot Histogram
		plt.hist([df[p] for df in yrs],color=c)
		plt.xlabel("Crime Type")
		plt.ylabel("Frequency")
		plt.legend(legend)
		plt.show()
	
	# Generates a scatter plot and general plot 
	def plotCrime(self,crimeType,year):
		cType = self.df['Primary Type'] == crimeType
		yrs = [ self.df[(self.df.Year == int(x)) & cType] for x in self.years.values() if x!="None"]
		if(year!="None"):
			yrs = [ x for x in yrs if x.Year.iloc[0] == int(year) ]
		
		for y in yrs:
			df = pd.DataFrame(y.Location.str.replace('(','').str.replace(')','').str.split(',',expand=True).values.tolist())
			kmeans = KMeans(n_clusters=4,random_state=0,max_iter=3000).fit_predict(df)
			distortions = []
			for i in range(1,11):
				km = KMeans(
					n_clusters=i, init='random',
					n_init=10, max_iter=300,
					tol=1e-04, random_state=0
				)
				km.fit(df)
				distortions.append(km.inertia_)
			
			# Plot Data
			plt.plot(range(1,11),distortions,marker='o')
			plt.xlabel('Number of Clusters')
			plt.ylabel('Distortion')
			plt.show()
			
			# Scatter Plot
			colors = ["red","green","blue","purple"]
			plt.scatter(y["Longitude"], y["Latitude"], marker=".", c=kmeans, cmap=matplotlib.colors.ListedColormap(colors))
			
			plt.ylim(41.6,42.1)
			plt.xlim(-88,-87.4)
			plt.legend(kmeans)
			plt.title(crimeType)
			plt.ylabel('Latitude')
			plt.xlabel('Longitude')
			plt.show()


# FUNCTIONS
# Processes the csv file and strips the unnecessary parts of the dataframe
def get_processed_df(filename):
	df = pd.read_csv(filename, na_values=[None,'NaN','Nothing'],header=0)
	df.drop_duplicates(subset=['ID','Case Number'],inplace=True)
	df.drop(['Case Number','IUCR','FBI Code','Updated On','X Coordinate','Y Coordinate'],inplace=True,axis=1)
	df = df.dropna(axis=0,how='any')
	
	years = [2014,2015,2016,2017]
	df = df[df.Year.isin(years)] #Filter by years
	return df

# MAIN
# Central component that displays the user input in a update loop.
def main():
	filename = "crime_data_update.csv"
	a = DataAnalysis(filename)
	cType = ""
	while(cType!="Exit"):
		cType = a.displayCrimeOptions()
		if cType in a.crimeDict.values() and cType!="Exit":
			year = a.displayYears()
			a.plotHist(cType)
			print("Input Year: " + year)
			a.plotCrime(cType,year)

main()

