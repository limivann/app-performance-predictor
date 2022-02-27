// change this 1 to 500
const numOfScrapes = 1;

const gplay = require("google-play-scraper");
const createCsvWriter = require("csv-writer").createObjectCsvWriter;
const categories = require("./constants/categories.js");
const collections = require("./constants/collections");

const csvWriter = createCsvWriter({
	path: "./output/output.csv",
	header: [
		{ id: "app_name", title: "APP_NAME" },
		{ id: "rating", title: "RATING" },
		{ id: "category", title: "CATEGORY" },
		{ id: "rating_count", title: "RATING_COUNT" },
		{ id: "installs", title: "INSTALLS" },
		{ id: "min_installs", title: "MIN_INSTALLS" },
		{ id: "max_installs", title: "MAX_INSTALLS" },
		{ id: "free", title: "FREE" },
		{ id: "price", title: "PRICE" },
		{ id: "currency", title: "CURRENCY" },
		{ id: "size", title: "SIZE" },
		{ id: "content_rating", title: "CONTENT_RATING" },
		{ id: "ad_supported", title: "AD_SUPPORTED" },
		{ id: "in_app_purchases", title: "IN_APP_PURCHASES" },
		{ id: "day_scraped", title: "DAY_SCRAPED" },
		{ id: "collection", title: "COLLECTIONS" },
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

console.log("Scrapping all Cats ... ");
console.time(
	`Time for scraping ${numOfScrapes} for each ${numOfCats} categories`
);

const scrappedAllDataPromise = new Promise((resolveSAP, rej) => {
	collections.forEach(async collection => {
		console.log(`SCRAPING COLLECTION: ${collection}`);
		console.log("==================================");
		categories.forEach(async category => {
			const categoryPromise = new Promise((resCP, rej) => {
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
							formattedData.push({
								app_name: appDetails.title,
								rating: appDetails.score,
								category: appDetails.genre,
								rating_count: appDetails.ratings,
								installs: appDetails.installs,
								min_installs: appDetails.minInstalls,
								max_installs: appDetails.maxInstalls,
								free: appDetails.free,
								price: appDetails.price,
								currency: appDetails.currency,
								size: appDetails.size,
								content_rating: appDetails.contentRating,
								ad_supported: appDetails.adSupported,
								in_app_purchases: appDetails.offersIAP,
								day_scraped: formattedDate,
								collection: collection,
							});
						});
						resCP(formattedData);
						currentCount++;
						console.log(
							`SCRAPING COMPLETE FOR ${category} FOR THE COLLECTION ${collection}`
						);
					});
			});
			categoryPromise.then(async data => {
				finalCsvData = [...finalCsvData, ...data];
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
	.then(() => console.log("WRITE TO FILE COMPLETE"));
