'use strict';
const path = require('path');
const {promisify} = require('util');
const childProcess = require('child_process');

const execFile = promisify(childProcess.execFile);
const bin = path.join(__dirname, '../main');

const parseMac = stdout => {
	try {
		const result = JSON.parse(stdout);
		if (result !== null) {
			result.platform = 'macos';
			return result;
		}
	} catch (error) {
		console.error(error);
		throw new Error('Error parsing window data');
	}
};

const getArguments = options => {
	if (!options) {
		return [];
	}

	const args = [];
	if (options.screenRecordingPermission === false) {
		args.push('--no-screen-recording-permission');
	}

	return args;
};

module.exports = async options => {
	return new Promise( (resolve) => {
		const {stdout} = await execFile(bin, getArguments(options));
		resolve(parseMac(stdout));
	});
};

module.exports.sync = options => {
	return new Promise( (resolve) => {
		const stdout = childProcess.execFileSync(bin, getArguments(options), {encoding: 'utf8'});
		resolve(parseMac(stdout));
	});
};
