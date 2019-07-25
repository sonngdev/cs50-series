document.addEventListener('DOMContentLoaded', () => {
  let username = localStorage.getItem('username');
  if (!username) {
    username = prompt('Please enter your name');
    localStorage.setItem('username', username);
  }

  document.querySelector('.username').textContent = username
})
