var gamebook = {
    'player' : {
        'started' : false,
        'currentSection' : -1,
        'collections' : {},
        counters : {},

        'collect' : function(type, name) {
            if (type in this.collections) {
                return;
            }
            this.collections[type] = {
                'name' : name,
                'contents' : [],
                'dropped' : {},
                'add' : function(what) {
                    if (this.contents.indexOf(what) === -1 &&
                        !(what in this.dropped)) {
                        this.contents.push(what);
                        this.contents.sort();
                    }
                },
                'drop' : function(what) {
                    var i = this.contents.indexOf(what);
                    if (i >= 0) {
                        this.contents.splice(i, 1);
                        this.dropped[what] = true;
                    }
                },
                'has' : function(what) {
                    return this.contents.indexOf(what) >= 0;
                }
            };
            gamebook.addCollectionView(type, name);
        },

        count : function(type, name) {
            if (type in this.counters) {
                return;
            }
            this.counters[type] = {
                inited : false,
                name : name,
                value : 0,
                minValue : null, //no minimum set
                inc : function(amount) {
                    this.value += amount;
                    this.inited = true;
                },
                dec : function(amount) {
                    this.value -= amount;
                    this.ensureNotBelowMin();
                    this.inited = true;
                },
                set : function(value) {
                    this.value = value;
                    this.ensureNotBelowMin();
                    this.inited = true;
                },
                init : function(value) {
                    if (!this.inited) {
                        this.value = value;
                        this.inited = true;
                    }
                },
                min : function(limit) {
                    this.minValue = limit;
                    this.ensureNotBelowMin();
                },
                ensureNotBelowMin : function() {
                    if (this.minValue !== null && this.value < this.minValue) {
                        this.value = this.minValue;
                    }
                }
            };
            gamebook.addCounterView(type, name);
        },

        'add' : function(type, what) {
            this.collections[type].add(what);
            gamebook.updateCollectionsView();
        },

        'drop' : function(type, what) {
            this.collections[type].drop(what);
            gamebook.updateCollectionsView();
        },

        'has' : function(type, what) {
            return this.collections[type].has(what);
        },

        inc : function(type, amount) {
            this.counters[type].inc(amount);
            gamebook.updateCountersView();
        },

        dec : function(type, amount) {
            this.counters[type].dec(amount);
            gamebook.updateCountersView();
        },

        min : function(type, limit) {
            this.counters[type].min(limit);
            gamebook.updateCountersView();
        },

        set : function(type, amount) {
            this.counters[type].set(amount);
            gamebook.updateCountersView();
        },

        init : function(type, amount) {
            this.counters[type].init(amount);
            gamebook.updateCountersView();
        },

        'hasMoreThan' : function(type, amount) {
            return this.counters[type].value > amount;
        },

        'hasLessThan' : function(type, amount) {
            return this.counters[type].value < amount;
        },

        'getState' : function() {
            return JSON.stringify({
                'collections' : this.collections,
                'currentSection' : this.currentSection,
                'counters' : this.counters
            });
        },

        'setState' : function(state) {
            var parsedState = JSON.parse(state);
            this.currentSection = parsedState.currentSection;
            for (var c in parsedState.collections) {
                var collection = parsedState.collections[c];
                if (!(c in this.collections)) {
                    this.collect(c, collection.name);
                } else {
                    this.collections[c].name = collection.name;
                }
                this.collections[c].contents = collection.contents;
                this.collections[c].dropped = collection.dropped;
            }
            for (var ct in parsedState.counters) {
                var counter = parsedState.counters[ct];
                if (ct in this.counters) {
                    this.counters[ct].name = counter.name;
                } else {
                    this.count(ct, counter.name);
                }
                this.counters[ct].minValue = counter.minValue;
                this.counters[ct].value = counter.value;
            }
        }
    },

    'sections' : {},

    'turnToFunctions' : {},

    'addSection' : function(nr, element) {
        var section = {'element' : element, 'nr' : nr};
        this.sections[nr] = section;
    },

    'turnTo' : function(nr) {
        if (!gamebook.player.started) {
            gamebook.start();
        }
        if (!(nr in this.sections)) {
            throw new Exception("Can not turn to non-existing section " +
                                nr + ".");
        }
        this.displaySection(nr);
    },

    prepare : function() {
        this.addClassToClass('section', 'nodisplay');
        this.runActionsInIntroSections();
    },

    'start' : function() {
        this.hideIntroSections();
        this.addClassToClass('startlink', 'nodisplay');
        this.addClassToClass('resumelink', 'nodisplay');
        gamebook.player.started = true;
    },

    'displaySection' : function(nr) {
        if (this.player.currentSection > 0) {
            var section = this.sections[this.player.currentSection];
            section.element.style.display = 'none';
        }
        this.player.currentSection = nr;
        this.saveGame();
        var e = this.sections[nr].element;
        this.runActions(e.getElementsByClassName('sectiontext')[0]);
        e.style.display = 'block';
    },

    //FIXME move out from gamebook object
    'saveGame' : function() {
        if (typeof window !== 'undefined' && 'localStorage' in window) {
            window.localStorage.setItem('savedGamebookPlayer',
                                        this.player.getState());
        }
    },

    //FIXME move out from gamebook object
    'hasSavedGame' : function() {
        if (typeof window !== 'undefined' && 'localStorage' in window) {
            return window.localStorage.getItem('savedGamebookPlayer');
        } else {
            return false;
        }
    },

    //FIXME move out from gamebook object
    'loadGame' : function() {
        if (typeof window !== 'undefined' && 'localStorage' in window) {
            var state = window.localStorage.getItem('savedGamebookPlayer');
            this.player.setState(state);
            this.turnTo(this.player.currentSection);
            this.updateCollectionsView();
        } else {
            //FIXME some kind of error, because we should never get here
        }
    },

    'hideIntroSections' : function() {
        this.addClassToClass('introsection', 'nodisplay');
        this.removeClassFromClass('displayintrolink', 'nodisplay');
        this.addClassToClass('hideintrolink', 'nodisplay');
    },

    'showIntroSections' : function() {
        this.runActionsInIntroSections();
        this.removeClassFromClass('introsection', 'nodisplay');
        this.addClassToClass('displayintrolink', 'nodisplay');
        this.removeClassFromClass('hideintrolink', 'nodisplay');
        document.body.scrollIntoView();
    },

    'runActionsInIntroSections' : function() {
        Array.prototype.forEach.call(
            document.getElementsByClassName('introsectionbody'),
            gamebook.runActions);
    },

    'addClassToClass' : function(className, addClass) {
        Array.prototype.forEach.call(
            document.getElementsByClassName(className),
            function(e) {
                e.classList.add(addClass);
            });
    },

    'removeClassFromClass' : function(className, removeClass) {
        Array.prototype.forEach.call(
            document.getElementsByClassName(className),
            function(e) {
                e.classList.remove(removeClass);
            });
    },

    'runActions' : function(e) {
        var enableNextLink = true;
        var hasXorScope = false;
        var hasAutoScope = false;
        var xorEnableNext = false;
        var lastCanHaveCost = null;
        var autoDisableAllRemaining = (
            gamebook.player.started  &&
                e.classList.contains('introsectionbody'));
        Array.prototype.forEach.call(e.childNodes, function(c) {
            if (!c.classList) {
                return;
            }
            // FIXME yes, this must be split up
            if (c.classList.contains('sectionref')) {
                if (enableNextLink && !autoDisableAllRemaining) {
                    gamebook.enableLink(c);
                    if (hasAutoScope) {
                        autoDisableAllRemaining = true;
                    }
                } else {
                    gamebook.disableLink(c);
                }
                lastCanHaveCost = c;
                enableNextLink = !(hasXorScope && !xorEnableNext);
                hasAutoScope = false;
                hasXorScope = false;
            } else if (autoDisableAllRemaining) {
                return; // no further actions will be taken after enabled auto
            } else if (c.classList.contains('collect')) {
                gamebook.player.collect(c.dataset.type, c.dataset.name);
            } else if (c.classList.contains('add')) {
                gamebook.player.add(c.dataset.type, c.dataset.what);
            } else if (c.classList.contains('drop')) {
                gamebook.player.drop(c.dataset.type, c.dataset.what);
            } else if (c.classList.contains('count')) {
                gamebook.player.count(c.dataset.type, c.dataset.name);
            } else if (c.classList.contains('set')) {
                gamebook.player.set(c.dataset.type,
                                    parseInt(c.dataset.amount, 10));
            } else if (c.classList.contains('init')) {
                gamebook.player.init(c.dataset.type,
                                     parseInt(c.dataset.amount, 10));
            } else if (c.classList.contains('inc')) {
                gamebook.player.inc(c.dataset.type,
                                    parseInt(c.dataset.amount, 10));
            } else if (c.classList.contains('dec')) {
                gamebook.player.dec(c.dataset.type,
                                    parseInt(c.dataset.amount, 10));
            } else if (c.classList.contains('min')) {
                gamebook.player.min(c.dataset.type,
                                    parseInt(c.dataset.limit, 10));
            } else if (c.classList.contains('has')) {
                enableNextLink = gamebook.player.has(c.dataset.type,
                                                     c.dataset.what);
            } else if (c.classList.contains('morethan')) {
                enableNextLink = gamebook.player.hasMoreThan(
                    c.dataset.type, parseInt(c.dataset.amount, 10));
            } else if (c.classList.contains('lessthan')) {
                enableNextLink = gamebook.player.hasLessThan(
                    c.dataset.type, parseInt(c.dataset.amount, 10));
            } else if (c.classList.contains('atleast')) {
                enableNextLink = gamebook.player.hasMoreThan(
                    c.dataset.type, parseInt(c.dataset.amount, 10) - 1);
            } else if (c.classList.contains('hasnot')) {
                enableNextLink = !gamebook.player.has(c.dataset.type,
                                                      c.dataset.what);
            } else if (c.classList.contains('xor')) {
                hasXorScope = true;
                xorEnableNext = !enableNextLink;
            } else if (c.classList.contains('auto')) {
                hasAutoScope = true;
            } else if (c.classList.contains('random')) {
                c.addEventListener('click',
                                   gamebook.enableRandomLinkAfter);
                c.classList.add("enabledlink");
                c.classList.remove("disabledlink");
                autoDisableAllRemaining = true;
            } else if (c.classList.contains('found')) {
                lastCanHaveCost = c;
                c.addEventListener('click', gamebook.takeFound);
            } else if (c.classList.contains('cost')) {
                gamebook.addCost(c, lastCanHaveCost);
            } else if (c.classList.contains('trade')) {
                gamebook.addTrade(c, lastCanHaveCost);
            }

        });
    },

    addCost : function(c, e) {
        var cost = parseInt(c.dataset.amount, 10);
        var counter = gamebook.player.counters[c.dataset.type];
        if (counter.value - cost >= counter.minValue) {
            e.classList.add("enabledlink");
            e.classList.remove("disabledlink");
            e.dataset.cost = c.dataset.amount;
            e.dataset.costtype = c.dataset.type;
        } else {
            e.classList.add("disabledlink");
            e.classList.remove("enabledlink");
        }
    },

    addTrade : function(c, e) {
        var what = c.dataset.what;
        var tradetype = c.dataset.type;
        if (gamebook.player.has(tradetype, what)) {
            e.classList.add("enabledlink");
            e.classList.remove("disabledlink");
            e.dataset.trade = what;
            e.dataset.tradetype = tradetype;
        } else {
            e.classList.add("disabledlink");
            e.classList.remove("enabledlink");
        }
    },

    'enableLink' : function(e) {
        e.addEventListener('click', gamebook.getTurnToFunction(e.dataset.ref));
        e.classList.add("enabledlink");
        e.classList.remove("disabledlink");
    },

    'disableLink' : function(e) {
        e.removeEventListener('click',
                           gamebook.getTurnToFunction(e.dataset.ref));
        e.classList.remove("enabledlink");
        e.classList.add("disabledlink");
    },

    'enableRandomLinkAfter' : function(event) {
        this.classList.remove("enabledlink");
        this.classList.add("disabledlink");
        var links = [];
        var e = this.nextSibling;
        while (e) {
            if (e.classList && e.classList.contains('sectionref')) {
                links.push(e);
            }
            e = e.nextSibling;
        }
        if (links.length > 0) {
            var selected = links[Math.floor(Math.random()*links.length)];
            gamebook.enableLink(selected);
        } else {
            console.log("Random with nothing to select?");
        }
        event.preventDefault();
    },

    'addCollectionView' : function(type, name) {
        this.addView('collection', type, name);
    },

    addCounterView : function(type, name) {
        this.addView('counter', type, name);
    },

    addView : function(view, type, name) {
        var ce = document.getElementById(view + 's');
        var template = document.getElementById(view + 'Template');
        var e = template.cloneNode(true);
        e.className = view;
        e.getElementsByClassName(view + 'heading')[0].innerHTML = name;
        e.dataset.type = type;
        ce.appendChild(e);
    },

    'updateCollectionsView' : function() {
        var ce = document.getElementById('collections');
        Array.prototype.forEach.call(ce.childNodes, function(c) {
            if (c.className === 'collection') {
                var type = c.dataset.type;
                var collection = gamebook.player.collections[type];
                var cc = c.getElementsByClassName('collectioncontents')[0];
                cc.innerHTML = collection.contents.join(', ');
            }
        });
    },

    'updateCountersView' : function() {
        var ce = document.getElementById('counters');
        Array.prototype.forEach.call(ce.childNodes, function(c) {
            if (c.className === 'counter') {
                var type = c.dataset.type;
                var counter = gamebook.player.counters[type];
                var cc = c.getElementsByClassName('countercontents')[0];
                cc.innerHTML = counter.value;
            }
        });
    },

    'getTurnToFunction' : function(nr) {
        if (nr in this.turnToFunctions) {
            return this.turnToFunctions[nr];
        } else {
            var f = function () {
                if (gamebook.payPrice(this)) {
                    gamebook.turnTo(nr);
                }
            };
            this.turnToFunctions[nr] = f;
            return f;
        }
    },

    'takeFound' : function(evt) {
        evt.preventDefault();
        if (!gamebook.payPrice(this)) {
            return false;
        }
        this.classList.remove("enabledlink");
        this.classList.add("disabledlink");
        var what = this.dataset.what;
        var type = this.dataset.type;
        gamebook.player.add(type, what);
        gamebook.disableLinksNowTooExpensive();
    },

    'payPrice' : function(e) {
        var cost, counter, trade, tradetype;
        if ('cost' in e.dataset && 'costtype' in e.dataset) {
            cost = parseInt(e.dataset.cost, 10);
            counter = gamebook.player.counters[e.dataset.costtype];
            if (counter.value - cost < counter.minValue) {
                return false;
            }
        }
        if ('trade' in e.dataset && 'tradetype' in e.dataset) {
            trade = e.dataset.trade;
            tradetype = e.dataset.tradetype;
            if (!gamebook.player.has(tradetype, trade)) {
                return false;
            }
        }
        if (cost) {
            counter.dec(cost);
            gamebook.updateCountersView();
        }
        if (trade) {
            gamebook.player.drop(tradetype, trade);
        }
        return true;
    },

    'disableLinksNowTooExpensive' : function() {
        var e = this.sections[this.player.currentSection].element;
        var cs = e.getElementsByClassName('sectiontext')[0].childNodes;
        Array.prototype.forEach.call(cs, function(c) {
            if (c.dataset && 'cost' in c.dataset && 'costtype' in c.dataset) {
                var cost = parseInt(c.dataset.cost, 10);
                var counter = gamebook.player.counters[c.dataset.costtype];
                if (counter.value - cost < counter.minValue) {
                    c.classList.remove("enabledlink");
                    c.classList.add("disabledlink");
                }
            }
        });
    }

};

// little hack to make easy to test from node.js
if (typeof exports !== 'undefined') {
    exports.gamebook = gamebook;
}
