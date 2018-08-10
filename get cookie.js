function getLICookie() {
    var name = "li_at" + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            alert( c.substring(name.length, c.length));
        }
    }
    alert ("Linkedin Not found/logged in");
};