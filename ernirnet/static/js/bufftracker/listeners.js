function setListeners() {
    $("input[type=checkbox]").change(updateSelectedSpells);

    $("#caster-level").change(updateGlobalCL);

    $(".cl-detail").change(updateResults);
}