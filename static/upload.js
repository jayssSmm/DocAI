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
    const dropData=e.dataTransfer.files()
    dataHandler(dropData)
})

dropZone.addEventListener('click', (e)=>{
    dropBox.click()
})

dropBox.addEventListener('change', (e)=>{
    dataHandler(dropBox.files)
})

dropBox.addEventListener('paste', (e)=>{
    const pasteData=e.clipboardData.items()
    dataHandler(pasteData)
})

function dataHandler(data){
    const formData = new FormData()
    formData.append("data", data)

    fetch("/upload", {
    method: "POST",
    body: formData
    })
}