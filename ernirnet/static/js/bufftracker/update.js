function updateResults() {

    CL = $("#caster-level").val();

    var inEffect = bonusesInEffect(selectedSpellIDs, numericalBonuses);
    var applicable = bonusesThatApply(inEffect, statistics, modifierTypes, 5);
    var combined = combineBonuses(applicable, statistics);

    displayResults(combined, statistics);
}

function displayResults(bonuses, statisticsArray) {

    var statistics = new Object();
    for (var statisticIndex = 0; statisticIndex < statisticsArray.length; statisticIndex++) {
        var currentStatistic = statisticsArray[statisticIndex];
        statistics[currentStatistic.name] = bonuses[currentStatistic.id];
    }
    $("#results-container").empty();
    $.each(statistics, function (statistic, value) {
        if (value !== 0) {
            var resultSpan = "<span class='row'>" + statistic + ": +" + value + "</span>";
            $("#results-container").append(resultSpan);
        }
    });
}