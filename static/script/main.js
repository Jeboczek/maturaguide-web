function updateNavHighlight(action) {
    console.log("Updating!")
}

function bindAllActions() {
    $(window).scroll(updateNavHighlight);
}

(() => {
    bindAllActions();
})()