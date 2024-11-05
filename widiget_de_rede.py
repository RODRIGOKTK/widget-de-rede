import tkinter as tk
import socket
import random
import webbrowser  # Para abrir o link no navegador
import winsound
import psutil  # Para obter informações detalhadas da interface de rede
import subprocess  # Para realizar o ping
import re  # Para extrair o tempo de resposta do ping

def get_ip():
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except:
        ip_address = "IP não encontrado"
    return ip_address

def get_active_mac():
    interfaces = psutil.net_if_addrs()
    for interface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                stats = psutil.net_if_stats()[interface]
                if stats.isup:
                    connection_type = "Wi-Fi" if "wi-fi" in interface.lower() or "wlan" in interface.lower() else "Ethernet"
                    return f"MAC: {addr.address} ({connection_type})"
    return "MAC não encontrado"

def get_network_speed():
    for interface, stats in psutil.net_if_stats().items():
        if stats.isup:
            return f"Velocidade: {stats.speed} Mbps" if stats.speed else "Velocidade: Não disponível"
    return "Velocidade: Não disponível"

def ping_google_dns():
    result = subprocess.run(["ping", "-n", "1", "8.8.8.8"], stdout=subprocess.PIPE, text=True)
    if "TTL=" in result.stdout:
        match = re.search(r"tempo[=<]\s*(\d+)\s*ms", result.stdout)
        if match:
            ping_time = match.group(1)
            return f"Ping para 8.8.8.8: {ping_time} ms"
        else:
            return "Ping bem-sucedido, tempo desconhecido"
    else:
        return "Ping para 8.8.8.8 falhou"

def update_info():
    global current_ip
    new_ip = get_ip()
    
    if new_ip != current_ip:
        current_ip = new_ip
        alert_ip_change()
    
    ip_label.config(text=f"IP: {current_ip}")
    mac_label.config(text=f"{get_active_mac()}")
    speed_label.config(text=f"{get_network_speed()}")
    ping_label.config(text=f"{ping_google_dns()}")
    
    window.after(5000, update_info)

def alert_ip_change():
    window.config(bg="yellow")
    winsound.Beep(1000, 500)
    window.after(1000, lambda: window.config(bg="white"))

def move_window():
    x = random.randint(0, window.winfo_screenwidth() - window.winfo_width())
    y = random.randint(0, window.winfo_screenheight() - window.winfo_height())
    window.geometry(f"+{x}+{y}")

def open_github():
    webbrowser.open("https://github.com/RODRIGOKTK/widget-de-rede")

def create_window():
    global window, ip_label, mac_label, speed_label, ping_label, current_ip
    current_ip = get_ip()
    
    window = tk.Tk()
    window.title("Informações de Rede")
    window.overrideredirect(True)
    window.geometry("+100+100")
    
    ip_label = tk.Label(window, text=f"IP: {current_ip}", font=("Arial", 16), bg="white")
    ip_label.pack(padx=10, pady=5)
    
    mac_label = tk.Label(window, text=f"{get_active_mac()}", font=("Arial", 16), bg="white")
    mac_label.pack(padx=10, pady=5)

    speed_label = tk.Label(window, text=f"{get_network_speed()}", font=("Arial", 16), bg="white")
    speed_label.pack(padx=10, pady=5)

    ping_label = tk.Label(window, text=f"{ping_google_dns()}", font=("Arial", 16), bg="white")
    ping_label.pack(padx=10, pady=5)
    
    finish_button = tk.Button(window, text="Finalizar", command=window.destroy, bg="red", fg="white")
    finish_button.pack(pady=5)
    
    move_button = tk.Button(window, text="Mover Janela", command=move_window, bg="blue", fg="white")
    move_button.pack(pady=5)
    
    github_button = tk.Button(window, text="@RODRIGOKTK", command=open_github, fg="blue", cursor="hand2")
    github_button.pack(anchor="se", padx=10, pady=10)
    
    window.attributes('-topmost', True)
    update_info()
    window.mainloop()

create_window()
