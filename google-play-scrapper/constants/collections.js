const gplay = require("google-play-scraper");
const collections = [
	gplay.collection.TOP_FREE,
	gplay.collection.TOP_PAID,
	gplay.collection.GROSSING,
];

module.exports = collections;
