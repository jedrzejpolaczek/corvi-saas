import requests
import pandas as pd
from typing import Optional, Dict, Any, List
import json

class CorviClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.access_token: Optional[str] = None
        
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login and store access token"""
        response = self.session.post(
            f"{self.base_url}/api/auth/token",
            json={"email": email, "password": password}
        )
        response.raise_for_status()
        
        data = response.json()
        self.access_token = data["access_token"]
        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
        return data
    
    def register(self, email: str, password: str, org_name: str) -> Dict[str, Any]:
        """Register new user and store access token"""
        response = self.session.post(
            f"{self.base_url}/api/auth/register",
            json={"email": email, "password": password, "org_name": org_name}
        )
        response.raise_for_status()
        
        data = response.json()
        self.access_token = data["access_token"]
        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
        return data
    
    def create_project(self, name: str, description: str = "") -> Dict[str, Any]:
        """Create a new project"""
        response = self.session.post(
            f"{self.base_url}/api/projects",
            json={"name": name, "description": description}
        )
        response.raise_for_status()
        return response.json()
    
    def upload_dataset(self, name: str, data: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        """Upload dataset"""
        # Convert DataFrame to CSV string
        csv_data = data.to_csv(index=False)
        
        # For now, we'll simulate upload - in real implementation, this would upload to S3/MinIO
        dataset_info = {
            "name": name,
            "target_column": target_column,
            "rows": len(data),
            "columns": list(data.columns),
            "size_bytes": len(csv_data.encode())
        }
        
        response = self.session.post(
            f"{self.base_url}/api/datasets",
            json=dataset_info
        )
        response.raise_for_status()
        return response.json()
    
    def create_experiment(self, 
                         name: str, 
                         dataset_id: int, 
                         algorithm: str,
                         model_type: str,
                         hyperparameters: Dict[str, Any],
                         trials: int = 50,
                         objective: str = "maximize") -> Dict[str, Any]:
        """Create and start experiment"""
        experiment_data = {
            "name": name,
            "dataset_id": dataset_id,
            "algorithm": algorithm,
            "model_type": model_type,
            "hyperparameters": hyperparameters,
            "trials": trials,
            "objective": objective
        }
        
        response = self.session.post(
            f"{self.base_url}/api/experiments",
            json=experiment_data
        )
        response.raise_for_status()
        return response.json()
    
    def get_experiment(self, experiment_id: int) -> Dict[str, Any]:
        """Get experiment details"""
        response = self.session.get(f"{self.base_url}/api/experiments/{experiment_id}")
        response.raise_for_status()
        return response.json()
    
    def list_experiments(self) -> List[Dict[str, Any]]:
        """List all experiments"""
        response = self.session.get(f"{self.base_url}/api/experiments")
        response.raise_for_status()
        return response.json()
