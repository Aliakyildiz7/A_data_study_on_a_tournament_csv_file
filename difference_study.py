import pandas as pd
import matplotlib.pyplot as plt

"""
This code
-Creates a pandas dataframe from a csv file Lichess provides after a tournament.
-Creates a new column called "Difference" by subtracting "Performance" from the "Rating"
    -A positive "Difference" mean player did better than expected.
    _A negative "Difference" mean player did worse than expected.
-Creates pie plots for each rating range showing percentage and number of players who did better and worse
    than expected.
-Finally creates a bar graph showing percentage of players who did better than expected in all rating ranges.

"""

#User Panel
sensitivity = 200 #Rating span for each rating range. You can change that value for different spans

#Creating the master data frame from a csv file
csv_name = "lichess_tournament_2023.11.09_z4RuEszs_eastern-blitz.csv"
master_data = pd.read_csv(csv_name,
                          usecols=["Rank", "Username", "Rating", "Score", "Performance"])

#Elimination of Players who joined the tournament but did not play a game
na_condition = master_data["Performance"].notna()
master_data = master_data.loc[na_condition]

#Creating a new column "Difference" and Sorting
#If "Difference" > 0, Player did better than expected
#else, player did worse than expected

master_data["Difference"] = master_data["Performance"] - master_data["Rating"]
master_data.sort_values(by="Difference", inplace=True, ascending=False, ignore_index=True)
print(master_data.head(10))


#Defining booleans for grouping in each rating range
cond_positive_players = master_data["Difference"] >= 0  # df of players who did better than their ratings (or equal)
cond_negative_players = master_data["Difference"] < 0  # df of players who did worse than their ratings


#Deciding max and minimum values of Rating_Ranges
max_rating = max(master_data["Rating"] + (sensitivity - max(master_data["Rating"]) % sensitivity))
min_rating = min(master_data["Rating"]) - min(master_data["Rating"]) % sensitivity



#Creating the dictionary which:
    #Keys are strings  that represent the rating range (e.g. Rating 500-750, Rating 750-1000 etc...)
    #Values are dataframes that consist of players in this rating range

master_diction = {}
for x in range(min_rating, max_rating, sensitivity):

    var_name = f"Rating {x}_{x + sensitivity}" #Dummy  variable for key names
    master_diction[var_name] = master_data.loc[(master_data["Rating"] >= x) & (master_data["Rating"] < x + sensitivity)]



#Creating two new dictionaries from the master dictionary depending on the sign of the "Difference"
positive_diction = {}
negative_diction = {}

for x in master_diction:
    positive_diction[x] = master_diction[x].loc[cond_positive_players]
    negative_diction[x] = master_diction[x].loc[cond_negative_players]



#Creating the dictionary which:
    #Keys refer to the rating range. Values contain a tuple such that:
        #tuple[0] shows the number of players with positive  difference in that range
        #tuple[1] shows the number of players with negative  difference in that range
result_diction = {}

for x in master_diction:
    result_diction[x] = (len(positive_diction[x]), len(negative_diction[x]))



#Pie graphing the percentage of positive and negative players in each rating range
for x in result_diction:

    if (result_diction[x][0]) == 0 and (result_diction[x][1]) == 0:
        continue #Do nothing if  there is no player in that range

    else:

        plt.figure(figsize=(12, 6))
        plt.pie(result_diction[x], labels = [f"Players who did better than expected ({(result_diction[x][0])})",
                  f"Players who did worse than expected ({(result_diction[x][1])})"], autopct ="%.2f %%")


        plt.title(f"{x} \n Number of Players: {sum(result_diction[x])}")
        plt.show()




#Bar Graphing the percantage of postive players in all Rating Ranges
#values = [(int(x[0]) / (int(x[0]) + int(x[1])))*100 for x in result_diction.values() if (int(x[0]) + int(x[1])) != 0]

values = []
for x in result_diction.values():
    if (int(x[0]) + int(x[1])) == 0:
        values.append(0) #If there  is  no player in the range, let positivity rate be 0
    else:
        values.append((int(x[0]) / (int(x[0]) + int(x[1]))) * 100)


labels = [x for x in result_diction]
plt.bar(labels, values, width=0.7)

#Positioning the labels on bars, making use of enumeration
for num, element in enumerate(values):
    plt.text(num, 30, f"%{values[num]:.2f}, \n({sum(result_diction[labels[num]])} Players)", horizontalalignment='center')


plt.title("Percentage of Players who did better than expected")
plt.show()

