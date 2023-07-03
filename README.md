# Toolbox
a tool box for multi purpose

## NFS

* `vi /etc/exports`

* `vi /etc/nfs.conf`:  
[nfsd]  
threads=8

`sudo systemctl restart nfs-kernel-server`

## Network IP

* `/etc/netplan/config.yaml`  

```yaml 
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      addresses:
        - 192.168.1.53/24
        - 192.168.120.254/24
      routes:
        - to: default
          via: 192.168.1.1
          metric: 100
        - to: default
          via: 192.168.120.254
          metric: 200
        - to: default
          via: 192.168.120.254
          metric: 300
          on-link: true
      gateway4: 192.168.1.1
      nameservers:
          addresses: [8.8.8.8, 8.8.4.4]
      dhcp4: false
      dhcp6: false
      mtu: 1500
```

`netplan apply`

## Filesystem Table

* `/etc/fstab`

192.168.120.4:/volume1/partimag /partimag nfs4 defaults 0 0

## DHCP Ubuntu

* `sudo apt-get install isc-dhcp-server`
* `vi /etc/dhcp/dhcpd.conf`