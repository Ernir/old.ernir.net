/**
 * @param {Array} selectedSpellIDs - array of the IDs of spells that have had their respective checkboxes checked
 * @param {Array} numericalBonuses - array of all given numerical bonuses, as parsed from the JSON (see initialize.js)
 * @returns {Array} - an array of bonuses that matches the given spells
 */
function bonusesInEffect(selectedSpellIDs, numericalBonuses) {

    var bonusesInEffect = [];
    for (var i = 0; i < numericalBonuses.length; i++) {
        var currentBonus = numericalBonuses[i];
        if (selectedSpellIDs.indexOf(currentBonus.associatedSpell) !== -1) {
            bonusesInEffect.push(currentBonus);
        }
    }
    return bonusesInEffect;
}

/**
 * //TODO: Document this crap
 * @param bonusesInEffect
 * @param statistics
 * @param modifierTypes
 * @param CL
 * @returns {Array}
 */
function bonusesThatApply(bonusesInEffect, statistics, modifierTypes, CL) {

    var highestBonusMap = new Array(statistics.length);
    var highestBonuses = new Array(bonusesInEffect.length);

    for (var bonusIndex = 0; bonusIndex < bonusesInEffect.length; bonusIndex++){
        highestBonuses[bonusIndex] = bonusesInEffect[bonusIndex];
    }

    for (var statisticIndex = 0; statisticIndex < statistics.length; statisticIndex++) {
        var currentStatistic = statistics[statisticIndex];
        highestBonusMap[currentStatistic.id] = new Array(modifierTypes.length);
        for (var modifierTypeIndex = 0; modifierTypeIndex < modifierTypes.length; modifierTypeIndex++) {
            var currentModifierType = modifierTypes[modifierTypeIndex];

            highestBonusMap[currentStatistic.id][currentModifierType.id] = 0;
        }
    }

    for (var bonusIndex = 0; bonusIndex < bonusesInEffect.length; bonusIndex++) {
        var currentBonus = bonusesInEffect[bonusIndex];
        var currentBonusValue = calculateBonus(currentBonus.bonus);

        if (!(currentBonusValue > highestBonusMap[currentBonus.applicableTo][currentBonus.modifier])) {
            highestBonuses[bonusIndex] = null;
        } else {
            currentBonus.bonus = currentBonusValue;
            highestBonusMap[currentBonus.applicableTo][currentBonus.modifier] = currentBonusValue;
        }
    }
    highestBonuses = highestBonuses.filter(function(element){return element != null});

    return highestBonuses;
}

function combineBonuses(applicableBonuses,statistics){
    var statisticsArray = new Array(statistics.length);
    for (var statisticIndex = 0; statisticIndex < statistics.length; statisticIndex++){
        var currentStatistic = statistics[statisticIndex];
        statisticsArray[currentStatistic.id] = 0;
    }

    for (var bonusIndex = 0; bonusIndex < applicableBonuses.length; bonusIndex++){
        var currentBonus = applicableBonuses[bonusIndex];
        statisticsArray[currentBonus.applicableTo] += currentBonus.bonus;
    }

    return statisticsArray;
}

/*
 So, this is a wrapper function around eval. Let me explain.
 The numericalBonuses variable contains information on the bonuses provided by each spell,
 in string format as a function of caster level. Alternatives were significantly more verbose and/or far less performant.
 This is as safe as any other local JS evaluation.
 This is also not unclear, thanks to this comment.
 */
function calculateBonus(bonusString, CL) {
    //TODO whitelist appropriate content
    return eval(bonusString);
}


/*
 HERE BEGIN THE TRULY UGLY FUNCTIONS
 */

function _1d8plusCL_Max1d8plus10(level) {
    var maximumBonus = 10;
    var integerPart = Math.max(level,maximumBonus);
    var bonus = "1d8 + " + integerPart;
    return bonus;
}