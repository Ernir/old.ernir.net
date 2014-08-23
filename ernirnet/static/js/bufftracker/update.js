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
    $.each($("input[type=radio]"), function (index, element) {
        if (element.id !== clickedElement.id) {
            var spellToRemove = parseInt(element.id.replace("spell-", ""));
            var position = selectedSpellIDs.indexOf(spellToRemove);
            if (position != -1) {
                selectedSpellIDs.splice(position, 1);
            }
        }
    })
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
    var CL = $("#caster-level").val()

    var message = constructMessage(CL);

    $.post("/api/bufftracker/bonuses/",
        JSON.stringify(message),
        function (data) {
            if (data.status === 200) {
                var numericalBonuses = data.content.numerical;
                var miscBonuses = data.content.misc;
            }
            displayResults(numericalBonuses, miscBonuses)
        },
        "json"
    );
}

/*
 Returns a JS object consisting of spell IDs as keys and the CL of the respective spells as values.
 */
function constructMessage(CL) {
    var message = Object();
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

    $("#results-container").empty();
    $.each(statisticsGroups, function (i, group) {
        $.each(group, function (j, statistics) {
            if (numericalBonuses[j] !== null && numericalBonuses[j] !== 0) {
                // The ternary thing is to add an appropriate sign to the displayed bonus
                var resultSpan = "<span class='row'>" + group[j] + ": " + (numericalBonuses[j] > 0 ? "+" : "") + numericalBonuses[j] + "</span>";
                $("#results-container").append(resultSpan);
            }
        })
    });
    for (var index = 0; index < miscBonuses.length; index++) {
        $("#results-container").append("<span class='row'>" + miscBonuses[index] + "</span>");
    }
}