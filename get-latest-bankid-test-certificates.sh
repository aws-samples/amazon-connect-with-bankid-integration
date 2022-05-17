#!/bin/bash
# Test BankID Certificate Script
#
# !!!! FOR BANKID TEST ENVIRONMENT ONLY !!!!
#
# This script is not at all relevent for production or if you generate
# your own certificates via:
# https://www.bankid.com/utvecklare/guider/teknisk-integrationsguide/rp-introduktion
#
# This bash file will download the publically available SSL certificates.
# You will need to confirm the appropriate download url from:
# https://www.bankid.com/en/utvecklare/test
#
# You will also need the publically available passphase for the SSL certificate.
# The latest information can be found:
# https://www.bankid.com/assets/bankid/rp/bankid-relying-party-guidelines-v3.6.pdf
#
# To override the download URL simply copy the url after the password
# ./get-latest-bankid-certificates.sh https://www.bankid.com/assets/bankid/rp/FPTestcert3_20200618.p12
#

URL="${1:-https://www.bankid.com/assets/bankid/rp/FPTestcert3_20200618.p12}"

DOWNLOAD_FILE=test-bankid.p12
CODE_PATH=./code/bankid-auth

echo -n "Please enter the BankID Passphase: "
read -rs password

echo -e "\nPath for test certificate: \n    ${URL}"
echo -e "Downloading p12 certificate to ${DOWNLOAD_FILE}"
curl "${URL}" --output ${DOWNLOAD_FILE}

echo -e "Unpacking test certificate into separate pem files"
openssl pkcs12 -info -nodes -in ${DOWNLOAD_FILE} -out ${CODE_PATH}/key.pem -nocerts -nodes -passin pass:"${password}"
openssl pkcs12 -info -nodes -in ${DOWNLOAD_FILE} -out ${CODE_PATH}/cert.pem -clcerts -nokeys  -passin pass:"${password}"

echo -e "Deleting downloaded p12 certificate ${DOWNLOAD_FILE}"
rm ${DOWNLOAD_FILE}
