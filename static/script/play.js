class ExcerciseContent {
    constructor(id = 0, content = "", answers = [], correct = "", type = 1) {
        this.id = id;
        this.content = content;
        this.answers = answers;
        this.correct = correct;
        this.type = type;
    }

    fromJson(json) {
        this.id = json["id"];
        this.content = json["content"];
        this.answers = json["answers"];
        this.correct = json["correct"];
        this.more_text = json["more_text"];
        this.type = json["type"];
    }

    getContent() {
        let html = "";
        html += `<h1>${this.content}</h1>`;
        if (this.more_text !== null){
            html += `<p>${this.more_text}</p>`
        }
        switch (this.type) {
            case 1:
            case 2:
            case 4:
                html += "<ul>";
                html += "<li>";
                this.answers.forEach((ans) => {
                    html += `<div id="${this.id}-${ans.index}" class="answer-circle">${ans.index}</div>`;
                });
                html += "</li>";
                html += "</ul>";
                break;
            case 3:
                html += "<ul>";
                this.answers.forEach((ans) => {
                    html += "<li>";
                    html += `<div id="${this.id}-${ans.index}" class="answer-circle">${ans.index}</div> ${ans.content}`;
                    html += "<li>";
                });
                html += "</ul>";

                break;
            default:
                break;
        }
        return html;
    }
}
class Excercise {
    constructor(header = "", content = "", footer = "", more_text = "", audio = "", img = "") {
        this.header = header;
        this.content = content;
        this.footer = footer;
        this.more_text = more_text;
        this.audio = audio;
        this.img = img;
        this.excercise_contents = [];
    }

    fromJson(json) {
        this.header = json["header"];
        this.content = json["content"];
        this.footer = json["footer"];
        this.more_text = json["more_text"];
        this.audio = json["audio"];
        this.img = json["img"];
        json["excercise_contents"].forEach((element) => {
            let excercise_content = new ExcerciseContent();
            excercise_content.fromJson(element);
            this.excercise_contents.push(excercise_content);
        });
    }

    getHeader() {
        let html = "";
        // TODO: Fetch images
        if (this.audio !== null) {
            html += `<div class="sound-play-holder">
                        <img src="/static/img/play.svg">
                        <div class="sound-play-progressbar">
                            <div class="progressbar-status"></div>
                        </div>
                    </div>`;
        }
        return html;
    }

    getContent() {
        let html = "";
        html +=
            this.header === undefined
                ? ""
                : `<h1 id="exercise-header">${this.header}</h1>`;
        html +=
            this.content === undefined
                ? ""
                : `<p id="exercise-content">${this.content.replace("\n", "<br>")}</p>`;
        html +=
            this.footer === undefined
                ? ""
                : `<h6 id="exercise-footer">${this.footer}</h6>`;

        html +=
            this.more_text === undefined
                ? ""
                : `<p id="more-text">${this.more_text.replace(/\n/g, "<br>")}</p>`;

        this.excercise_contents.forEach((ec) => {
            html += `<div class="answer">${ec.getContent()}</div>`;
        });
        return html;
    }
}

class Question {
    constructor(title = "", content = "", category = "") {
        this.title = title;
        this.category = category;
        this.content = content;
        this.excercise;
    }

    fromJson(json) {
        this.title = json["title"];
        this.category = json["category"];
        this.content = json["content"];
        this.excercise = new Excercise();
        this.excercise.fromJson(json["excercise"]);
    }

    getHeader() {
        let html = "";
        html += `<h6 id="question-category">${this.category}</h6>`;
        html += `<h1 id="question-title">${this.title}</h1>`;
        html += `<p id="question-content">${this.content}</p>`;
        html += this.excercise.getHeader();
        return html;
    }

    getContent() {
        return this.excercise.getContent();
    }
}

class Play {
    constructor() {
        this.get = this.getParams();
        this.questionArray = [];
        this.actualQuestion = 0;
        this.makeAPIQuerry();
    }

    start() {
        this.actualQuestion = 0;
        this.refreshNavBar();
        this.renderActualQuestion();
    }

    renderActualQuestion() {
        let questionToRender = this.questionArray[this.actualQuestion];
        $("div#play-content-header").html(questionToRender.getHeader());
        $("div#play-content-article").html(questionToRender.getContent());
    }

    async refreshNavBar() {
        let html = "";
        this.questionArray.forEach((question, i) => {
            html += `<li id="q-${i}" style="opacity: 0">${question.title}</li>`;
        });

        $("ul#question-links").html(html);
        this.attachNavButton();

        for (let i = 0; i < this.questionArray.length; i++) {
            await $(`li#q-${i}`)
                .animate({ opacity: "0", opacity: "1" }, 50)
                .promise();
        }
    }

    attachNavButton() {
        $("ul#question-links li").click((action) => {
            this.changeQuestion.call(this, action);
        });
    }

    highlightActiveLink(){
        $("ul#question-links li.active").removeClass("active");
        $(`ul#question-links li#q-${this.actualQuestion}`).addClass("active");
    }

    changeQuestion(action) {
        let newQuestionId = action.currentTarget.id.substr(2);
        this.actualQuestion = newQuestionId;

        this.highlightActiveLink();

        this.renderActualQuestion();
    }

    getParams() {
        this.GET_table = {};
        let GET_path = window.location.search.substr(1).split("&");
        GET_path.forEach((element) => {
            this.GET_table[element[0]] = element[1];
        });
        return this.GET_table;
    }

    parseJsonResponse(jsonResponse, status) {
        jsonResponse.forEach((element) => {
            let question = new Question();
            question.fromJson(element);
            this.questionArray.push(question);
        });

        this.start();
    }

    makeAPIQuerry() {
        $.getJSON(
            `/api/generate_quiz${window.location.search}`,
            "",
            (jsonResponse) => {
                this.parseJsonResponse.call(this, jsonResponse);
            }
        );
    }
}
let pl = new Play();
