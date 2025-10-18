import React, { useState } from 'react';
import AdvancedSettings, { AdvancedSettingsData } from '../components/AdvancedSettings';

interface ExperimentConfig {
  dataset: File | null;
  customModel: File | null;
  predefinedModel: string;
  advancedSettings: AdvancedSettingsData;
}

interface OptimizationResults {
  bestParams: Record<string, any>;
  bestScore: number;
  trialCount: number;
  metrics: {
    accuracy: number;
    precision: number;
    recall: number;
    f1Score: number;
    rocAuc?: number;
  };
  crossValidation: {
    mean: number;
    std: number;
    scores: number[];
  };
}

interface Experiment {
  id: string;
  name: string;
  status: 'Running' | 'Completed' | 'Failed' | 'Pending';
  progress: number;
  created: string;
  runtime: string;
  accuracy?: number;
  results?: OptimizationResults;
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
  const [experiments, setExperiments] = useState<Experiment[]>([]);

  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('All');
  const [selectedExperiment, setSelectedExperiment] = useState<Experiment | null>(null);
  const [showResults, setShowResults] = useState(false);

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
      
      // Create a descriptive experiment name
      const datasetName = config.dataset?.name.replace('.csv', '') || 'dataset';
      const modelName = config.predefinedModel || config.customModel?.name || 'custom';
      const algorithm = config.advancedSettings.optimization_algorithm;
      
      const newExperiment: Experiment = {
        id: result.experiment_id.toString(),
        name: `${datasetName} - ${modelName} (${algorithm})`,
        status: 'Running',
        progress: 0,
        created: new Date().toISOString().split('T')[0],
        runtime: '0m'
      };
      
      console.log('🆕 Adding new experiment to list:', newExperiment);
      setExperiments(prev => {
        const updated = [newExperiment, ...prev];
        console.log('📝 Updated experiments list:', updated);
        return updated;
      });
      
      alert(`Experiment started successfully!\nID: ${result.experiment_id}\nName: ${newExperiment.name}\nWatch the experiments list for progress updates.`);
      
