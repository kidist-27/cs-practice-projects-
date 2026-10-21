import socket


def main():
    hostname = input("Enter a hostname: ").strip()

    if not hostname:
        print("Hostname cannot be empty.")
        return

    try:
        addresses = socket.getaddrinfo(
            hostname, None, type=socket.SOCK_STREAM
        )
        ips = sorted({result[4][0] for result in addresses})

        print(f"\nHostname: {hostname}")
        for ip in ips:
            print(f"IP address: {ip}")

    except socket.gaierror:
        print("Could not resolve hostname. Check DNS or spelling.")


if __name__ == "__main__":
    main()
