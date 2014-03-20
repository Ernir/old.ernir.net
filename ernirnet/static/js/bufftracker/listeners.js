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

    $("#caster-level").change(function () {
        if($("#caster-level").val() < 1){
            $("#caster-level").val(1);
        } else if ($("#caster-level").val() > 100){
            $("#caster-level").val(100);
        }
        updateResults();
    });
}