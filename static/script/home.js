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

  getSubjectCardHTMLFromData(data) {
    return `<div class="category" id="${data["id"]}"><h1>${
      data["name"]
    }</h1><h6>${data["type"] == "P" ? "podstawowy" : "rozserzony"}</h6></div>`;
  }

  getTypeCardHTMLFromData(data) {
    return `<div class="category" id="${data["id"]}"><h1>${
      data["content"]
    }</h1>${
      data["footer"] === undefined ? "" : "<h6>" + data["footer"] + "</h6>"
    }</div>`;
  }

  bindButtons() {
    $("div.category").unbind("click");
    let thisObj = this;
    $("div.category").click((event) => {
      let choiceId = undefined;
      switch (thisObj.mode) {
        case 0: // Subject
          thisObj.pickedSubject = event.currentTarget.id;
          thisObj.mode = 1;
          thisObj.doTransition(event.currentTarget, () => {
            thisObj.showTypeCards(), thisObj.bindButtons();
          });
          break;
        case 1: // Type
          choiceId = event.currentTarget.id;
          if (choiceId == 0) {
            thisObj.mode = 0;
            thisObj.pickedSubject = undefined;
            thisObj.doTransition(
              event.currentTarget,
              () => {
                thisObj.showSubjectsCards().then(() => {
                  thisObj.bindButtons();
                });
              },
              true
            );
          } else {
            thisObj.mode = 2;
            thisObj.pickedMode = choiceId;
            if (choiceId == 1) {
              // Trening
              thisObj.doTransition(event.currentTarget, () => {
                thisObj.showTraningCards(thisObj.pickedSubject).then(() => {
                  thisObj.bindButtons();
                });
              });
            } else {
              thisObj.doTransition(event.currentTarget, () => {
                thisObj.showSheetCards(thisObj.pickedSubject).then(() => {
                  thisObj.bindButtons();
                });
              });
            }
          }
          break;
        case 2: // Exam / Category picker
          choiceId = event.currentTarget.id;
          if (choiceId == 0) {
            thisObj.mode = 1;
            thisObj.pickedMode = undefined;
            thisObj.doTransition(
              event.currentTarget,
              () => {
                thisObj.showTypeCards();
                thisObj.bindButtons();
              },
              true
            );
          } else {
            thisObj.pickedCategory = choiceId;
            window.location.href = `/play?subject=${thisObj.pickedSubject}&${
              thisObj.pickedMode == 1
                ? "category=" + thisObj.pickedCategory
                : "cke_year=" + thisObj.pickedCategory
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
      htmlToAdd += this.getTypeCardHTMLFromData(element);
    });
    $("div.category-holder").html(htmlToAdd);
    $("h1#category-header").html("Wybierz typ nauki");
  }

  async showTraningCards(subject_id) {
    const getTypeCardHTMLFromData = this.getTypeCardHTMLFromData;
    return $.getJSON(
      `/api/get_categories?subject_id=${subject_id}`,
      "",
      function (data, textStatus, jqXHR) {
        let htmlToAdd = getTypeCardHTMLFromData({ id: 0, content: "wróć" });
        data.forEach((element) => {
          // Reformat
          element = {
            id: element["id"],
            content: element["name"],
          };
          htmlToAdd += getTypeCardHTMLFromData(element);
        });
        $("div.category-holder").html(htmlToAdd);
        $("h1#category-header").html("Wybierz kategorie");
      }
    );
  }

  async showSheetCards(subject_id) {
    const getTypeCardHTMLFromData = this.getTypeCardHTMLFromData;
    return $.getJSON(
      `/api/get_cke_sheets?subject_id=${subject_id}`,
      "",
      function (data, textStatus, jqXHR) {
        let htmlToAdd = getTypeCardHTMLFromData({ id: 0, content: "wróć" });
        data.forEach((element) => {
          // Reformat
          element = {
            id: element,
            content: element,
          };
          htmlToAdd += getTypeCardHTMLFromData(element);
        });
        $("div.category-holder").html(htmlToAdd);
        $("h1#category-header").html("Wybierz rok");
      }
    );
  }

  async showSubjectsCards() {
    const getSubjectCardHTMLFromData = this.getSubjectCardHTMLFromData;
    return $.getJSON(
      "/api/get_subjects",
      "",
      function (data, textStatus, jqXHR) {
        let htmlToAdd = "";
        data.forEach((element) => {
          htmlToAdd += getSubjectCardHTMLFromData(element);
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
