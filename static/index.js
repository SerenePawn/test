let socket = new WebSocket("ws://localhost:8000/ws/")

socket.onmessage = function(e) {
    num = JSON.parse(e.data).val_num
    txt = JSON.parse(e.data).val_text
    appendThis = "<div>" + num + ". " + txt + "</div>"
    $(".messages").append(appendThis)
};

obj = document.getElementsByClassName('textSend')[0];
obj.onclick = sendMsg;
function sendMsg(){
    // Т.к. приложение ну очень простое, то не буду выводить сам словарь
    // в отдельную переменную
    socket.send(
            JSON.stringify({
                'val':document.getElementsByClassName('textInput')[0].value
            })
        );
}
