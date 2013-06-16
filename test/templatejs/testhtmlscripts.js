#!/usr/bin/env node

exports.setUp = function(cb) {
    this.hs = hs = require('./htmlscripts.js');
    cb();
};

exports.test1 = function(test) {
    test.deepEqual(this.hs.gamebook.player.collections, {});
    test.done();
};

var reporter = require('nodeunit').reporters['default'];

process.chdir(__dirname);
reporter.run(['./testhtmlscripts.js']);

