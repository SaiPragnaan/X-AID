from setuptools import find_packages,setup

setup(
    name="medical-chatbot",
    version='0.0.1',
    author='Sai Pragnaan',
    author_email='pragnaan98@gmail.com',
    install_requires=["langchain","streamlit","python-dotenv","PyPDF2","langchain_google_genai"],
    packages=find_packages()
)