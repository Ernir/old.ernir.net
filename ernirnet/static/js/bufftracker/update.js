function updateSelectedSpells() {
    var currentSpellId = parseInt(this.id.replace("spell-", ""));
    if (this.checked) {
        selectedSpellIDs.push(currentSpellId);
    }
    else {
        selectedSpellIDs.splice(selectedSpellIDs.indexOf(currentSpellId), 1);
    }
    updateResults();
}

function updateGlobalCL() {
    var globalCL = $("#caster-level").val();
    $(".cl-detail").val(globalCL);

    updateResults();
}

function updateResults() {
    var CL = $("#caster-level").val()

    //constructMessage(CL);
    getBonuses(CL);
}

/*
    Returns a JS object consisting of spell IDs as keys and the CL of the respective spells as values.
 */
function constructMessage(CL){
    var message = Object();
    for (var i = 0; i < selectedSpellIDs.length; i++ ){
        var currentID = selectedSpellIDs[i];
        var $currentDetailedCL = $("#caster-level-" + currentID);
        if($currentDetailedCL.length > 0){
            message[currentID] = $currentDetailedCL.val();
        } else {
            message[currentID] = CL;
        }
    }
    return message;
}

/*
    TODO: Replace with a function that uses constructMessage.
 */
function getBonuses(CL) {
    var parameters = "?cl=" + CL;

    for (var i = 0; i < selectedSpellIDs.length; i++) {
        parameters += ("&spells=" + selectedSpellIDs[i]);
    }

    var numericalBonuses;
    var miscBonuses;

    $.getJSON("/api/bufftracker/bonuses/" + parameters, function (data) {
        if (data.status === 200) {
            numericalBonuses = data.content.numerical;
            miscBonuses = data.content.misc;
        }
        displayResults(numericalBonuses, miscBonuses)
    });

}



function displayResults(numericalBonuses, miscBonuses) {

    $("#results-container").empty();
    $.each(statistics, function (index, name) {
        if (numericalBonuses[index] !== null) {
            var resultSpan = "<span class='row'>" + statistics[index] + ": +" + numericalBonuses[index] + "</span>";
            $("#results-container").append(resultSpan);
        }
    });
    for (var index = 0; index < miscBonuses.length; index++) {
        $("#results-container").append("<span class='row'>" + miscBonuses[index] + "</span>");
    }
}