# MediChain: Blockchain-Based Patient Data Repository

MediChain is a blockchain-inspired system designed for securely managing patient data with homomorphic encryption and decentralized queries. This project processes a dataset, encrypts the data, stores it in a simulated blockchain, and uses machine learning models for secure predictions.

---

## Backend Development Workflow

This document outlines the step-by-step process to implement and integrate the backend components of MediChain.

---

### 1. **Data Preparation**
**Objective**: Set up and preprocess the dataset for further processing.

- Place the dataset in the `backend/data/` directory (e.g., `dataset.csv`).
- Write utility functions in `utils.py` to:
  - Load the dataset as a Pandas DataFrame.
  - Save processed data back to a CSV file.
- Optionally clean and preprocess the dataset (e.g., handle missing values, normalize fields).

---

### 2. **Encryption Module**
**Objective**: Implement homomorphic encryption to secure patient data.

- **Tasks**:
  1. Install a homomorphic encryption library (e.g., `phe` or `PySEAL`).
  2. Create the following functions in `backend/encryption/homomorphic.py`:
     - `encrypt_data(data)`: Encrypt the entire dataset.
     - `decrypt_data(data)`: Decrypt the dataset for validation.
     - `process_encrypted_data(data)`: Perform computations directly on encrypted data (e.g., summation or model inference).
  3. Test the encryption and decryption using sample data.

---

### 3. **Machine Learning Model**
**Objective**: Train and prepare the machine learning model for encrypted predictions.

- **Tasks**:
  1. Use a Jupyter Notebook (`ml_pipeline.ipynb`) to:
     - Preprocess the dataset (e.g., feature scaling, encoding categorical variables).
     - Train a model (e.g., Random Forest, Logistic Regression).
     - Evaluate the model (e.g., accuracy, confusion matrix).
  2. Serialize the trained model as `model.pkl` using `joblib` or `pickle`.
  3. Write a script in `ml_pipeline.py` to:
     - Load the trained model.
     - Preprocess encrypted data for predictions.
     - Use the model to make predictions on encrypted data.

---

### 4. **Blockchain Module**
**Objective**: Simulate blockchain behavior for secure and decentralized data management.

- **Tasks**:
  1. Implement the blockchain structure in `backend/blockchain/blockchain.py`:
     - Create a `Block` class with attributes like `index`, `timestamp`, `data`, `hash`, and `previous_hash`.
     - Create a `Blockchain` class to manage the chain, add blocks, and validate the chain.
  2. Write a function to add encrypted data as transactions to the blockchain.
  3. Implement a basic consensus algorithm in `backend/blockchain/consensus.py` (optional for single-node systems).

---

### 5. **Backend Workflow Integration**
**Objective**: Integrate all components into a unified backend pipeline.

- **Tasks**:
  1. Write the main entry script in `main.py`:
     - Load the dataset using utility functions.
     - Encrypt the data using `encrypt_data()`.
     - Add encrypted data to the blockchain.
     - Use the ML model to make predictions on the encrypted data.
     - Decrypt and save the results to `results.csv`.
  2. Test the entire pipeline to ensure all modules work together.

---

### 6. **Testing and Debugging**
**Objective**: Ensure the system works seamlessly and identify any issues.

- **Tasks**:
  - Write unit tests for each module (encryption, ML, blockchain).
  - Write integration tests for the full pipeline in `main.py`.

---

### 7. **Documentation**
**Objective**: Provide clear and concise documentation for the backend system.

- **Tasks**:
  - Add comments and docstrings to all modules and scripts.
  - Update this `README.md` with:
    - Project overview.
    - Instructions for running the backend.
    - Description of each module and its purpose.
    - Example outputs or screenshots.

---

## Running the Backend

1. **Install Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
