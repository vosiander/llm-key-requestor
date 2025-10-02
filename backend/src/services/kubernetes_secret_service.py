"""Kubernetes Secret Service for managing key request state."""
import base64
from loguru import logger
import uuid
from datetime import datetime
from typing import Optional

from kubernetes import client, config
from kubernetes.client import V1Secret, V1ObjectMeta, ApiException

from src.models.key_request import KeyRequestData, KeyRequestState

class KubernetesSecretService:
    """Service for managing key request secrets in Kubernetes."""
    
    def __init__(self, namespace: Optional[str] = None):
        """
        Initialize Kubernetes client and set namespace.
        
        Args:
            namespace: Kubernetes namespace to use. If None, uses current namespace.
        """
        try:
            # Try to load in-cluster config first (when running in k8s)
            config.load_incluster_config()
            logger.info("Loaded in-cluster Kubernetes configuration")
        except config.ConfigException:
            # Fall back to kubeconfig (for local development)
            config.load_kube_config()
            logger.info("Loaded Kubernetes configuration from kubeconfig")
        
        self.core_v1 = client.CoreV1Api()
        
        # Determine namespace
        if namespace:
            self.namespace = namespace
        else:
            # Try to get current namespace from service account
            try:
                with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as f:
                    self.namespace = f.read().strip()
                logger.info(f"Using namespace from service account: {self.namespace}")
            except FileNotFoundError:
                # Default to 'default' namespace if not in cluster
                self.namespace = 'default'
                logger.info(f"Using default namespace: {self.namespace}")
        
        logger.info(f"KubernetesSecretService initialized with namespace: {self.namespace}")
    
    def _generate_secret_name(self, request_id: str) -> str:
        """Generate secret name from request ID."""
        return f"llm-key-request-{request_id}"
    
    def _secret_to_request_data(self, secret: V1Secret) -> KeyRequestData:
        """
        Convert Kubernetes secret to KeyRequestData model.
        
        Args:
            secret: Kubernetes V1Secret object
            
        Returns:
            KeyRequestData model
        """
        # Decode base64 data
        data = {}
        if secret.data:
            for key, value in secret.data.items():
                data[key] = base64.b64decode(value).decode('utf-8')
        
        # Parse dates from annotations
        annotations = secret.metadata.annotations or {}
        
        return KeyRequestData(
            request_id=data.get('request_id', ''),
            email=data.get('email', ''),
            model=data.get('model', ''),
            state=KeyRequestState(data.get('state', KeyRequestState.PENDING)),
            created_at=datetime.fromisoformat(annotations.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(annotations.get('updated_at', datetime.now().isoformat())),
            api_key=data.get('api_key') if 'api_key' in data else None
        )
    
    def _request_data_to_secret(self, data: KeyRequestData) -> V1Secret:
        """
        Convert KeyRequestData to Kubernetes secret.
        
        Args:
            data: KeyRequestData model
            
        Returns:
            Kubernetes V1Secret object
        """
        # Prepare data fields (will be base64 encoded automatically)
        secret_data = {
            'request_id': data.request_id,
            'email': data.email,
            'model': data.model,
            'state': data.state.value,
        }
        
        if data.api_key:
            secret_data['api_key'] = data.api_key
        
        # Prepare annotations for metadata
        annotations = {
            'app.kubernetes.io/component': 'llm-key-request',
            'email': data.email,
            'state': data.state.value,
            'created_at': data.created_at.isoformat(),
            'updated_at': data.updated_at.isoformat(),
        }
        
        # Prepare labels
        labels = {
            'app.kubernetes.io/name': 'llm-key-requestor',
            'app.kubernetes.io/component': 'llm-key-request',
            'request-state': data.state.value,
        }
        
        return V1Secret(
            metadata=V1ObjectMeta(
                name=self._generate_secret_name(data.request_id),
                namespace=self.namespace,
                labels=labels,
                annotations=annotations
            ),
            string_data=secret_data,  # Use string_data for automatic base64 encoding
            type='Opaque'
        )
    
    async def find(self, request_id: str) -> Optional[KeyRequestData]:
        """
        Find secret by request ID.
        
        Args:
            request_id: Unique request identifier
            
        Returns:
            KeyRequestData if found, None otherwise
        """
        try:
            secret_name = self._generate_secret_name(request_id)
            secret = self.core_v1.read_namespaced_secret(secret_name, self.namespace)
            return self._secret_to_request_data(secret)
        except ApiException as e:
            if e.status == 404:
                logger.debug(f"Secret not found for request_id: {request_id}")
                return None
            logger.error(f"Error finding secret for request_id {request_id}: {e}")
            raise
    
    async def find_by_email(self, email: str) -> Optional[KeyRequestData]:
        """
        Find secret by email address.
        
        Args:
            email: User email address
            
        Returns:
            KeyRequestData if found, None otherwise
        """
        try:
            # List secrets with component label and filter by email annotation
            label_selector = 'app.kubernetes.io/component=llm-key-request'
            secrets = self.core_v1.list_namespaced_secret(
                self.namespace,
                label_selector=label_selector
            )
            
            # Filter by email annotation
            for secret in secrets.items:
                annotations = secret.metadata.annotations or {}
                if annotations.get('email') == email:
                    return self._secret_to_request_data(secret)
            
            logger.debug(f"No secret found for email: {email}")
            return None
            
        except ApiException as e:
            logger.error(f"Error finding secret by email {email}: {e}")
            raise
    
    async def find_by_status(self, state: KeyRequestState) -> list[KeyRequestData]:
        """
        Find all secrets with given state.
        
        Args:
            state: Key request state to filter by
            
        Returns:
            List of KeyRequestData objects
        """
        try:
            # Use label selector to filter by state
            label_selector = f'app.kubernetes.io/component=llm-key-request,request-state={state.value}'
            secrets = self.core_v1.list_namespaced_secret(
                self.namespace,
                label_selector=label_selector
            )
            
            results = []
            for secret in secrets.items:
                try:
                    results.append(self._secret_to_request_data(secret))
                except Exception as e:
                    logger.error(f"Error parsing secret {secret.metadata.name}: {e}")
                    continue
            
            logger.trace(f"Found {len(results)} secrets with state {state.value}")
            return results
            
        except ApiException as e:
            logger.error(f"Error finding secrets by status {state.value}: {e}")
            raise
    
    async def create(self, email: str, model: str) -> KeyRequestData:
        """
        Create new key request secret with pending state.
        
        Args:
            email: User email address
            model: LLM model identifier
            
        Returns:
            Created KeyRequestData
        """
        now = datetime.utcnow()
        request_id = str(uuid.uuid4())
        
        data = KeyRequestData(
            request_id=request_id,
            email=email,
            model=model,
            state=KeyRequestState.PENDING,
            created_at=now,
            updated_at=now,
            api_key=None
        )
        
        try:
            secret = self._request_data_to_secret(data)
            created_secret = self.core_v1.create_namespaced_secret(
                self.namespace,
                secret
            )
            logger.info(f"Created key request secret for email {email}, request_id {request_id}")
            return self._secret_to_request_data(created_secret)
            
        except ApiException as e:
            logger.error(f"Error creating secret for email {email}: {e}")
            raise
    
    async def update(self, request_id: str, **kwargs) -> KeyRequestData:
        """
        Update secret fields (state, api_key, etc.).
        
        Args:
            request_id: Request identifier
            **kwargs: Fields to update (state, api_key, etc.)
            
        Returns:
            Updated KeyRequestData
        """
        try:
            # Get existing secret
            secret_name = self._generate_secret_name(request_id)
            secret = self.core_v1.read_namespaced_secret(secret_name, self.namespace)
            
            # Convert to data model
            data = self._secret_to_request_data(secret)
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(data, key):
                    setattr(data, key, value)
            
            # Update timestamp
            data.updated_at = datetime.utcnow()
            
            # Convert back to secret
            updated_secret = self._request_data_to_secret(data)
            
            # Replace the secret
            self.core_v1.replace_namespaced_secret(
                secret_name,
                self.namespace,
                updated_secret
            )
            
            logger.info(f"Updated secret for request_id {request_id}")
            return data
            
        except ApiException as e:
            logger.error(f"Error updating secret for request_id {request_id}: {e}")
            raise
    
    async def delete(self, request_id: str) -> bool:
        """
        Delete a key request secret.
        
        Args:
            request_id: Request identifier
            
        Returns:
            True if deleted successfully
        """
        try:
            secret_name = self._generate_secret_name(request_id)
            self.core_v1.delete_namespaced_secret(secret_name, self.namespace)
            logger.info(f"Deleted secret for request_id {request_id}")
            return True
            
        except ApiException as e:
            if e.status == 404:
                logger.warning(f"Secret not found for deletion: {request_id}")
                return False
            logger.error(f"Error deleting secret for request_id {request_id}: {e}")
            raise
