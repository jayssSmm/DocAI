document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('history-sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    const toggleBtn = document.getElementById('history-toggle');
    const closeBtn = document.getElementById('close-sidebar');

    // Centralized function to handle visual state
    const closeSidebar = () => {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    };

    // Keep your extractSession for the opening logic
    async function handleHistoryOpen() {
        let isOpening = !sidebar.classList.contains('active');
        
        // Visual Toggle
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');

        if (isOpening) {
            removeSessionFromHistory();
            try {
                let response = await fetch('/session', { credentials: 'include' });
                if (response.ok) {
                    let sessions = await response.json();
                    sessions.forEach(s => addSessionToHistory(s.title, s.id));
                }
            } catch (err) {
                console.error('Fetch error:', err);
            }
        }
    }

    toggleBtn.addEventListener('click', handleHistoryOpen);
    
    // Explicitly use the closing function for X and Overlay
    closeBtn.addEventListener('click', closeSidebar);
    overlay.addEventListener('click', closeSidebar);

    function addSessionToHistory(title, id) {
        const list = document.getElementById('sessions-list');
        const item = document.createElement('div');
        item.dataset.id = id;
        item.className = 'session-item';
        item.textContent = title || "New Conversation";
        list.prepend(item);
    }

    function removeSessionFromHistory() {
        document.getElementById('sessions-list').innerHTML = '';
    }
});