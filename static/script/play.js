// Keep all classes in one file to increase page speed by optimizing http requests

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
        this.explanationContent =
            json["explanation"] === null ? null : json["explanation"]["content"];
    }

    _getCheckedClass(checkedInThisExcercise, correct, submitted, answer) {
        if (checkedInThisExcercise !== null) {
            if (submitted) {
                if (checkedInThisExcercise == answer.index) {
                    return answer.index == correct ? "selected" : "wrong";
                } else {
                    return answer.index == correct ? "selected" : "";
                }
            } else {
                return checkedInThisExcercise == answer.index ? "selected" : "";
            }
        } else {
            return submitted && answer.index == correct ? "selected" : "";
        }
    }

    getContent(answers, questionId) {
        let checkedInThisExcercise = answers.getAnswer(
            parseInt(questionId),
            this.id
        );
        let html = `<div class="answer">`;
        html += `<h1>${this.content}</h1>`;
        if (this.more_text !== null) {
            html += `<p>${this.more_text}</p>`;
        }
        switch (this.type) {
            case 1:
            case 2:
            case 4:
                html += "<ul>";
                html += "<li>";
                this.answers.forEach((ans) => {
                    html += `<div id="${this.id}-${ans.index
                        }" class="answer-circle ${this._getCheckedClass(
                            checkedInThisExcercise,
                            answers.getCorrectAnswer(questionId, this.id),
                            answers.isQuestionSubmitted(questionId),
                            ans
                        )}">${ans.index}</div>`;
                });
                html += "</li>";
                html += "</ul>";
                break;
            case 3:
                html += "<ul>";
                this.answers.forEach((ans) => {
                    html += "<li>";
                    html += `<div id="${this.id}-${ans.index
                        }" class="answer-circle ${this._getCheckedClass(
                            checkedInThisExcercise,
                            answers.getCorrectAnswer(questionId, this.id),
                            answers.isQuestionSubmitted(questionId),
                            ans
                        )}">${ans.index}</div> ${ans.content}`;
                    html += "<li>";
                });
                html += "</ul>";

                break;
            default:
                break;
        }
        html += "</div>";
        if (answers.isQuestionSubmitted(questionId) && this.explanationContent !== null) {
            html += `<div class="explanation">`;

            html += `<h3>Wyjaśnienie</h3>`;
            html += `<p>${this.explanationContent.replace(/\n/g, "<br>")}</p>`;

            html += "</div>";
        }
        return html;
    }
}
class Excercise {
    constructor(
        header = "",
        content = "",
        footer = "",
        more_text = "",
        audio = "",
        img = ""
    ) {
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
        if (this.img !== null) {
            html += `<img class="excercise-img" src="${this.img}">`;
        }
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

    getContent(answers, questionId) {
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
            html += ec.getContent(answers, questionId);
        });
        return html;
    }
}

class Question {
    constructor(id = 0, title = "", content = "", category = "") {
        this.id = id;
        this.title = title;
        this.category = category;
        this.content = content;
        this.excercise;
    }

    fromJson(json) {
        this.id = json["id"];
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

    getContent(answers, lastQuestionIndex) {
        let html = this.excercise.getContent(answers, this.id);
        if (answers.isQuestionSubmitted(this.id) && lastQuestionIndex == this.id) {
            html += '<button id="exit-button">Koniec</button>';
        } else {
            html += answers.isQuestionSubmitted(this.id)
                ? `<button id="next-button">Dalej</button>`
                : `<button id="check-button">Sprawdź</button>`;
        }
        return html;
    }
}

class PlayResult {
    constructor() {
        this.answerAndCorrect = {};
        this.checkedAnswers = {};
        this.submittedQuestions = {};
    }

    loadAnswersFromApiJson(json) {
        json.forEach((question) => {
            this.answerAndCorrect[question["id"]] = {};
            this.checkedAnswers[question["id"]] = {};
            this.submittedQuestions[question["id"]] = false;
            question["excercise"]["excercise_contents"].forEach(
                (excerciseContent) => {
                    this.answerAndCorrect[question["id"]][excerciseContent["id"]] =
                        excerciseContent["correct"];
                    this.checkedAnswers[question["id"]][excerciseContent["id"]] = null;
                }
            );
        });
    }

    getAnswer(questionId, answerId) {
        return this.checkedAnswers[questionId][answerId];
    }

    selectAnswer(questionId, answerId, buttonIndex) {
        this.checkedAnswers[questionId][answerId] = buttonIndex;
    }

    getCorrectAnswer(questionId, answerID) {
        return this.answerAndCorrect[questionId][answerID];
    }

    submitQuestion(questionId) {
        this.submittedQuestions[questionId] = true;
    }

    isQuestionSubmitted(questionId) {
        return this.submittedQuestions[questionId];
    }
}

class QuestionSoundPlayer {
    constructor(soundUrl) {
        this.soundUrl = soundUrl;
        this.progressBar = $("div.progressbar-status");
        this.playButton = $("div.sound-play-holder img:first-child");
        this._playImg = "/static/img/play.svg";
        this._pauseImg = "/static/img/pause.svg";
        this._stopped = true;
        this.audioObject = new Audio(this.soundUrl);

        this.bindAll();
    }

