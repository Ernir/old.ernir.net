function setListeners() {
    $("input[type=checkbox]").change(function () {
        var currentSpellId = parseInt(this.id.replace("spell-", ""));
        if (this.checked) {
            selectedSpellIDs.push(currentSpellId);
        }
        else {
            selectedSpellIDs.splice(selectedSpellIDs.indexOf(currentSpellId), 1);
        }
        updateResults();
    });

    $("#caster-level").change(updateCL);
}