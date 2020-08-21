"use strict";

$("#bitchForm").submit(function (e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr("action");
    $.post(url, form.serialize());
    $("#uploadStatus").html("Upload successful!");
});
