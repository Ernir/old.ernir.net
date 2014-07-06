/*
 Global variables
 (Hey, it's JS. Did you expect there wouldn't be any?
 */
var selectedSpellIDs = [];

var statistics;
var modifierTypes;
var CL; //Caster Level

$(function () {
    $.getJSON("/api/bufftracker/statistics/", function (data) {
        if (data.status === 200) {
            statistics = data.content;
        }
    });

    $.getJSON("/api/bufftracker/modifiers/", function (data) {
        if (data.status === 200) {
            modifierTypes = data.content;
        }
    });
    setListeners();
});