import csv
import pandas as pd

def main():
	filename = "crime_data.csv"
	endfile = "crime_data_update.csv"
	
	print("Converting " + filename + " to pandas dataframe")
	df = pd.read_csv(filename, dtype={'Longitude':str,'Location':str})
	
	print("Converting Date columns to datetime")
	df['Date'] = pd.to_datetime(df['Date'])
	
	print("Appending Year Column to dataframe")
	df['Year'] = df['Date'].dt.year
	
	print(df.head())
	print("Exporting to " + endfile)
	df.to_csv(endfile, encoding="utf-8", index=False)

main()
