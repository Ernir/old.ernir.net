/*
 Global variables
 (Hey, it's JS. Did you expect there wouldn't be any?
 */
var selectedSpellIDs = [];

var numericalBonuses;
var statistics;
var modifierTypes;
var CL; //Caster Level

$(function() {
    $.getJSON("/api/bufftracker",function(data){
        numericalBonuses =data.content.numericalBonuses;
        statistics = data.content.statistics;
        modifierTypes = data.content.modifierTypes;
        setListeners();
    });
})