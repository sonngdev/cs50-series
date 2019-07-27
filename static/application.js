document.addEventListener('DOMContentLoaded', () => {
  // Set username
  let username = localStorage.getItem('username');
  if (!username) {
    username = prompt('Please enter your name');
    localStorage.setItem('username', username);
  }
  document.querySelector('#username').textContent = username;

  // Remember channel
  const regex = /\/channels\/(\w+)/gi;
  const match = regex.exec(location.pathname);
  if (match) {
    const channelname = match[1];
    localStorage.setItem('channelname', channelname);
  } else {
    const channelname = localStorage.getItem('channelname');
    const previousUrl = document.referrer;
    if (channelname && !previousUrl.includes(location.origin)) {
      location.href = `${location.origin}/channels/${channelname}`
    }
    localStorage.removeItem('channelname');
  }
})
