document.addEventListener('DOMContentLoaded', () => {

    const sidebar = document.getElementById('history-sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    const toggleBtn = document.getElementById('history-toggle');
    const closeBtn = document.getElementById('close-sidebar');

    const toggleSidebar = () => {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    };

    toggleBtn.addEventListener('click', extractSession);
    closeBtn.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', toggleSidebar);

    function addSessionToHistory(title) {
        const list = document.getElementById('sessions-list');
        const placeholder = list.querySelector('.placeholder');
        if (placeholder) placeholder.remove();

        const item = document.createElement('div');
        item.className = 'session-item';
        item.textContent = title || "New Conversation";
        
        // Add at the top
        list.prepend(item);
    };

    //Handles redundancy
    function removeSessionFromHistory(){
        document.getElementById('sessions-list').innerHTML='';
    }

    async function extractSession(){

        let isActive = sidebar.classList.toggle('active');
        overlay.classList.toggle('active');

        if (isActive){
            removeSessionFromHistory()
            let response = await fetch('/session',{credentials: 'include'});
            if (!response.ok) {
            console.error('Failed to fetch sessions:', response.status);
            return;
            };
            let sessions = await response.json();
            for (let session of sessions){
                addSessionToHistory(session.title)
            };
        };
    }

});