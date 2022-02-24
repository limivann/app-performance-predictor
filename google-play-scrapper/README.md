# Google play scrapper

## Google play store scrapper for SC1015 Data Science Project

The aim is generate a fresh and updated dataset for google play apps to make sure our project uses the most recent dataset.

This is done by sending api request using a api wrapper to scrape the google play store and then write the data collected into a csv file.

## Code organisation

The code is organised as follows.

- `./constants/` folder: contains all constants for categories and collections for scrapper options
- `./output/` folder: contains all csv output scrapped
- `./utils/` folder: contains other scrapping methods

## Scrapping options

To change the number of scrapes go to `app.js` and change the value of **numOfScrapes** variable

To change the categories to scrape go to `./constants/categories` and add/remove items from the array

For more information on categories type please refer to `categories.txt`

## Run

To make it run properly, clone this repo (app-rating-predictor) and make sure you have the following prerequisites.

- [Node](https://nodejs.org/en/download/) ^16.3.0
- [npm](https://nodejs.org/en/download/package-manager/)

From your command line go to google-play-scrapper folder and run the following scripts in the terminal.

1\. Go to google-play-scrapper folder

```terminal
$ cd google-play-scrapper
```

2\. Install dependencies

```terminal
$ npm install
```

3\. Start scrapping

```terminal
$ npm start
```

The output folder will then contain the scrapped data.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
