const newSessBtn = document.getElementById('new-session-btn');

newSessBtn.addEventListener('click', async (e) => {
    let response = await fetch('/session/new',{credentials:'include'})
})