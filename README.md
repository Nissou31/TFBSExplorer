[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) &nbsp;
[![forthebadge](https://forthebadge.com/images/badges/open-source.svg)](https://forthebadge.com) &nbsp;

# Cis-regulating TFBS Searcher API 🧬🔬

## Overview 📝

The project consists of solving the problem of finding cis-regulating Transcription Factor Binding Sites (TFBS) of a set of genes. Using the `Biopython` module and interaction with the **NCBI** and **JASPAR** databases, we created a FastAPI-based backend that searches for TFBS in a set of genes supposedly co-regulated by a transcription factor (TF). The method used is the sliding window, and our approach involves calculating the distance between the occurrences (hits) of TFBS on promoter sequences.

## Purpose

The primary purpose of this project is to provide an automated, efficient, and scalable way to identify potential TFBS in promoter sequences. This can be useful for various biological and medical research applications, including gene regulation studies and identifying potential targets for genetic interventions.

## Technologies Used

- **Python 3.9**
- **FastAPI**: For creating the API
- **Biopython**: For handling biological data
- **NCBI API**: For retrieving sequence data
- **JASPAR Database**: For accessing TFBS matrices
- **Docker**: For containerization

## Useful URLs

- **NCBI (National Center for Biotechnology Information)**: [https://www.ncbi.nlm.nih.gov/](https://www.ncbi.nlm.nih.gov/)
- **JASPAR Database**: [https://jaspar.genereg.net/](https://jaspar.genereg.net/)
- **Biopython Documentation**: [https://biopython.org/wiki/Documentation](https://biopython.org/wiki/Documentation)
- **FastAPI Documentation**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

## Project Tree 🌲

    ├── README.md          
    │
    ├── data
    │    ├── motifs         
    │    └── sequences     
    │
    ├── app
    │    ├── __init__.py
    │    ├── main.py
    │    ├── models
    │    │    └── models.py
    │    ├── endpoints
    │    │    ├── __init__.py
    │    │    ├── health.py
    │    │    ├── tfbs.py
    │    │    └── welcome.py
    │    └── utils
    │         ├── pwm.py
    │         └── utils.py
    │
    ├── tests
    │    ├── __init__.py
    │    ├── test_health.py
    │    ├── test_tfbs.py
    │    └── test_welcome.py
    │
    ├── .dockerignore
    ├── .gitignore
    ├── Dockerfile
    └── requirements.txt

## Getting Started 🚀

Before cloning the project into your local disk, please check the requirements.

### Requirements 🧾

- `Python 3.9`
- `Valid SSL CERTIFICATE for Python`
- `Biopython`
- `FastAPI`
- `Uvicorn`

### Usage 💻

1. **Clone the Repository**

    ```sh
    git clone https://github.com/Nissou31/bio-informatique-api.git
    cd bio-informatique-api
    ```

2. **Set up Environment**

    - Create a `.env` file based on the `.env.example` file.
    - Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. **Run the Application**

    ```sh
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

4. **Testing Endpoints**

    Use the provided curl commands to test different functionalities. For example:

    ```sh
    curl -X POST "http://127.0.0.1:8000/tfbs" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d '{
              "email": "your@email.com",
              "m": "MA0114.4",
              "t": -2.0,
              "l": 1000,
              "w": 40,
              "s": 0.3,
              "p": 0.1,
              "mrna": [
                  "NM_007389", "NM_079420", "NM_001267550",
                  "NM_002470", "NM_003279", "NM_005159",
                  "NM_003281", "NM_002469", "NM_004997",
                  "NM_004320", "NM_001100", "NM_006757"
              ]
          }'
    ```

## Contribution Guidelines ✏️

We welcome contributions from the community! If you'd like to contribute, please follow these steps:

1. **Fork the repository**.
2. **Create a new branch** for your feature or bugfix.
3. **Make your changes**.
4. **Run tests** to ensure everything works.
5. **Submit a pull request**.

Please make sure your code adheres to our coding standards and includes proper documentation and tests.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Authors ✏️

- **AMRI Anes Saad Eddine**

We hope you find this project useful and contribute to its development. If you have any questions or need further assistance, feel free to open an issue or reach out!

