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