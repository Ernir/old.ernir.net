function setListeners() {
    $("input[type=checkbox]").change(updateSelectedSpells);
    $("input[type=radio]").click(radioButtonClicked);

    $("#caster-level").change(updateGlobalCL);

    $(".cl-detail").change(updateResults);
}