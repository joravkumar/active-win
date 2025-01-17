#!/usr/bin/env node
'use strict';
const meow = require('meow');
const activeWin = require('./index');

const cli = meow(`
	Usage
	  $ active-win [property]

	  Returns title, id, app, pid, or the specified property

	Examples
	  $ active-win
	  npm install
	  54
	  Terminal
	  368
	  $ active-win app
	  Terminal
`);


function main() {
	activeWin().then((ret) => {
		const validProps = ['title', 'id', 'app', 'path', 'url', 'browser'];
		const prop = cli.input[0];

		if (prop) {
			if (validProps.indexOf(prop) === -1) {
				console.error(`Specify a valid property: ${validProps.join(', ')}`);
				process.exit(1);
			}

			console.log(ret[prop]);
			process.exit();
		}

		console.log(ret);
	});
}

async function handleTracking() {
    try {
      	const appData = await activeWin();
	  	console.log(appData);
    } catch (error) {
		console.log(error);
    } finally {
		//global.gc();
      	setTimeout(handleTracking, 3000);
    }
};

handleTracking();