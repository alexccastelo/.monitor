import psutil
from flask import Flask, render_template
from flask_socketio import SocketIO
import time
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)


def get_system_info():
    while True:
        cpu_percent = psutil.cpu_percent(interval=None)
        memory_info = psutil.virtual_memory()

        # Emitir os dados para os clientes conectados via Socket.IO
        socketio.emit(
            "update_data",
            {"cpu_percent": cpu_percent, "memory_percent": memory_info.percent},
        )

        # Verificar se o uso de memória é maior ou igual a 80%
        if memory_info.percent >= 85:
            socketio.emit(
                "memory_alert", {"message": "Alerta: Uso de memória está alto!"}
            )

        time.sleep(1)


# Função para obter o uso de CPU e memória em tempo real
def get_system_info():
    while True:
        cpu_percent = psutil.cpu_percent(interval=None)
        memory_info = psutil.virtual_memory()

        # Emitir os dados para os clientes conectados via Socket.IO
        socketio.emit(
            "update_data",
            {"cpu_percent": cpu_percent, "memory_percent": memory_info.percent},
        )

        time.sleep(1)


# Rota inicial que renderiza a página HTML
@app.route("/")
def index():
    return render_template("index.html")


# Configuração do Socket.IO para atualizações em tempo real
@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


# Executar o servidor Flask com Socket.IO em uma thread separada
if __name__ == "__main__":
    # Iniciar a função de monitoramento em uma thread separada
    monitor_thread = Thread(target=get_system_info)
    monitor_thread.daemon = True
    monitor_thread.start()

    # Iniciar o servidor Flask com Socket.IO
    socketio.run(app, debug=True)
