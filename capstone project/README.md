## HarvardX CS50W: Web Programming with Python and JavaScript


### Final project: BeInformed

BeInformed is a news delivery site that uses NewsAPIin the background to provide latest breaking news from major news service providers across the globe. News is very important nowadays and by news I mean genuine news and news that matters to you the most. All this time, I never worked with any API and hence decided to create a site that would show news from across various top news agencies which would help the user be well-informed with the help of NewsAPI. NewsAPI is a powerful API that has a great collection of news originating from different countries across various categories. It was a good experience working with this API as it was well documented and
my site provides most of the endpoints in action so that every user gets his own feed based on the categories he/she is interested in and a comprehensive search feature so that the users get just what they need. It was quite a challenge to deal with all the responses that would be delivered by the API and render the site accordingly, nonetheless it was great fun and immense learning.

Additionally the API allows only 100 requests per day in the developer plan hence care is taken to avoid unnecessary multiple query requests; like when the home page is loaded on startup only one query request is made and the received data is held onto as the API provides fresh content at an interval of one hour and the news is one hour older than real-time.

The project adheres to stated requirements like use of django models, javascript and mobile responsiveness.

#### Files and directories
  - `news` - main application directory.
    - `static/news` contains all static content.
        - `css` contains compiled CSS file.
           - `index.css` - css file to style the home and other templates.
           - `lgin.css` - css file to style the register and login templates.
        - `images` - image used for register and login templates.
        - `js` -  JavaScript files used in project.
            - `index.js` - script that runs in all of the templates except for `login.html` and `register.html` template.

    - `templates/news` contains all application templates.
        - `layout.html` - base template. `login.html` and `register.html` templates extend it.
        - `login.html` - provides login facility to already registered user
        - `register.html` - new users can register here so that they too can get curated content based on their category subscription
        - `index_layout.html` - base template. All other templates extend it except `login.html` and `register.html`.
        - `home.html` - this template renders the home page on startup.
        - `search.html` - renders the search results.
        - `category.html` - renders the articles of selected category.
        - `feed.html` - shows the curated feed to that particular user based on the categories they follow (only for registered users).
        .
    - `admin.py` - the corresponding models in models.py file are registered here.
    - `models.py` contains two models, viz the User model and the Categories model.
    - `urls.py` - all application URLs.
    - `views.py` contains all application views.
  - `capstone` - project directory.
    - `.env` - contains the API key unique to me which will be configured in the settings.py file to be used as an environment variable.
  - `.gitignore` - is populated with `.env` so as to safeguard potential leak of the API key online
  -  `requirements.txt` - has two additional modules namely the `request` module to query the API for information and the `django-environ` module to configure this    django application with environment variables.

The project's video: https://youtu.be/MshADuMuBSM
