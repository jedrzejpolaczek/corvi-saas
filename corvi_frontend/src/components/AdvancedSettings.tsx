import React, { useState } from 'react';

interface AdvancedSettingsProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (settings: AdvancedSettingsData) => void;
}

export interface AdvancedSettingsData {
  optimization_algorithm: string;
  max_trials: number;
  timeout: number;
  cross_validation_folds: number;
  test_size: number;
  random_state: number;
  scoring_metric: string;
  early_stopping: boolean;
  early_stopping_rounds: number;
}

export default function AdvancedSettings({ isOpen, onClose, onSave }: AdvancedSettingsProps) {
  const [settings, setSettings] = useState<AdvancedSettingsData>({
    optimization_algorithm: 'random_search',
    max_trials: 50,
    timeout: 3600,
    cross_validation_folds: 5,
    test_size: 0.2,
    random_state: 42,
    scoring_metric: 'accuracy',
    early_stopping: true,
    early_stopping_rounds: 10
  });

  const optimizationAlgorithms = [
    { value: 'random_search', label: 'Random Search' },
    { value: 'bayesian', label: 'Bayesian Optimization' },
    { value: 'grid_search', label: 'Grid Search' },
    { value: 'evolutionary', label: 'Evolutionary Algorithm' },
    { value: 'optuna', label: 'Optuna TPE' }
  ];

  const scoringMetrics = [
    { value: 'accuracy', label: 'Accuracy' },
    { value: 'f1', label: 'F1 Score' },
    { value: 'precision', label: 'Precision' },
    { value: 'recall', label: 'Recall' },
    { value: 'roc_auc', label: 'ROC AUC' },
    { value: 'r2', label: 'R² Score (Regression)' },
    { value: 'mse', label: 'Mean Squared Error' },
    { value: 'mae', label: 'Mean Absolute Error' }
  ];

  const handleInputChange = (field: keyof AdvancedSettingsData, value: any) => {
    setSettings(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSave = () => {
    onSave(settings);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">Advanced Settings</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <div className="px-6 py-4 space-y-6">
          {/* Optimization Algorithm */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Optimization Algorithm
            </label>
            <select
              value={settings.optimization_algorithm}
              onChange={(e) => handleInputChange('optimization_algorithm', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 text-gray-900 bg-white hover:border-green-400"
            >
              {optimizationAlgorithms.map(alg => (
                <option key={alg.value} value={alg.value}>{alg.label}</option>
              ))}
            </select>
          </div>

          {/* Max Trials */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Maximum Trials
            </label>
            <input
              type="number"
              min="1"
              max="1000"
              value={settings.max_trials}
              onChange={(e) => handleInputChange('max_trials', parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            />
          </div>

          {/* Timeout */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Timeout (seconds)
            </label>
            <input
              type="number"
              min="60"
              max="86400"
              value={settings.timeout}
              onChange={(e) => handleInputChange('timeout', parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            />
          </div>

          {/* Cross Validation Folds */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Cross Validation Folds
            </label>
            <input
              type="number"
              min="2"
              max="20"
              value={settings.cross_validation_folds}
              onChange={(e) => handleInputChange('cross_validation_folds', parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            />
          </div>

          {/* Test Size */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Test Size (0.1 - 0.5)
            </label>
            <input
              type="number"
              min="0.1"
              max="0.5"
              step="0.05"
              value={settings.test_size}
              onChange={(e) => handleInputChange('test_size', parseFloat(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            />
          </div>

          {/* Random State */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Random State
            </label>
            <input
              type="number"
              min="0"
              value={settings.random_state}
              onChange={(e) => handleInputChange('random_state', parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            />
          </div>

          {/* Scoring Metric */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Scoring Metric
            </label>
            <select
              value={settings.scoring_metric}
              onChange={(e) => handleInputChange('scoring_metric', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 text-gray-900 bg-white hover:border-green-400"
            >
              {scoringMetrics.map(metric => (
                <option key={metric.value} value={metric.value}>{metric.label}</option>
              ))}
            </select>
          </div>

          {/* Early Stopping */}
          <div>
            <div className="flex items-center">
              <input
                id="early-stopping"
                type="checkbox"
                checked={settings.early_stopping}
                onChange={(e) => handleInputChange('early_stopping', e.target.checked)}
                className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
              />
              <label htmlFor="early-stopping" className="ml-2 block text-sm text-gray-700">
                Enable Early Stopping
              </label>
            </div>
          </div>

          {/* Early Stopping Rounds */}
          {settings.early_stopping && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Early Stopping Rounds
              </label>
              <input
                type="number"
                min="1"
                max="50"
                value={settings.early_stopping_rounds}
                onChange={(e) => handleInputChange('early_stopping_rounds', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
              />
            </div>
          )}
        </div>

        <div className="px-6 py-4 border-t border-gray-200 flex justify-end space-x-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="px-4 py-2 text-white bg-green-500 hover:bg-green-600 rounded-md transition-colors"
          >
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
}