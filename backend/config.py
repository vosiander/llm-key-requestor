"""Configuration management for LLM Key Requestor."""

import logging
import os
from pathlib import Path
from typing import Optional

import requests
import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from injector import Injector, Module, provider

from src.models.key_request import EmailConfig
from src.services.approval_plugins.base import ApprovalPlugin
from src.services.email_service import EmailService
import importlib

logger = logging.getLogger(__name__)


class ConfigModule(Module):
    """Injector module for providing configured services."""
    
    def __init__(self, config_manager):
        """
        Initialize the config module.
        
        Args:
            config_manager: ConfigManager instance to get configuration from
        """
        self.config_manager = config_manager
    
    @provider
    def provide_email_service(self) -> EmailService:
        """
        Provide configured EmailService instance.
        
        Returns:
            EmailService configured with SMTP settings from config
        """
        return EmailService(config=self.config_manager.get_smtp_config())


class LLMModel(BaseModel):
    """Model representing an LLM provider configuration."""
    
    id: str
    title: str
    icon: str
    color: str
    description: str


class LiteLLMConfig(BaseModel):
    """LiteLLM backend configuration."""
    
    base_url: str = Field(default="http://localhost:4000")
    api_key: str = Field(default="")
    enable_litellm_models: bool = Field(default=True)


