import os
import shlex
from time import sleep

from mcstatus import JavaServer


class Server:
    def __init__(self, jar: str, path: str, minimumRAM: str, maximumRAM: str):
        if not os.path.exists(jar):
            raise Exception(f"File doesn't exist: {jar}")

        self.minimumRAM: str = minimumRAM
        self.maximumRAM: str = maximumRAM
        self.jar = jar
        self.path = path
        self.session = "server"
        self.status = JavaServer("localhost") 

    def start(self):
        if not os.system(f"tmux list-sessions | grep {self.session} > /dev/null") == 0:
            os.system("tmux new -d -s server")
            
        if not self.isOnline():
            self.sendCommand(f"cd {self.path}")
            self.sendCommand(
                f"java -Xms{self.minimumRAM} -Xmx{self.maximumRAM} -jar {self.jar} nogui"
            )
        else:
            print("Already running")
        pass

    def stop(self, countdown = True, countdownSeconds = 20):
        if os.system(f"tmux list-sessions | grep {self.session} > /dev/null") != 0:
            pass
        if not self.isOnline():
            pass

        if countdown:
            for x in range(countdownSeconds, 1, -1):
                # print(x)
                command = 'title @a title ["",{"text":"Server Shutdown in ' + str(x) + ' seconds","color":"red"}]'
                # print(command)
                self.sendCommand(command)
                sleep(1)

        self.sendCommand("stop")
        while self.isOnline(): pass
        sleep(3)
        self.sendCommand("exit")

    def restart(self):
        if self.isOnline():
            self.stop()
        self.start()

    def sendCommand(self, command: str):
        tmux_command = f"tmux send -t {self.session} {shlex.quote(command)} ENTER"
        os.system(tmux_command)
        # check_call(tmux_command, shell=True)

    def isOnline(self):
        try:
            self.status.status()
        except ConnectionRefusedError:
            return False
        else:
            return True
