import React, { useEffect, useState } from "react";
import { api } from "../api/client";
import { JobStatus } from "../components/JobStatus";

export default function Experiments(){
  const [projectId, setProjectId] = useState<number>(1);
  const [expId, setExpId] = useState<number | null>(null);
  const [algo, setAlgo] = useState("random");

  const start = async ()=>{
    if(algo==="corvi_opt"){
      const f = await api.get("/features/"); if(f.data.tier === "freemium"){ alert("Upgrade required to use Corvi-Opt"); return; }
    }
    const res = await api.post("/experiments/", {project_id: projectId, name: "demo", algorithm: algo, backend: "local", space: {budget: 10, x:{type:"int", low:0, high:10}}});
    setExpId(res.data.id);
  };

  return (
    <div className="space-y-4">
      <div className="flex gap-2 items-center">
        <label>Algorithm</label>
        <select value={algo} onChange={e=> setAlgo(e.target.value)}>
          <option value="grid">Grid</option>
          <option value="random">Random</option>
          <option value="corvi_opt">Corvi-Opt (Bayesian + pruning)</option>
        </select>
        <button onClick={start}>Start</button>
      </div>
      {expId && <JobStatus experimentId={expId} />}
    </div>
  );
}
