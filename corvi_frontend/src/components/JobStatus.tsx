import React, { useState, useEffect } from 'react'

interface JobStatusProps {
  experimentId: string
  onComplete: () => void
}

export default function JobStatus({ experimentId, onComplete }: JobStatusProps) {
  const [status, setStatus] = useState('running')
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    // Simulate progress for demo
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval)
          setStatus('completed')
          onComplete()
          return 100
        }
        return prev + 2
      })
    }, 1000)

    return () => clearInterval(interval)
  }, [onComplete])

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-gray-700">Progress</span>
        <span className="text-sm text-gray-500">{progress}%</span>
      </div>
      
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div 
          className="bg-green-600 h-2 rounded-full transition-all duration-300"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      
      <div className="text-sm text-gray-600">
        {status === 'running' ? 'Optimizing model...' : 'Optimization complete!'}
      </div>
      
      <div className="text-xs text-gray-500">
        Experiment ID: {experimentId}
      </div>
    </div>
  )
}