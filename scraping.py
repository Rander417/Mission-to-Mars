# ----- IMPORTS -----

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
# ----- END IMPORTS -----


# ----- CONNECTIONS & DATA LOAD -----
# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)
# ----- END CONNECTIONS & DATA LOAD -----


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# set up the HTML parser:
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
slide_elem = soup.select_one('ul.item_list li.slide')


# ----- Begin SCRAPING -----

# Assign the title and summary text to variables - will reference later
slide_elem.find("div", class_='content_title')

# The title is in that mix of HTML in our output
# But we need to get just the text, and the extra HTML stuff isn’t necessary. 

# Use the parent element to find the first `a` tag and save it as `news_title`
# This returns the most recent title published
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# This gets the summary info
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### 10.3.4 Scrape Mars Data: Featured Image

# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')


# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ----- 10.3.5 Scrape Mars Data: Mars Facts

html_df = pd.read_html('http://space-facts.com/mars/')[0]
html_df.columns=['description', 'value']
html_df.set_index('description', inplace=True)
html_df


# convert DataFrame back into HTML-ready code
html_df.to_html()


# Scrape completed
browser.quit()
# ----- END SCRAPING -----