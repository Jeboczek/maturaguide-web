const BIO = {
    jakub : `<h1>Hej, jestem <span id="maincolor"> Jakub Pawłowski.</span></h1>
    <p>Podchodzę z województwa Warmińsko-Mazurskiego i w projekcie odpowiadam za API, stronę internetową oraz infrastrukturę serwerową. Informatyka od zawsze była moją pasją, w którą pragnę wkładać jak najwięcej czasu. Jestem fanem społeczności otwartego oprogramowania oraz systemów operacyjnych GNU/Linux 🐧. Na co dzień korzystam ze środowiska KDE Plasma oraz programuję w językach Python, oraz JavaScript. Aktualnie uczę się Darta oraz Fluttera.</p>`,
    oktawian : `<h1>Cześć! Nazywam się <span id="maincolor"> Oktawian Kausz</span>.</h1>
    <p>Mam dziewiętnaście lat i pochodzę z okolic stolicy województwa Warmińsko-Mazurskiego – Olsztyna. W projekcie odpowiadam za aplikację mobilną oraz szatę graficzną całego projektu. Wcześniej zajmowałem się grafiką, jednak od 2018 roku bardziej skupiłem się na programowaniu i od tego czasu wciąż rozszerzam swoją wiedzę na temat projektowania aplikacji na Androida. W wolnym czasie pracuje też nad swoją drugą pasją – uczę się języka hiszpańskiego 🇪🇸</p>`,
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