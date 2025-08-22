import React, { useState } from "react";
import { api } from "../api/client";

export const DataUpload: React.FC<{projectId: number,onDone:(res:any)=>void}> = ({projectId,onDone})=>{
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<any[]>([]);
  const [issues, setIssues] = useState<string[]>([]);
  const submit = async ()=>{
    if(!file) return;
    const form = new FormData(); form.append("project_id", String(projectId)); form.append("file", file);
    const res = await api.post("/datasets/upload", form, {headers:{"Content-Type":"multipart/form-data"}});
    setPreview(res.data.preview); setIssues(res.data.issues); onDone(res.data);
  };
  return (
    <div className="space-y-3">
      <input type="file" accept=".csv,.parquet" onChange={e=> setFile(e.target.files?.[0] || null)} />
      <button onClick={submit} disabled={!file}>Upload</button>
      {issues.length>0 && <div>Data Issues: {issues.join(", ")}</div>}
      {preview.length>0 && <div style={{maxHeight:256, overflow:'auto', border:'1px solid #eee'}}>
        <table className="text-xs w-full">
          <thead><tr>{Object.keys(preview[0]).map(k=> <th key={k} className="p-1 text-left border-b">{k}</th>)}</tr></thead>
          <tbody>{preview.map((r,i)=> <tr key={i}>{Object.values(r).map((v,j)=> <td key={j} className="p-1 border-b">{String(v)}</td>)}</tr>)}</tbody>
        </table>
      </div>}
    </div>
  );
};
