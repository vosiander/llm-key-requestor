"""Configuration management for LLM Key Requestor."""

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


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
            api_key=self.settings.litellm_api_key or yaml_config.get('api_key', '')
        )
    
    def get_models(self) -> list[LLMModel]:
        """Get list of available LLM models from configuration."""
        models_data = self._config_data.get('models', [])
        return [LLMModel(**model) for model in models_data]


# Global config manager instance
config_manager = ConfigManager()
