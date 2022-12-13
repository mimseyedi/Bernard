import os; os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
import subprocess
from pathlib import Path
import warnings; warnings.filterwarnings('ignore')
try:
    import requests
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL)
finally:
    import requests
try:
    from clint.textui import progress
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "clint"], stdout=subprocess.DEVNULL)
finally:
    from clint.textui import progress
try:
    from rich.console import Console
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
finally:
    from rich.console import Console
    screen = Console()
try:
    from prompt_toolkit.shortcuts import confirm
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "prompt-toolkit==3.0.16"], stdout=subprocess.DEVNULL)
finally:
    from prompt_toolkit.shortcuts import confirm
try:
    import tensorflow
    from imageai.Detection import ObjectDetection
    from PIL import Image
    activate_init = True
except ImportError as module:
    screen.print("You do not have the required modules to run this script!", style="yellow")
    screen.print("Required modules:\ntensorflow\nkeras\nnumpy\npillow\nscipy\nh5py\nmatplotlib\nopencv-python\nkeras-resnet\n",
                 style="yellow")
    screen.print("Considering the large size of these modules and their long installation, ")

    ask_to_install = confirm("do you want them to be installed?")
    if ask_to_install:
        subprocess.run([sys.executable, "-m", "pip", "install", "tensorflow==2.4.0"])
        subprocess.run([sys.executable, "-m", "pip", "install", "keras==2.4.3"])
        subprocess.run([sys.executable, "-m", "pip", "install", "numpy==1.19.3"])
        subprocess.run([sys.executable, "-m", "pip", "install", "pillow==7.0.0"])
        subprocess.run([sys.executable, "-m", "pip", "install", "scipy==1.4.1"])
        subprocess.run([sys.executable, "-m", "pip", "install", "h5py==2.10.0"])
        subprocess.run([sys.executable, "-m", "pip", "install", "matplotlib==3.3.2"])
        subprocess.run([sys.executable, "-m", "pip", "install", "opencv-python"])
        subprocess.run([sys.executable, "-m", "pip", "install", "keras-resnet==0.2.0"])

        from imageai.Detection import ObjectDetection
        from PIL import Image

        activate_init = True
    else:
        activate_init = False


# The location of the scripts directory.
scripts_path = Path(__file__).parent
# A message for guidance and how to use the script.
guide_message = """With the objd command, you can accurately identify the objects inside a jpg image.

Parameters:
objd 'image.jpg'
        └── output: 'image_detected.jpg'
        
to specify the output file:
objd 'image.jpg' 'image_detected.jpg'
        └── output: 'image_detected.jpg'"""


# A function to download and save the model required for processing.
def get_the_model(url: str):
    screen.print("Downloading the model...", style="green")
    request = requests.get(url, stream=True)
    with open(Path(scripts_path, ".yolo.h5"), "wb") as model_file:
        total_length = int(request.headers.get('content-length'))
        for chunk in progress.bar(request.iter_content(chunk_size=1024),
                                  expected_size=(total_length / 1024) + 1):
            if chunk:
                model_file.write(chunk)
                model_file.flush()


# A function to identify objects in the image.
def object_detection(image_url: Path, output_url: Path, model='yolo'):
    if model == 'yolo':
        detector = ObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(Path(scripts_path, ".yolo.h5"))
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image=image_url,
                                                     output_image_path=output_url,
                                                     minimum_percentage_probability=30)

        screen.print(f"The processing is done and the result can be seen in '{output_url}'", style="green")

        ask_to_open = confirm("Do you want to see the output?")
        if ask_to_open:
            Image.open(output_url).show()


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        screen.print("Error: You must select a jpg photo to process!", style="red")

    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with any parameter except -h.
    # Pattern: objd image.jpg
    elif len(sys.argv) == 2 and sys.argv[1] != "-h":
        image_url = Path(os.getcwd(), sys.argv[1])
        if sys.argv[1].endswith(".jpg"):
            if image_url.exists():
                model_path = Path(scripts_path, ".yolo.h5")
                if model_path.exists():
                    if Path(os.getcwd(), f"{sys.argv[1][:-4]}_detected.jpg").exists():
                        os.remove(Path(os.getcwd(), f"{sys.argv[1][:-4]}_detected.jpg"))

                    object_detection(image_url=os.path.join(os.getcwd(), sys.argv[1]),
                                     output_url=os.path.join(os.getcwd(), f"{sys.argv[1][:-4]}_detected.jpg"),
                                     model="yolo")
                else:
                    get_the_model("https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5")

                    if Path(os.getcwd(), f"{sys.argv[1][:-4]}_detected.jpg").exists():
                        os.remove(Path(os.getcwd(), f"{sys.argv[1][:-4]}_detected.jpg"))

                    object_detection(image_url=os.path.join(os.getcwd(), sys.argv[1]),
                                     output_url=os.path.join(os.getcwd(), f"{sys.argv[1][:-4]}_detected.jpg"),
                                     model="yolo")
            else:
                screen.print(f"Error: '{sys.argv[1]}' not found!", style="red")
        else:
            screen.print("Error: You must select a jpg photo to process!", style="red")

    # If the script is called with any parameter except -h.
    # Pattern: objd image.jpg image_detected.jpg
    elif len(sys.argv) == 3 and sys.argv[1] != "-h":
        image_url = Path(os.getcwd(), sys.argv[1])
        output_url = Path(os.getcwd(), sys.argv[2])

        if sys.argv[1].endswith(".jpg"):
            if sys.argv[2].endswith(".jpg"):
                if not output_url.exists():
                    if image_url.exists():
                        model_path = Path(scripts_path, ".yolo.h5")
                        if model_path.exists():
                            object_detection(image_url=os.path.join(os.getcwd(), sys.argv[1]),
                                             output_url=os.path.join(os.getcwd(), sys.argv[2]),
                                             model="yolo")
                        else:
                            get_the_model("https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5")

                            object_detection(image_url=os.path.join(os.getcwd(), sys.argv[1]),
                                             output_url=os.path.join(os.getcwd(), sys.argv[2]),
                                             model="yolo")
                    else:
                        screen.print(f"Error: '{sys.argv[1]}' not found!", style="red")
                else:
                    screen.print(f"Error: A file named '{sys.argv[2]}' already exists in this path!", style="red")
            else:
                screen.print("Error: You must select a jpg photo for output!", style="red")
        else:
            screen.print("Error: You must select a jpg photo to process!", style="red")

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    if activate_init: init()
