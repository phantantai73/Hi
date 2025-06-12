import socket
import threading
import time

def send_packet(server_ip, server_port, packet, packet_count, thread_id, stop_event):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((server_ip, server_port))
            for i in range(packet_count):
                if stop_event.is_set():
                    print(f"[Luồng {thread_id}] Dừng gửi do timeout.")
                    break
                s.sendall(packet)
                print(f"[Luồng {thread_id}] Đã gửi gói tin {i + 1}/{packet_count}")
    except Exception as e:
        print(f"[Luồng {thread_id}] Lỗi: {e}")

def stop_thread_after_timeout(stop_event, timeout=5):
    time.sleep(timeout)
    stop_event.set()

def main():
    try:
        server_address = input("Nhập địa chỉ server (ví dụ: dragonsmp.myftp.org:15571)__cre:buibadat1987: ")
        if ":" not in server_address:
            raise ValueError("Định dạng địa chỉ không hợp lệ. Phải là ip:port")
        server_ip, server_port = server_address.split(":")
        server_port = int(server_port)

        packet_size_mb = 1
        packet = b"\x00" * (packet_size_mb * 1024 * 1024)  # Gói tin 1MB

        packet_count = 10
        thread_count = int(input("Nhập số lượng luồng: "))

        threads = []
        stop_events = []

        for i in range(thread_count):
            stop_event = threading.Event()
            stop_events.append(stop_event)

            thread = threading.Thread(target=send_packet,
                                      args=(server_ip, server_port, packet, packet_count, i + 1, stop_event),
                                      name=f"SenderThread-{i+1}")
            timer = threading.Thread(target=stop_thread_after_timeout, args=(stop_event,), name=f"TimerThread-{i+1}")

            threads.append(thread)
            thread.start()
            timer.start()

        for thread in threads:
            thread.join()

        print("Hoàn tất gửi gói tin.")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()


 
 




