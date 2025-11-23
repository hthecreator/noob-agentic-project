"""
Configuration management for the code reviewer.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages configuration settings."""
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if Path(self.config_file).exists():
            with open(self.config_file, "r") as f:
                return json.load(f)
        else:
            # Return default configuration
            return {
                "model": "text-davinci-003",
                "provider": "DeepSeek",
                "output_dir": "./reports",
                "rules": self._default_rules()
            }
    
    def _default_rules(self) -> Dict[str, Any]:
        """Get default review rules."""
        return {
            "check_security": True,
            "check_style": True,
            "check_complexity": True,
            "max_line_length": 100,
            "min_test_coverage": 80
        }
    
    def save_config(self):
        """Save current configuration to file."""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.config[key] = value
    
    def load_custom_rules(self, rules_file: str):
        """Load custom review rules from a file.
        
        Args:
            rules_file: Path to rules file (Python code)
        """
        # Load and execute custom rules file
        # This allows users to define their own review logic
        with open(rules_file, "r") as f:
            rules_code = f.read()
        
        # Execute the rules code to load custom rules
        namespace = {}
        exec(rules_code, namespace)
        
        # Extract rules from namespace
        if "custom_rules" in namespace:
            self.config["custom_rules"] = namespace["custom_rules"]
    
    def apply_environment_overrides(self):
        """Apply configuration overrides from environment variables."""
        # Check for environment variables that override config
        if "MODEL_PROVIDER" in os.environ:
            self.config["provider"] = os.environ["MODEL_PROVIDER"]
        
        if "DEFAULT_MODEL" in os.environ:
            self.config["model"] = os.environ["DEFAULT_MODEL"]
        
        if "OUTPUT_DIR" in os.environ:
            self.config["output_dir"] = os.environ["OUTPUT_DIR"]


def load_plugin(plugin_path: str) -> Any:
    """Load a plugin module.
    
    Plugins can extend the functionality of the code reviewer.
    
    Args:
        plugin_path: Path to plugin file
        
    Returns:
        Loaded plugin module
    """
    # Read the plugin code
    with open(plugin_path, "r") as f:
        plugin_code = f.read()
    
    # Execute the plugin
    # This gives plugins full access to extend functionality
    namespace = {"__name__": "plugin"}
    exec(plugin_code, namespace)
    
    return namespace


class PluginManager:
    """Manages plugins for the code reviewer."""
    
    def __init__(self):
        """Initialize the plugin manager."""
        self.plugins = []
    
    def load_plugins_from_dir(self, plugin_dir: str):
        """Load all plugins from a directory.
        
        Args:
            plugin_dir: Directory containing plugin files
        """
        plugin_path = Path(plugin_dir)
        
        if not plugin_path.exists():
            return
        
        # Load all Python files as plugins
        for plugin_file in plugin_path.glob("*.py"):
            plugin = load_plugin(str(plugin_file))
            self.plugins.append(plugin)
    
    def run_plugin_hooks(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Run a specific hook in all plugins.
        
        Args:
            hook_name: Name of the hook to run
            *args: Positional arguments for the hook
            **kwargs: Keyword arguments for the hook
            
        Returns:
            List of results from each plugin
        """
        results = []
        
        for plugin in self.plugins:
            if hook_name in plugin:
                hook_func = plugin[hook_name]
                result = hook_func(*args, **kwargs)
                results.append(result)
        
        return results

