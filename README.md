# DeathCauseTagger (WOG laptop compatible version)
DeathCauseTagger is a web application that tags death causes to their respective ICD10 codes

## Installation Instructions
This set of instructions assumes that you already have anaconda prompt installed on your computer.
1. Download the zipped folder containing the source code from main branch (Click on Code and then Download ZIP).
2. Unzip the zipped folder.
3. Launch anaconda prompt.
4. Navigate to where the unzipped folder is. For example, if your unzipped folder is in Downloads directory, then run the following commands in anaconda prompt:
```
cd downloads
cd DeathCauseTagger-main
```
5. Create a new Python environment by running the following commands in anaconda prompt:
```
conda create -n tagger python=3.7
conda activate tagger
```
6. Install the required dependencies by running the following command in anaconda prompt (This might take a while):
```
pip install -r requirements.txt
```

## Usage Instructions
1. Navigate to app folder in DeathCauseTagger-main folder by running the following command in anaconda prompt:
```
cd app
```
2. Launch DeathCauseTagger by running the following command in anaconda prompt:
```
python app.py
```
3. Upload CSV file containing the death causes that you want to tag. You can test DeathCauseTagger with the test files provided in test files folder.
