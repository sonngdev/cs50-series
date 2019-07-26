document.addEventListener('DOMContentLoaded', () => {
  const username = document.querySelector('#username').textContent;
  const channelname = document.querySelector('#channelname').value;
  const form = document.querySelector('#form-message');

  let socket = io.connect(`${location.protocol}//${document.domain}:${location.port}`);

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
    li.innerHTML = `\
      <p class="mb-0">${message.text}</p>\
      <span><small>${message.sender} | ${moment(message.timestamp).format('DD-MM-YYYY, hh:mm:ss A')}</small></span>\
    `;
    li.classList.add('mb-3');
    document.querySelector('#message-list').append(li);
  })
})
