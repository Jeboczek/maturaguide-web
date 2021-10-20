class Excercise {
    constructor()
}

class Question {
    // Question presenter
    constructor(title = "", content = "", category = "") {
        this.title = title
        this.category = category
        this.content = content
        this.excercise
    }


}

class Play {
    constructor() {
        this.get = this.getParams()
    }

    getParams() {
        this.GET_table = {}
        let GET_path = window.location.search.substr(1).split("&")
        GET_path.forEach((element) => {
            this.GET_table[element[0]] = element[1]
        })
        return this.GET_table
    }

    makeAPIQuerry(GET_table) {
        $.getJSON("url", GET_table,
            function (data, textStatus, jqXHR) {

            }
        );
    }
}

let pl = new Play()