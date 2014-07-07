function updateCL() {
    if ($("#caster-level").val() < 1) {
        $("#caster-level").val(1);
    } else if ($("#caster-level").val() > 100) {
        $("#caster-level").val(100);
    }
    updateResults();
}

function updateResults() {

    defaultCL = $("#caster-level").val();

//    var inEffect = bonusesInEffect(selectedSpellIDs, numericalBonuses);
//    var applicable = bonusesThatApply(inEffect, statistics, modifierTypes, 5);
//    var combined = combineBonuses(applicable, statistics);

    getBonuses(defaultCL);
}

function getBonuses(CL) {
    var parameters = "?cl=" + CL;

    for (var i = 0; i < selectedSpellIDs.length; i++){
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