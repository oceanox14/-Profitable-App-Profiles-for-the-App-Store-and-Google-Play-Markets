#!/usr/bin/env python
# coding: utf-8

# # Data Analyzing to Develop Profitable App for App Store and Google Play Market

# In this project we aim to find mobile app profiles that are profitable for App Store and Google Play Market. We're working as data analysts for a company that builds Android and iOS mobile apps, and our job is to enable our team of developers to make data-driven decisions with respect to the kind of apps they build.
# 
# At our company, we only build apps that are free to download and install, and our main source of revenue consists of in-app ads. This means that our revenue for any given app is mostly influenced by the number of users that use our app. Our goal for this project is to analyze data to help our developers understand what kinds of apps are likely to attract more users.

# __OPENING AND EXPLORING DATA__

# As of September 2018, there were approximately 2 million iOS apps available on the App Store, and 2.1 million Android apps on Google Play.

# Collecting data for over four million apps requires a significant amount of time and money, so we'll try to analyze a sample of data instead. To avoid spending resources with collecting new data ourselves, we should first try to see whether we can find any relevant existing data at no cost. Luckily, these are two data sets that seem suitable for our purpose:

# - A data set containing data about approximately ten thousand Android apps from Google Play. You can download the data set directly from this link.
# https://www.kaggle.com/lava18/google-play-store-apps
# - A data set containing data about approximately seven thousand iOS apps from the App Store. You can download the data set directly from this link.
# https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps

# Let's start by opening the two data sets and then continue with exploring the data.

# In[1]:


from csv import reader

### The Google Play data set ###
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

### The App Store Dataset  ###
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# To make it easier to explore the two data sets, we'll first write a function named explore_data() that we can use repeatedly to explore rows in a more readable way. We'll also add an option for our function to show the number of rows and columns for any data set.

# In[2]:


def explore_data(dataset, start, end, rows_and_columns = False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[3]:


print(android_header)
print('\n')
explore_data(android, 0, 3, True)


# In[4]:


print(ios_header)
print('\n')
explore_data(ios, 0, 3, True)


# ## __DATA CLEANING__

# We need to clean in data to handling accurate data . That's why we're cleaning unnecessary and duplicate datas.

# ### **1- DELETING WRONG DATA**

# The Google Play data set has a dedicated discussion section, and we can see that one of the discussions outlines an error for row 10472. Let's print this row and compare it against the header and another row that is correct.

# In[5]:


print(android[10472])
android_header


# In[6]:


del android[10472]


# ### **2. REMOVING DUPLICATED DATA**
# 
# Google Play dataset includes duplicated entries. Such as below, example of Instagram. we need to find duplivated data and deleting them with help of the for loop.

# In[7]:


for app in android:
    name = app[0]
    if name == "Instagram":
        print(app)


# In[8]:


unique_apps = []
duplicate_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
    
print("duplicated apps:", len(duplicate_apps))
print('\n')
print("Examples of duplicated data", duplicate_apps[:5])


# We cannot delete duplicate data randomly. We need to find clues as to which of the duplicate data is the most recent. Even if you have to go through all the duplicate data :(

# In[9]:


reviews_max = {}
for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


# In[10]:


len(reviews_max)


# Let's cleaning our dataset from defined duplicate data.

# In[11]:


android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# In[12]:


explore_data(android_clean, 0, 3, True)


# We controled ios dataset as below, and we cant find any duplicated data.

# In[13]:


unique_apps = []
duplicate_apps = []

for app in ios:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
    
print("duplicated apps:", len(duplicate_apps))
print('\n')
print("Examples of duplicated data", duplicate_apps[:5])


# ###  3.Removing Non-English Data

# We want to design app for English-speaking audience.  However, if we explore the data long enough, we'll find that both datasets have apps with names that suggest they are not designed for an English-speaking audience. For examples:

# In[14]:


print(ios[813][1])
print(ios[6731][1])
print('\n')
print(android_clean[4412][0])


# We're not interested in keeping these apps, so we'll remove them.  One way to do this is to remove each app with a name containing a symbol that isn't commonly used in English text — English text usually includes letters from the English alphabet, numbers composed of digits from 0 to 9, punctuation marks (., !, ?, ;), and other symbols (+, *, /).
# 
# Each character we use in a string has a corresponding number associated with it. For instance, the corresponding number for character 'a' is 97, character 'A' is 65, and character '爱' is 29,233. We can get the corresponding number of each character using the ord() built-in function.

# In[15]:


print(ord("a"))
print(ord("A"))
print(ord("爱"))
print(ord("+"))


# he numbers corresponding to the characters we commonly use in an English text are all in the range 0 to 127, according to the ASCII (American Standard Code for Information Interchange) system.
# 
# If an app name contains a character that is greater than 127, then it probably means that the app has a non-English name.

# In[16]:


# We have to func. to find non-English app.
def is_english(x):
    for i in x:
        if ord(i) > 127:
            return False
    return True    


# In[17]:


print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))


