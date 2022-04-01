let socket = new WebSocket("ws://localhost:8000/ws/1")

socket.onmessage = function(e) {
    $(".messages").append(JSON.parse(e.data).val)
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