all: upload-centos7 upload-centos6 upload-ubuntu1404

upload-centos7: CentOS-7-x86_64-GenericCloud.raw
	echo glance image-create --name "CentOS 7" --disk-format raw --container-format bare --file $< --is-public True

upload-centos6: CentOS-6-x86_64-GenericCloud.raw
	echo glance image-create --name "CentOS 6" --disk-format raw --container-format bare --file $< --is-public True

upload-ubuntu1404: ubuntu-14.04-server-cloudimg-amd64-disk1.raw 
	echo glance image-create --name "Ubuntu 14.04.1 LTS" --disk-format raw --container-format bare --file $< --is-public True

ubuntu-14.04-server-cloudimg-amd64-disk1.qcow2:
	wget -O $@ https://cloud-images.ubuntu.com/releases/14.04.1/release/ubuntu-14.04-server-cloudimg-amd64-disk1.img

CentOS-7-x86_64-GenericCloud.qcow2.xz:
	wget -O $@ wget http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2.xz

CentOS-6-x86_64-GenericCloud.qcow2.xz:
	wget -O $@ wget http://cloud.centos.org/centos/6/images/CentOS-6-x86_64-GenericCloud.qcow2.xz

%.qcow2: %.qcow2.xz
	xz -dk $<

%.raw: %.qcow2
	qemu-img convert -f qcow2 -O raw $< $@
