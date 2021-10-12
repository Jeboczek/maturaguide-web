const BIO = {
    jakub : `<h1>Hej, jestem <span id="maincolor"> Jakub Pawłowski.</span></h1>
    <p>Na co dzień robię coś takiego jak dzień robię coś takiego jak dzień robię coś takiego jak dzień robię coś
        takiego jak dzień robię coś takiego jak dzień robię coś takiego jak </p>`,
    oktawian : `<h1>Witaj, nazywam się <span id="maincolor"> Oktawian Kausz!</span></h1>
    <p>Na co dzień robię coś takiego jak dzień robię coś takiego jak dzień robię coś takiego jak dzień robię coś
        takiego jak dzień robię coś takiego jak dzień robię coś takiego jak </p>`,
}

function onAvatarClick(event) {
    let clickedPerson = event.target.id;
    if (clickedPerson != $("div.avatar.active").attr("id")) {
        // Change active class
        $("div.avatar.active").removeClass("active")
        $(`div.avatar#${clickedPerson}`).addClass("active")
        // Change content
        let content = $("div.about-us-content");
        content.fadeOut(200, () => {
            content.html(BIO[clickedPerson]);
            content.fadeIn(200); 
        });        
    }
}

function attachAllEvents() {
    $("div.avatar").click(onAvatarClick);
}


(() => {
    attachAllEvents();
})()