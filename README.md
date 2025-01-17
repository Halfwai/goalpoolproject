# Football Goal Pool

This project is based around building a fantasy football game for the coming world cup. Instead of the usual points based approach, this project will use goals as the main means of scoring players. There are two basic games build here, the first is a classic league, where users can create a team and then swap players through each round to try and get the highest score, the second is a draft based game where small leagues hold a draft to pick their players. Once the draft is finished the teams are set and it's a luck based game to see who's team scores highest.

## Files

There is one app contained in this Django project, the goal pool app. In templates I have created 12 different html pages using 1 layout page for the header and footer. Static contains 4 different Javascript files, one that runs on all pages, and 3 that have specific tasks on specific pages. Static also contains some images used on the site including a site logo and a background image. Views.py contains the majority of the working code to navigate the 7 classes defined in models.py, and functions.py contains a function I abstracted from the main code. With more time I plan on abstracting more functions from views so that it's easier to test each working part as my code gets a little long and convoluted at times. I also added django-extensions in order to run scripts that do a lot of the heavy lifting in terms of updating my database. I am currently using api-football as my data source, but as you can see I have some test scripts using the fpl python module that uses the fpl api for premier league data. I am also using the pytz as part of my update.py file to check when games are on and when I need to be calling the api.

## How to run

There are two commands needed to run this project on a home server. First you need to install the required packages
```
  pip install -r requirements.txt
```
Then you can run the server
```
  python manage.py runserver
```

