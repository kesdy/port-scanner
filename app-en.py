import socket
from concurrent.futures import ThreadPoolExecutor

def display_banner():
    banner = r"""
 ______  __                  ____               __      
/\__  _\/\ \                /\  _`\            /\ \__   
\/_/\ \/\ \ \___      __    \ \ \L\ \___   _ __\ \ ,_\  
   \ \ \ \ \  _ `\  /'__`\   \ \ ,__/ __`\/\`'__\ \ \/  
    \ \ \ \ \ \ \ \/\  __/    \ \ \/\ \L\ \ \ \/ \ \ \_ 
     \ \_\ \ \_\ \_\ \____\    \ \_\ \____/\ \_\  \ \__\
      \/_/  \/_/\/_/\/____/     \/_/\/___/  \/_/   \/__/
             Developed by Kesdy | Instagram: @kesdyy  
                      Port Scanner Tool
    """
    print(banner)

def scan_port(ip, port):
    """Port Scanning. Used to check open ports on a specified IP address. Developed by Kesdy."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Timeout duration (1 second)
            s.connect((ip, port))
            return port, True  # Port is open
    except Exception as e:
        return port, False  # Port is closed

def port_scanner(ip, ports):
    """Scans the specified ports and returns open ports."""
    print(f"Scanning ports on {ip}... ({len(ports)} ports to scan)")
    open_ports = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda p: scan_port(ip, p), ports)

    for port, is_open in results:
        if is_open:
            open_ports.append(port)
            print(f"[Open] Port {port}")

    if not open_ports:
        print("\nNo open ports found.")
    else:
        print(f"\nOpen ports: {open_ports}")

if __name__ == "__main__":
    display_banner()  # Show the banner

    print("Kesdy - All rights reserved\n")

    print("1 - Scan a specific port")
    print("2 - Scan a range of ports")
    print("3 - Scan all ports (1-65535)")

    try:
        choice = int(input("\nChoose an option (1, 2, 3): "))

        if choice not in [1, 2, 3]:
            print("Invalid choice. Program is terminating.")
            input("Press any key to close...")
            exit()

        target_ip = input("\nTarget IP address: ").strip()
        if not target_ip:
            print("Target IP address cannot be empty!")
            input()
            exit()

        if choice == 1:
            port = int(input("Enter the port number to scan: "))
            if port < 1 or port > 65535:
                print("Invalid port number! The port number must be between 1 and 65535.")
                exit()
            port_scanner(target_ip, [port])

        elif choice == 2:
            start_port = int(input("Start port: "))
            end_port = int(input("End port: "))
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                print("Invalid port range! Port numbers must be between 1 and 65535, and the start port must be less than the end port.")
                exit()
            ports = range(start_port, end_port + 1)
            port_scanner(target_ip, ports)

        elif choice == 3:
            confirm = input("Scanning all ports may take a long time. Do you want to continue? (Y/N): ")
            if confirm.lower() != 'y':
                print("Operation canceled.")
                exit()
            ports = range(1, 65536)
            port_scanner(target_ip, ports)

    except ValueError:
        print("Invalid input. Please enter a number.")

    print("\nProgram terminated. Kesdy - All rights reserved.")
    input("Press any key to close...")
