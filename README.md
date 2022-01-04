# Ecommerce-price-compare
**Compare prices of products on famous E-commerce websites: Jiomart &amp; Amazon Fresh. A web scraping project I had done in the last week of July, 2021.**

# Requirements:
[Chromedriver](https://chromedriver.chromium.org/)

**Python:**
```python
#IMPORTS
from selenium import webdriver
from bs4 import BeautifulSoup

import pandas as pd
import openpyxl as pxl

import keyboard
from time import sleep
```

# Project details:

**Idea:**

I buy all my groceries and other neccessities from online stores and have had to spend a lot of time comparing prices accross E commerce sites to understand which site gives the best deal currently. As this was a repetitive process and thus I decided to automate it. :)

**Process:** 
- I started by taking the input of the user's Pincode and the products he needs. 
- Next, I opened a new browser using `selenium` and `chromedriver` and sent a get request to jiomart first, once Jiomart is scraped then we move ahead to Amazon Fresh.
- Once the website loads, I enter the Pincode to so that we don't end up scraping products which are unavailable in our area. ( Using `keyboard` library)
- Now, we enter the product in the search bar and search for it. Next, we apply all the filters we want to.
- Now, using `BeautifulSoup` we scrape the page, looking for particular html tags which help us in getting the products we want.
- All of this data is stored in a `pandas` dataframe.
- Finally, this dataframe is converted to a xlsx file and stored on the system. 


**Challenges:**
- A lot of products on the websites were marked incorrectly by the algorithm they use, and thus I had to perform quite some text pre-processing so as to get reasonable results.
- The websites seem to have random webpage load times and thus, I could not optimize the process and decided to go ahead with hardcoded delays in most places.

**Output (as of 27th September, 2021):**
![image](https://user-images.githubusercontent.com/84278440/134847493-1e90185c-7914-4ffc-b5d2-24e284094023.png)


**After project thoughts:**
- The 2 websites are very different and have taught me a lot and have made me more confident in my scraping skills.
- The code has a lot of delay(hardcoded) so as to ensure it runs smoothly and encounters no errors, but this also makes it slow. I wish to further improve the performance once I learn more about it. 
- I use this product often and it really saves me a lot of time. So, I am happy I did this project! :D 
