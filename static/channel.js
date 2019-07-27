document.addEventListener('DOMContentLoaded', () => {
  const username = document.querySelector('#username').textContent;
  const channelname = document.querySelector('#channelname').value;
  const form = document.querySelector('#form-message');

  let socket = io.connect(`${location.protocol}//${document.domain}:${location.port}`);

  function deleteMessage() {
    const { messageId } = this.dataset;
    socket.emit('delete message', { channelname, message_id: messageId, deleter: username })
  }

  socket.on('connect', () => {
    form.onsubmit = () => {
      const message = document.querySelector('#message').value;
      socket.emit('submit message', { message, username, channelname });
      form.reset();
      form.focus();
      return false;
    }
  })

  socket.on('announce message', message => {
    const li = document.createElement('li');
    li.classList.add('mb-3', 'message');
    li.dataset.sender = username;
    li.dataset.messageId = message.id;

    const p = document.createElement('p');
    p.classList.add('mb-0');
    p.textContent = message.text;
    li.append(p);

    const span = document.createElement('span');
    const small = document.createElement('small');
    small.textContent = `${message.sender} | ${moment(message.timestamp).format('DD-MM-YYYY, hh:mm:ss A')}`;
    span.append(small);
    li.append(span);

    if (username === message.sender) {
      const button = document.createElement('button');
      button.classList.add('btn', 'btn-link', 'btn-sm', 'ml-2', 'message-delete');
      button.textContent = 'Delete';
      button.dataset.messageId = message.id;
      button.onclick = deleteMessage;
      li.append(button);
    }

    document.querySelector('#message-list').append(li);
  })

  socket.on('announce deleted message', deletedMessage => {
    const messageId = deletedMessage.id;
    document.querySelector(`.message[data-message-id="${messageId}"`).remove();
  })

  document.querySelectorAll('.message').forEach(message => {
    const sender = message.dataset.sender;
    if (sender === username) {
      const button = document.createElement('button');
      button.classList.add('btn', 'btn-link', 'btn-sm', 'ml-2', 'message-delete');
      button.textContent = 'Delete';
      button.dataset.messageId = message.dataset.messageId;
      button.onclick = deleteMessage;
      message.append(button);
    }
  })
})
