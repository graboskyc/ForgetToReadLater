async function getCurrentTab() {
    let queryOptions = { active: true, lastFocusedWindow: true };
    // `tab` will either be a `tabs.Tab` instance or `undefined`.
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab;
}

async function writeArticle() {
    var txt_link = document.getElementById("link");
    var txt_title = document.getElementById("title");
    var msg = {};
    msg["link"] = txt_link.getAttribute("value");
    msg["title"] = txt_title.getAttribute("value");
    console.log(msg);
    var resp = await fetch('http://192.168.2.251:9994/api/newItem', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(msg)
    });
    console.log(resp);

    document.getElementById("ctr_form").classList.add('hidden');
    document.getElementById("ctr_saved").classList.remove('hidden');
}

window.onload = async function() {
    document.getElementById("ctr_saved").classList.add('hidden');
    document.getElementById("ctr_form").classList.remove('hidden');

    var tab = await getCurrentTab();
    var txt_link = document.getElementById("link");
    var txt_title = document.getElementById("title");
    //console.log(tab);
    txt_link.setAttribute("value", tab.url);
    txt_title.setAttribute("value", tab.title);

    var btn = document.getElementById("submit");
    btn.onclick = writeArticle();
};

