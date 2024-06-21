# Configure network settings to match the environment and configuration of client
cp ./01-network-manager-all.yaml /etc/netplan/01-network-manager-all.yaml
netplan apply
