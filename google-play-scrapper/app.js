// change this 1 to 500
const numOfScrapes = 350;
const fileName = "output_6";

const gplay = require("google-play-scraper");
const createCsvWriter = require("csv-writer").createObjectCsvWriter;
const fs = require("fs");
const categories = require("./constants/categories.js");
const collections = require("./constants/collections");

// create file
fs.writeFile(`./output/${fileName}.csv`, "", err => {
	if (err) {
		console.error(err);
		return;
	}
	//file written successfully
});

const csvWriter = createCsvWriter({
	path: `./output/${fileName}.csv`,
	header: [
		{ id: "app_name", title: "APP_NAME" },
		{ id: "rating", title: "RATING" },
		{ id: "category", title: "CATEGORY" },
		{ id: "collection", title: "COLLECTIONS" },
		{ id: "rating_count", title: "RATING_COUNT" },
		{ id: "rating_1", title: "1_STAR_RATINGS" },
		{ id: "rating_2", title: "2_STAR_RATINGS" },
		{ id: "rating_3", title: "3_STAR_RATINGS" },
		{ id: "rating_4", title: "4_STAR_RATINGS" },
		{ id: "rating_5", title: "5_STAR_RATINGS" },
		{ id: "review_count", title: "REVIEW_COUNT" },
		{ id: "installs", title: "INSTALLS" },
		{ id: "min_installs", title: "MIN_INSTALLS" },
		{ id: "max_installs", title: "MAX_INSTALLS" },
		{ id: "free", title: "FREE" },
		{ id: "price", title: "PRICE" },
		{ id: "currency", title: "CURRENCY" },
		{ id: "size", title: "SIZE" },
		{ id: "developer", title: "DEVELOPER" },
		{ id: "developer_addr", title: "DEVELOPER_ADDRESS" },
		{ id: "content_rating", title: "CONTENT_RATING" },
		{ id: "family_genre", title: "FAMILY_GENRE" },
		{ id: "ad_supported", title: "AD_SUPPORTED" },
		{ id: "in_app_purchases", title: "IN_APP_PURCHASES" },
		{ id: "released_date", title: "RELEASED_DATE" },
		{ id: "last_updated", title: "LAST_UPDATED" },
		{ id: "day_scraped", title: "DAY_SCRAPED" },
	],
});
const numOfCats = categories.length;
const numOfCollections = collections.length;

console.log(numOfCollections, numOfCats);
let currentCount = 0;
const countGoal = numOfCollections * numOfCats;
let finalCsvData = [];

const formatDate = (date, format) => {
	const map = {
		mm: date.getMonth() + 1,
		dd: date.getDate(),
		yy: date.getFullYear().toString().slice(-2),
		yyyy: date.getFullYear(),
	};

	return format.replace(/mm|dd|yy|yyy/gi, matched => map[matched]);
};

const sleepFor = sleepDuration => {
	const now = new Date().getTime();
	while (new Date().getTime() < now + sleepDuration) {
		/* Do nothing */
	}
};

const listOfSkippedCategoriesForTopPaid = [gplay.category.GAME_ACTION];

const listOfSkippedCategoriesForGrossing = [
	gplay.category.GAME_ACTION,
	gplay.category.GAME_BOARD,
	gplay.category.GAME_ADVENTURE,
];

console.log("STARTING GOOGLE PLAY SCRAPER");
console.time("TIME FOR SCRAPING ALL CATS");

const scrappedAllDataPromise = new Promise((resolveSAP, rejSAP) => {
	collections.forEach(async collection => {
		sleepFor(2000);
		console.log(`SCRAPING COLLECTION: ${collection}`);
		console.log("==================================");
		categories.forEach(async category => {
			sleepFor(4000);
			console.log(
				`SCRAPPING CATEGORY: ${category} IN COLLECTION ${collection}`
			);
			const categoryPromise = new Promise((resCP, rejCP) => {
				if (collection === gplay.collection.TOP_FREE) {
					// Check
				}
				if (collection == gplay.collection.TOP_PAID) {
					if (listOfSkippedCategoriesForTopPaid.includes(category)) {
						currentCount++;
						resCP([]);
						console.log(
							`SCRAPING COMPLETE FOR ${category} FOR THE COLLECTION ${collection} [SKIPPED]`
						);
						return;
					}
				}
				if (collection == gplay.collection.GROSSING) {
					if (listOfSkippedCategoriesForGrossing.includes(category)) {
						currentCount++;
						resCP([]);
						console.log(
							`SCRAPING COMPLETE FOR ${category} FOR THE COLLECTION ${collection} [SKIPPED]`
						);
						return;
					}
				}
				gplay
					.list({
						category: category,
						collection: collection,
						num: numOfScrapes,
						fullDetail: true,
					})
					.then(async data => {
						const formattedData = [];
						const today = new Date();
						const formattedDate = formatDate(today, "dd/mm/yy");

						data.map(async appDetails => {
							const dateObj = new Date(appDetails.updated);
							const lastUpdatedDate = formatDate(dateObj, "dd/mm/yy");

							const rating_hist = appDetails.histogram;
							const rating_1 = rating_hist["1"];
							const rating_2 = rating_hist["2"];
							const rating_3 = rating_hist["3"];
							const rating_4 = rating_hist["4"];
							const rating_5 = rating_hist["5"];

							formattedData.push({
								app_name: appDetails.title,
								rating: appDetails.score,
								category: appDetails.genre,
								collection: collection,
								rating_count: appDetails.ratings,
								rating_1: rating_1,
								rating_2: rating_2,
								rating_3: rating_3,
								rating_4: rating_4,
								rating_5: rating_5,
								review_count: appDetails.reviews,
								installs: appDetails.installs,
								min_installs: appDetails.minInstalls,
								max_installs: appDetails.maxInstalls,
								free: appDetails.free,
								price: appDetails.price,
								currency: appDetails.currency,
								size: appDetails.size,
								developer: appDetails.developer,
								developer_addr: appDetails.developerAddress,
								content_rating: appDetails.contentRating,
								family_genre: appDetails.familyGenre,
								ad_supported: appDetails.adSupported,
								in_app_purchases: appDetails.offersIAP,
								released_date: appDetails.released,
								last_updated: lastUpdatedDate,
								day_scraped: formattedDate,
							});
						});
						currentCount++;
						resCP(formattedData);
						console.log(
							`SCRAPING COMPLETE FOR ${category} FOR THE COLLECTION ${collection}`
						);
					})
					.catch(err => {
						console.log("ERROR: " + err);
						rejCP(err);
						currentCount++;
					});
			});
			categoryPromise
				.then(async data => {
					finalCsvData = [...finalCsvData, ...data];
					if (currentCount == countGoal) {
						resolveSAP(finalCsvData);
					}
				})
				.catch(err => {
					if (currentCount == countGoal) {
						resolveSAP(finalCsvData);
					}
				});
		});
	});
});

scrappedAllDataPromise
	.then(async data => {
		let status = await csvWriter.writeRecords(data);
	})
	.then(() => {
		console.log("WRITE TO FILE COMPLETE");
		console.timeEnd("TIME FOR SCRAPING ALL CATS");
	})
	.catch(err => {
		console.log("SOMETHING WENT WRONG: " + err);
	});
