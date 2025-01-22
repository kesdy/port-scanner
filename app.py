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
             Kesdy Tarafından | Instagram: @kesdyy  
                      Port Tarama Aracı
    """
    print(banner)

def scan_port(ip, port):
    """Port Taraması. Belirtilen İP üzerinde açık portları görüntülemeye yarar. Kesdy."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Timeout süresi (1 saniye)
            s.connect((ip, port))
            return port, True  # Port açık
    except Exception as e:
        return port, False  # Port kapalı

def port_scanner(ip, ports):
    """Belirtilen portları tarar ve açık portları döndürür."""
    print(f"{ip} adresinde port taraması yapılıyor... ({len(ports)} port taranacak)")
    open_ports = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda p: scan_port(ip, p), ports)

    for port, is_open in results:
        if is_open:
            open_ports.append(port)
            print(f"[Açık] Port {port}")

    if not open_ports:
        print("\nAçık port bulunamadı.")
    else:
        print(f"\nAçık portlar: {open_ports}")

if __name__ == "__main__":
    display_banner()  # Banner'ı göster

    print("Kesdy - Tüm hakları saklıdır\n")

    print("1 - Belirli bir portu tarama")
    print("2 - Belirli bir başlangıç ve bitiş aralığını tarama")
    print("3 - Tüm portları tarama (1-65535)")

    try:
        choice = int(input("\nSeçiminizi yapın (1, 2, 3): "))

        if choice not in [1, 2, 3]:
            print("Geçersiz seçim. Program kapatılıyor.")
            input("Kapatmak için bir tuşa basın...")
            exit()

        target_ip = input("\nHedef IP adresi: ").strip()
        if not target_ip:
            print("Hedef IP adresi boş bırakılamaz!")
            input()
            exit()

        if choice == 1:
            port = int(input("Tarayacağınız port numarasını girin: "))
            if port < 1 or port > 65535:
                print("Geçersiz port numarası! Port numarası 1 ile 65535 arasında olmalıdır.")
                exit()
            port_scanner(target_ip, [port])

        elif choice == 2:
            start_port = int(input("Başlangıç portu: "))
            end_port = int(input("Bitiş portu: "))
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                print("Geçersiz port aralığı! Port numaraları 1 ile 65535 arasında olmalı ve başlangıç portu bitiş portundan küçük olmalıdır.")
                exit()
            ports = range(start_port, end_port + 1)
            port_scanner(target_ip, ports)

        elif choice == 3:
            confirm = input("Tüm portları taramak uzun sürebilir. Devam etmek istiyor musunuz? (E/H): ")
            if confirm.lower() != 'e':
                print("İşlem iptal edildi.")
                exit()
            ports = range(1, 65536)
            port_scanner(target_ip, ports)

    except ValueError:
        print("Geçersiz giriş. Lütfen bir sayı girin.")

    print("\nProgram sonlandırıldı. Kesdy - Tüm hakları saklıdır.")
    input("Kapatmak için bir tuşa basın...")
