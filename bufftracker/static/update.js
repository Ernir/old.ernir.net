/*
 Pushes/removes the corresponding elements from selectedSpellIDs when a checkbox is marked.
 */
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

/*
 As updateSelectedSpells(), but for radio buttons.
 Also contains hacks to make radio buttons de-selectable.
 */
function radioButtonClicked() {
    var previousValue = $(this).prop('previousValue');
    var name = $(this).prop('name');

    if (previousValue == 'checked') {
        $(this).removeAttr('checked');
        $(this).prop('previousValue', false);
    }
    else {
        $("input[name=" + name + "]:radio").prop('previousValue', false);
        $(this).prop('previousValue', 'checked');
    }

    var currentSpellId = parseInt(this.id.replace("spell-", ""));

    if (this.checked) {
        selectedSpellIDs.push(currentSpellId);
    }
    else {
        selectedSpellIDs.splice(selectedSpellIDs.indexOf(currentSpellId), 1);
    }

    var clickedElement = this;
    var $radioButtons = $("input[type=radio]");
    $.each($radioButtons, function (index, element) {
        if (element.id !== clickedElement.id) {
            var spellToRemove = parseInt(element.id.replace("spell-", ""));
            var position = selectedSpellIDs.indexOf(spellToRemove);
            if (position != -1) {
                selectedSpellIDs.splice(position, 1);
            }
        }
    });
    updateResults();
}

/*
 Duh.
 */
function updateGlobalCL() {
    var globalCL = $("#caster-level").val();
    $(".cl-detail").val(globalCL);

    updateResults();
}

/*
 Posts an object from constructMessage to the api via AJAX, calls displayResults on success.
 */
function updateResults() {
    var CL = $("#caster-level").val();

    var message = constructMessage(CL);

    $.ajax({
        url: "/behind-the-scenes/bonuses/",
        type: "get",
        data: message,

        success: function (json) {
            var numericalBonuses = json.content.numerical;
            var miscBonuses = json.content.misc;
            displayResults(numericalBonuses, miscBonuses)
        }
    });
}

/*
 Returns a JS object consisting of spell IDs as keys and the CL of the respective spells as values.
 */
function constructMessage(CL) {
    var message = {};
    for (var i = 0; i < selectedSpellIDs.length; i++) {
        var currentID = selectedSpellIDs[i];
        var $currentDetailedCL = $("#caster-level-" + currentID);
        if ($currentDetailedCL.length > 0) {
            message[currentID] = $currentDetailedCL.val();
        } else {
            message[currentID] = CL;
        }
    }
    return message;
}

/*
 Loops over the statisticsGroups object to display bonuses.
 This is the function that actually updates the page.
 */
function displayResults(numericalBonuses, miscBonuses) {

    var $resultsContainer = $("#results-container");
    $resultsContainer.empty();
    $.each(statisticsGroups, function (i, group) {
        $.each(group.statistics, function (j, statistic) {
            if(numericalBonuses[statistic.id]) {
                var resultDiv = "<div>"
                    + statistic.name
                    + ": " + (numericalBonuses[statistic.id] > 0 ? "+" : "")
                    + numericalBonuses[statistic.id]
                    + "</div>";
                $resultsContainer.append(resultDiv);
            }
        });
    });
    $.each(miscBonuses, function(i, bonus) {
        $resultsContainer.append("<div>" + bonus + "</div>")
    })
}