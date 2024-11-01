import tkinter as tk
import socket
import random
import winsound
import psutil  # Para obter informações detalhadas da interface de rede
import subprocess  # Para realizar o ping
import re  # Para extrair o tempo de resposta do ping

def get_ip():
    try:
        # Obtém o IP da interface de rede ativa
        ip_address = socket.gethostbyname(socket.gethostname())
    except:
        ip_address = "IP não encontrado"
    return ip_address

def get_active_mac():
    # Percorre as interfaces de rede para encontrar a que está ativa e conectada
    interfaces = psutil.net_if_addrs()
    for interface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:  # Verifica se é um MAC Address
                # Verifica se a interface está conectada
                stats = psutil.net_if_stats()[interface]
                if stats.isup:  # Verifica se a interface está ativa
                    connection_type = "Wi-Fi" if "wi-fi" in interface.lower() or "wlan" in interface.lower() else "Ethernet"
                    return f"MAC: {addr.address} ({connection_type})"
    return "MAC não encontrado"

def get_network_speed():
    # Obtém a velocidade da interface de rede ativa
    for interface, stats in psutil.net_if_stats().items():
        if stats.isup:
            return f"Velocidade: {stats.speed} Mbps" if stats.speed else "Velocidade: Não disponível"
    return "Velocidade: Não disponível"

def ping_google_dns():
    # Executa o comando de ping para o servidor DNS público do Google
    result = subprocess.run(["ping", "-n", "1", "8.8.8.8"], stdout=subprocess.PIPE, text=True)
    
    # Verifica se o ping foi bem-sucedido
    if "TTL=" in result.stdout:
        # Extrai o tempo de resposta do ping (latência) usando regex
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
        # Se o IP mudou, emitir alerta sonoro e visual
        current_ip = new_ip
        alert_ip_change()
    
    # Atualiza o texto com o novo IP, MAC, Velocidade e Ping para o Google DNS
    ip_label.config(text=f"IP: {current_ip}")
    mac_label.config(text=f"{get_active_mac()}")
    speed_label.config(text=f"{get_network_speed()}")
    ping_label.config(text=f"{ping_google_dns()}")
    
    # Chama a função novamente a cada 5 segundos
    window.after(5000, update_info)

def alert_ip_change():
    # Alerta visual: muda a cor de fundo da janela temporariamente
    window.config(bg="yellow")
    
    # Alerta sonoro: emite um beep
    winsound.Beep(1000, 500)  # Frequência de 1000 Hz por 500 ms
    
    # Retorna a cor original após 1 segundo
    window.after(1000, lambda: window.config(bg="white"))

def move_window():
    # Gera coordenadas aleatórias para mover a janela
    x = random.randint(0, window.winfo_screenwidth() - window.winfo_width())
    y = random.randint(0, window.winfo_screenheight() - window.winfo_height())
    window.geometry(f"+{x}+{y}")  # Define a nova posição da janela

# Função para criar a janela flutuante e mantê-la sobreposta
def create_window():
    global window, ip_label, mac_label, speed_label, ping_label, current_ip
    current_ip = get_ip()  # Define o IP inicial
    
    window = tk.Tk()
    window.title("Informações de Rede")
    
    # Remove as bordas da janela
    window.overrideredirect(True)
    window.geometry("+100+100")  # Define a posição inicial da janela
    
    # Exibe o IP
    ip_label = tk.Label(window, text=f"IP: {current_ip}", font=("Arial", 16), bg="white")
    ip_label.pack(padx=10, pady=5)
    
    # Exibe o MAC da interface ativa com o tipo de conexão (Wi-Fi ou Ethernet)
    mac_label = tk.Label(window, text=f"{get_active_mac()}", font=("Arial", 16), bg="white")
    mac_label.pack(padx=10, pady=5)

    # Exibe a Velocidade da rede
    speed_label = tk.Label(window, text=f"{get_network_speed()}", font=("Arial", 16), bg="white")
    speed_label.pack(padx=10, pady=5)

    # Exibe o resultado do Ping para 8.8.8.8 com tempo de resposta
    ping_label = tk.Label(window, text=f"{ping_google_dns()}", font=("Arial", 16), bg="white")
    ping_label.pack(padx=10, pady=5)
    
    # Botão de finalizar
    finish_button = tk.Button(window, text="Finalizar", command=window.destroy, bg="red", fg="white")
    finish_button.pack(pady=5)
    
    # Botão de mover janela
    move_button = tk.Button(window, text="Mover Janela", command=move_window, bg="blue", fg="white")
    move_button.pack(pady=5)
    
    # Mantém a janela no topo sempre
    window.attributes('-topmost', True)

    # Atualiza o IP, MAC, Velocidade e Ping periodicamente
    update_info()

    window.mainloop()

# Chama a função para exibir a janela
create_window()
