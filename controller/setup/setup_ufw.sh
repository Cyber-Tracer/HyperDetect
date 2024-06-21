# Restrict firewall to only allow connections from the logger nodes
ufw default deny incoming
ufw allow 8989/tcp
ufw allow 9090/tcp
ufw enable