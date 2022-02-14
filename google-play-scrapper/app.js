var gplay = require("google-play-scraper");

gplay
	.app({ appId: "com.google.android.apps.translate" })
	.then(console.log, console.log);

console.log("Scrapping complete!");
