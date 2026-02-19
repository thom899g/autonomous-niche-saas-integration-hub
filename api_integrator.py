from typing import Any
import logging
from .api_connector import APIConnector

class APIIntegrator:
    """
    Class responsible for integrating various SaaS APIs into a cohesive solution.
    
    Attributes:
        connectors: Dictionary mapping connector names to their instances.
        logger: Logger instance for logging debug information and errors.
    """

    def __init__(self) -> None:
        self.connectors = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

    def add_connector(self, name: str, connector: APIConnector) -> None:
        """
        Adds a new API connector to the integrator.
        
        Args:
            name: Name under which the connector will be stored.
            connector: Instance of APIConnector to add.
        """
        self.connectors[name] = connector
        self.logger.info(f"Added connector {name}")

    def connect_apis(self, config: Dict) -> bool:
        """
        Connects multiple APIs based on the provided configuration.
        
        Args:
            config: Dictionary containing API connection details and integration logic.
            
        Returns:
            Boolean indicating whether the integration was successful.
        """
        try:
            self.logger.info("Starting API integration process")
            
            # Validate config
            if not self._validate_config(config):
                raise ValueError("Invalid configuration provided")

            # Connect each required service
            for service in config['services']:
                connector = self.connectors.get(service['name'])
                if not connector:
                    raise ValueError(f"Connector {service['name']} not found")
                
                self.logger.info(f"Connecting {service['name']}")
                connector.connect(**service['params'])

            return True
            
        except Exception as e:
            self.logger.error(f"API integration failed: {str(e)}")
            raise

    def _validate_config(self, config: Dict) -> bool:
        """
        Validates the configuration for API integration.
        
        Args:
            config: Dictionary