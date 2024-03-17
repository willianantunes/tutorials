# OpenVPN on Azure

To understand it, please read the article [OpenVPN Community on Azure with Terraform](https://www.willianantunes.com/blog/2024/03/openvpn-community-on-azure-with-terraform/).

## Prerequisites

- [Create a service principal on Azure](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/service_principal_client_secret).
- Configure the following environment variables in `docker-compose.yml` file:
  - ARM_CLIENT_ID
  - ARM_CLIENT_SECRET
  - ARM_TENANT_ID
  - ARM_SUBSCRIPTION_ID

## Running the Terraform code

Run the following command to start the container:

```shell
docker compose run --rm docker-client-tf-did bash
```

To create the infrastructure, run the following command:

```shell
terraform init
terraform apply
```

## Accessing the VPN server

Access the virtual machine through the serial console on Azure Portal using its user and the password output from `terraform output vm_password`. Then run the commands:

```shell
sudo systemctl restart openvpn
systemctl status openvpn
```

To manage your OpenVPN server, run the following command:

```shell
sudo ./openvpn-management.sh
```

## Private AKS cluster connection through the VPN

If you want to connect to the private AKS cluster, beyond generating the OVPN file, in case you are using Ubuntu 18, [you need to add the following lines to the OpenVPN configuration file](https://askubuntu.com/a/1036209/869618):

```
# INIT This updates the resolvconf with dns settings
script-security 2
up /etc/openvpn/update-resolv-conf
down /etc/openvpn/update-resolv-conf
# END OF This updates the resolvconf with dns settings
```

Create the file `/etc/openvpn/update-resolv-conf` with permission 755 with the following content:

```shell
#!/bin/bash
# 
# Parses DHCP options from openvpn to update resolv.conf
# To use set as 'up' and 'down' script in your openvpn *.conf:
# up /etc/openvpn/update-resolv-conf
# down /etc/openvpn/update-resolv-conf
#
# Used snippets of resolvconf script by Thomas Hood and Chris Hanson.
# Licensed under the GNU GPL.  See /usr/share/common-licenses/GPL. 
# 
# Example envs set from openvpn:
#
#     foreign_option_1='dhcp-option DNS 193.43.27.132'
#     foreign_option_2='dhcp-option DNS 193.43.27.133'
#     foreign_option_3='dhcp-option DOMAIN be.bnc.ch'
#

if [ ! -x /sbin/resolvconf ] ; then
    logger "[OpenVPN:update-resolve-conf] missing binary /sbin/resolvconf";
    exit 0;
fi

[ "$script_type" ] || exit 0
[ "$dev" ] || exit 0

split_into_parts()
{
	part1="$1"
	part2="$2"
	part3="$3"
}

case "$script_type" in
  up)
	NMSRVRS=""
	SRCHS=""
	foreign_options=$(printf '%s\n' ${!foreign_option_*} | sort -t _ -k 3 -g)
	for optionvarname in ${foreign_options} ; do
		option="${!optionvarname}"
		echo "$option"
		split_into_parts $option
		if [ "$part1" = "dhcp-option" ] ; then
			if [ "$part2" = "DNS" ] ; then
				NMSRVRS="${NMSRVRS:+$NMSRVRS }$part3"
			elif [ "$part2" = "DOMAIN" ] ; then
				SRCHS="${SRCHS:+$SRCHS }$part3"
			fi
		fi
	done
	R=""
	[ "$SRCHS" ] && R="search $SRCHS
"
	for NS in $NMSRVRS ; do
        	R="${R}nameserver $NS
"
	done
	echo -n "$R" | /sbin/resolvconf -a "${dev}.openvpn"
	;;
  down)
	/sbin/resolvconf -d "${dev}.openvpn"
	;;
esac
```

Getting the cluster credentials with the command:

```shell
az aks get-credentials --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME --admin
```

Given you are connected to the VPN, you should be able to access the private AKS cluster, for example, with the command:

```shell
kubectl get nodes
```
