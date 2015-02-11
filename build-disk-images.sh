#!/bin/bash -xe

cat <<EOF > sources.list
deb http://snapshots.internal.jiocloud.com/latest/ceph.com/debian trusty main
deb http://snapshots.internal.jiocloud.com/latest/apt.internal.jiocloud.com/internal trusty main
deb http://snapshots.internal.jiocloud.com/latest/apt.puppetlabs.com trusty main dependencies
deb http://snapshots.internal.jiocloud.com/latest/jiocloud.rustedhalo.com/ubuntu/ trusty main
deb http://snapshots.internal.jiocloud.com/latest/archive.ubuntu.com/ubuntu/ trusty main restricted universe multiverse
deb http://snapshots.internal.jiocloud.com/latest/archive.ubuntu.com/ubuntu/ trusty-security main restricted universe multiverse
deb http://snapshots.internal.jiocloud.com/latest/archive.ubuntu.com/ubuntu/ trusty-updates main restricted universe multiverse
EOF
mkdir -p keys
cat <<EOF > keys/rustedhalo.key
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

mQENBFM0FdsBCADbcuhgf4ny6HQXSCrskXK3hp8HUA4UbW9xIO/fqUzKTvxRuwUR
yRZHXVdCCaLOD8En+h4fnAs2PY3ueVfcIDt9DsJcmqWE+cbFG191Yw8hQV/MtxXU
YNAS6oKOwMheC3BtxdbplJ4hbg065m38wPmcgt/rJiAQZBxrKggCHTvIQunvJnmG
/7OMuwhkzewEAaG5E1mmdVq+IMJAg0ltMiRANASo07wrB0At4q62ozBomua6Hk3s
69ie5ZGiQtyIOgB1mO4RwxS0MoMd+ffq6Kyc8GPoM9EFj4zYGIyOZBa4YqI9cs9A
88E5910lHNx8p2wZCsN+Z00IDN3c6nGmHrzNABEBAAG0Kkppb0Nsb3VkIFJlcG9z
aXRvcnkgPHN1cHBvcnRAamlvY2xvdWQuY29tPokBOAQTAQIAIgUCUzQV2wIbAwYL
CQgHAwIGFQgCCQoLBBYCAwECHgECF4AACgkQhgQCvoVZb3oKVwf+Pr3hBs1h5oOk
VFHwQ/whCcnLjdY1so9wVeZ0TsZVRTrepyKB4Bi+yy4xtYZ572JLbORqRIfdOTgE
06cagaoi2Mc1e5sW/l0ifOvfjlrxIECMX4ftL2igZ7Cu4GB8+WmuDdHpsTdi1Fvx
9cn2eHAylHS3oblwoKpdfiHLPkP0Dt5aJFKOyBQfDPhjX4LF0S0aC0Zg43jNIZdf
nnC71P2+i5WwvljJV2+DTtp3/ImBMKVKgAISxOtBsA5PC+yP6X4lsUUwEP4amti8
jnq2HAjKkpM3UTAWLbHN3x6O2Mg+OIvjYUhrbYeHqQEQurUoPUx2FjZhrXDM/Cxg
tnaES5wRqLkBDQRTNBXbAQgAs4OQ1KlirGpiZC4hEvfmrkBKiJUk1sxsRzqqatkv
Ul5ay3DWoknYO+C7RIzYTwMQ9lv/QwJA2T+FpYykiu6gg872W5aje9xqg98z9DTM
C2lZ79yUMNiMNdKr6Zd05Q6zz0EQVaTMwrYEb+DOW0H8ka7HJA2MJc/ot0Bf2G2A
uavopMiikaVX67901qvHKqQMFgFzbe0C16poK057W3iFEnYAYTzJ6sLhCukfMkwk
6cIApeCEDz9d1tq5aiYcgXhnhnLnXBR9nUlI5qdfU/6+Nmcgh+izjtQp+U5cKHhl
YaiPfbVLQVUg/jbhem0XZuXJ9LdaNoeDdG+7KP7s+N+fIwARAQABiQEfBBgBAgAJ
BQJTNBXbAhsMAAoJEIYEAr6FWW96QewH/20zMCYcDgt8AoRJsyhLPLw8Xa8N57YD
EJfNUKA/74UrUSiLNktXzOVRLa1vAp5kdd9x6HNg5C0bt8kjvYzTvVChRBGt7NRg
SViL4sowyCFpT23JhHRajMmiJPigG+c4gjIJF4DbnpSG8WPC3jDPV891EZCodmaz
klc+BnhnZrb4FcB04RdQ/WXgVshDCzVQhmdIEILGKYHMTjlK/HkV6YqH7l7+jRvJ
phmH35+GJQumLfXWlvDchtBjUTo5ZDCa7TWhwhXZoFg5nxadQDX4TwHhZBQH1TX5
Chk4NnD90SYZt36sTLITe5O/BgYlRMqVo+bVj0tmjMJP/B4PZjABX7A=
=iZW7
-----END PGP PUBLIC KEY BLOCK-----
EOF

DIB_APT_SOURCES=$(pwd)/sources.list DIB_ADD_APT_KEYS=$(pwd)/keys bin/disk-image-create -o ubuntu2015012401 ubuntu ubuntu baremetal dhcp-all-interfaces stable-interface-names apt-sources 

