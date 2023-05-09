import os
import pandas as ps
import numpy as np
from matplotlib import pyplot as plt
# 129436125
# 129910940
# 133748381

print(*[filename.split(".")[0] for filename in os.listdir("./opinions")], sep="\n")

product_code = input("Please enter the product code: ")

opinions = ps.read_json(f"./opinions/{product_code}.json")
print(opinions)

max_score = 5
opinions["stars"] = (opinions["score"] * max_score).round(2)

opinions_count = opinions.shape[0]
pros_count = opinions.pros.astype(bool).sum()
cons_count = opinions.cons.astype(bool).sum()
average_score = (opinions.stars.mean()*max_score).round(2)

print(f"""For the product with the {product_code} code there is {opinions_count} opinions posted.
For {pros_count} opinions the list of product advanatges is given
and for {cons_count} opinions the list of product disadvatages is given.
The average score for the product is {average_score}.""")

if not os.path.exists("./charts"):
    os.mkdir("./charts")

recommendations = opinions.recommendation.value_counts(dropna=False).reindex([True,False,np.nan], fill_value=0)
print(recommendations)
recommendations.plot.pie(label="", labels=["Recommend", "Not recommend", "Neutral"], colors = ["forestgreen", "crimson", "gray"], autopct = lambda p: "{:.1f}%".format(round(p)) if p > 0 else "")
plt.title("Recommendations")
plt.savefig(f"./charts/{product_code}_pie.svg")
plt.close()

stars = opinions.stars.value_counts().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
stars.plot.bar(color="lightskyblue")
plt.ylim(0,max(stars)+10)
plt.title("Star count distribution")
plt.xlabel("Number of stars")
plt.ylabel("Number pf opinions")
plt.xticks(rotation = 0)
plt.grid(True, "major", "y")
for index, value in enumerate(stars):
    plt.text(index, value+1.5, str(value), ha = "center")
plt.show()