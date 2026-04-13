import { marked } from 'https://cdn.jsdelivr.net/npm/marked/+esm'

const dropZone=document.getElementById('drop-zone')
const dropBox=document.getElementById('drop-box')
const statusEle=document.getElementById('status')

const guestId = localStorage.getItem("guest_id") || crypto.randomUUID()
localStorage.setItem("guest_id", guestId)

let session_id = null

dropZone.addEventListener('dragover', (e)=>{
    e.preventDefault()
})

dropZone.addEventListener('drop', (e)=>{
    e.preventDefault()
    const dropData=e.dataTransfer.files[0]
    dataHandler(dropData)
})

dropZone.addEventListener('click', (e)=>{
    dropBox.click()
})

dropBox.addEventListener('change', (e)=>{
    dataHandler(e.target.files[0])
})

dropBox.addEventListener('paste', (e)=>{
    const pasteData=e.clipboardData.files[0]
    dataHandler(pasteData)
})

document.addEventListener('DOMContentLoaded', () => {
    sessList.addEventListener('click', (e)=>{
        const item = e.target.closest('.session-item');

        if (item) {
            session_id = item.dataset.id; 

            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
            document.getElementById('input').focus();
        }
    })
})

function dataHandler(file){

    const maxSize=10*1024*1024

    if (file.size>maxSize){
        alert('Error: File size Exceeds 10MB limit')
        return
     }else if (file.type!=='application/pdf'){
        alert('Error: Upload pdf Only')
        return
    }else{
        uploadFile(file)
    }
}

function uploadFile(file){

    statusEle.textContent='Thinking..'
    const formData = new FormData()

    formData.append("file", file)
    formData.append('session_id', JSON.stringify(session_id))
    
    fetch("/upload", {
    method: "POST",
    credentials:'include',
    headers: {
        "x-guest-id": guestId
    },
    body: formData
    })
    .then (response=>response.json())
    .then (data=>statusEle.innerHTML=marked.parse(data.message))
    .finally(alert('All Files Uploaded successfully'))
}