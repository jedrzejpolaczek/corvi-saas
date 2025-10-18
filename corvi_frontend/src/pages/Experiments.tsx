import React, { useState } from 'react';
import AdvancedSettings, { AdvancedSettingsData } from '../components/AdvancedSettings';

interface ExperimentConfig {
  dataset: File | null;
  customModel: File | null;
  predefinedModel: string;
  advancedSettings: AdvancedSettingsData;
}

interface Experiment {
  id: string;
  name: string;
  status: 'Running' | 'Completed' | 'Failed' | 'Pending';
  progress: number;
  created: string;
  runtime: string;
  accuracy?: number;
}

export default function Experiments() {
  console.log('🔥 Experiments component loaded - VERSION 3.0');
  console.log('🔥 Experiments loaded with Tailwind CDN!');
  const [config, setConfig] = useState<ExperimentConfig>({
    dataset: null,
    customModel: null,
    predefinedModel: '',
    advancedSettings: {
      optimization_algorithm: 'random_search',
      max_trials: 50,
      timeout: 3600,
      cross_validation_folds: 5,
      test_size: 0.2,
      random_state: 42,
      scoring_metric: 'accuracy',
      early_stopping: true,
      early_stopping_rounds: 10
    }
  });

  const [showAdvancedSettings, setShowAdvancedSettings] = useState(false);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [experiments, setExperiments] = useState<Experiment[]>([
    { id: '1', name: 'Revenue Optimization Model', status: 'Running', progress: 75, created: '2024-10-17', runtime: '2h 34m', accuracy: 0.87 },
    { id: '2', name: 'Customer Churn Prediction', status: 'Completed', progress: 100, created: '2024-10-16', runtime: '1h 22m', accuracy: 0.92 },
    { id: '3', name: 'Price Optimization', status: 'Pending', progress: 0, created: '2024-10-17', runtime: '-' }
  ]);

  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('All');

  const handleDatasetChange = (file: File | null) => {
    setConfig(prev => ({ ...prev, dataset: file }));
  };

  const handleModelChange = (file: File | null) => {
    setConfig(prev => ({ ...prev, customModel: file, predefinedModel: '' }));
  };

  const handlePredefinedModelChange = (model: string) => {
    setConfig(prev => ({ ...prev, predefinedModel: model, customModel: null }));
  };

  const handleAdvancedSettingsChange = (settings: AdvancedSettingsData) => {
    setConfig(prev => ({ ...prev, advancedSettings: settings }));
  };

  const handleStartOptimization = async () => {
    console.log('🚀 Starting optimization...');
    console.log('Dataset:', config.dataset?.name);
    console.log('Custom Model:', config.customModel?.name);
    console.log('Predefined Model:', config.predefinedModel);
    console.log('Settings:', config.advancedSettings);
    
    if (!config.dataset || (!config.customModel && !config.predefinedModel)) {
      alert('Please select a dataset and a model before starting optimization.');
      return;
    }
    setIsOptimizing(true);
    try {
      const formData = new FormData();
      formData.append('dataset', config.dataset!);
      if (config.customModel) formData.append('model', config.customModel);
      else formData.append('predefined_model', config.predefinedModel);
      formData.append('settings', JSON.stringify(config.advancedSettings));

      console.log('📤 Sending request to /api/experiments');
      const response = await fetch('/api/experiments', {
        method: 'POST',
        body: formData
      });

      console.log('📨 Response status:', response.status);
      const responseText = await response.text();
      console.log('📨 Response text:', responseText);

      if (!response.ok) throw new Error(`HTTP ${response.status}: ${responseText}`);

      const result = JSON.parse(responseText);
      console.log('✅ Success:', result);
      
      const newExperiment: Experiment = {
        id: result.experiment_id,
        name: `Experiment ${Date.now()}`,
        status: 'Running',
        progress: 0,
        created: new Date().toISOString().split('T')[0],
        runtime: '0m'
      };
      setExperiments(prev => [newExperiment, ...prev]);
      alert('Experiment started successfully!');
    } catch (e) {
      console.error('❌ Error:', e);
      alert(`Failed to start optimization: ${e}`);
    } finally {
      setIsOptimizing(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.reload();
  };

  const filteredExperiments = experiments.filter(exp => {
    const matchesSearch = exp.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'All' || exp.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Running': return 'bg-blue-100 text-blue-800';
      case 'Completed': return 'bg-green-100 text-green-800';
      case 'Failed': return 'bg-red-100 text-red-800';
      case 'Pending': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-8">
              <h1 className="text-2xl font-bold text-blue-600">Corvi</h1>
              <nav className="hidden md:flex space-x-6">
                <a href="#" className="text-gray-600 hover:text-gray-900">Dashboard</a>
                <a href="#" className="text-blue-600 font-medium border-b-2 border-blue-600">Experiments</a>
                <a href="#" className="text-gray-600 hover:text-gray-900">Models</a>
                <a href="#" className="text-gray-600 hover:text-gray-900">Datasets</a>
                <a href="#" className="text-gray-600 hover:text-gray-900">Analytics</a>
              </nav>
            </div>
            <div className="flex items-center space-x-4">
              <button className="p-2 text-gray-400 hover:text-gray-600" aria-label="notifications">🔔</button>
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm font-medium">DU</span>
                </div>
                <span className="text-sm font-medium text-gray-700">Demo User</span>
              </div>
              <button
                onClick={handleLogout}
                className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex gap-8">
          {/* LEFT SIDEBAR - New Form Design based on HTML */}
          <div className="w-96 flex-shrink-0">
            <div className="max-w-3xl mx-auto">
              <form className="space-y-6" onSubmit={(e) => { e.preventDefault(); handleStartOptimization(); }}>
                {/* Dataset file */}
                <div>
                  <label className="block text-gray-700 text-base font-medium mb-1">Dataset file</label>
                  <p className="text-gray-400 text-sm mb-2">Helper text</p>
                  <div className="flex">
                    <input 
                      type="text" 
                      className="flex-grow px-4 py-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-green-500" 
                      placeholder=""
                      value={config.dataset ? config.dataset.name : ''}
                      readOnly
                    />
                    <input
                      type="file"
                      accept=".csv,.xlsx,.xls"
                      onChange={(e) => handleDatasetChange(e.target.files?.[0] || null)}
                      className="hidden"
                      id="dataset-file-input"
                    />
                    <button 
                      type="button" 
                      onClick={() => document.getElementById('dataset-file-input')?.click()}
                      className="bg-green-500 text-white px-6 py-2 rounded-r-lg hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                    >
                      Przeglądaj
                    </button>
                  </div>
                </div>
                
                {/* Upload your own model */}
                <div>
                  <label className="block text-gray-700 text-base font-medium mb-1">Upload your own model (.py)</label>
                  <p className="text-gray-400 text-sm mb-2">Helper text</p>
                  <div className="flex">
                    <input 
                      type="text" 
                      className="flex-grow px-4 py-2 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-green-500" 
                      placeholder=""
                      value={config.customModel ? config.customModel.name : ''}
                      readOnly
                    />
                    <input
                      type="file"
                      accept=".py"
                      onChange={(e) => handleModelChange(e.target.files?.[0] || null)}
                      className="hidden"
                      id="model-file-input"
                    />
                    <button 
                      type="button" 
                      onClick={() => document.getElementById('model-file-input')?.click()}
                      className="bg-green-500 text-white px-6 py-2 rounded-r-lg hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                    >
                      Przeglądaj
                    </button>
                  </div>
                </div>
                
                {/* Predefined models dropdown */}
                <div>
                  <p className="text-gray-500 text-center mb-2">Or choose from list:</p>
                  <div className="relative">
                    <select 
                      className="block w-full px-4 py-3 border border-gray-300 rounded-lg appearance-none focus:outline-none focus:ring-2 focus:ring-green-500 text-gray-500"
                      value={config.predefinedModel}
                      onChange={(e) => handlePredefinedModelChange(e.target.value)}
                    >
                      <option value="">Select a predefined</option>
                      <option value="linear_regression">Linear Regression</option>
                      <option value="random_forest">Random Forest</option>
                      <option value="xgboost">XGBoost</option>
                      <option value="neural_network">Neural Network</option>
                    </select>
                    <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-green-500">
                      <svg className="w-4 h-4 fill-current" viewBox="0 0 20 20">
                        <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"/>
                      </svg>
                    </div>
                  </div>
                </div>
                
                {/* Advanced Settings */}
                <div>
                  <button 
                    type="button" 
                    onClick={() => setShowAdvancedSettings(true)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg text-green-500 font-medium hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500"
                  >
                    Advanced Settings
                  </button>
                </div>
                
                {/* Start Optimization */}
                <div>
                  <button 
                    type="submit"
                    disabled={!config.dataset || (!config.customModel && !config.predefinedModel) || isOptimizing}
                    className={`w-full px-4 py-4 font-medium rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 flex items-center justify-center transition-colors ${
                      !config.dataset || (!config.customModel && !config.predefinedModel) || isOptimizing
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : 'bg-green-500 text-white hover:bg-green-600'
                    }`}
                  >
                    {isOptimizing ? 'Starting...' : 'Start Optimization'}
                    <svg className="w-4 h-4 ml-2 fill-current" viewBox="0 0 20 20">
                      <path d="M10 18l-6-6h4V2h4v10h4l-6 6z"/>
                    </svg>
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* RIGHT SIDE - Experiments List (unchanged) */}
          <div className="flex-1">
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">Your Experiments</h2>
                  <div className="text-sm text-gray-600">{filteredExperiments.length} experiments</div>
                </div>
                <div className="flex gap-4">
                  <input
                    type="text"
                    placeholder="Search experiments..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="flex-1 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  />
                  <select
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                    className="p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                  >
                    <option value="All">All Status</option>
                    <option value="Running">Running</option>
                    <option value="Completed">Completed</option>
                    <option value="Failed">Failed</option>
                    <option value="Pending">Pending</option>
                  </select>
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Progress</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Runtime</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {filteredExperiments.map((experiment) => (
                      <tr key={experiment.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm font-medium text-gray-900">{experiment.name}</div>
                          {experiment.accuracy && (
                            <div className="text-sm text-gray-500">Accuracy: {(experiment.accuracy * 100).toFixed(1)}%</div>
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(experiment.status)}`}>
                            {experiment.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="w-16 bg-gray-200 rounded-full h-2 mr-2">
                              <div
                                className={`h-2 rounded-full ${experiment.status === 'Completed' ? 'bg-green-600' : 'bg-blue-600'}`}
                                style={{ width: `${experiment.progress}%` }}
                              />
                            </div>
                            <span className="text-sm text-gray-600">{experiment.progress}%</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{experiment.created}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{experiment.runtime}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <button className="text-blue-600 hover:text-blue-800 mr-3">View</button>
                          {experiment.status === 'Running' && (
                            <button className="text-red-600 hover:text-red-800">Stop</button>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {filteredExperiments.length === 0 && (
                <div className="text-center py-12">
                  <div className="text-gray-400 text-6xl mb-4">🧪</div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No experiments found</h3>
                  <p className="text-gray-600">Create your first experiment to get started with ML optimization.</p>
                </div>
              )}
            </div>
          </div>
        </div>

        <AdvancedSettings
          isOpen={showAdvancedSettings}
          onClose={() => setShowAdvancedSettings(false)}
          onSave={handleAdvancedSettingsChange}
        />
      </div>
    </div>
  );
}