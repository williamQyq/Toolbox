# Toolbox
a tool box for multi purpose

## NFS

* `vi /etc/exports`

* `vi /etc/nfs.conf`:  
[nfsd]  
threads=8

`sudo systemctl restart nfs-kernel-server`

## Network IP

* `/etc/netplan`  
  `.yaml`

```yaml 
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      addresses:
        - 192.168.1.53/24
        - 192.168.120.254/24
      gateway4: 192.168.1.1
      nameservers:
          addresses: [8.8.8.8, 8.8.4.4]
      dhcp4: no
      dhcp6: no
      set-name: eth0
      mtu: 1500
      wakeonlan: true
      netmask: 255.255.255.0
      broadcast: 192.168.120.255
```

`netplan apply`

## Filesystem Table

* `/etc/fstab`

## DHCP Ubuntu

* `sudo apt-get install isc-dhcp-server`
* `vi /etc/dhcp/dhcpd.conf`