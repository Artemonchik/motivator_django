"use strict";
var popup1 = $("#popup1");

var manSign = document.getElementById("ManSign");
manSign.addEventListener("click", function (ev) {
    $("#popup1").toggle();
    popup1.children().not("#profile_block_bottom_panel_quard").hide();
    $("#mains").show();
});

$("#settings").toggle();


var contentOfPopup1;
$(".settings_symbol").click(function (e) {
    var mains = $("#mains");
    var settings = $("#settings");
    if (mains.is(":visible")) {
        settings.show();
        mains.hide();
    } else {
        popup1.children().not("#profile_block_bottom_panel_quard").hide();
        mains.show();
    }
});

$("#changepasswordbutton").on("click", function (event) {
    popup1.children().not("#profile_block_bottom_panel_quard").hide();
    $("#changepasswordblock").show();
});
