
ln -s /usr/local/etc/ssl/cert.pem /etc/ssl/

pkg install -y pkg

cp /usr/local/etc/pkg/repos/df-latest.conf.sample /usr/local/etc/pkg/repos/df-latest.conf

echo 'autoboot_delay="1"' >> /boot/loader.conf
echo 'beastie_disable="YES"' >> /boot/loader.conf

#build fuse kernel mod
cd /usr
make src-create-shallow
cd /usr/src/sys/vfs/fuse
make
make install
rm -rf /usr/src/*
echo 'fuse_load="YES"' >> /boot/loader.conf



cat /boot/loader.conf


boot0cfg -t 1 ad0

#for auto dhcp for all the nc
cat << 'EOF' >> /etc/rc.local
for iface in $(ifconfig -l); do
    if [ "$iface" != "lo0" ]; then
        dhclient $iface >/dev/null 2>&1
    fi
done
EOF

chmod +x /etc/rc.local

#just in case
echo 'ifconfig_em0="DHCP"' >> /etc/rc.conf
echo 'ifconfig_vtnet0="DHCP"' >> /etc/rc.conf


