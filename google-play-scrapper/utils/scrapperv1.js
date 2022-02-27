// const scrapedCollectionPromise = new Promise((res, rej) => {
// 	categories.forEach(async category => {
// 		console.log(`SCRAPING ${numOfScrapes} TOP FREE ${category}`);
// 		const categoryPromise = new Promise((res, rej) => {
// 			console.time(`Time taken for scrapping ${category}`);
// 			gplay
// 				.list({
// 					category: category,
// 					collection: gplay.collection.TOP_FREE,
// 					num: numOfScrapes,
// 					fullDetail: true,
// 				})
// 				.then(async data => {
// 					// array of objects\
// 					console.log(data);
// 					const formattedData = [];

// 					const today = new Date();
// 					const formattedDate = formatDate(today, "dd/mm/yy");

// 					data.map(async appDetails => {
// 						formattedData.push({
// 							app_name: appDetails.title,
// 							rating: appDetails.score,
// 							category: appDetails.genre,
// 							rating_count: appDetails.ratings,
// 							installs: appDetails.installs,
// 							min_installs: appDetails.minInstalls,
// 							max_installs: appDetails.maxInstalls,
// 							free: appDetails.free,
// 							price: appDetails.price,
// 							currency: appDetails.currency,
// 							size: appDetails.size,
// 							content_rating: appDetails.contentRating,
// 							ad_supported: appDetails.adSupported,
// 							in_app_purchases: appDetails.offersIAP,
// 							day_scraped: formattedDate,
// 						});
// 					});
// 					res(formattedData);
// 					currentCatCount++;
// 				})
// 				.then(() => {
// 					console.log(`Scrapped complete for ${category}`);
// 					console.timeEnd(`Time taken for scrapping ${category}`);
// 				})
// 				.catch(err =>
// 					console.log(`Something when wrong when scrapping ${category}` + err)
// 				);
// 		});
// 		categoryPromise.then(async data => {
// 			finalCsvData = [...finalCsvData, ...data];
// 			if (currentCatCount == numOfCats) {
// 				res(finalCsvData);
// 			}
// 		});
// 	});
// });

// scrapedCollectionPromise
// 	.then(async data => await csvWriter.writeRecords(data))
// 	.then(() => {
// 		console.log("Done writing into output.csv");
// 		console.timeEnd(
// 			`Time for scraping ${numOfScrapes} for each ${numOfCats} categories`
// 		);
// 	})
// 	.catch(err => console.log("Error found: " + err));