      // Start mock progress simulation
      console.log('🏃 Starting progress simulation for experiment:', result.experiment_id);
      simulateProgress(result.experiment_id.toString());
    } catch (e) {
      console.error('❌ Error:', e);
      alert(`Failed to start optimization: ${e}`);
    } finally {
      setIsOptimizing(false);
    }
  };

  const downloadOptimizedModel = (experiment: Experiment) => {
    if (!experiment.results) return;
    
    // Generate model code based on the optimized parameters
    const modelCode = generateModelCode(config.predefinedModel, experiment.results.bestParams, experiment.results);
    
    // Create and download the file
    const blob = new Blob([modelCode], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `optimized_${config.predefinedModel}_model.py`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const generateModelCode = (modelType: string, params: Record<string, any>, results: OptimizationResults) => {
    const timestamp = new Date().toISOString();
    const modelName = modelType.replace('_', '').toLowerCase();
    
    let imports = '';
    let modelInit = '';
    let comments = '';
    
    switch (modelType) {
      case 'random_forest':
        imports = 'from sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\nimport pandas as pd\nimport numpy as np';
        modelInit = `RandomForestClassifier(\n${Object.entries(params).map(([key, value]) => `    ${key}=${typeof value === 'string' ? `'${value}'` : value}`).join(',\n')},\n    random_state=42\n)`;
        comments = '# Optimized Random Forest Classifier\n# This model achieved ' + (results.bestScore * 100).toFixed(2) + '% accuracy through hyperparameter optimization';
        break;
        
      case 'xgboost':
        imports = 'import xgboost as xgb\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\nimport pandas as pd\nimport numpy as np';
        modelInit = `xgb.XGBClassifier(\n${Object.entries(params).map(([key, value]) => `    ${key}=${typeof value === 'string' ? `'${value}'` : value}`).join(',\n')},\n    random_state=42\n)`;
        comments = '# Optimized XGBoost Classifier\n# This model achieved ' + (results.bestScore * 100).toFixed(2) + '% accuracy through hyperparameter optimization';
        break;
        
      case 'linear_regression':
        imports = 'from sklearn.linear_model import Ridge\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_squared_error, r2_score\nimport pandas as pd\nimport numpy as np';
        modelInit = `Ridge(\n${Object.entries(params).map(([key, value]) => `    ${key}=${typeof value === 'string' ? `'${value}'` : value}`).join(',\n')},\n    random_state=42\n)`;
        comments = '# Optimized Ridge Regression Model\n# This model achieved ' + (results.bestScore * 100).toFixed(2) + '% R² score through hyperparameter optimization';
        break;
        
      case 'neural_network':
        imports = 'from sklearn.neural_network import MLPClassifier\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score\nfrom sklearn.preprocessing import StandardScaler\nimport pandas as pd\nimport numpy as np';
        modelInit = `MLPClassifier(\n${Object.entries(params).map(([key, value]) => `    ${key}=${typeof value === 'string' ? `'${value}'` : value}`).join(',\n')},\n    random_state=42\n)`;
        comments = '# Optimized Neural Network Classifier\n# This model achieved ' + (results.bestScore * 100).toFixed(2) + '% accuracy through hyperparameter optimization';
        break;
        
      default:
        imports = 'from sklearn.ensemble import RandomForestClassifier\nimport pandas as pd\nimport numpy as np';
        modelInit = `RandomForestClassifier(random_state=42)`;
        comments = '# Default optimized model';
    }
    
    return `#!/usr/bin/env python3
"""
Optimized ${modelType.toUpperCase().replace('_', ' ')} Model
Generated by Corvi Optimization Platform
Generated on: ${timestamp}

Optimization Results:
- Best Score: ${(results.bestScore * 100).toFixed(2)}%
- Cross-validation Mean: ${(results.crossValidation.mean * 100).toFixed(2)}% ± ${(results.crossValidation.std * 100).toFixed(2)}%
- Total Trials: ${results.trialCount}
- Optimization Algorithm: ${config.advancedSettings.optimization_algorithm}
"""

${imports}
import joblib
from datetime import datetime

${comments}

class OptimizedModel:
    def __init__(self):
        """Initialize the optimized model with best parameters."""
        self.model = ${modelInit}
        self.scaler = StandardScaler() if '${modelType}' == 'neural_network' else None
        self.is_fitted = False
        
        # Model metadata
        self.optimization_results = {
            'best_score': ${results.bestScore},
            'cross_validation_mean': ${results.crossValidation.mean},
            'cross_validation_std': ${results.crossValidation.std},
            'trial_count': ${results.trialCount},
            'optimization_date': '${timestamp}',
            'best_params': ${JSON.stringify(params, null, 12)}
        }
    
    def fit(self, X, y):
        """Train the optimized model."""
        if self.scaler:
            X = self.scaler.fit_transform(X)
        
        self.model.fit(X, y)
        self.is_fitted = True
        return self
    
    def predict(self, X):
        """Make predictions with the optimized model."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        
        if self.scaler:
            X = self.scaler.transform(X)
            
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Get prediction probabilities (if supported)."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        
        if self.scaler:
            X = self.scaler.transform(X)
            
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(X)
        else:
            raise AttributeError("Model does not support probability predictions")
    
    def save_model(self, filepath):
        """Save the trained model to disk."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'metadata': self.optimization_results
        }
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    @classmethod
    def load_model(cls, filepath):
        """Load a saved model from disk."""
        model_data = joblib.load(filepath)
        instance = cls()
        instance.model = model_data['model']
        instance.scaler = model_data.get('scaler')
        instance.optimization_results = model_data['metadata']
        instance.is_fitted = True
        return instance
    
    def get_feature_importance(self):
        """Get feature importance (if supported)."""
        if hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        elif hasattr(self.model, 'coef_'):
            return abs(self.model.coef_).flatten()
        else:
            return None


def example_usage():
    """Example of how to use the optimized model."""
    # Load your data
    # df = pd.read_csv('your_dataset.csv')
    # X = df.drop('target', axis=1)  # Features
    # y = df['target']  # Target variable
    
    # Split the data
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train the optimized model
    model = OptimizedModel()
    # model.fit(X_train, y_train)
    
    # Make predictions
    # predictions = model.predict(X_test)
    # accuracy = accuracy_score(y_test, predictions)
    # print(f"Test Accuracy: {accuracy:.4f}")
    
    # Save the model
    # model.save_model('optimized_${modelName}_model.joblib')
    
    print("Model ready for training!")
    print("Optimization Results:", model.optimization_results)


if __name__ == "__main__":
    example_usage()
`;
  };

  const generateBestParams = (model: string) => {
    const params: Record<string, any> = {};
    
    switch (model) {
      case 'random_forest':
        params.n_estimators = Math.floor(Math.random() * 200) + 100; // 100-300
        params.max_depth = Math.floor(Math.random() * 15) + 5; // 5-20
        params.min_samples_split = Math.floor(Math.random() * 8) + 2; // 2-10
        params.min_samples_leaf = Math.floor(Math.random() * 4) + 1; // 1-5
        params.max_features = ['sqrt', 'log2', 'auto'][Math.floor(Math.random() * 3)];
        break;
      case 'xgboost':
        params.n_estimators = Math.floor(Math.random() * 300) + 100;
        params.learning_rate = (Math.random() * 0.2 + 0.01).toFixed(3);
        params.max_depth = Math.floor(Math.random() * 8) + 3;
        params.subsample = (Math.random() * 0.4 + 0.6).toFixed(2);
        params.colsample_bytree = (Math.random() * 0.4 + 0.6).toFixed(2);
        break;
      case 'linear_regression':
        params.alpha = (Math.random() * 10 + 0.1).toFixed(3);
        params.fit_intercept = Math.random() > 0.5;
        params.normalize = Math.random() > 0.5;
        break;
      case 'neural_network':
        params.hidden_layer_sizes = `(${Math.floor(Math.random() * 100) + 50}, ${Math.floor(Math.random() * 50) + 25})`;
        params.activation = ['relu', 'tanh', 'logistic'][Math.floor(Math.random() * 3)];
        params.learning_rate_init = (Math.random() * 0.01 + 0.001).toFixed(4);
        params.alpha = (Math.random() * 0.001 + 0.0001).toFixed(5);
        break;
      default:
        params.parameter1 = Math.random().toFixed(3);
        params.parameter2 = Math.floor(Math.random() * 100);
    }
    
    return params;
  };

  const simulateProgress = (experimentId: string) => {
    console.log('🎯 Setting up progress simulation for experiment:', experimentId);
    let progress = 0;
    let runtime = 0;
    
    const updateProgress = () => {
      progress += Math.random() * 15 + 5; // Random progress between 5-20%
      runtime += Math.floor(Math.random() * 30) + 10; // Add 10-40 seconds
      
      console.log(`📊 Updating experiment ${experimentId}: ${Math.floor(progress)}% progress, ${runtime}s runtime`);
      
      if (progress >= 100) {
        progress = 100;
        const finalAccuracy = 0.75 + Math.random() * 0.20; // Random accuracy between 75-95%
        
        // Generate realistic optimization results
        const optimizationResults: OptimizationResults = {
          bestParams: generateBestParams(config.predefinedModel),
          bestScore: finalAccuracy,
          trialCount: Math.floor(Math.random() * 30) + 20, // 20-50 trials
          metrics: {
            accuracy: finalAccuracy,
            precision: finalAccuracy + (Math.random() - 0.5) * 0.1,
            recall: finalAccuracy + (Math.random() - 0.5) * 0.1,
            f1Score: finalAccuracy + (Math.random() - 0.5) * 0.08,
            rocAuc: finalAccuracy + (Math.random() - 0.5) * 0.05
          },
          crossValidation: {
            mean: finalAccuracy,
            std: Math.random() * 0.05 + 0.01,
            scores: Array.from({length: 5}, () => finalAccuracy + (Math.random() - 0.5) * 0.1)
          }
        };
        
        console.log(`✅ Completing experiment ${experimentId} with results:`, optimizationResults);
        
        setExperiments(prev => prev.map(exp => 
          exp.id === experimentId 
            ? { 
                ...exp, 
                progress: 100, 
                status: 'Completed' as const, 
                runtime: `${Math.floor(runtime / 60)}m ${runtime % 60}s`,
                accuracy: finalAccuracy,
                results: optimizationResults
              }
            : exp
        ));
        return;
      }
      
      setExperiments(prev => prev.map(exp => 
        exp.id === experimentId 
          ? { 
              ...exp, 
              progress: Math.floor(progress), 
              runtime: `${Math.floor(runtime / 60)}m ${runtime % 60}s`
            }
          : exp
      ));
      
      // Schedule next update in 2-5 seconds
      const nextUpdateIn = 2000 + Math.random() * 3000;
      console.log(`⏰ Next update for experiment ${experimentId} in ${Math.floor(nextUpdateIn/1000)}s`);
      setTimeout(updateProgress, nextUpdateIn);
    };
    
    // Start the progress simulation after 1 second
    console.log('⏱️ Starting progress updates in 1 second...');
    setTimeout(updateProgress, 1000);
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
        {/* Status notification for running experiments */}
        {experiments.some(exp => exp.status === 'Running') && (
          <div className="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg className="w-5 h-5 text-blue-400 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-blue-800">
                  {experiments.filter(exp => exp.status === 'Running').length} experiment(s) currently running
                </p>
                <p className="text-sm text-blue-600">
                  Progress updates will appear automatically in the experiments list below.
                </p>
              </div>
            </div>
          </div>
        )}
        
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
                  <div className="flex items-center space-x-4">
                    <div className="text-sm text-gray-600">{filteredExperiments.length} experiments</div>
                    <div className="text-xs text-blue-600">Total: {experiments.length}</div>
                    <button 
                      onClick={() => window.location.reload()} 
                      className="text-xs text-gray-500 hover:text-gray-700 underline"
                      title="Refresh page"
                    >
                      🔄 Refresh
                    </button>
                  </div>
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
                          {experiment.status === 'Completed' && experiment.results ? (
                            <button 
                              onClick={() => {
                                setSelectedExperiment(experiment);
                                setShowResults(true);
                              }}
                              className="text-blue-600 hover:text-blue-800 mr-3 font-semibold"
                            >
                              📊 View Results
                            </button>
                          ) : (
                            <button className="text-gray-400 mr-3 cursor-not-allowed">View</button>
                          )}
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

        {/* Results Modal */}
        {showResults && selectedExperiment && selectedExperiment.results && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b border-gray-200">
                <div className="flex justify-between items-center">
                  <h2 className="text-2xl font-bold text-gray-900">Optimization Results</h2>
                  <button 
                    onClick={() => setShowResults(false)}
                    className="text-gray-500 hover:text-gray-700 text-2xl"
                  >
                    ×
                  </button>
                </div>
                <p className="text-gray-600 mt-1">{selectedExperiment.name}</p>
              </div>

              <div className="p-6 space-y-8">
                {/* Best Parameters */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">🎯 Best Hyperparameters</h3>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="grid grid-cols-2 gap-4">
                      {Object.entries(selectedExperiment.results.bestParams).map(([key, value]) => (
                        <div key={key} className="flex justify-between">
                          <span className="font-medium text-gray-700">{key}:</span>
                          <span className="text-gray-900 font-mono">{value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Performance Metrics */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">📈 Performance Metrics</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-blue-50 rounded-lg p-4 text-center">
                      <div className="text-2xl font-bold text-blue-600">
                        {(selectedExperiment.results.metrics.accuracy * 100).toFixed(1)}%
                      </div>
                      <div className="text-sm text-blue-600">Accuracy</div>
                    </div>
                    <div className="bg-green-50 rounded-lg p-4 text-center">
                      <div className="text-2xl font-bold text-green-600">
                        {(selectedExperiment.results.metrics.precision * 100).toFixed(1)}%
                      </div>
                      <div className="text-sm text-green-600">Precision</div>
                    </div>
                    <div className="bg-purple-50 rounded-lg p-4 text-center">
                      <div className="text-2xl font-bold text-purple-600">
                        {(selectedExperiment.results.metrics.recall * 100).toFixed(1)}%
                      </div>
                      <div className="text-sm text-purple-600">Recall</div>
                    </div>
                    <div className="bg-orange-50 rounded-lg p-4 text-center">
                      <div className="text-2xl font-bold text-orange-600">
                        {(selectedExperiment.results.metrics.f1Score * 100).toFixed(1)}%
                      </div>
                      <div className="text-sm text-orange-600">F1 Score</div>
                    </div>
                  </div>
                </div>

                {/* Cross Validation */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">🔄 Cross-Validation Results</h3>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="grid grid-cols-3 gap-4 mb-4">
                      <div className="text-center">
                        <div className="text-xl font-bold text-gray-900">
                          {(selectedExperiment.results.crossValidation.mean * 100).toFixed(1)}%
                        </div>
                        <div className="text-sm text-gray-600">Mean Score</div>
                      </div>
                      <div className="text-center">
                        <div className="text-xl font-bold text-gray-900">
                          ±{(selectedExperiment.results.crossValidation.std * 100).toFixed(2)}%
                        </div>
                        <div className="text-sm text-gray-600">Std Deviation</div>
                      </div>
                      <div className="text-center">
                        <div className="text-xl font-bold text-gray-900">
                          {selectedExperiment.results.trialCount}
                        </div>
                        <div className="text-sm text-gray-600">Trials</div>
                      </div>
                    </div>
                    <div>
                      <div className="text-sm font-medium text-gray-700 mb-2">Individual Fold Scores:</div>
                      <div className="flex space-x-2">
                        {selectedExperiment.results.crossValidation.scores.map((score, idx) => (
                          <span key={idx} className="bg-white px-3 py-1 rounded text-sm font-mono">
                            {(score * 100).toFixed(1)}%
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Experiment Summary */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">📋 Experiment Summary</h3>
                  <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Runtime:</span>
                      <span className="font-medium">{selectedExperiment.runtime}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Status:</span>
                      <span className="font-medium text-green-600">{selectedExperiment.status}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Best Score:</span>
                      <span className="font-medium">{(selectedExperiment.results.bestScore * 100).toFixed(2)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Created:</span>
                      <span className="font-medium">{selectedExperiment.created}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="p-6 border-t border-gray-200 bg-gray-50">
                <div className="flex justify-between items-center">
                  <div className="text-sm text-gray-600">
                    💡 <strong>Tip:</strong> Download the optimized model to use in your projects
                  </div>
                  <div className="flex space-x-3">
                    <button 
                      onClick={() => setShowResults(false)}
                      className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                    >
                      Close
                    </button>
                    <button 
                      className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 flex items-center"
                      onClick={() => downloadOptimizedModel(selectedExperiment)}
                    >
                      🐍 Download Model (.py)
                    </button>
                    <button 
                      className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                      onClick={() => {
                        const resultsJson = JSON.stringify(selectedExperiment.results, null, 2);
                        const blob = new Blob([resultsJson], { type: 'application/json' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `optimization_results_${selectedExperiment.id}.json`;
                        a.click();
                        URL.revokeObjectURL(url);
                      }}
                    >
                      📄 Export Results (.json)
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}