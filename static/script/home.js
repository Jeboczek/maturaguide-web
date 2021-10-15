class NavbarUpdater{

    constructor(){
        this.bindAllActions();
    }

    getHeights(){
        let categorySelectorTop = $("div.category-selector")[0].offsetTop
        let categorySelectorBottom = $("div.category-selector")[0].offsetTop + $("div.category-selector")[0].offsetHeight
        return [categorySelectorTop, categorySelectorBottom];
    }

    isLookingAtCategorySelector(){
        let metrics = this.getHeights()
        let t = metrics[0];
        let b = metrics[1];
        return $(window).scrollTop() >= t && $(window).scrollTop() <= b
    }

    updateNavHighlight(event) {
        if(this.isLookingAtCategorySelector()){
            $("a.nav-link[href=\"/#learn\"]").attr("id", "active")
            $("a.nav-link[href=\"/\"]").attr("id", "")
        }else{
            $("a.nav-link[href=\"/#learn\"]").attr("id", "")
            $("a.nav-link[href=\"/\"]").attr("id", "active")
        }
    }

    bindAllActions() {
        let thisObj = this
        $(window).scroll((event) => {
            thisObj.updateNavHighlight.call(thisObj, event)
        });
    }

}


class QuizPicker{
    constructor(){
        this.refreshSubjectsCards();
    }
    
    getSubjectCardHTMLFromData(data){
        return `<div class="category"><h1>${data["name"]}</h1><h6>${data["type"] == "P" ? "podstawowy" : "rozserzony"}</h6></div>`
    }
    
    
    refreshSubjectsCards() {
        const getSubjectCardHTMLFromData = this.getSubjectCardHTMLFromData
        $.getJSON("/api/get_subjects", "",
            function (data, textStatus, jqXHR) {
                let htmlToAdd = "";
                data.forEach(element => {
                    htmlToAdd += getSubjectCardHTMLFromData(element);
                });
                $("div.category-holder").html(htmlToAdd);
            }
        );
    }
}



(() => {
    let qp = new QuizPicker();
    let nu = new NavbarUpdater();
})()