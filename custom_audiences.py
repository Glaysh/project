#!/usr/bin/env python
# coding: utf-8

# # Custom demographic groups
# 
# KATERYNA KASHCHENKO
# 
# A notebook with examples of the formation of user demographic groups.
# 
# General principles of the formation of demographic groups:
# - are formed on the basis of the values of the directory of socio-demographic variables
# - available operators:
#     ```
#     = (equality)
#     != (inequality)
#     > (greater than)
# < (less than)
# >= (greater than or equal to) 
#     <= (less than or equal to)
# AND (AND)
# OR (OR)
# IN() (entering the list of values)
# ``
# 
# Let 's take a closer look at the example of the following demographic groups:
# 1. Men 35-44 years old
# 2. Men 18-24 years old or women 25-34 years old
# 3. All 20-56 years old
# 4. Not managers 25-54 years old
# 5. Working residents of Greater Moscow
# 
# Parameters:
# - Period: September 2021
# - Type of Internet use: there are no restrictions, we count on all (Web Desktop, Web Mobile, App Mobile)
# - Resource: Ivi
# 
# Statistics:
# - Reach (reach)

# # Initialization
# 
# When building a report, the first step in any laptop is downloading libraries that will help you access the CrossWeb API and work with data.
# 
# Execute the following cell, to do this, go to it and press Ctrl+Enter

# In[1]:


get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

import sys
import os
import re
import json
import datetime
import time
import pandas as pd
#import matplotlib.pyplot as plt
from IPython.display import JSON

from mediascope_api.core import net as mscore
from mediascope_api.crossweb import tasks as cwt
from mediascope_api.crossweb import catalogs as cwc

# Setting up the display

# Enabling the display of all columns
pd.set_option('display.max_columns', None)
# Setting the maximum number of output lines. Uncomment the desired line
# 200 lines
# pd.set_option("display.max_rows", 200)
# Displaying all lines. important! Displaying a large Data Frame requires a lot of resources
# pd.set_option("display.max_rows", None)

# Creating objects to work with the API
mnet = mscore.MediascopeApiNetwork()
mtask = cwt.CrossWebTask()
cats = cwc.CrossWebCats()


# ## List of socio-demographic variables
# To form the syntax of demographic groups, we will need a reference book of socio-demographic variables.
# 
# We will find the necessary socio-demographic variables using the search method in the directory. Working with the directory is described in detail in the notebook [catalogs](catalogs.ipynb). 

# In[2]:


# For example, we will find variables in the directory containing the text "Gender"
cats.find_property('Пол', expand=True)


# ### General parameters for tasks
# 
# To begin with, we will set the general parameters

# In[3]:


# Setting the period
# The period is specified as a list ('Beginning', 'End'). You can specify severalпериодов
date_filter = [('2021-09-01', '2021-09-30')]

Setting a filter by Internet usage types
usetype_filter = [1,2,3]


# ## Tasks
# 
# Let's move on to the formation of tasks.
# 
# 
# ### Task #1. Men 35-44 years old

# From the reference book we see that for the selection of men we need the value of 1 variable **sex**
# ```
# gender = 1
# ```
# The age group 35-44 corresponds to the value of 4 variables ** age group**
# ```
# age group = 4
# ```
# Combining expressions via and operator
# ```
# gender = 1 And age group = 4
# ```

# ### Get the resource ID
# To build a report, you need to get the resource ID __Ivi__.
# 
# To do this, we will use the search method in the media directory. Working with the media directory is described in detail in the notebook [catalogs](catalogs.ipynb). 
# 
# Get the resource ID **Ivi**

# In[4]:


cats.get_resource(resource='Ivi')


# Thus, the required identifier is as follows:
# 
# - **-**Ivi** resource ID = 1067

# In[9]:


# Setting the name to display in DataFrame
project_name = 'Ivi M35-44'

# We set a filter by geography, in our case it is not required
geo_filter = None

# We set a filter by demography, in our case, the expression compiled above for the variable "Men 35-44 years old"
demo_filter = 'sex = 1 AND ageGroup = 4'

# We set the media filter, in our case it is the ID of the Ivi
mart_filter = 'crossMediaResourceId = 1067'

# Specifying a list of slices to form the calculation structure
slices = ["researchMonth", "crossMediaResourceId"]

# Specify a list of statistics to calculate
statistics = ['reach']

# Creating a task for the Cross Web API in JSON format
task_json = mtask.build_task('media', project_name, date_filter, usetype_filter, geo_filter,
                             demo_filter, mart_filter, slices, statistics)

# We send the task for calculation and wait for it to be completed
task_audience = mtask.wait_task(mtask.send_audience_task(task_json))

# Getting the result
df_1 = mtask.result2table(mtask.get_result(task_audience),project_name)
df_1


# ### Task #2. Men 18-24 years old or women 25-34 years old

# We return to the reference book of socio-demographic variables. To select men aged 18-24, we need the value of 1 variable ** gender** and the value of 2 variables ** age group**
# ```
# gender = 1 And age group = 2
# ```
# For the selection of women aged 25-34, the syntax will be as follows`
# ```
# gender = 2 And age group = 3
# ```
# We combine using the OR operator
# ```
# ((gender = 1 and age group = 2) OR (set = 2 AND age group = 3)
# ```

