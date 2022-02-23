const gplay = require("google-play-scraper");
const createCsvWriter = require("csv-writer").createObjectCsvWriter;

const csvWriter = createCsvWriter({
	path: "./output/topFreeActionGames.csv",
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

const numOfScrapes = 1;
console.log(`Scrapping ${numOfScrapes} top free action games ...`);

gplay
	.list({
		category: gplay.category.GAME_ACTION,
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
		await csvWriter.writeRecords(formattedData);
	})
	.then(() => console.log("Scrapped complete!"))
	.catch(err => console.log("Something went wrong " + err));