    stop() {
        this.audioObject.pause();
        this.audioObject.currentTime = 0;
    }

    bindAll() {
        this.bindButton();
        this.bindProgressbar();
        this.bindProgressbarClick();
        this.bindOnEnd();
    }

    bindButton() {
        this.playButton.click(() => {
            if (this._stopped) {
                this.audioObject.play();
                this.playButton.attr("src", this._pauseImg);
                this._stopped = false;
            } else {
                this.audioObject.pause();
                this.playButton.attr("src", this._playImg);
                this._stopped = true;
            }
        });
    }

    bindProgressbar() {
        this.audioObject.addEventListener("timeupdate", (event) => {
            this.progressBar.css(
                "width",
                `${(this.audioObject.currentTime / this.audioObject.duration) * 100}%`
            );
        });
    }

    _calculateAudioPercent(clickEvent) {
        let progressBarHandler = $("div.sound-play-progressbar")[0];
        let offset = progressBarHandler.offsetLeft;
        let progressWidth = progressBarHandler.clientWidth;
        let clientX = clickEvent.x;
        return (clientX - offset) / progressWidth;
    }

    bindProgressbarClick() {
        this.progressBar.parent().click((event) => {
            let percent = this._calculateAudioPercent(event.originalEvent);
            this.audioObject.currentTime = this.audioObject.duration * percent;
        });
    }

    bindOnEnd() {
        this.audioObject.addEventListener("ended", (event) => {
            this._stopped = true;
            this.playButton.attr("src", this._playImg);
        });
    }
}
class Play {
    constructor() {
        this.get = this.getParams();
        this.questionArray = [];
        this.actualQuestion = 0;
        this.makeAPIQuerry();
        this.answers = new PlayResult();
        this.lastQuestionIndex = 0;
    }

    start() {
        this.actualQuestion = 0;
        this.refreshNavBar();
        this.renderActualQuestion();
        this.highlightActiveLink();
    }

    renderActualQuestion() {
        if (this.actualQuestionSound !== undefined) {
            this.actualQuestionSound.stop();
            delete this.actualQuestionSound;
        }
        let questionToRender = this.questionArray[this.actualQuestion];
        $("div#play-content-header").html(questionToRender.getHeader());
        $("div#play-content-article").html(
            questionToRender.getContent(this.answers, this.lastQuestionIndex)
        );

        let audioFile =
            this.questionArray[this.actualQuestion]["excercise"]["audio"];
        if (audioFile !== null) {
            this.actualQuestionSound = new QuestionSoundPlayer(audioFile);
        }
        if (
            !this.answers.isQuestionSubmitted(
                this.questionArray[this.actualQuestion]["id"]
            )
        ) {
            this.attachAnswerButtons();
        }
        this.attachNextAndCheckButtons();
        this.showExplanations();
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

    attachAnswerButtons() {
        $("div.answer ul li").click((event) => {
            let target =
                event.target.className.trim() == "answer-circle"
                    ? event.target
                    : $(event.currentTarget).find("div.answer-circle").length == 1
                        ? $(event.currentTarget).find("div.answer-circle")[0]
                        : null;
            if (target === null) {
                return;
            }
            let questionId = this.questionArray[this.actualQuestion]["id"];
            let answerId = parseInt(target.id.split("-")[0]);
            let newAnswer = target.id.split("-")[1];
            let oldAnswer = this.answers.getAnswer(questionId, answerId);

            if (oldAnswer == newAnswer) {
                return;
            } else {
                this.answers.selectAnswer(questionId, answerId, newAnswer);
                $(event.currentTarget)
                    .parent()
                    .find(".selected")
                    .removeClass("selected");
                $(target).addClass("selected");
            }
        });
    }

    attachNextAndCheckButtons() {
        $("button#check-button").click(() => {
            this.answers.submitQuestion(
                this.questionArray[this.actualQuestion]["id"]
            );
            this.renderActualQuestion();
            this.highlightActiveLink();
        });
        $("button#next-button").click(() => {
            this.actualQuestion = parseInt(this.actualQuestion) + 1;
            this.renderActualQuestion();
            this.highlightActiveLink();
        });
        $("button#exit-button").click(() => {
            window.location.href = "/#learn";
        });
    }

    highlightActiveLink() {
        $("ul#question-links li").each((i, element) => {
            let questionId = this.questionArray[element.id.replace("q-", "")]["id"];
            let submited = this.answers.isQuestionSubmitted(questionId);
            if (submited) {
                $(element).addClass("submited");
            }
        });

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
        this.answers.loadAnswersFromApiJson(jsonResponse);

        jsonResponse.forEach((element) => {
            let question = new Question();
            question.fromJson(element);
            this.questionArray.push(question);
        });

        this.lastQuestionIndex = this.questionArray.at(-1)["id"];

        this.start();
    }

    async showExplanations(){
        let explanations = $("div.explanation")
        for (let i = 0; i < explanations.length; i++) {
            await $(explanations[i]).find("h3").animate({"opacity": 0, "opacity": 1}, 500)           
            await $(explanations[i]).find("p").animate({"opacity": 0, "opacity": 1}, 700)           
        }
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
