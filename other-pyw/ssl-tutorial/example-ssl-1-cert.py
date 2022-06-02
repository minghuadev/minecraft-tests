#!/usr/bin/env python
# example ssl:

import socket
import ssl


# [1] https://docs.python.org/3/library/ssl.html
# [2] https://stackoverflow.com/questions/70977935/why-do-i-receive-unable-to-get-local-issuer-certificate-ssl-c997

def verify1():
    hostname = 'www.python.org'
    context = ssl.create_default_context(
                             capath="./" # add capath to skip default certs.
                             )

    # optionally, can load the ca bundle, when the capath above is not None:
    #    the -full chain contains issuers and subject server.
    #    the -part chain contains only the two issuers, GlobalSign nv-sa, and GlobalSign
    #    the -root contains only the root issuer, GlobalSign.
    # ref [2]
    #context.load_verify_locations('www-python-org-chain-full.pem') # ok
    #context.load_verify_locations('www-python-org-chain-part.pem') # ok
    #context.load_verify_locations('www-python-org-chain-root.pem') # ok
    #context.load_verify_locations('tmp_cert_pem_1') # fail: unable to get issuer cert
    context.load_verify_locations('tmp_cert_pem_2') # ok. same as root.

    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                print(ssock.version())
    except Exception as e:
        print("Exception in verify1(): ", repr(e))
    except:
        print("Exception in verify1(): unknown")

def verify2():
    hostname = 'www.python.org'
    # PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT,
                             capath="./" # add capath to skip default certs.
                             )
    context.load_verify_locations('www-python-org-chain-root.pem')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:

        # need to make connection to port 443 or the wrapper will fail:
        # https://www.geeksforgeeks.org/socket-programming-python/
        host_ip = socket.gethostbyname(hostname)
        sock.connect( (host_ip, 443))

        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(ssock.version())


# [3] https://stackoverflow.com/questions/64712576/python-print-all-public-key-certificate-information-x-509-format
# [4] https://stackoverflow.com/questions/41831322/is-there-an-asn-1-specification-for-for-x-509-v3-certificates
# [5] https://www.itu.int/ITU-T/recommendations/rec.aspx?id=4123&showfl=1 -- ITU-T X.509 (08/1997)

import asn1tools
def cert_print_asn1(cert):
    foo = asn1tools.compile_files("AlgorithmObjectIdentifiers.asn", "uper")
    output = foo.decode("Certificate", cert)
    print("Cert output: ", output)

def cert_print_text(cert, seqn):

    file_name = "tmp_cert_pem_%d" % seqn
    with open(file_name, "w") as out_f:
        out_f.write(cert)
        out_f.close()

    print("  use command to see:  openssl x509 -in %s -text" % file_name)
    #cert_print_asn1(cert)

def cert_loads_and_prints(file_name):
    in_data = ""
    state = 0
    seqn = 1
    with open(file_name, "r") as in_f:
        while True:
            in_line = in_f.readline()
            if not in_line:
                break
            if state == 0:
                if in_line.find("-----BEGIN CERTIFICATE-----") >= 0:
                    state = 1
                    in_data += in_line
            elif state == 1:
                in_data += in_line
                if in_line.find("-----END CERTIFICATE-----") >= 0:
                    cert_print_text(in_data, seqn)
                    state = 0
                    in_data = ""
                    seqn += 1
    if len(in_data) != 0:
        print("Finished. Data left ", len(in_data))


if __name__ == '__main__':
    # testing with python 3.7

    # env before installing asn1tools
    # Package         Version Location
    # --------------- ------- -----------------------------------------------------------------
    # awscrt          0.12.1
    # AWSIoTPythonSDK 1.4.9   h:\aws-iot-lx\srcs\aws-iot-device-sdk-python
    # awsiotsdk       1.7.1
    # pip             19.2.3
    # setuptools      41.2.0
    #
    # env packages installed for asn1tools:
    # asn1tools-0.163.0 bitstruct-8.14.1 diskcache-5.4.0 prompt-toolkit-3.0.29 pyparsing-3.0.9 wcwidth-0.2.5
    #
    verify1() # ok
    verify2() # not working initially, ok after adding capath and cert

    cert_loads_and_prints("www-python-org-chain-part.pem")


