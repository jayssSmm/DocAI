import { marked } from 'https://cdn.jsdelivr.net/npm/marked/+esm'

const statusEle=document.getElementById('status')
const aiForm=document.getElementById('ai-form')
const submitBtn=document.getElementById('submit')

aiForm.addEventListener('submit',(e)=>{

    e.preventDefault()

    statusEle.textContent='Thinking..'
    submitBtn.disabled=true

    const prompt=document.getElementById('input').value
    const model=document.getElementById('model').value

    document.getElementById('input').value=''

    fetch('/prompt',{
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'prompt': prompt,
            'model': model
        })
    })
    .then (response=>response.json())
    .then (data=>statusEle.innerHTML=marked.parse(data.message))
    .finally(()=>{
        submitBtn.disabled=false
    })
})