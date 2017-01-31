import pandas




def accuracy(new, awardStr):
	correct 		= new[new[awardStr] == True]['Year'].count()
	notcorrect 		= new[new[awardStr] == False]['Year'].count()
	acc = correct/float(correct + notcorrect)
	print acc * 100

history = pandas.read_csv("oscars_history.csv")
history = history.iloc[0:25]
new 	= history[history.Year == 0]
new1 	= history[history.Year == 0]
del new['Oscar Winner']
del new1['Year']

for row in history.iterrows():
	oscarwinner = row[1]['Oscar Winner'].strip()
	tempList 	= []
	for x in range(0,4):
		booleanVal = (str(row[1][x]).strip() == oscarwinner)
		if str(row[1][x]).strip() == 'nan':
			booleanVal = None
		tempList.append(booleanVal)
	PandaSeries = pandas.Series({ "Critics Choice": tempList[0], "Producers": tempList[1], "DAG Director" : tempList[2], "BAFTA" : tempList[3],  "Year" : int(row[1]['Year'])  })
	new 		= new.append(PandaSeries, ignore_index = True)



accuracy(new, 'Critics Choice')
accuracy(new, 'Producers')
accuracy(new, 'DAG Director')
accuracy(new, 'BAFTA')



movieList = []

for row in history.iterrows():
	for x in range(0,4):
		 movie = str(row[1][x]).strip()
		 if movie not in movieList:
		 	movieList.append(movie)


for ele in movieList:
	cc 		=  history[history['Critics Choice'] == ele]["Year"].count()
	prod 	= history[history['Producers'] == ele]["Year"].count()
	dag 	= history[history['DAG Director'] == ele]["Year"].count()
	bafta 	= history[history['BAFTA'] == ele]["Year"].count()
	winner 	= history[history['Oscar Winner'] == ele]["Year"].count()

	PandaSeries = pandas.Series({ "Critics Choice": cc, "Producers": prod, "DAG Director" : dag, "BAFTA" : bafta,  "Oscar Winner" : winner  })
	new1 		= new1.append(PandaSeries, ignore_index = True)

new1.to_csv("temp.csv")