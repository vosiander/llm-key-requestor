"""HTTP approval plugin."""
import requests
from loguru import logger
from src.services.approval_plugins.base import ApprovalPlugin, ApprovalDecision


class HttpApprovalPlugin(ApprovalPlugin):
    """Approval plugin that queries an HTTP endpoint for approval decisions."""
    
    def __init__(self):
        """
        Initialize HTTP plugin.
        
        Note:
            Configuration parameters (endpoint, timeout) are set after instantiation
            via setattr by the ConfigManager.
        """
        self.endpoint = ""
        self.timeout = 5
        logger.info(f"HttpApprovalPlugin initialized")
    
    async def evaluate(self, email: str, model: str, request_id: str) -> ApprovalDecision:
        """
        Query HTTP endpoint for approval decision.
        
        Args:
            email: User email address
            model: LLM model identifier
            request_id: Request identifier
            
        Returns:
            APPROVE, DENY, or CONTINUE based on endpoint response.
            Returns CONTINUE on error or timeout.
        """
        payload = {
            "email": email,
            "model": model,
            "request_id": request_id
        }
        
        try:
            logger.debug(
                f"HttpApprovalPlugin: Sending POST request to {self.endpoint} "
                f"for request_id={request_id}"
            )
            
            response = requests.post(
                self.endpoint,
                json=payload,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            response_data = response.json()
            decision_str = response_data.get("decision", "").upper()
            
            # Validate decision
            if decision_str not in ["APPROVE", "DENY", "CONTINUE"]:
                logger.warning(
                    f"HttpApprovalPlugin: Invalid decision '{decision_str}' from endpoint "
                    f"for request_id={request_id}, returning CONTINUE"
                )
                return ApprovalDecision.CONTINUE
            
            decision = ApprovalDecision(decision_str)
            logger.info(
                f"HttpApprovalPlugin: {decision.value} - received from endpoint "
                f"for request_id={request_id}"
            )
            return decision
            
        except requests.exceptions.Timeout:
            logger.warning(
                f"HttpApprovalPlugin: Request timeout to {self.endpoint} "
                f"for request_id={request_id}, returning CONTINUE"
            )
            return ApprovalDecision.CONTINUE
            
        except requests.exceptions.RequestException as e:
            logger.warning(
                f"HttpApprovalPlugin: Request error to {self.endpoint} "
                f"for request_id={request_id}: {e}, returning CONTINUE"
            )
            return ApprovalDecision.CONTINUE
            
        except (ValueError, KeyError) as e:
            logger.warning(
                f"HttpApprovalPlugin: Failed to parse response from {self.endpoint} "
                f"for request_id={request_id}: {e}, returning CONTINUE"
            )
            return ApprovalDecision.CONTINUE
