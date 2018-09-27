"use strict";
console.log("okey");

var plus = document.getElementById("plus");
var newChallengeWidth = $(document.getElementById("new_challenge")).width();

plus.addEventListener("click", function (e) {
    var newChallengeBlock = $(document.getElementById("new_challenge"));
    if (newChallengeBlock.css("display").toLowerCase() === "none") {
        newChallengeBlock.width(0).css("display", "block");
        newChallengeBlock.css("opacity","0");
        newChallengeBlock.animate({width: newChallengeWidth}, 200,function () {
            $(this).dequeue();
        });
        newChallengeBlock.queue(function () {
            $(this).animate({opacity:"1"},100)
        })
    } else {
        newChallengeBlock.animate({opacity:"0"},100,function () {
            newChallengeBlock.animate({width: 0}, 200,function () {
                newChallengeBlock.css("display","none")
            });
        });
    }
    newChallengeBlock.animate({display: block});
    console.log("opened new_challenge");
});

plus.addEventListener("selectstart", function (e) {
    e.preventDefault();
}, true);

var photoInput = document.querySelector("#add_photo_block > input");
photoInput.addEventListener("change", function () {
    var photoBlock = document.getElementById("add_photo_block");
    console.log("added photo");
    photoBlock.style.backgroundImage = photoInput.files[0].name;
    console.log(photoInput.files);
}, false);

var buttonLikeList = $(".time_left").add(".time_left_liked");
buttonLikeList.click(function (e) {
    var href = $(this).data("href");
    e.preventDefault();
    var button = $(this);
    $.ajax(href,{
        method:"GET",
        success:function (data,status,jqXHR) {
            console.log(status);
            console.log(this);
            button.toggleClass("time_left").toggleClass("time_left_liked");
            if(href.indexOf("unlike") !== -1){
                button.data("href", href.replace("/unlike/", "/like/"))
            }
            else {
                button.data("href", href.replace("/like/", "/unlike/"))
            }
        },
    });
});

