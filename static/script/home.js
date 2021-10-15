class NavbarUpdater {
  constructor() {
    this.bindAllActions();
  }

  getHeights() {
    let categorySelectorTop = $("div.category-selector")[0].offsetTop;
    let categorySelectorBottom =
      $("div.category-selector")[0].offsetTop +
      $("div.category-selector")[0].offsetHeight;
    return [categorySelectorTop, categorySelectorBottom];
  }

  isLookingAtCategorySelector() {
    let metrics = this.getHeights();
    let t = metrics[0] - 100;
    let b = metrics[1] + 100;
    return $(window).scrollTop() >= t && $(window).scrollTop() <= b;
  }

  updateNavHighlight(event) {
    if (this.isLookingAtCategorySelector()) {
      $('a.nav-link[href="/#learn"]').attr("id", "active");
      $('a.nav-link[href="/"]').attr("id", "");
    } else {
      $('a.nav-link[href="/#learn"]').attr("id", "");
      $('a.nav-link[href="/"]').attr("id", "active");
    }
  }

  bindAllActions() {
    let thisObj = this;
    $(window).scroll((event) => {
      thisObj.updateNavHighlight.call(thisObj, event);
    });
  }
}

class QuizPicker {
  constructor() {
    this.showSubjectsCards().then(() => {
      this.bindButtons();
    });
    this.mode = 0;
    this.pickedSubject = null;
    this.pickedMode = null;
    this.pickedCategory = null;
  }

  getCardHTMLFromData(id = undefined, content = undefined, footer = undefined) {
    return `<div class="category" ${
      id === undefined ? "" : 'id="' + id + '"'
    }>${
      content === undefined ? "" : "<h1>" + content + "</h1>"
    }${
      footer === undefined ? "" : "<h6>" + footer + "</h6>"
    }</div>`;
  }

  getSubjectCardHTMLFromData(data) {
    return this.getCardHTMLFromData(
      data["id"],
      data["name"],
      data["type"] == "P" ? "podstawowy" : "rozserzony"
    );
  }

  bindButtons() {
    $("div.category").unbind("click");
    let thisObj = this;
    $("div.category").click((event) => {
      let choiceId = undefined;
      switch (this.mode) {
        case 0: // Subject
          this.pickedSubject = event.currentTarget.id;
          this.mode = 1;
          this.doTransition(event.currentTarget, () => {
            this.showTypeCards(), this.bindButtons();
          });
          break;
        case 1: // Type
          choiceId = event.currentTarget.id;
          if (choiceId == 0) {
            this.mode = 0;
            this.pickedSubject = undefined;
            this.doTransition(
              event.currentTarget,
              () => {
                this.showSubjectsCards().then(() => {
                  this.bindButtons();
                });
              },
              true
            );
          } else {
            this.mode = 2;
            this.pickedMode = choiceId;
            if (choiceId == 1) {
              // Trening
              this.doTransition(event.currentTarget, () => {
                this.showTraningCards(this.pickedSubject).then(() => {
                  this.bindButtons();
                });
              });
            } else {
              this.doTransition(event.currentTarget, () => {
                this.showSheetCards(this.pickedSubject).then(() => {
                  this.bindButtons();
                });
              });
            }
          }
          break;
        case 2: // Exam / Category picker
          choiceId = event.currentTarget.id;
          if (choiceId == 0) {
            this.mode = 1;
            this.pickedMode = undefined;
            this.doTransition(
              event.currentTarget,
              () => {
                this.showTypeCards();
                this.bindButtons();
              },
              true
            );
          } else {
            this.pickedCategory = choiceId;
            window.location.href = `/play?subject=${this.pickedSubject}&${
              this.pickedMode == 1
                ? "category=" + this.pickedCategory
                : "cke_year=" + this.pickedCategory
            }`;
          }
      }
    });
  }

  showTypeCards() {
    let htmlToAdd = "";
    [
      { id: 0, content: "wróć" },
      { id: 1, content: "trening" },
      { id: 2, content: "arkusz" },
    ].forEach((element) => {
      htmlToAdd += this.getCardHTMLFromData(...Object.values(element));
    });
    $("div.category-holder").html(htmlToAdd);
    $("h1#category-header").html("Wybierz typ nauki");
  }

  async showTraningCards(subject_id) {
    const getCardHTMLFromData = this.getCardHTMLFromData;
    return $.getJSON(
      `/api/get_categories?subject_id=${subject_id}`,
      "",
      function (data, textStatus, jqXHR) {
        let htmlToAdd = getCardHTMLFromData(0, "wróć");
        data.forEach((element) => {
          // Reformat
          element = {
            id: element["id"],
            content: element["name"],
          };
          htmlToAdd += getCardHTMLFromData(...Object.values(element));
        });
        $("div.category-holder").html(htmlToAdd);
        $("h1#category-header").html("Wybierz kategorie");
      }
    );
  }

  async showSheetCards(subject_id) {
    const getCardHTMLFromData = this.getCardHTMLFromData;
    return $.getJSON(
      `/api/get_cke_sheets?subject_id=${subject_id}`,
      "",
      function (data, textStatus, jqXHR) {
        let htmlToAdd = getCardHTMLFromData(0, "wróć");
        data.forEach((element) => {
          // Reformat
          element = {
            id: element,
            content: element,
          };
          htmlToAdd += getCardHTMLFromData(...Object.values(element));
        });
        $("div.category-holder").html(htmlToAdd);
        $("h1#category-header").html("Wybierz rok");
      }
    );
  }

  async showSubjectsCards() {
    let thisObj = this 
    return $.getJSON(
      "/api/get_subjects",
      "",
      function (data, textStatus, jqXHR) {
        let htmlToAdd = "";
        data.forEach((element) => {
          htmlToAdd += thisObj.getSubjectCardHTMLFromData.call(thisObj, element);
        });
        $("div.category-holder").html(htmlToAdd);
        $("h1#category-header").html("Wybierz swój przedmiot");
      }
    );
  }

  doTransition(clicked, updateFunction, revert = false) {
    $(clicked).addClass("clicked");
    setTimeout(() => {
      $("div.category-content").animate(
        { left: "0%", display: "none", left: revert ? "100%" : "-100%" },
        200,
        () => {
          updateFunction();
          $("div.category-content").css("left", revert ? "-100%" : "100%");
          $("div.category-content").animate(
            { display: "flex", left: "0%" },
            200
          );
        }
      );
    }, 400);
  }
}

(() => {
  let qp = new QuizPicker();
  let nu = new NavbarUpdater();
})();
