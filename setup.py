from setuptools import setup
from setuptools import find_packages

# find_packages will find all the packages with __init__.py
print(find_packages())

setup(
    # namn på paketet
    name="taxipred",  
    # pakektets version  
    version="0.0.1",   
    # beskrivning av vad paketet innehåller, samt vem som skapat det 
    description="this package contains taxipred app",
    author="Pontus Ågren Grundström",
    author_email="pontus.agrengrundstrom@gmail.com",
    # paket som installeras automatiskt när man install taxipred. (dependencies för taxipred paketet)
    install_requires=["streamlit", "pandas", "fastapi", "uvicorn", "pydantic", "python-dotenv", "joblib", "scikit-learn"],     
    # berättar att paketet 'taxipred' ligger i mappen src, för att setup inte ska leta efter taxipred i rooten där setup.py filen finns, alltså src/taxipred/
    package_dir={"": "src"},    
    # inkluderar filer som inte är .py filer, i detta fall, alla .csv filer som finns i src/taxipred/data, dessa filer följer med i paketet vid installation
    package_data={"taxipred": ["data/*.csv", "models/*.joblib", "assets/*.png"]},  
    # letar efter paket genom att kolla efter mappar med __init__.py 
    packages=find_packages(where="src"),   
)
