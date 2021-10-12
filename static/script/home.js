function attachAllElements() {
    
}

function getSubjectCardHTMLFromData(data){
    return `<div class="category"><h1>${data["name"]}</h1><h6>${data["type"] == "P" ? "podstawowy" : "rozserzony"}</h6></div>`
}

function refreshSubjectsCards() {
    $.getJSON("/api/get_subjects", "",
        function (data, textStatus, jqXHR) {
            htmlToAdd = "";
            data.forEach(element => {
                htmlToAdd += getSubjectCardHTMLFromData(element);
            });
            $("div.category-holder").html(htmlToAdd);
        }
    );
}


(() => {
    attachAllElements();
    refreshSubjectsCards();
})()