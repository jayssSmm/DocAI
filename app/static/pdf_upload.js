import { marked } from 'https://cdn.jsdelivr.net/npm/marked/+esm'

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
    
    fetch("/upload", {
    method: "POST",
    body: formData
    })
    .then (response=>response.json())
    .then (data=>statusEle.innerHTML=marked.parse(data.message))
    .finally(alert('All Files Uploaded successfully'))
}