# The function seems to work fine, but some English app names use emojis or other symbols (™, — (em dash), – (en dash), etc.) that fall outside of the ASCII range. Because of this, we'll remove useful apps if we use the function in its current form.

# In[18]:


print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# To minimize the impact of data loss, we'll only remove an app if its name has more than three non-ASCII characters:

# In[19]:


def is_english(x):
    non_ascii = 0
    
    for i in x:
        if ord(i) > 127:
            non_ascii +=1
    
    if non_ascii > 3:
        return False
    else:
        return True
    
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))  


# In[20]:


english_android = []
english_ios = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        english_android.append(app)
        
for app in ios:
    name = app[0]
    if is_english(name):
        english_ios.append(app)  


# In[21]:


explore_data(english_android, 0, 3, True)
print('\n')
explore_data(english_ios, 0, 3, True)


# ### 4. Removing Non-free Apps

# In[22]:


free_android = []

for app in english_android:
    price = app[7]
    if price == '0':
        free_android.append(app)       


# In[23]:


explore_data(free_android, 0, 3, True) 


# In[24]:


free_ios = []

for app in english_ios:
    price = app[4]
    if price == '0.0' or "Free":
        free_ios.append(app) 


# In[25]:


explore_data(free_ios, 0, 3, True) 


# We're left with 8864 Android apps and 3222 iOS apps, which should be enough for our analysis.

# ## __MOST COMMON APPS BY GENRE__
# 

# Our aim is to determine the kinds of apps that are likely to attract more users because our revenue is highly influenced by the number of people using our apps.
# 
# Our  strategy for an app idea is comprised of three steps:
# 
# 1. Build a minimal Android version of the app, and add it to Google Play.
# 2. If the app has a good response from users, we then develop it further.
# 3. If the app is profitable after six months, we also build an iOS version of the app and add it to the App Store.
# 
# Because our end goal is to add the app on both Google Play and the App Store, we need to find app profiles that are successful in both markets. 
# 
# Let's begin the analysis by determining the most common genres for each market.

# Our conclusion was that we'll need to build a frequency table for the prime_genre column of the App Store data set, and for the Genres and Category columns of the Google Play data set.

# In[26]:


# We have to create "freguency table" with the help of function.

def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages


# In order to be able to sort, we need to convert the data structure from a dictionary to a tuple.
def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[27]:


display_table(free_ios, -5)


# We can see that among the free English apps, more than a half(58.16%) are games.Entertainment apps are close to 8%, followed by photo and video apps, which are close to 5%. Only 3.66% of the apps are designed for education, followed by social networking apps which amount for 3.29% of the apps in our data set.
# 
# The general impression is that App Store is dominated by apps that are designed for fun (games, entertainment, photo and video, social networking, sports, music, etc.), while apps with practical purposes (education, shopping, utilities, productivity, lifestyle, etc.) are more rare.

# In[28]:


display_table(free_android, 1) #category


# In[29]:


display_table(free_android, -4)


# According to the frequency tables we analyzed showed us that apps designed for fun dominate the App Store, while Google Play shows a more balanced landscape of both practical and fun apps. Now, we'd like to determine the kind of apps with the most users.
# 
# Now, we'd like to determine the kind of apps with the most users.

# ## Most Popular Apps by Genre on the App Store

# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play data set, we can find this information in the Installs column, but this information is missing for the App Store data set. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app.

# In[35]:


genres_ios = freq_table(free_ios, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in free_ios:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


# **For App Store, Social & Network apps could be more profitable.**

# We have data about the number of installs for the Google Play market, so we should be able to get a clearer picture about genre popularity. However, the install numbers don't seem precise enough — we can see that most values are open-ended (100+, 1,000+, 5,000+, etc.):

# For instance, we don't know whether an app with 100,000+ installs has 100,000 installs, 200,000, or 350,000. However, we don't need very precise data for our purposes — we only want to find out which app genres attract the most users.
# 
# We're going to leave the numbers as they are, which means that we'll consider that an app with 100,000+ installs has 100,000 installs, and an app with 1,000,000+ installs has 1,000,000 installs, and so on.To perform computations, however, we'll need to convert each install number from a string to a float. This means we need to remove the commas and the plus characters, or the conversion will fail and cause an error.

# In[41]:


categories_android = freq_table(free_android, 1)


for category in categories_android:
    total = 0
    len_category = 0
    for app in free_android:
        category_app = app[1]
        if category_app == category:
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            total += float(n_installs)
            len_category +=1
   
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# In[ ]:


Video Players and Social Apps are more profitable than o


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




