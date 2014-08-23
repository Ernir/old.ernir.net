/*
 Global variables.
 (Hey, it's JS. Did you expect there wouldn't be any?
 */
var selectedSpellIDs;
var statisticsGroups;
var modifierTypes;

var $detailedCLInputs;

$(function () {
    $.getJSON("/api/bufftracker/statistics/", function (data) {
        if (data.status === 200) {
            statisticsGroups = data.content;
        }
    });

    $.getJSON("/api/bufftracker/modifiers/", function (data) {
        if (data.status === 200) {
            modifierTypes = data.content;
        }
    });
    setListeners();

    selectedSpellIDs = [];
});