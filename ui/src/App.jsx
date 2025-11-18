import React, { useState } from 'react'

export default function App(){
  const [uploadId, setUploadId] = useState('')
  const [file, setFile] = useState(null)

  async function send(){
    if(!file) return alert('Selecciona un archivo')
    const b = await file.arrayBuffer()
    const base64 = btoa(String.fromCharCode(...new Uint8Array(b)))
    const res = await fetch('/webhook', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ filename: file.name, data_base64: base64, source: 'ui' })
    })
    const data = await res.json()
    setUploadId(data.upload_id)
  }

  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <h1>PoC UI</h1>
      <input type="file" onChange={e=>setFile(e.target.files[0])} />
      <button onClick={send}>Enviar</button>
      {uploadId && <p>Upload ID: {uploadId}</p>}
    </div>
  )
}
