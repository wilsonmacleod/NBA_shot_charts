# NBA Shot Chart Generator

An app/website I made that generates shot charts for any player that has attempted a shot in the NBA in the past 10 years (season 2010-11 to 2019-20.)

I pulled the data from the unofficial ```nba.stats.com``` API, processed it using ```Pandas```  and then used ```Plotly``` to generate my charts. 

There are ```1828011``` individual shot data points included in the data-set and ```4919``` player/season combos. 

I chose ```Django``` as my web-framework because of its out of the box readiness in terms of its built-in DB and security features, I also have been writing too many ```React``` applications lately and Javascript makes me miss Python.

I then deployed the app using ```nginx``` for the static files and ```gunicorn``` and ```supervisord``` to run Django.

Check out the site [**here**](https://nbashotcharts.wilsonmacleod.com/%2F).

