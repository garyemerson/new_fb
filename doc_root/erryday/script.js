"use strict";

// $(function(){
//     $("#navbar").load("navbar.html");
// });

$(document).ready( function() {
    $('.image').click(function() {
        if ($(this).attr('enlarged') === 'true') {
            $(this).css({ height: 150, width: 'auto'});
            $(this).attr('enlarged', 'false');
        } else {
            $(this).css({ height: 'auto', width: '100%'});
            $(this).attr('enlarged', 'true');
        }
        //var id = $(this.attr('id')).split("_")[0];
        //var images_div_id = "images_" + id;
        //document.getElementById(images_div_id).scrollTo(this);
        //$(this).scrollIntoView({ inline: 'center' })
    })
})