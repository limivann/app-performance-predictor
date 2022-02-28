const gplay = require("google-play-scraper");
const collections = [
	gplay.collection.TOP_FREE,
	gplay.collection.TOP_PAID,
	gplay.collection.GROSSING,
	// gplay.collection.TOP_FREE_GAMES,
	// gplay.collection.TOP_PAID_GAMES,
	// gplay.collection.TOP_GROSSING_GAMES,
	// gplay.collection.TRENDING,
	// gplay.collection.NEW_FREE,
	// gplay.collection.NEW_PAID,
	// gplay.collection.NEW_FREE_GAMES,
	// gplay.collection.NEW_PAID_GAMES,
];

module.exports = collections;
