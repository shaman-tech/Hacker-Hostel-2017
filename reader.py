import pandas as pd
import numpy as np
import sqlite3

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

def populate_product_num(df):
	supplier_columns = ['PONUM','PODate','SUPPLIER','ShippingLine','ETAJamaica','ETATGG','AADTGG','DateOffloaded','Dateleft']
	for index, prod_num in enumerate(df['PONUM']):
		if prod_num == '?' and df.loc[index,'SUPPLIER'] == "?":
			for column in supplier_columns:
				df.loc[index,column] = df.loc[index-1,column]
		elif df.loc[index,'SUPPLIER'] == "?" and prod_num != "?":
			for column in supplier_columns[2:]:
				df.loc[index,column] = df.loc[index-1,column]
		elif prod_num == "?":
			for column in supplier_columns:
				df.loc[index,column] = df.loc[index-1,column]
	return df 

# cn = sqlite3.connect('db.sqlite')
# curs = cn.cursor()
fields = "PONUM,PODate,SUPPLIER,ProductDescription,Qty,SizeContainer,ContainerNUM,ShippingLine,ETAJamaica,ETATGG,AADTGG,DateOffloaded,Dateleft"#create_sql_command(column_names)
df = pd.read_csv('TGG_Merchandise.csv',skiprows=5, names=fields.split(","))
df = df.fillna(0)
df['PONUM']= df['PONUM'].astype(int)
column_names = list(df.columns)
column_values  = df.values
df = df.replace(0, '?')
df = df.replace("","?")
df = populate_product_num(df)
df.to_csv('sample.csv')
# for row in column_values:
# 	create_table_command = "{} TGG_MERCHANDISE ({}) {} ({})".format('INSERT INTO',fields,'VALUES',create_sql_command(row))
# 	curs.execute((create_table_command))






# for name in column_names:
# 	print(name.split())
