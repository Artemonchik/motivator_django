console.log("okey");

var plus = document.getElementById("plus");
plus.addEventListener("click", function (e) {
    var x = document.getElementById("new_challenge");
    x.style.display = "block";
    console.log("opened new_challenge");
});
var photoInput = document.querySelector("#add_photo_block > input");
photoInput.addEventListener("change", function () {
    var photoBlock = document.getElementById("add_photo_block");
    console.log("added photo")
    photoBlock.style.backgroundImage = photoInput.files[0].name;
    console.log(photoInput.files);
}, false);


