import pandas as pd

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


df = pd.read_csv('TGG_Merchandise.csv',skiprows=4)
df = df.fillna(0)
scaler = lambda x: round(x,2)
df['PO #'].apply(scaler)
column_names = list(df.columns)
column_values  = df.values
fields = create_sql_command(column_names)
for row in column_values:
	create_table_command = "{} TTG_MERCHANDISE ({}) {} ({})".format('INSERT INTO',fields,'VALUES',create_sql_command(row))
	print("'%s'"%create_table_command)
	print("")

# for name in column_names:
# 	print(name.split())