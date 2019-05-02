import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import average



# Create empty dataframe
df = pd.DataFrame()
# Dataset
tips2 = pd.read_csv('jumpDistvsRank.csv')

df['y'] = [1,2,3,4,5,6,7,8,8,8,8,8,8,8,8]
df['x'] = [2,2,3,4,5,6,6,7,9,99,99,99,99,99,2]
 
#sns.regplot(x=df["x"], y=df["y"]) #scatterplot
#sns.barplot(x=df["x"], y=df["y"],ci=None, color="salmon")

#sns.barplot(x=tips2["rank"], y=tips2["distance"],ci=None, color="green", estimator=sum)
sns.regplot(x=tips2["rank"], y=tips2["distance"],ci=None, color="salmon")
sns.lmplot(x="rank", y="distance", data=tips2, ci=None);


plt.show()



