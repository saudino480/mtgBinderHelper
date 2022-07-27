## mtgBinderHelper

Project is still a work in progress. Hoping to have the app fulfill the following goals:

- Card storage and price tracking
	- Tracking will include the ability to see which cards have crossed the $1 mark and for how many weeks, also if cards have gone under $1.
	- Cards can be marked by their physical location in your collection. This will be a custom field,
	essentially just an extra search criteria. You can set alerts based on these categories.

- Mass Entry of Cards
	- API connection to echoMTG will be one of the first things implemented. You can enter your account information and it will download and add your collection to your collection. You'll be able to tag cards either en masse or individually before they are commited to the DB.
	- CSV will also be accepted, with guidelines and an example CSV you can download.

Special thanks to the people working at Flask and Miguel Grinberg for his tutorials on adding tables to Flask applications that you can find [here.](https://github.com/miguelgrinberg/flask-gridjs)

- Flexible Search Options
	- 