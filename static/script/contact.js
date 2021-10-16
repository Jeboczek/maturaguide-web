class Contact{
    constructor(){

    }
}

class ContactSuccess{
    constructor(){
        this.bindAllButton();
    }

    bindAllButton(){
        $("button#homepage-redirect").click(() => {
            window.location.href = "/";
        })
    }
}


(() => {
    switch (window.location.pathname.replaceAll("/", "")) {
        case "kontakt":
            let ct = new Contact();
            break;
    
        case "kontaktsuccess":
            let cs = new ContactSuccess();
            break;

        default:
            console.error("Error in contact.js.\nThe script does not know what document it is in")
            break;
    }
})()