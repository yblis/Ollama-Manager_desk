import requests
from typing import List, Dict, Optional

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
        """Get list of running model instances using tags endpoint."""
        try:
            response = requests.get(f"{OllamaAPI.BASE_URL}/tags")
            response.raise_for_status()
            models = response.json().get('models', [])
            # Filter and transform the model data
            running_instances = []
            for model in models:
                running_instances.append({
                    'instance_id': model['digest'][:8],  # Use first 8 chars of digest as ID
                    'model': model['name'],
                    'started': model['modified_at']
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
