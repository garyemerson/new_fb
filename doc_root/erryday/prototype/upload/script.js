"use strict";

// TODO:
// - "for day" input and column in sql table
// - add ability to preview select pictures
// - view "day: 8/1/2020", "posted on: 8/4/2020"
// ---
// - keep create time to be start of draft? Create post time column too?
// - auto save new text or new photos
//      - what will with loaded photos look like? Make separate area for draft photo list and preview?
// - add url param for user that will auto select author and populate draft. Useful for bookmarking
// - draft status column in sql table
// - auto populate textarea when author chosen from dropdown
//      - disable textarea
//      - display "loading..."
//      - populate with content
//      - re-enable

function formData(author, files, postText) {
    let formData = new FormData();
    formData.append("author", author);
    formData.append("text", postText);
    for (let i = 0; i < files.length; i++) {
        formData.append("img" + i, files.item(i));
    }
    return formData;
}

function submitHandler() {
    document.getElementById("uploadStatus").innerHTML = "starting...";

    let author;
    if (document.getElementById("author").value && document.getElementById("author").value.length > 0) {
        author = document.getElementById("author").value;
    } else {
        author = document.getElementById("author-select").value;
    }
    let fileInput = document.getElementById("fileInput");
    let postText = document.getElementById("postText").value;
    console.log("files:", fileInput.files);
    
    let xhr = new XMLHttpRequest();
    xhr.upload.addEventListener('progress', function handleEvent(e) {
        console.log("lengthComputable: " + e.lengthComputable + ", loaded: " + e.loaded + ", total: " + e.total + "(" + e.loaded / e.total + ")");
        let percentStr = (100 * e.loaded / e.total).toFixed(2) + "%";
        document.getElementById("uploadStatus").innerHTML = percentStr;
    });
    xhr.onload = () => {
        console.log("POST succeeded");
        document.getElementById("uploadStatus").innerHTML = "Upload successful!";
    };
    xhr.onerror = xhr.onabort = () => {
        console.log("POST failed");
        document.getElementById("uploadStatus").innerHTML = "Upload failed!";
    };
    xhr.open("POST", "submit.cgi");
    xhr.send(formData(author, fileInput.files, postText));
}

function authorSelectChange() {
    let postText = document.getElementById("postText");
    postText.disabled = true;
    postText.value = "loading...";
    let xhr = new XMLHttpRequest();
    xhr.onload = (e) => postText.value = xhr.response;
    xhr.onerror = xhr.onabort = (e) => console.log("getting draft failed:", e);
    xhr.onloadend = () => postText.disabled = false;
    xhr.open("GET", "/erryday/prototype/get_draft.cgi");
    xhr.send();
}

window.onload = function () {
    document.getElementById("submitButton").onclick = submitHandler;
    //document.getElementById("author-select").onchange = authorSelectChange;
};

$(function(){
    $("#navbar").load("../navbar.html");
});
