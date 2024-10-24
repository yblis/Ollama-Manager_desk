import requests
from typing import List, Dict, Optional
from datetime import datetime

class OllamaAPI:
    BASE_URL = "http://localhost:11434/api"
    
    @staticmethod
    def list_models() -> List[Dict]:
        """Get list of installed models."""
        try:
            response = requests.get(f"{OllamaAPI.BASE_URL}/tags")
            response.raise_for_status()
            return response.json().get('models', [])
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to fetch models: {str(e)}")

    @staticmethod
    def pull_model(model_name: str) -> bool:
        """Pull a new model."""
        try:
            response = requests.post(
                f"{OllamaAPI.BASE_URL}/pull",
                json={"name": model_name}
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to pull model: {str(e)}")

    @staticmethod
    def delete_model(model_name: str) -> bool:
        """Delete an installed model."""
        try:
            response = requests.delete(
                f"{OllamaAPI.BASE_URL}/delete",
                json={"name": model_name}
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to delete model: {str(e)}")

    @staticmethod
    def list_running() -> List[Dict]:
        """Get list of running model instances."""
        try:
            response = requests.get(f"{OllamaAPI.BASE_URL}/ps")
            response.raise_for_status()
            models = response.json().get('models', [])
            # Transform the model data
            running_instances = []
            for model in models:
                running_instances.append({
                    'instance_id': model['digest'][:8],
                    'model': model['name'],
                    'started': model.get('expires_at', datetime.now().isoformat()),
                    'size_vram': model.get('size_vram', 0)
                })
            return running_instances
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to fetch running instances: {str(e)}")

    @staticmethod
    def stop_instance(instance_id: str) -> bool:
        """Stop a running model instance."""
        try:
            response = requests.post(
                f"{OllamaAPI.BASE_URL}/stop",
                json={"instance_id": instance_id}
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to stop instance: {str(e)}")
