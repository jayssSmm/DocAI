import { marked } from 'https://cdn.jsdelivr.net/npm/marked/+esm'

const dropZone=document.getElementById('drop-zone')
const dropBox=document.getElementById('drop-box')
const statusEle=document.getElementById('status')

dropZone.addEventListener('dragover', (e)=>{
    e.preventDefault()
})

dropZone.addEventListener('drop', (e)=>{
    e.preventDefault()
    const dropData=e.dataTransfer.files
    dataHandler(dropData)
})

dropZone.addEventListener('click', (e)=>{
    dropBox.click()
})

dropBox.addEventListener('change', (e)=>{
    dataHandler(e.target.files)
})

dropBox.addEventListener('paste', (e)=>{
    const pasteData=e.clipboardData.files
    dataHandler(pasteData)
})

function dataHandler(files){

    const maxSize=10*1024*1024
    let arrFile=[]

    for (let i=0;i<files.length;i++){
        let currentFile=files[i]
        if (currentFile.size>maxSize){
            alert('File size Exceeds 10MB limit')
            return
        }else{
            arrFile.push(files[i])
        }
    }
    uploadFile(arrFile)
}

function uploadFile(arrFile){
    const formData = new FormData()

    for (let i=0;i<arrFile.length;i++){
        formData.append("file", arrFile[i])
    }
    
    fetch("/upload", {
    method: "POST",
    body: formData
    })
    .then (response=>response.json())
    .then (data=>statusEle.innerHTML=marked.parse(data.message))
}