class Config(BaseSettings):
    """Application configuration with YAML file and environment variable support."""
    
    # LiteLLM configuration with environment variable overrides
    litellm_base_url: Optional[str] = Field(
        default=None,
        alias="LITELLM_BASE_URL",
        description="LiteLLM backend base URL"
    )
    litellm_api_key: Optional[str] = Field(
        default=None,
        alias="LITELLM_API_KEY",
        description="LiteLLM backend API key"
    )
    enable_litellm_models: Optional[bool] = Field(
        default=None,
        alias="ENABLE_LITELLM_MODELS",
        description="Enable fetching models from LiteLLM"
    )
    
    # Path to config file
    config_file: str = Field(
        default="config.yaml",
        alias="CONFIG_FILE",
        description="Path to YAML configuration file"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class ConfigManager:
    """Manages application configuration from YAML file with environment overrides."""
    
    def __init__(self):
        self.settings = Config()
        self._config_data = None
        self._load_config()
        
        # Set up dependency injection
        self.injector = Injector([ConfigModule(self)])
    
    def _load_config(self):
        """Load configuration from YAML file."""
        config_path = Path(self.settings.config_file)
        
        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path.absolute()}"
            )
        
        with open(config_path, 'r') as f:
            self._config_data = yaml.safe_load(f)
    
    def get_litellm_config(self) -> LiteLLMConfig:
        """
        Get LiteLLM configuration with environment variable overrides.
        
        Environment variables take precedence over YAML values.
        """
        yaml_config = self._config_data.get('litellm', {})
        
        return LiteLLMConfig(
            base_url=self.settings.litellm_base_url or yaml_config.get('base_url', 'http://localhost:4000'),
            api_key=self.settings.litellm_api_key or yaml_config.get('api_key', ''),
            enable_litellm_models=self.settings.enable_litellm_models if self.settings.enable_litellm_models is not None else yaml_config.get('enable_litellm_models', True)
        )
    
    def get_models(self) -> list[LLMModel]:
        """Get list of available LLM models from configuration."""
        models_data = self._config_data.get('models', [])
        return [LLMModel(**model) for model in models_data]
    
    def fetch_litellm_models(self) -> list[LLMModel]:
        """
        Fetch available models from LiteLLM backend.
        
        Returns:
            List of LLMModel objects fetched from LiteLLM, or empty list on error.
        """
        litellm_config = self.get_litellm_config()
        
        if not litellm_config.enable_litellm_models:
            logger.info("LiteLLM models fetching is disabled")
            return []
        
        try:
            # LiteLLM follows OpenAI API format with /v1/models endpoint
            url = f"{litellm_config.base_url.rstrip('/')}/v1/models"
            headers = {}
            
            if litellm_config.api_key:
                headers["Authorization"] = f"Bearer {litellm_config.api_key}"
            
            response = requests.get(url, headers=headers, timeout=10.0)
            response.raise_for_status()
            
            data = response.json()
            models = []
            
            # LiteLLM returns models in OpenAI format: {"data": [{"id": "model-name", ...}, ...]}
            for model_data in data.get("data", []):
                model_id = model_data.get("id", "")
                if model_id:
                    # Create LLMModel with default metadata for litellm models
                    models.append(LLMModel(
                        id=model_id,
                        title=model_id.replace("-", " ").title(),
                        icon="mdi:robot",
                        color="#6366f1",
                        description=f"Model from LiteLLM: {model_id}"
                    ))
            
            logger.info(f"Successfully fetched {len(models)} models from LiteLLM")
            return models
                
        except requests.HTTPError as e:
            logger.error(f"HTTP error fetching models from LiteLLM: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching models from LiteLLM: {e}")
            return []
    
    def get_all_models(self) -> list[LLMModel]:
        """
        Get merged list of local and LiteLLM models.
        
        Returns:
            Combined list of models, with local models taking precedence for duplicates.
        """
        # Get local models from config
        local_models = self.get_models()
        
        # Get LiteLLM models if enabled
        litellm_models = self.fetch_litellm_models()
        
        # Create a dictionary to track models by ID (local models take precedence)
        models_dict = {}
        
        # Add LiteLLM models first
        for model in litellm_models:
            models_dict[model.id] = model
        
        # Add local models (will override litellm models with same ID)
        for model in local_models:
            models_dict[model.id] = model
        
        # Return merged list
        merged_models = list(models_dict.values())
        logger.info(f"Returning {len(merged_models)} total models ({len(local_models)} local, {len(litellm_models)} from LiteLLM)")
        
        return merged_models
    
    def get_smtp_config(self) -> EmailConfig:
        """
        Get SMTP configuration with environment variable overrides.
        
        Environment variables take precedence over YAML values.
        """
        yaml_smtp = self._config_data.get('smtp', {})
        
        return EmailConfig(
            smtp_host=os.getenv('SMTP_HOST', yaml_smtp.get('host', 'localhost')),
            smtp_port=os.getenv('SMTP_PORT', yaml_smtp.get('port', 587)),
            smtp_user=os.getenv('SMTP_USER', yaml_smtp.get('user', '')),
            smtp_password=os.getenv('SMTP_PASSWORD', yaml_smtp.get('password', '')),
            smtp_from=os.getenv('SMTP_FROM', yaml_smtp.get('from', 'noreply@example.com')),
            smtp_use_tls=os.getenv('SMTP_USE_TLS', str(yaml_smtp.get('use_tls', True))).lower() in ('true', '1', 'yes')
        )
    
    def get_queue_interval(self) -> str:
        """
        Get approval queue interval with environment variable override.
        
        Returns interval string (e.g., '30s', '1m').
        """
        yaml_approval = self._config_data.get('approval', {})
        return os.getenv('APPROVAL_QUEUE_INTERVAL', yaml_approval.get('queue_interval', '30s'))
    
    def get_kubernetes_namespace(self) -> Optional[str]:
        """
        Get Kubernetes namespace with environment variable override.
        
        Returns None to use current namespace, or specific namespace string.
        """
        yaml_k8s = self._config_data.get('kubernetes', {})
        namespace = os.getenv('KUBERNETES_NAMESPACE', yaml_k8s.get('namespace', ''))
        return namespace if namespace else None
    
    def get_approval_plugins(self) -> list[ApprovalPlugin]:
        """
        Get list of configured approval plugins using dynamic loading.
        
        Plugins are loaded dynamically from configuration based on plugin name.
        Each plugin must follow the naming convention:
        - Module: src.services.approval_plugins.{name}_plugin
        - Class: {Name}ApprovalPlugin (with capitalized first letter)
        
        Returns:
            List of ApprovalPlugin instances configured in YAML.
            Returns empty list if no plugins configured.
        """
        plugins_config = self._config_data.get('approval_plugins', [])
        
        if not plugins_config:
            logger.warning("No approval plugins configured - all requests will be denied by default")
            return []
        
        plugins = []
        for plugin_def in plugins_config:
            try:
                plugin_name = plugin_def.get('name')
                plugin_config = plugin_def.get('config', {})
                
                if not plugin_name:
                    logger.error(f"Plugin definition missing 'name' field: {plugin_def}")
                    continue
                
                # Dynamically load plugin
                plugin = self._load_plugin(plugin_name, plugin_config)
                plugins.append(plugin)
                logger.info(f"Loaded plugin: {plugin.__class__.__name__}")
                
            except Exception as e:
                logger.error(f"Failed to load approval plugin from config {plugin_def}: {e}", exc_info=True)
        
        logger.info(f"Loaded {len(plugins)} approval plugins")
        return plugins
    
    def _load_plugin(self, plugin_name: str, plugin_config: dict) -> ApprovalPlugin:
        """
        Dynamically load and instantiate a plugin by name with dependency injection.
        
        Args:
            plugin_name: Name of the plugin (e.g., 'http', 'blacklist')
            plugin_config: Configuration dictionary for the plugin
            
        Returns:
            ApprovalPlugin instance
            
        Raises:
            ImportError: If plugin module cannot be imported
            AttributeError: If plugin class cannot be found
            Exception: If plugin instantiation fails
        """
        # Convert plugin name to module name: 'http' -> 'http_plugin'
        module_name = f'src.services.approval_plugins.{plugin_name}_plugin'
        
        # Convert plugin name to class name: 'http' -> 'HttpApprovalPlugin'
        class_name = f'{plugin_name.capitalize()}ApprovalPlugin'
        
        try:
            # Dynamically import the module
            module = importlib.import_module(module_name)
            
            # Get the plugin class from the module
            plugin_class = getattr(module, class_name)
            
            # Create plugin instance with dependency injection
            # This handles @inject decorated dependencies
            plugin = self.injector.create_object(plugin_class)
            
            # Set configuration parameters from YAML on the plugin instance
            for key, value in plugin_config.items():
                setattr(plugin, key, value)
            
            return plugin
            
        except ImportError as e:
            raise ImportError(
                f"Failed to import plugin module '{module_name}'. "
                f"Ensure the plugin file exists at src/services/approval_plugins/{plugin_name}_plugin.py"
            ) from e
        except AttributeError as e:
            raise AttributeError(
                f"Plugin class '{class_name}' not found in module '{module_name}'. "
                f"Ensure the class is named correctly."
            ) from e
        except Exception as e:
            raise Exception(
                f"Failed to instantiate plugin '{class_name}' with config {plugin_config}. "
                f"Error: {str(e)}"
            ) from e


# Global config manager instance
config_manager = ConfigManager()
