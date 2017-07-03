import pandas as pd
import numpy as np 

def create_sql_command(row_entry):
	index = ""
	for column_value in row_entry:
		if index == "":
			if type(column_value) == str:
				index = "'%s'"%(column_value)
			else:
				index = str(column_value)
		else:
			if type(column_value) == str:
				index = index + ", " + "'%s'"%(column_value)
			else:
				index = index + ", " + str(column_value)
	return str(index)

def change_float_int(df_column):
	for index,value in enumerate(df_column.values):
		df_column[index] = int(value)
	return df_column


df = pd.read_csv('TGG_Merchandise.csv',skiprows=4)
df = df.fillna(0)
df['PO #']= df['PO #'].astype(int)
# scaler = lambda x: int(x)
# df['PO #'].apply(scaler)
column_names = list(df.columns)
column_values  = df.values
fields = create_sql_command(column_names)
for row in column_values:
	create_table_command = "{} TTG_MERCHANDISE ({}) {} ({})".format('INSERT INTO',fields,'VALUES',create_sql_command(row))
	print("'%s'"%create_table_command)
	print("")

# for name in column_names:
# 	print(name.split())