#!/bin/bash
set -e

# Certificate handling
# If custom certificates are mounted in /certs, add them to the system trust store
if [ -d "/certs" ] && [ "$(ls -A /certs)" ]; then
    echo "Custom certificates found in /certs. Adding to system trust store..."
    
    # Copy certificates to system CA directory
    for cert in /certs/*.crt /certs/*.pem; do
        if [ -f "$cert" ]; then
            echo "Adding certificate: $(basename "$cert")"
            cp "$cert" /usr/local/share/ca-certificates/
        fi
    done
    
    # Update CA certificates
    update-ca-certificates
    
    echo "Certificates updated successfully."
else
    echo "No custom certificates found in /certs. Using system defaults."
fi

# Execute the main command
exec "$@"
