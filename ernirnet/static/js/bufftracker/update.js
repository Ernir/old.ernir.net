function updateResults() {

    CL = $("#caster-level").val();

//    var inEffect = bonusesInEffect(selectedSpellIDs, numericalBonuses);
//    var applicable = bonusesThatApply(inEffect, statistics, modifierTypes, 5);
//    var combined = combineBonuses(applicable, statistics);

    getBonuses(CL);
}

function getBonuses(CL) {
    var parameters = "?cl=" + CL;

    console.log(parameters);
    for (var i = 0; i < selectedSpellIDs.length; i++){
        parameters += ("&spells=" + selectedSpellIDs[i]);
    }

    var bonuses;

    $.getJSON("/api/bufftracker/bonuses/" + parameters, function (data) {
        if (data.status === 200) {
            bonuses = data.content.numerical;
        }
        displayResults(bonuses)
    });

}

function displayResults(bonuses) {

    $("#results-container").empty();
    $.each(statistics, function (index, name) {
        if (bonuses[index] !== null) {
            var resultSpan = "<span class='row'>" + statistics[index] + ": +" + bonuses[index] + "</span>";
            $("#results-container").append(resultSpan);
        }
    });
}