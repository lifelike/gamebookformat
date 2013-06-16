#!/usr/bin/env node

var htmlscriptsfile = '../../gamebookformatplay.js';

exports.setUp = function(cb) {
    delete require.cache[require.resolve(htmlscriptsfile)];
    this.hs = require(htmlscriptsfile);
    this.gamebook = this.hs.gamebook;
    this.player = this.gamebook.player;

    // this is punishment for mixing view and model code in gamebook :(
    this.gamebook.addCollectionView = function() {
    };
    this.gamebook.updateCollectionsView = function() {
    };

    cb();
};

exports.testPlayerCollectAddItem = function(test) {
    this.player.collect('item', 'Carrying');
    test.ok(!this.player.has('item', 'sword'));
    this.player.add('item', 'sword');
    test.ok(this.player.has('item', 'sword'));
    test.done();
};

exports.testPlayerCollectAddDropItem = function(test) {
    this.player.collect('item', 'Carrying');
    test.ok(!this.player.has('item', 'sword'));
    this.player.add('item', 'sword');
    test.ok(this.player.has('item', 'sword'));
    this.player.drop('item', 'sword');
    test.ok(!this.player.has('item', 'sword'));
    test.deepEqual(this.player.collections['item'].dropped, {'sword' : true});
    test.done();
};

exports.testPlayerEmptyState = function(test) {
    stStr = this.player.getState();
    test.strictEqual(typeof stStr, "string");
    st = JSON.parse(stStr);
    test.deepEqual(st.collections, {});
    test.equal(st.currentSection, -1);
    test.done();
};

exports.testPlayerCollectionStateOneItem = function(test) {
    this.player.collect('item', 'Items');
    this.player.add('item', 'sword');
    st = JSON.parse(this.player.getState());
    test.deepEqual(st.collections, {'item' : {'name' : 'Items',
                                              'contents' : ['sword'],
                                              'dropped' : {}}});
    test.done();
};

exports.testPlayerStateCurrentSection = function(test) {
    this.player.currentSection = 2;
    st = JSON.parse(this.player.getState());
    test.equal(st.currentSection, 2);
    test.done();
};

exports.testPlayerSetState = function(test) {
    this.player.setState('{"currentSection":3}');
    test.equal(this.player.currentSection, 3);
    test.done();
};

exports.testPlayerSetStateCollection = function(test) {
    this.player.setState(
        '{"collections":{"a":{"name":"A","contents":[],"dropped":{}}}}');
    test.equal(this.player.collections.a.name, 'A');
    test.deepEqual(this.player.collections.a.contents, []);
    test.deepEqual(this.player.collections.a.dropped, {});
    test.done();
};

var reporter = require('nodeunit').reporters['default'];

process.chdir(__dirname);
reporter.run(['./testhtmlscripts.js']);

