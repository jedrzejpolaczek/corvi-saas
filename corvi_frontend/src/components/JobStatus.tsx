import React, { useEffect, useState } from "react";

export const JobStatus: React.FC<{experimentId:number}> = ({experimentId})=>{
  const [log, setLog] = useState<string[]>([]);
  useEffect(()=>{
    const ws = new WebSocket((location.protocol.startsWith("https")?"wss":"ws")+`://${location.host}/api/experiments/ws/jobs/${experimentId}`);
    ws.onmessage = ev => setLog(prev=>[ev.data, ...prev].slice(0,200));
    ws.onopen = ()=> ws.send("ping");
    const t = setInterval(()=> ws.readyState===1 && ws.send("ping"), 10000);
    return ()=>{ clearInterval(t); ws.close(); };
  },[experimentId]);
  return <pre style={{background:'#f6f6f6', padding:8, height:256, overflow:'auto', fontSize:12}}>{log.join("\n")}</pre>;
}
