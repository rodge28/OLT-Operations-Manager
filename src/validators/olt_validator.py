import ipaddress


class OLTValidator:

    @staticmethod
    def validate_hostname(hostname: str):

        hostname = hostname.strip()

        if not hostname:
            raise ValueError("Hostname is required.")

        if len(hostname) > 100:
            raise ValueError("Hostname is too long.")

        return hostname


    @staticmethod
    def validate_ip(ip):

        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise ValueError("Invalid IP address.")

        return ip


    @staticmethod
    def validate_port(port):

        port = int(port)

        if port < 1 or port > 65535:
            raise ValueError("Invalid SSH port.")

        return port
