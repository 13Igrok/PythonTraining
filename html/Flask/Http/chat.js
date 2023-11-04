<!DOCTYPE html>
<html>
<head>
  <title>Чат</title>
  <style>
    #chatbox {
      width: 300px;
      height: 400px;
      overflow-y: scroll;
    }
  </style>
</head>
<body>
  <h1>Чат</h1>

  <div id="chatbox"></div>

  <form id="message-form">
    <input type="text" id="message-input" placeholder="Введите сообщение">
    <button type="submit">Отправить</button>
  </form>

  <script>
    const chatbox = document.getElementById('chatbox');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');

    const socket = new WebSocket('ws://localhost:8000/chat'); // Замените на ваш сервер WebSocket

    socket.onopen = function(event) {
      console.log('Соединение установлено!');
    };

    socket.onmessage = function(event) {
      const message = JSON.parse(event.data);
      chatbox.innerHTML += '<p><strong>' + message.username + ':</strong> ' + message.text + '</p>';
    };

    messageForm.addEventListener('submit', function(event) {
      event.preventDefault();

      const message = {
        username: 'User', // Замените на имя пользователя, полученное из регистрации
        text: messageInput.value
      };

      socket.send(JSON.stringify(message));
      messageInput.value = '';
    });
  </script>
</body>
</html>