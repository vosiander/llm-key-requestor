"""Email Service for sending notifications."""
from loguru import logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import aiosmtplib

from src.models.key_request import EmailConfig

class EmailService:
    """Service for handling SMTP email notifications."""
    
    def __init__(self, config: EmailConfig):
        """
        Initialize email service with SMTP configuration.
        
        Args:
            config: EmailConfig with SMTP settings
        """
        self.config = config
        logger.info(f"EmailService initialized with SMTP host {config.smtp_host}:{config.smtp_port}")
    
    def _create_approval_email(self, email: str, model: str, api_key: str, gateway_url: str) -> MIMEMultipart:
        """
        Create approval email message.
        
        Args:
            email: Recipient email address
            model: LLM model identifier
            api_key: Generated API key
            gateway_url: Gateway base URL for API access
            
        Returns:
            MIMEMultipart email message
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'API Key Approved for {model}'
        msg['From'] = self.config.smtp_from
        msg['To'] = email
        
        # Plain text version
        text_content = f"""
Your API key request has been approved!

Model: {model}
API Key: {api_key}
Gateway URL: {gateway_url}

Please keep your API key secure and do not share it with others.

Thank you for using our service!
"""
        
        # HTML version
        html_content = f"""
<html>
  <head></head>
  <body>
    <h2>API Key Request Approved</h2>
    <p>Your API key request has been approved!</p>
    
    <table style="border-collapse: collapse; margin: 20px 0;">
      <tr>
        <td style="padding: 8px; font-weight: bold;">Model:</td>
        <td style="padding: 8px;">{model}</td>
      </tr>
      <tr>
        <td style="padding: 8px; font-weight: bold;">API Key:</td>
        <td style="padding: 8px; font-family: monospace; background-color: #f5f5f5;">{api_key}</td>
      </tr>
      <tr>
        <td style="padding: 8px; font-weight: bold;">Gateway URL:</td>
        <td style="padding: 8px; font-family: monospace; background-color: #f5f5f5;">{gateway_url}</td>
      </tr>
    </table>
    
    <p><strong>Important:</strong> Please keep your API key secure and do not share it with others.</p>
    
    <p>Thank you for using our service!</p>
  </body>
</html>
"""
        
        # Attach both versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        return msg
    
    def _create_denial_email(self, email: str, model: str, reason: str) -> MIMEMultipart:
        """
        Create denial email message.
        
        Args:
            email: Recipient email address
            model: LLM model identifier
            reason: Reason for denial
            
        Returns:
            MIMEMultipart email message
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'API Key Request Denied for {model}'
        msg['From'] = self.config.smtp_from
        msg['To'] = email
        
        # Plain text version
        text_content = f"""
Your API key request has been denied.

Model: {model}
Reason: {reason}

If you believe this is an error, please contact support.

Thank you for your understanding.
"""
        
        # HTML version
        html_content = f"""
<html>
  <head></head>
  <body>
    <h2>API Key Request Denied</h2>
    <p>Your API key request has been denied.</p>
    
    <table style="border-collapse: collapse; margin: 20px 0;">
      <tr>
        <td style="padding: 8px; font-weight: bold;">Model:</td>
        <td style="padding: 8px;">{model}</td>
      </tr>
      <tr>
        <td style="padding: 8px; font-weight: bold;">Reason:</td>
        <td style="padding: 8px;">{reason}</td>
      </tr>
    </table>
    
    <p>If you believe this is an error, please contact support.</p>
    
    <p>Thank you for your understanding.</p>
  </body>
</html>
"""
        
        # Attach both versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        return msg
    
    async def send_approval_notification(self, email: str, model: str, api_key: str, gateway_url: str) -> bool:
        """
        Send approval email with API key.
        
        Args:
            email: Recipient email address
            model: LLM model identifier
            api_key: Generated API key
            gateway_url: Gateway base URL for API access
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            msg = self._create_approval_email(email, model, api_key, gateway_url)
            
            # Configure SMTP
            smtp_kwargs = {
                'hostname': self.config.smtp_host,
                'port': self.config.smtp_port,
            }
            
            # Use STARTTLS for port 587, direct TLS for port 465
            if self.config.smtp_port == 587:
                smtp_kwargs['start_tls'] = True
            elif self.config.smtp_port == 465:
                smtp_kwargs['use_tls'] = True
            elif self.config.smtp_use_tls:
                # Fallback to config setting for other ports
                smtp_kwargs['use_tls'] = True
            
            # Add authentication if credentials provided
            if self.config.smtp_user and self.config.smtp_password:
                smtp_kwargs['username'] = self.config.smtp_user
                smtp_kwargs['password'] = self.config.smtp_password
            
            # Send email
            await aiosmtplib.send(
                msg,
                **smtp_kwargs
            )
            
            logger.info(f"Approval email sent to {email} for model {model}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send approval email to {email}: {e}")
            return False
    
    async def send_denial_notification(self, email: str, model: str, reason: str) -> bool:
        """
        Send denial notification email.
        
        Args:
            email: Recipient email address
            model: LLM model identifier
            reason: Reason for denial
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            msg = self._create_denial_email(email, model, reason)
            
            # Configure SMTP
            smtp_kwargs = {
                'hostname': self.config.smtp_host,
                'port': self.config.smtp_port,
            }
            
            # Use STARTTLS for port 587, direct TLS for port 465
            if self.config.smtp_port == 587:
                smtp_kwargs['start_tls'] = True
            elif self.config.smtp_port == 465:
                smtp_kwargs['use_tls'] = True
            elif self.config.smtp_use_tls:
                # Fallback to config setting for other ports
                smtp_kwargs['use_tls'] = True
            
            # Add authentication if credentials provided
            if self.config.smtp_user and self.config.smtp_password:
                smtp_kwargs['username'] = self.config.smtp_user
                smtp_kwargs['password'] = self.config.smtp_password
            
            # Send email
            await aiosmtplib.send(
                msg,
                **smtp_kwargs
            )
            
            logger.info(f"Denial email sent to {email} for model {model}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send denial email to {email}: {e}")
            return False
