pip install numpy scipy matplotlib Pillow rasterio kivy
pwd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
fileName="/app.py"
echo $pwd
filePath=$pwd$fileName
echo $filePath
python $filePath