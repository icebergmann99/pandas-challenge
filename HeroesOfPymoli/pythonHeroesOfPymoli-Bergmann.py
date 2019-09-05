#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
data = pd.read_csv(file_to_load)


# ## Player Count

# * Display the total number of players
# 

# In[2]:


#calculating number of players
players = data["SN"].nunique()

#displaying number of players in jupyter notebook
players


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[3]:


#finding values
items = data["Item ID"].nunique()
avg_price = data["Price"].mean()
total_rev = data["Price"].sum()
purchases = data["Purchase ID"].count()

#creating labeled list of values
PT = {"Total Purchases" : [purchases],"Unique Items" : [items],"Average Price" : [avg_price], "Total Revenue" : [total_rev]}

#converting list to dataframe
Purchase_Totals = pd.DataFrame(PT)

#formats appropriate columns in dataframe
Purchase_Totals["Average Price"] = Purchase_Totals["Average Price"].map('${:,.2f}'.format)
Purchase_Totals["Total Revenue"] = Purchase_Totals["Total Revenue"].map('${:,.2f}'.format)

#formatting all floating point values
#pd.options.display.float_format = '{:.2f}'.format

#displaying totals dataframe in jupyter notebook
Purchase_Totals


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[4]:


#finding number of males
male_df = data[data["Gender"] == "Male"]
male = male_df["Gender"].count()

#finding number of females
female_df = data[data["Gender"] == "Female"]
female = female_df["Gender"].count()

#finding number of other
other_df = data[data["Gender"] == "Other / Non-Disclosed"]
other = other_df["Gender"].count()

#creating list of gender counts
GD = {"Male" : [male], "Female" : [female], "Other / Non-Disclosed" : [other]}

#converting list to dataframe
Gender_Demo = pd.DataFrame(GD)

#finding percentages across dataframe
Gender_Demo = ((Gender_Demo/purchases)*100)

#inefficiently reformatting each column in the dataframe
Gender_Demo["Male"] = Gender_Demo["Male"].map('{:,.0f}%'.format)
Gender_Demo["Female"] = Gender_Demo["Female"].map('{:,.0f}%'.format)
Gender_Demo["Other / Non-Disclosed"] = Gender_Demo["Other / Non-Disclosed"].map('{:,.0f}%'.format)

#displaying dataframe in jupyter notebooks
Gender_Demo


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[5]:


#male
#finding values
#m_items = male_df["Item ID"].nunique()
m_avg_price = male_df["Price"].mean()
m_total_rev = male_df["Price"].sum()
m_purchases = male_df["Purchase ID"].count()
#This gives you the average of the average purchace per person, but dues not appear to be what they actually want.
#m_avg = male_df.groupby("SN").mean()
#m_avgpp = m_avg["Price"].mean()
m_avgpp = m_total_rev/(male_df["SN"].nunique())

#creating labeled list of values
m_PT = {"Gender": "Male", "Total Purchases" : [m_purchases],"Average Price" : [m_avg_price], "Total Revenue" : [m_total_rev], "Avg Total Per Person" : [m_avgpp]}
#creating dataframe
m_PT_df = pd.DataFrame(m_PT)
m_PT_df.set_index("Gender")


#female
#finding values
#f_items = female_df["Item ID"].nunique()
f_avg_price = female_df["Price"].mean()
f_total_rev = female_df["Price"].sum()
f_purchases = female_df["Purchase ID"].count()
#f_avg = female_df.groupby("SN").mean()
#f_avgpp = f_avg["Price"].mean()
f_avgpp = f_total_rev/(female_df["SN"].nunique())

#creating labeled list of values
f_PT = {"Gender": "Female", "Total Purchases" : [f_purchases],"Average Price" : [f_avg_price], "Total Revenue" : [f_total_rev], "Total Revenue" : [f_total_rev], "Avg Total Per Person" : [f_avgpp]}
#creating dataframe
f_PT_df = pd.DataFrame(f_PT)

#other
#finding values
#o_items = other_df["Item ID"].nunique()
o_avg_price = other_df["Price"].mean()
o_total_rev = other_df["Price"].sum()
o_purchases = other_df["Purchase ID"].count()
#o_avg = other_df.groupby("SN").mean()
#o_avgpp = o_avg["Price"].mean()
o_avgpp = o_total_rev/(other_df["SN"].nunique())

#creating labeled list of values
o_PT = {"Gender": "Other / Non-Disclosed", "Total Purchases" : [o_purchases], "Average Price" : [o_avg_price], "Total Revenue" : [o_total_rev], "Total Revenue" : [o_total_rev], "Avg Total Per Person" : [o_avgpp]}
#creating dataframe
o_PT_df = pd.DataFrame(o_PT)

#=============================

#merge dataframes

PT_merge = m_PT_df.merge(f_PT_df, how="outer")
PT_All = PT_merge.merge(o_PT_df, how="outer")
PT_All = PT_All.set_index("Gender")
PT_All = PT_All.sort_index(ascending=True)