# In[11]:


# Setting the name to display in DataFrame
project_name = 'Ivi M18-24 + W25-34'

# We set a filter by geography, in our case it is not required
geo_filter = None

# We set a filter by demography, in our case, the expression compiled above for the variable "Men 18-24 years old or women 25-34 years old"
demo_filter = '(sex = 1 AND ageGroup = 2) OR (sex = 2 AND ageGroup = 3)'

# We set the media filter, in our case it is the ID of the Ivi
mart_filter = 'crossMediaResourceId = 1067'

# Specify a list of slices to form the calculation structure
slices = ["researchMonth", "crossMediaResourceId"]

# Specifying a list of statistics to calculate
statistics = ['reach']

# Creating a task for the Cross Web API in JSON format
task_json = mtask.build_task('media', project_name, date_filter, usetype_filter, geo_filter,
                             demo_filter, mart_filter, slices, statistics)

# We send the task for calculation and wait for it to be completed
task_audience = mtask.wait_task(mtask.send_audience_task(task_json))

# Getting the result
df_2 = mtask.result2table(mtask.get_result(task_audience), project_name)
df_2


# ### Task #3. All 20-56 years old

# The age of 20-56 years will not be able to collect from the variable **age group **, we will need the variable **age**.
# 
# Let's set the age range using the comparison operators "greater than or equal to" (**>=**) and "less than or equal to" (**<=**):
# `
# age >= 20 And age <= 56
# `

# In[12]:


# Setting the name to display in DataFrame
project_name = 'Ivi All 20-56'

# We set a filter by geography, in our case it is not required
geo_filter = None

# We set a filter by demography, in our case, the expression compiled above for the variable "All 20-56 years"
demo_filter = 'age >= 20 AND age <= 56'

# We set the media filter, in our case it is the ID of the Ivi
mart_filter = 'crossMediaResourceId = 1067'

# Specifying a list of slices to form the calculation structure
slices = ["researchMonth", "crossMediaResourceId"]

# Specify a list of statistics to calculate
statistics = ['reach']

# Creating a task for the Cross Web API in JSON format
task_json = mtask.build_task('media', project_name, date_filter, usetype_filter, geo_filter,
                             demo_filter, mart_filter, slices, statistics)

# We send the task for calculation and wait for it to be completed
task_audience = mtask.wait_task(mtask.send_audience_task(task_json))

# Getting the result
df_3 = mtask.result2table(mtask.get_result(task_audience), project_name)
df_3


# ###### Task #4. Not managers 25-54 years old

# For a team of the age group 25-54, we will need the values 3, 4 and 5 of the variable **ageGroup**. To simplify, we will not make three conditions using OR, but use the IN operator
# ```
# ageGroup IN (3, 4, 5)
# ```
# The condition "not managers" ble is also briefly set using the inequality operator "!="
# ```
# occupation != 1
# ```
# Connected via the operator and
# ```
# ageGroup IN (3, 4, 5) AND occupation != 1
# ```

# In[13]:


# Setting the name to display in DataFrame
project_name = 'Ivi 25-54 not dir'

# We set a filter by geography, in our case it is not required
geo_filter = None

# We set a filter by demography, in our case, the expression compiled above for the variable "At least 25-54 years old"
demo_filter = 'ageGroup IN (3, 4, 5) AND occupation != 1'

# We set the media filter, in our case it is the ID of the Ivi
mart_filter = 'crossMediaResourceId = 1067'

# Specifying a list of slices to form the calculation structure
slices = ["researchMonth", "crossMediaResourceId"]

# Specifying a list of statistics to calculate
statistics = ['reach']

# Creating a task for the Cross Web API in JSON format
task_json = mtask.build_task('media', project_name, date_filter, usetype_filter, geo_filter,
                             demo_filter, mart_filter, slices, statistics)

# We send the task for calculation and wait for it to be completed
task_audience = mtask.wait_task(mtask.send_audience_task(task_json))

# Getting the result
df_4 = mtask.result2table(mtask.get_result(task_audience), project_name)
df_4


# ### Task #5. Working residents of Greater Moscow

# We will set the geography of "Greater Moscow" using the variable **Urban pop**
# ```
# city Pop = 1
# ```
# To select employees, we will need the variable **work**
# ```
# job = 1 
# ```

# In[15]:


# Setting the name to display in DataFrame
project_name = 'Ivi BM work'

# We set a filter by geography, in our case, the expression compiled above for Greater Moscow
geo_filter = 'cityPop = 1'

# We set a filter by demography, in our case, the expression compiled above for working
demo_filter = 'work = 1'

# We set the media filter, in our case it is the ID of the Ivi
mart_filter = 'crossMediaResourceId = 1067'

# Specifying a list of slices to form the calculation structure
slices = ["researchMonth", "crossMediaResourceId"]

# Specify a list of statistics to calculate
statistics = ['reach']

# Creating a task for the Cross Web API in JSON format
task_json = mtask.build_task('media', project_name, date_filter, usetype_filter, geo_filter,
                             demo_filter, mart_filter, slices, statistics)

# We send the task for calculation and wait for it to be completed
task_audience = mtask.wait_task(mtask.send_audience_task(task_json))

# Getting the result
df_5 = mtask.result2table(mtask.get_result(task_audience), project_name)
df_5

