import React, { useState } from 'react'
import { api } from './api/client'
import Experiments from './pages/Experiments'
import { DataUpload } from './components/DataUpload'

export default function App(){
  const [token, setToken] = useState<string | null>(null)
  const [pid, setPid] = useState<number>(1)

  const login = async (e: React.FormEvent)=>{
    e.preventDefault()
    const form = new FormData(e.target as HTMLFormElement)
    const email = String(form.get("email"))
    const password = String(form.get("password"))
    const r = await api.post("/auth/token", {email, password})
    setToken(r.data.access_token)
    api.defaults.headers.common["Authorization"] = `Bearer ${r.data.access_token}`
  }

  return (
    <div className="p-6 space-y-6">
      {!token && (
        <form onSubmit={login} className="space-x-2">
          <input name="email" placeholder="email" defaultValue="demo@corvi.ai" />
          <input name="password" placeholder="password" type="password" defaultValue="demo" />
          <button type="submit">Login</button>
        </form>
      )}
      {token && (
        <div className="space-y-4">
          <h1 className="text-2xl font-bold">Corvi</h1>
          <h2 className="font-semibold">Step 1 – Upload Data</h2>
          <DataUpload projectId={pid} onDone={()=>{}} />
          <h2 className="font-semibold">Step 2/3 – Run HPO</h2>
          <Experiments />
        </div>
      )}
    </div>
  )
}
