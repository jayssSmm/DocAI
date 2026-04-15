import { marked } from 'https://cdn.jsdelivr.net/npm/marked/+esm'
import { sendPrompt } from './text_upload.js'

const statusEle=document.getElementById('status')
const aiForm=document.getElementById('ai-form')
const submitBtn=document.getElementById('submit')

const newSessBtn = document.getElementById('new-session-btn')
const sidebar = document.getElementById('history-sidebar');
const overlay = document.getElementById('sidebar-overlay');
const sessList=document.getElementById('sessions-list')

function getGuestId() {
    const existing = localStorage.getItem("guest_id")
    if (existing) return existing          // reuse across refreshes

    const newId = crypto.randomUUID()
    localStorage.setItem("guest_id", newId)
    return newId
}

export function setSessionId(newId){
    session_id = newId;
}

export const guestId = getGuestId()

export let session_id = null

document.addEventListener('DOMContentLoaded', () => {
    newSessBtn.addEventListener('click',()=>{
        session_id = null
        statusEle.textContent='Waiting for your prompt...'
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');

        document.getElementById('input').focus();
    })

    sessList.addEventListener('click', (e)=>{
        const item = e.target.closest('.session-item');

        if (item) {
            session_id = item.dataset.id; // Now this will not be undefined
            statusEle.textContent='Waiting for your prompt...'

            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
            document.getElementById('input').focus();
        }
    })
})

aiForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    statusEle.textContent = 'Thinking..';
    submitBtn.disabled = true;

    const prompt = document.getElementById('input').value;
    const model = document.getElementById('model').value;
    document.getElementById('input').value = '';

    sendPrompt({ prompt, model, session_id, guestId })
    .then(data => {
        const cleaned = data.message
        .replace(/\n{3,}/g, '\n\n')
        .trim();
        statusEle.innerHTML = marked.parse(cleaned);
        session_id = data.session_id;
    })
    .finally(() => {
      submitBtn.disabled = false;
    });
});
