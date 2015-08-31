/*
 Global variables.
 (Hey, it's JS. Did you expect there wouldn't be any?
 */
var selectedSpellIDs;
var statisticsGroups;

$(function () {
    $.getJSON("/behind-the-scenes/statistics/", function (data) {
        statisticsGroups = data.groups;
    });

    setListeners();

    selectedSpellIDs = [];
});