// change this 1 to 500
const numOfScrapes = 1;

const gplay = require("google-play-scraper");
const createCsvWriter = require("csv-writer").createObjectCsvWriter;
const categories = require("./constants/categories.js");
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
	],
});

const numOfCats = categories.length;
let count = 0;
console.log("Scrapping all Cats ... ");

let finalCsvData = [];
const scrappingPromise = new Promise((res, rej) => {
	categories.forEach(async category => {
		console.log(`Scrapping ${numOfScrapes} TOP FREE ${category} ...`);
		const categoryPromise = new Promise((res, rej) => {
			gplay
				.list({
					category: category,
					collection: gplay.collection.TOP_FREE,
					num: numOfScrapes,
					fullDetail: true,
				})
				.then(async data => {
					// array of objects\
					const formattedData = [];
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
						});
					});
					res(formattedData);
					count++;
				})
				.then(() => console.log(`Scrapped complete for ${category}`))
				.catch(err =>
					console.log(`Something when wrong when scrapping ${category}` + err)
				);
		});
		categoryPromise.then(async data => {
			finalCsvData = [...finalCsvData, ...data];
			if (count == numOfCats) {
				res(finalCsvData);
			}
		});
	});
});

scrappingPromise.then(async data => await csvWriter.writeRecords(data));