PT_All["Average Price"] = PT_All["Average Price"].map('${:,.2f}'.format)
PT_All["Total Revenue"] = PT_All["Total Revenue"].map('${:,.2f}'.format)
PT_All["Avg Total Per Person"] = PT_All["Avg Total Per Person"].map('${:,.2f}'.format)

PT_All


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[6]:


bins = [0, 9, 14, 19, 24, 29, 34, 39, 100000]
groups = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

demographics = data.copy()

demographics.drop_duplicates(subset="SN", keep = "first", inplace = True)

demographics["Total Count"] = pd.cut(demographics["Age"], bins, labels=groups)

demographics_group = demographics.groupby("Total Count")

demo = pd.DataFrame(demographics_group[["Total Count"]].count())

demo["Percentage of Players"] = ((demo["Total Count"] / players)*100).map('{:,.2f}%'.format)

demo


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[31]:


purchase = data.copy()

purchase["Age Ranges"] = pd.cut(purchase["Age"], bins, labels=groups)

purchase_group = purchase.groupby("Age Ranges")

purchase_num = pd.DataFrame(purchase_group[["Purchase ID"]].count())

#rename Purchase ID column to Purchase Count
purchase_num.rename(columns={"Purchase ID":"Purchase Count"}, inplace=True) 

purchase_num["Average Purchase Price"] = pd.DataFrame(purchase_group[["Price"]].mean())

purchase_num["Total Purchase Value"] = pd.DataFrame(purchase_group[["Price"]].sum())

purchase_num["Avg Total Purchase per Person"] = purchase_num["Total Purchase Value"] / demo["Total Count"]

#formatting
purchase_num["Average Purchase Price"] = purchase_num["Average Purchase Price"].map('${:,.2f}'.format)
purchase_num["Total Purchase Value"] = purchase_num["Total Purchase Value"].map('${:,.2f}'.format)
purchase_num["Avg Total Purchase per Person"] = purchase_num["Avg Total Purchase per Person"].map('${:,.2f}'.format)

purchase_num


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[52]:


top_group = data.groupby("SN")

top = pd.DataFrame(top_group[["Purchase ID"]].count())

#rename Purchase ID column to Purchase Count
top.rename(columns={"Purchase ID":"Purchase Count"}, inplace=True) 

top["Average Purchase Price"] = pd.DataFrame(top_group[["Price"]].mean())
top["Total Purchase Value"] = pd.DataFrame(top_group[["Price"]].sum())

top = top.sort_values(by="Total Purchase Value", ascending=False)

#formatting
top["Average Purchase Price"] = top["Average Purchase Price"].map('${:,.2f}'.format)
top["Total Purchase Value"] = top["Total Purchase Value"].map('${:,.2f}'.format)

top.head()


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[100]:


#working dataframe
popular = data[["Item ID", "Item Name", "Price", "Purchase ID"]]

#group count
popular_group = popular.groupby(["Item ID", "Item Name"])
popular_group.count()

#inital dataframe from group
popular = pd.DataFrame(popular_group[["Purchase ID"]].count())

#rename Purchase ID column to Purchase Count
popular.rename(columns={"Purchase ID":"Purchase Count"}, inplace=True) 

#add total purchase value to working dataframe from group
popular["Total Purchase Value"] = pd.DataFrame(popular_group[["Price"]].sum())


popular["Item Price"] = popular["Total Purchase Value"] / popular["Purchase Count"]

popular = popular[["Purchase Count", "Item Price", "Total Purchase Value"]]
most_popular = popular.sort_values(by="Purchase Count", ascending=False)

#popular_Most_popular = popular.copy()
most_popular["Item Price"] = popular["Item Price"].map('${:,.2f}'.format)
most_popular["Total Purchase Value"] = popular["Total Purchase Value"].map('${:,.2f}'.format)

most_popular.head()


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[101]:


profit_popular = popular.sort_values(by="Total Purchase Value", ascending=False)

#popular_Most_popular = popular.copy()
profit_popular["Item Price"] = popular["Item Price"].map('${:,.2f}'.format)
profit_popular["Total Purchase Value"] = popular["Total Purchase Value"].map('${:,.2f}'.format)

profit_popular.head()


# In[108]:


#printing all outputs so this could export out of jupyter notebook
#in hindsight some sort of consistancy of variables would have helped program look cleaner.

print(f"Heroes of Pymoli has {players} players.")
print("\n")

print("Purchasing Analysis (Total)")
print(Purchase_Totals)
print("\n")

print("Gender Demographics")
print(Gender_Demo)
print("\n")

print("Purchasing Analysis (Gender)")
print(PT_All)
print("\n")

print("Age Demographics")
print(demo)
print("\n")

print("Purchasing Analysis (Age)")
print(purchase_num)
print("\n")

print("Purchasing Analysis (Age)")
print(purchase_num)
print("\n")

print("Top Spenders")
print(top.head())
print("\n")

print("Most Popular Items")
print(most_popular.head())
print("\n")

print("Most Profitable Items")
print(profit_popular.head())
print("\n")

