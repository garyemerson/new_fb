"use strict";
var xhrGlobal = null;
function formData(files, postText) {
    var formData = new FormData();
    formData.append("text", postText);
    for (var i = 0; i < files.length; i++) {
        var f = files.item(i);
        // let metaJsonStr = JSON.stringify({
        //   lastModified: f.lastModified,
        //   lastModifiedDate: (<any>f)["lastModifiedDate"]?.valueOf(),
        //   name: f.name,
        //   webkitRelativePath: (<any>f)["webkitRelativePath"] as string,
        //   size: f.size,
        //   type: f.type});
        // formData.append(`meta${i}`, metaJsonStr);
        formData.append("img" + i, f);
    }
    return formData;
}
function fileUploadClickHandler() {
    document.getElementById("uploadStatus").innerHTML = "starting...";
    // document.getElementById("uploadStatus").className = "loading";
    var fileInput = document.getElementById("fileInput");
    var postText = document.getElementById("postText").value;
    console.log("files:", fileInput.files);
    var xhr = new XMLHttpRequest();
    xhrGlobal = xhr;
    xhr.upload.addEventListener('progress', function handleEvent(e) {
        console.log("lengthComputable: " + e.lengthComputable + ", loaded: " + e.loaded + ", total: " + e.total);
        console.log("" + e.loaded / e.total);
        var percentStr = (100 * e.loaded / e.total).toFixed(2) + "%";
        document.getElementById("uploadStatus").innerHTML = percentStr;
    });
    xhr.onreadystatechange = function () {
        console.log("onreadystatechange");
        if (this.readyState !== XMLHttpRequest.DONE) {
            return;
        }
        // document.getElementById("uploadStatus").className = "";
        if (this.status === 200) {
            console.log("POST succeeded");
            document.getElementById("uploadStatus").innerHTML = "Upload successful!";
        }
        else {
            console.log("POST failed");
            document.getElementById("uploadStatus").innerHTML = "Upload failed!";
        }
    };
    // xhr.setRequestHeader("Content-Type", "multipart/form-data");
    xhr.open("POST", "submit.cgi", true);
    // xhr.send(postText);
    xhr.send(formData(fileInput.files, postText));
    // xhr.send(formData(fileInput.files!, postText));
}
window.onload = function () {
    document.getElementById("submitButton").onclick = fileUploadClickHandler;
};
$("#bitchForm").submit(function (e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr("action");
    $.post(url, form.serialize());
    $("#uploadStatus").html("Upload successful!");
});
