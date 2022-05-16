import os
import subprocess
import platform
print("platform.system() : ", platform.system())
def shell_run():
  if(platform.system() == "Linux"):
    print("Linux 란다.")
    model_shell = os.path.join(os.path.dirname(__file__), "konlpy.sh")
    print("Linux 란다.1")
    subprocess.run([model_shell, "arguments"], shell=True)
    print("Linux 란다.2")
    # os.system("!pip install konlpy")

