# Football Goal Pool

This project is based around building a fantasy football game for the coming world cup. Instead of the usual points based approach, this project will use goals as the main means of scoring players. There are two basic games build here, the first is a classic league, where users can create a team and then swap players through each round to try and get the highest score, the second is a draft based game where small leagues hold a draft to pick their players. Once the draft is finished the teams are set and it's a luck based game to see who's team scores highest.

## Distinctiveness and Complexity

There is nothing quite like this on the CS50w course in terms of the app I have build. While many of the CS50w projects are based around cloning large and popular websites, I created this app as a desire to "digitize" as it were, a game that I have been playing with my friends in the past through pen and paper and excel spreadsheets. In terms of complexity, this website has more routes and more pages than any of the web apps that we have completed so far, and I have used a combination of Javascript and Django to access the databases and render different parts of the page. View.py alone had over 450 lines of code, and the various javascript files, models, scripts and functions have created a large file. Note that while the project is currently running based on the World cup, I initially did some testing using an API for the premier league, and it would not take too much effort to adapt and adjust the app to focus on that, something that I intend to do once the world cup finishes.

## Files

There is one app contained in this Django project, the goal pool app. In templates I have created 12 different html pages using 1 layout page for the header and footer. Static contains 4 different Javascript files, one that runs on all pages, and 3 that have specific tasks on specific pages. Static also contains some images used on the site including a site logo and a background image. Views.py contains the majority of the working code to navigate the 7 classes defined in models.py, and functions.py contains a function I abstracted from the main code. With more time I plan on abstracting more functions from views so that it's easier to test each working part as my code gets a little long and convoluted at times. I also added django-extensions in order to run scripts that do a lot of the heavy lifting in terms of updating my database. I am currently using api-football as my data source, but as you can see I have some test scripts using the fpl python module that uses the fpl api for premier league data.

## How to run

I currently have my app running via www.pythonanywhere.com, you can currently find it at www.footballgoalpool.com. If you want to run it on your own computer, as long as you have django and django-extensions installed it should run through manage.py runserver.

## Additional Information

While this project is finished in the sense that it is ready for submission, and I have deployed it for my friends to help me test and play, it is still a work in progress in many ways, and I plan on continuing to work on new features so I can deploy a more complete version in time for the 23/24 premier league season. As much as this is a project in the sense of wanting to create something worthwhile for CS50w, it was also a passion project for something that I wanted to create and share with the world, and in that sense it may never be truly complete.

### Thanks

I just wanted to add my own personal thanks here, I completed CS50x last year, but it's taken me a little longer to complete CS50w as I was inspire to enrolled in a BSc in Computer Science, I'm currently in my second semester. CS50 has been my inspiration for a big career shift from teaching, and it's been an absolute revelation. I know that Brian has moved on from Harvard, but he's a fantastic teacher and I've really enjoyed this course, and I look forward to seeing what sort of content the CS50 team will come up with in the future. This was CS50w.