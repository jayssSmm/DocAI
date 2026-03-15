const statusEle=document.getElementById('status')
const aiForm=document.getElementById('ai-form')
const submitBtn=document.getElementById('submit')

aiForm.addEventListener('submit',()=>{
    statusEle.textContent='Thinking..'
    submitBtn.disabled=true
})

window.addEventListener('pageshow',()=>{
    submitBtn.disabled=false
})


const dropZone=document.getElementById('drop-zone')
const dropBox=document.getElementById('drop-box')

dropZone.addEventListener('dragover', (e)=>{
    e.preventDefault()
})

dropZone.addEventListener('drop', (e)=>{
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
    const formData = new FormData()
    
    for (let i = 0; i < files.length; i++) {
        formData.append("file", files[i])
    }

    fetch("/upload", {
    method: "POST",
    body: formData
    })
    .then (response=>response.json())
    .then (data=>alert(data.message))
}
