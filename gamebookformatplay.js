var gamebook = {
    'player' : {
        'started' : false,
        'currentSection' : -1,
        'collections' : {},

        'collect' : function(type, name) {
            if (type in this.collections) {
                return;
            }
            this.collections[type] = {
                'name' : name,
                'contents' : [],
                'dropped' : {},
                'add' : function(what) {
                    if (this.contents.indexOf(what) === -1
                        && !(what in this.dropped)) {
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

        'getState' : function() {
            return JSON.stringify({
                'collections' : this.collections,
                'currentSection' : this.currentSection
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
        if (!nr in this.sections) {
            throw new Exception("Can not turn to non-existing section "
                                + nr + ".");
        }
        this.displaySection(nr);
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
        var e = this.sections[nr].element;
        this.runActions(e.getElementsByClassName('sectiontext')[0]);
        e.style.display = 'block';
        this.player.currentSection = nr;
        this.saveGame();
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
        var autoDisableAllRemainingLinks = (
            gamebook.player.started
            && e.classList.contains('introsectionbody'));
        Array.prototype.forEach.call(e.childNodes, function(c) {
            if (!c.classList) {
                return;
            }
            if (c.classList.contains('sectionref')) {
                if (enableNextLink && !autoDisableAllRemainingLinks) {
                    gamebook.enableLink(c);
                    if (hasAutoScope) {
                        autoDisableAllRemainingLinks = true;
                    }
                } else {
                    gamebook.disableLink(c);
                }
                enableNextLink = !(hasXorScope && !xorEnableNext);
                hasAutoScope = false;
                hasXorScope = false;
            } else if (c.classList.contains('collect')) {
                gamebook.player.collect(c.dataset.type, c.dataset.name);
            } else if (c.classList.contains('add')) {
                gamebook.player.add(c.dataset.type, c.dataset.what);
            } else if (c.classList.contains('drop')) {
                gamebook.player.drop(c.dataset.type, c.dataset.what);
            } else if (c.classList.contains('has')) {
                enableNextLink = gamebook.player.has(c.dataset.type,
                                                     c.dataset.what);
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
                autoDisableAllRemainingLinks = true;
            }
        });
    },

    'enableLink' : function(e) {
        e.addEventListener('click',
                           gamebook.getTurnToFunction(e.dataset.ref));
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
            var selected = links[Math.floor(Math.random()*links.length)]
            gamebook.enableLink(selected);
        } else {
            console.log("Random with nothing to select?");
        }
        event.preventDefault();
    },

    'addCollectionView' : function(type, name) {
        var ce = document.getElementById('collections');
        var template = document.getElementById('collectionTemplate');
        var e = template.cloneNode(true);
        e.className = "collection";
        e.getElementsByClassName('collectionheading')[0].innerHTML = name;
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

    'getTurnToFunction' : function(nr) {
        if (nr in this.turnToFunctions) {
            return this.turnToFunctions[nr];
        } else {
            var f = function () {
                gamebook.turnTo(nr);
            };
            this.turnToFunctions[nr] = f;
            return f;
        }
    }

};

// little hack to make easy to test from node.js
if (typeof exports !== 'undefined') {
    exports.gamebook = gamebook;
}
