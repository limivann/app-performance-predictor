const gplay = require("google-play-scraper");
const createCsvWriter = require("csv-writer").createObjectCsvWriter;

// csv headers
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

gplay
	.app({ appId: "com.google.android.apps.translate" })
	.then(async data => {
		// array of objects
		let formattedData = [
			{
				app_name: data.title,
				rating: data.score,
				category: data.genre,
				rating_count: data.ratings,
				installs: data.installs,
				min_installs: data.minInstalls,
				max_installs: data.maxInstalls,
				free: data.free,
				price: data.price,
				currency: data.currency,
				size: data.size,
				content_rating: data.contentRating,
				ad_supported: data.adSupported,
				in_app_purchases: data.offersIAP,
			},
		];
		await csvWriter.writeRecords(formattedData);
	})
	.then(() => console.log("Scrapped complete!"))
	.catch(err => console.log("Something went wrong " + err));
