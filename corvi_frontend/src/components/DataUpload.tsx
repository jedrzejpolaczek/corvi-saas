import React, { useState } from 'react';

interface DataUploadProps {
  onDatasetChange?: (file: File | null) => void;
  onModelChange?: (file: File | null) => void;
  onPredefinedModelChange?: (model: string) => void;
  onAdvancedSettings?: () => void;
  onStartOptimization?: () => void;
}

export default function DataUpload({
  onDatasetChange,
  onModelChange,
  onPredefinedModelChange,
  onAdvancedSettings,
  onStartOptimization
}: DataUploadProps) {
  const [selectedDataset, setSelectedDataset] = useState<File | null>(null);
  const [selectedModel, setSelectedModel] = useState<File | null>(null);
  const [selectedPredefined, setSelectedPredefined] = useState<string>('');
  const [isDragOverDataset, setIsDragOverDataset] = useState(false);
  const [isDragOverModel, setIsDragOverModel] = useState(false);

  const predefinedModels = [
    { value: '', label: 'Select a predefined model' },
    { value: 'random_forest', label: 'Random Forest Classifier' },
    { value: 'gradient_boosting', label: 'Gradient Boosting Classifier' },
    { value: 'svm', label: 'Support Vector Machine' },
    { value: 'neural_network', label: 'Neural Network (MLP)' },
    { value: 'logistic_regression', label: 'Logistic Regression' },
    { value: 'xgboost', label: 'XGBoost Classifier' },
    { value: 'lightgbm', label: 'LightGBM Classifier' },
    { value: 'catboost', label: 'CatBoost Classifier' }
  ];

  const handleDatasetFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null;
    setSelectedDataset(file);
    onDatasetChange?.(file);
  };

  const handleModelFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null;
    setSelectedModel(file);
    onModelChange?.(file);
  };

  const handlePredefinedChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const value = event.target.value;
    setSelectedPredefined(value);
    onPredefinedModelChange?.(value);
  };

  const handleDragOver = (event: React.DragEvent, type: 'dataset' | 'model') => {
    event.preventDefault();
    if (type === 'dataset') {
      setIsDragOverDataset(true);
    } else {
      setIsDragOverModel(true);
    }
  };

  const handleDragLeave = (type: 'dataset' | 'model') => {
    if (type === 'dataset') {
      setIsDragOverDataset(false);
    } else {
      setIsDragOverModel(false);
    }
  };

  const handleDrop = (event: React.DragEvent, type: 'dataset' | 'model') => {
    event.preventDefault();
    const files = Array.from(event.dataTransfer.files);
    const file = files[0];
    
    if (type === 'dataset') {
      setIsDragOverDataset(false);
      if (file && (file.name.endsWith('.csv') || file.name.endsWith('.xlsx'))) {
        setSelectedDataset(file);
        onDatasetChange?.(file);
      }
    } else {
      setIsDragOverModel(false);
      if (file && file.name.endsWith('.py')) {
        setSelectedModel(file);
        onModelChange?.(file);
      }
    }
  };

  const canStartOptimization = selectedDataset && (selectedModel || selectedPredefined);

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-8">
      {/* Dataset File Upload */}
      <div className="space-y-3">
        <div>
          <h3 className="text-lg font-medium text-gray-900">Dataset file</h3>
          <p className="text-sm text-gray-500">Upload your dataset in CSV or Excel format</p>
        </div>
        
        <div
          className={`relative border-2 border-dashed rounded-lg p-6 transition-colors ${
            isDragOverDataset
              ? 'border-green-400 bg-green-50'
              : selectedDataset
              ? 'border-green-300 bg-green-50'
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragOver={(e) => handleDragOver(e, 'dataset')}
          onDragLeave={() => handleDragLeave('dataset')}
          onDrop={(e) => handleDrop(e, 'dataset')}
        >
          <div className="flex items-center justify-between">
            <div className="flex-1">
              {selectedDataset ? (
                <div className="flex items-center space-x-2">
                  <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                  <span className="text-sm font-medium text-gray-900">{selectedDataset.name}</span>
                  <span className="text-xs text-gray-500">({(selectedDataset.size / 1024).toFixed(1)} KB)</span>
                </div>
              ) : (
                <div className="text-center">
                  <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                  <div className="mt-2">
                    <p className="text-sm text-gray-600">Drop your dataset file here, or click to browse</p>
                    <p className="text-xs text-gray-500 mt-1">Supports CSV, Excel files</p>
                  </div>
                </div>
              )}
            </div>
            
            <button
              type="button"
              className="ml-4 px-4 py-2 bg-green-500 text-white text-sm font-medium rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors"
              onClick={() => document.getElementById('dataset-upload')?.click()}
            >
              Przeglądaj
            </button>
          </div>
          
          <input
            id="dataset-upload"
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={handleDatasetFileChange}
            className="sr-only"
          />
        </div>
      </div>

      {/* Model Upload */}
      <div className="space-y-3">
        <div>
          <h3 className="text-lg font-medium text-gray-900">Upload your own model (.py)</h3>
          <p className="text-sm text-gray-500">Upload a custom Python model file</p>
        </div>
        
        <div
          className={`relative border-2 border-dashed rounded-lg p-6 transition-colors ${
            isDragOverModel
              ? 'border-green-400 bg-green-50'
              : selectedModel
              ? 'border-green-300 bg-green-50'
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragOver={(e) => handleDragOver(e, 'model')}
          onDragLeave={() => handleDragLeave('model')}
          onDrop={(e) => handleDrop(e, 'model')}
        >
          <div className="flex items-center justify-between">
            <div className="flex-1">
              {selectedModel ? (
                <div className="flex items-center space-x-2">
                  <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                  <span className="text-sm font-medium text-gray-900">{selectedModel.name}</span>
                  <span className="text-xs text-gray-500">({(selectedModel.size / 1024).toFixed(1)} KB)</span>
                </div>
              ) : (
                <div className="text-center">
                  <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M9 12h6m6 0h6m-6 6v6m-6-6v6m6-6v6" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                    <path d="M21 10.5V21a1.5 1.5 0 001.5 1.5h7.5" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                  <div className="mt-2">
                    <p className="text-sm text-gray-600">Drop your Python model file here, or click to browse</p>
                    <p className="text-xs text-gray-500 mt-1">Supports .py files</p>
                  </div>
                </div>
              )}
            </div>
            
            <button
              type="button"
              className="ml-4 px-4 py-2 bg-green-500 text-white text-sm font-medium rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors"
              onClick={() => document.getElementById('model-upload')?.click()}
            >
              Przeglądaj
            </button>
          </div>
          
          <input
            id="model-upload"
            type="file"
            accept=".py"
            onChange={handleModelFileChange}
            className="sr-only"
          />
        </div>
      </div>

      {/* Divider */}
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-gray-300" />
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="px-2 bg-white text-gray-500">Or choose from list:</span>
        </div>
      </div>

      {/* Predefined Models */}
      <div className="space-y-3">
        <select
          value={selectedPredefined}
          onChange={handlePredefinedChange}
          className="w-full px-4 py-3 text-base border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white"
        >
          {predefinedModels.map((model) => (
            <option key={model.value} value={model.value}>
              {model.label}
            </option>
          ))}
        </select>
      </div>

      {/* Advanced Settings */}
      <div className="space-y-4">
        <button
          type="button"
          onClick={onAdvancedSettings}
          className="w-full px-4 py-3 text-green-600 font-medium bg-white border border-green-300 rounded-lg hover:bg-green-50 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors"
        >
          Advanced Settings
        </button>

        {/* Start Optimization Button */}
        <button
          type="button"
          onClick={onStartOptimization}
          disabled={!canStartOptimization}
          className={`w-full px-6 py-4 text-white font-semibold rounded-lg transition-all duration-200 flex items-center justify-center space-x-2 ${
            canStartOptimization
              ? 'bg-green-500 hover:bg-green-600 focus:ring-green-500 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
              : 'bg-gray-300 cursor-not-allowed'
          } focus:outline-none focus:ring-2 focus:ring-offset-2`}
        >
          <span>Start Optimization</span>
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>

      {/* Helper Text */}
      {!canStartOptimization && (
        <div className="text-center">
          <p className="text-sm text-gray-500">
            Please upload a dataset and select a model to start optimization
          </p>
        </div>
      )}
    </div>
  );
}