# I know this can be better
from console import console
import pkg_resources, os
installed = 0
uninstalled = 0
command = "pip install "
for lib in ['openai','SpeechRecognition','PyAudio','python-dotenv']:
    try:
        dist = pkg_resources.get_distribution(lib)
        installed += 1
        command = command + lib + " "
    except pkg_resources.DistributionNotFound:
        uninstalled += 1
        command = command + lib + " "
command = command + " --upgrade"
console.success("(I) Installed libraries:",installed)
console.success("(I) Libraries to install:",uninstalled)
os.system(command)
console.informationsucc("Toutes les dépendances ont été installé, veuillez lancer voiceassist.py")
console.input("Appuyer sur 'Entrer' pour fermer l'installation")