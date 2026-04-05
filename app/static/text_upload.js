import { marked } from 'https://cdn.jsdelivr.net/npm/marked/+esm'

const statusEle=document.getElementById('status')
const aiForm=document.getElementById('ai-form')
const submitBtn=document.getElementById('submit')
const newSessBtn = document.getElementById('new-session-btn')

let session_id = null

newSessBtn.addEventListener('click',()=>{
    session_id = null
})

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
            'model': model,
            'session_id': session_id,
        })
    })
    .then (response=>response.json())
    .then (data=>{
        statusEle.innerHTML = marked.parse(data.message)
        session_id = data.session_id
        console.log(session_id)
    })
    .finally(()=>{
        submitBtn.disabled=false
    })
})