import { marked } from 'https://cdn.jsdelivr.net/npm/marked/+esm'
import { session_id } from './main_llm.js'
import { guestId } from './main_llm.js'
import { setSessionId } from './main_llm.js'

const dropZone=document.getElementById('drop-zone')
const dropBox=document.getElementById('drop-box')
const statusEle=document.getElementById('status')

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

function dataHandler(file){

    const maxSize=10*1024*1024

    if (file.size>maxSize){
        alert('File size Exceeds 10MB limit')
        statusEle.textContent='Waiting for your prompt...'
        return
     }else if (file.type!=='application/pdf'){
        alert('Error: Upload pdf Only')
        statusEle.textContent='Waiting for your prompt...'
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
    .then (response=>{
        if (response.status==500) {
            alert('File too Big');
            statusEle.textContent='Waiting for your prompt...'
            return
        }
        return response.json()
    })
    .then (data=>{
        const cleaned = data.message
        .replace(/\n{3,}/g, '\n\n')
        .trim();
        statusEle.innerHTML=marked.parse(cleaned)
        setSessionId(data.session_id)
    })
}