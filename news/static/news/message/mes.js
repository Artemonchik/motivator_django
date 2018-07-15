
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
var messageInput = document.getElementById("id_message");

messageInput.form.onsubmit = function (ev) {
    var text = messageInput.value;
    clearInterval(check);
    var request = new XMLHttpRequest();
    request.open("POST",messageUrl,true);
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    var formData = new FormData();
    formData.append("message",text);

    request.send(formData);
    messageInput.value = "";
    ev.preventDefault();

    request.onload = function (ev1) {
        console.log(request.responseText);
        var el = document.createElement("div");
        el.className = "your_messages";
        el.textContent = text;
        var dw = document.getElementById("dialog_window");
        dw.insertBefore(el,dw.children[0]);
        count++;
        check = setInterval(checkNewMessages,3000,checkUrl,userId);
    };
    return false;
};

function checkNewMessages(url,id) {
    var request = new XMLHttpRequest();
    request.open("GET", url+"?"+"id="+id+"&count="+count);
    request.send();
    request.onload = function (ev) {
        if(request.responseText === "No messages")return;
        console.log(request.responseText);
        var resp = request.responseText.split(",");
        count += resp.length;
        for(let i = 0; i < resp.length; i++){
            var dw = document.getElementById("dialog_window");
            var mes = document.createElement("div");
            mes.textContent = resp[i];
            mes.className = "messages_of_opponent";
            dw.insertBefore(mes, dw.children[0])
        }

    };
    console.log(count);
}
check = setInterval(checkNewMessages,3000,checkUrl,userId)