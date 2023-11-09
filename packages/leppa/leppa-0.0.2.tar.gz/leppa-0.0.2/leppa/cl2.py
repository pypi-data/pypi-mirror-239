import os

qubit_16_bit_generator = """
from qiskit import IBMQ


# Load IBM Quantum Experience account
IBMQ.enable_account('89450b58976ce1c7091a58b9612be3b845389d83091e1e526bf385a0b04a55a6c90d8c576894dd945c8722b0afc15663192646420a003f4257978aec56d64bde')

# Get the provider
provider = IBMQ.get_provider()

# Get the hub name
hub_name = provider.credentials.hub

# Print the hub name
print("Hub name:", hub_name)

from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, execute,IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.circuit.library import QFT
import numpy as np

pi = np.pi


provider = IBMQ.get_provider(hub='ibm-q')

backend = provider.get_backend('ibmq_qasm_simulator')

q = QuantumRegister(5,'q')
c = ClassicalRegister(5,'c')

circuit = QuantumCircuit(q,c)

circuit.x(q[4])
circuit.x(q[2])
circuit.x(q[0])
circuit.append(QFT(num_qubits=5, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name='qft'), q)
circuit.measure(q,c)
circuit.draw(output='mpl', filename='qft1.png')
print(circuit)

job = execute(circuit, backend, shots=1000)

job_monitor(job)

counts = job.result().get_counts()

print("\n QFT Output")
print("-------------")
print(counts)
input()

q = QuantumRegister(5,'q')
c = ClassicalRegister(5,'c')

circuit = QuantumCircuit(q,c)

circuit.x(q[4])
circuit.x(q[2])
circuit.x(q[0])
circuit.append(QFT(num_qubits=5, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name='qft'), q)
circuit.measure(q,c)
circuit.draw(output='mpl',filename='qft2.png')

print(circuit)

job = execute(circuit, backend, shots=1000)

job_monitor(job)

counts = job.result().get_counts()

print("\n QFT with inverse QFT Output")
print("------------------------------")
print(counts)
input()
"""

noise_error = """
from qiskit import QuantumCircuit, assemble, Aer, transpile
from qiskit.visualization import plot_histogram
from qiskit.ignis.mitigation.measurement import CompleteMeasFitter, complete_meas_cal, tensored_meas_cal

# Define the quantum circuit
qc = QuantumCircuit(3, 3)

# Apply gates and operations to the circuit
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)
qc.measure([0, 1, 2], [0, 1, 2])

# Transpile the circuit
backend = Aer.get_backend('qasm_simulator')
transpiled_qc = transpile(qc, backend)

# Simulate the noisy circuit
qobj = assemble(transpiled_qc, shots=1000)
job = backend.run(qobj)
result = job.result()
counts = result.get_counts()

# Perform error mitigation
cal_circuits, state_labels = complete_meas_cal(qubit_list=[0, 1, 2])
cal_job = backend.run(assemble(cal_circuits, backend=backend))
cal_results = cal_job.result()
meas_fitter = CompleteMeasFitter(cal_results, state_labels)
mitigated_counts = meas_fitter.filter.apply(counts)

# Print the original counts
print("Original counts:")
print(counts)

# Print the mitigated counts
print("Mitigated counts:")
print(mitigated_counts)

# Plot the histograms of the original and mitigated counts
plot_histogram([counts, mitigated_counts], legend=['Original', 'Mitigated'])
"""

quantum_teleportation = """
from qiskit import QuantumCircuit, transpile, assemble, Aer, execute

# Create a quantum circuit with three qubits: Alice's, Bob's, and the shared entangled qubit
q = QuantumCircuit(3, 3)

# Alice prepares the state to be teleported
q.h(0)  # Apply Hadamard gate to Alice's qubit
q.s(0)  # Apply S gate to Alice's qubit
q.barrier()

# Create entanglement between Alice's qubit (q1) and the shared qubit (q2)
q.h(1)  # Apply Hadamard gate to q2
q.cx(1, 2)  # Apply CNOT gate with q1 as the control and q2 as the target
q.barrier()

# Alice performs Bell measurement
q.cx(0, 1)  # Apply CNOT gate with q0 as the control and q1 as the target
q.h(0)  # Apply Hadamard gate to q0
q.measure(0, 0)  # Measure q0 and store the result in classical bit 0
q.measure(1, 1)  # Measure q1 and store the result in classical bit 1
q.barrier()

# Apply teleportation correction gates on Bob's qubit
q.x(2).c_if(0, 1)  # Apply X gate to q2 if the result of measurement 0 is 1
q.z(2).c_if(1, 1)  # Apply Z gate to q2 if the result of measurement 1 is 1
q.measure(2, 2)  # Measure q2 and store the result in classical bit 2

# Simulate the circuit
simulator = Aer.get_backend('qasm_simulator')
compiled_circuit = transpile(q, simulator)
job = execute(compiled_circuit, simulator, shots=1)
result = job.result()
counts = result.get_counts(q)

print("Quantum Teleportation Result:", counts)
"""

randomized_benchmarking_protocol = """
import numpy as np
from qiskit import QuantumCircuit, transpile, Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Generate a random quantum circuit
def generate_random_circuit(num_qubits, depth):
    circuit = QuantumCircuit(num_qubits, num_qubits)
    for _ in range(depth):
        for qubit in range(num_qubits):
            circuit.rx(np.random.uniform(0, 2 * np.pi), qubit)
            circuit.ry(np.random.uniform(0, 2 * np.pi), qubit)
            circuit.rz(np.random.uniform(0, 2 * np.pi), qubit)
        for qubit in range(num_qubits - 1):
            circuit.cz(qubit, qubit + 1)
    return circuit

# Perform randomized benchmarking
def randomized_benchmarking(num_qubits, depths, num_sequences, shots):
    backend = Aer.get_backend('statevector_simulator')
    results = []
    for depth in depths:
        success_counts = 0
        for _ in range(num_sequences):
            # Generate a random circuit and the corresponding inverse circuit
            circuit = generate_random_circuit(num_qubits, depth)
            inverse_circuit = circuit.inverse()

            # Apply the circuit and obtain the final statevector
            circuit_result = execute(circuit, backend=backend).result()
            final_statevector = circuit_result.get_statevector()

            # Apply the inverse circuit and obtain the final statevector
            inverse_result = execute(inverse_circuit, backend=backend).result()
            inverse_statevector = inverse_result.get_statevector()

            # Calculate the success rate based on state fidelity
            fidelity = np.abs(np.dot(final_statevector, inverse_statevector.conj())) ** 2
            success_counts += shots * (1 - fidelity)

        success_rate = success_counts / (num_sequences * shots)
        results.append(success_rate)
    return results

# Example usage
num_qubits = 2
depths = [1, 2, 3, 4]
num_sequences = 100
shots = 1024

results = randomized_benchmarking(num_qubits, depths, num_sequences, shots)
print(results)


plt.bar(depths, results)
plt.xlabel('Circuit Depth')
plt.ylabel('Success Rate')
plt.title('Randomized Benchmarking Results')
plt.xticks(depths)
plt.show()
"""

qubit_5_QFT = """
from qiskit import IBMQ

# Load IBM Quantum Experience account
IBMQ.enable_account('89450b58976ce1c7091a58b9612be3b845389d83091e1e526bf385a0b04a55a6c90d8c576894dd945c8722b0afc15663192646420a003f4257978aec56d64bde')

# Get the provider
provider = IBMQ.get_provider()

# Get the hub name
hub_name = provider.credentials.hub

# Print the hub name
print("Hub name:", hub_name)


from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, execute,IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.circuit.library import QFT
import numpy as np

pi = np.pi


provider = IBMQ.get_provider(hub='ibm-q')

backend = provider.get_backend('ibmq_qasm_simulator')

q = QuantumRegister(5,'q')
c = ClassicalRegister(5,'c')

circuit = QuantumCircuit(q,c)

circuit.x(q[4])
circuit.x(q[2])
circuit.x(q[0])
circuit.append(QFT(num_qubits=5, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name='qft'), q)
circuit.measure(q,c)
circuit.draw(output='mpl', filename='qft1.png')
print(circuit)

job = execute(circuit, backend, shots=1000)

job_monitor(job)

counts = job.result().get_counts()

print("\n QFT Output")
print("-------------")
print(counts)
input()

q = QuantumRegister(5,'q')
c = ClassicalRegister(5,'c')

circuit = QuantumCircuit(q,c)

circuit.x(q[4])
circuit.x(q[2])
circuit.x(q[0])
circuit.append(QFT(num_qubits=5, approximation_degree=0, do_swaps=True, inverse=False, insert_barriers=False, name='qft'), q)
circuit.measure(q,c)
circuit.draw(output='mpl',filename='qft2.png')

print(circuit)

job = execute(circuit, backend, shots=1000)

job_monitor(job)

counts = job.result().get_counts()

print("\n QFT with inverse QFT Output")
print("------------------------------")
print(counts)
input()
"""

preprocessing_text_doc = """
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Function for Part-of-Speech (POS) tagging
def perform_pos_tagging(text):
    # Tokenize the input text
    words = nltk.word_tokenize(text)
    # Perform POS tagging
    pos_tags = nltk.pos_tag(words)
    return pos_tags

# Function for tokenization
def tokenize_text(text):
    # Tokenize the input text
    words = word_tokenize(text)
    return words

# Function for lemmatization
def lemmatize_text(text):
    # Tokenize the input text
    words = word_tokenize(text)
    # Initialize a WordNet Lemmatizer
    lemmatizer = WordNetLemmatizer()
    # Apply lemmatization to each word
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    # Reconstruct the text with lemmatization
    result_text = ' '.join(lemmatized_words)
    return result_text

# Function for stop word removal
def remove_stopwords(text):
    # Tokenize the input text
    words = word_tokenize(text)
    # Define a list of English stopwords
    stop_words = set(stopwords.words('english'))
    # Remove stop words
    filtered_words = [word for word in words if word.lower() not in stop_words]
    # Reconstruct the text without stop words
    result_text = ' '.join(filtered_words)
    return result_text

# Function for stemming
def perform_stemming(text):
    # Tokenize the input text
    words = word_tokenize(text)
    # Initialize a Porter Stemmer
    stemmer = PorterStemmer()
    # Apply stemming to each word
    stemmed_words = [stemmer.stem(word) for word in words]
    # Reconstruct the text with stemming
    result_text = ' '.join(stemmed_words)
    return result_text

# Input text
input_text = "This is an example of a document for tokenization. This is an example document for POS tagging and stemming."

# Apply stop word removal
stopword_removed_text = remove_stopwords(input_text)

# Apply stemming
stemmed_text = perform_stemming(input_text)

# Tokenize the text
tokenized_text = tokenize_text(input_text)

# Lemmatize the text
lemmatized_text = lemmatize_text(input_text)

# Apply POS tagging
pos_tags_result = perform_pos_tagging(input_text)

# Display the results
print("Original Text:")
print(input_text)

print("\nAfter Stopword Removal:")
print(stopword_removed_text)

print("\nAfter Stemming:")
print(stemmed_text)

print("\nTokenized Text:")
print(tokenized_text)

print("\nLemmatized Text:")
print(lemmatized_text)

print("\nPOS Tagging Results:")
for word, pos_tag in pos_tags_result:
    print(f"{word}: {pos_tag}")

"""

retrieval_doc = """
import re
from collections import defaultdict

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(list)

    def add_document(self, doc_id, content):
        words = re.findall(r'\w+', content.lower())
        for word in words:
            self.index[word].append(doc_id)

    def search(self, query):
        query_terms = query.lower().split()
        if all(term in self.index for term in query_terms):
            result = set(self.index[query_terms[0]])
            for term in query_terms[1:]:
                result.intersection_update(self.index[term])
            return list(result)
        else:
            return []

    def print_term_document_matrix(self, documents):
        print("Term-Document Matrix:")
        for term, doc_ids in self.index.items():
            row = [1 if doc_id in doc_ids else 0 for doc_id in documents.keys()]
            print(f"{term}: {row}")

    def print_inverted_index(self):
        print("Inverted Index:")
        for term, doc_ids in self.index.items():
            print(f"{term}: {doc_ids}")

if __name__ == "__main__":
    # Sample documents
    documents = {
        1: "This is the first document.",
        2: "This document is the second document.",
        3: "And this is the third one.",
        4: "Is this the first document?"
    }

    # Create an inverted index
    index = InvertedIndex()
    for doc_id, content in documents.items():
        index.add_document(doc_id, content)

    # Print Term-Document Matrix and Inverted Index
    index.print_term_document_matrix(documents)
    print("\n-----------------------------------\n")
    index.print_inverted_index()
    print("\n-----------------------------------\n")

    # Perform a search
    query = input("Enter your search query: ")
    results = index.search(query)

    if results:
        print("Matching documents:")
        for doc_id in results:
            print(f"Document {doc_id}: {documents[doc_id]}")
    else:
        print("No matching documents found.")
"""

bayesian_network = """
import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

###################### DO NOT LOAD THIS DATA LINK DIRECTLY GO ON THIS LINK AND DOWNLOAD THE DATASET
data = pd.read_csv('https://raw.githubusercontent.com/abcxyz-0/prac/main/IR/heart.csv')
###################### DO NOT LOAD THIS DATA LINK DIRECTLY GO ON THIS LINK AND DOWNLOAD THE DATASET


# Define the Bayesian network structure
model = BayesianNetwork([('Age', 'HeartDisease'),
                         ('Sex', 'HeartDisease'),
                         ('ChestPainType', 'HeartDisease'),
                         ('RestingBP', 'HeartDisease'),
                         ('Cholesterol', 'HeartDisease'),
                         ('FastingBS', 'HeartDisease'),
                         ('RestingECG', 'HeartDisease'),
                         ('MaxHR', 'HeartDisease'),
                         ('ExerciseAngina', 'HeartDisease'),
                         ('Oldpeak', 'HeartDisease'),
                         ('ST_Slope', 'HeartDisease')])

# Estimate CPDs from data
model.fit(data, estimator=MaximumLikelihoodEstimator)

# Create an inference object
inference = VariableElimination(model)

# Provide evidence for diagnosis
evidence = {
    'Age': 40,
    'Sex': 'M',
    'ChestPainType': 'ATA',
    'RestingBP': 140,
    'Cholesterol': 289,
    'FastingBS': 0,
    'RestingECG': 'Normal',
    'MaxHR': 172,
    'ExerciseAngina': 'N',
    'Oldpeak': 0,
    'ST_Slope': 'Up'
}

# Query the model for the probability of Heart Disease
query_result = inference.query(variables=['HeartDisease'], evidence=evidence)
print(query_result)

# Diagnose the patient based on the probability
if query_result.values[1] > query_result.values[0]:
    print("The patient is likely to have Heart Disease.")
else:
    print("The patient is likely not to have Heart Disease.")
"""

agglomerative = """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, normalize
import scipy.cluster.hierarchy as shc

# Load the dataset from the given URL
url = 'https://raw.githubusercontent.com/RAHULKASHYAP02/Credit-Card-Segmentation/master/CC%20GENERAL.csv'
X = pd.read_csv(url)

# Drop the 'CUST_ID' column from the data
X = X.drop('CUST_ID', axis=1)

# Handle missing values by forward filling
X.fillna(method='ffill', inplace=True)

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Normalize the data
X_normalized = normalize(X_scaled)

# Convert the numpy array into a pandas DataFrame
X_normalized = pd.DataFrame(X_normalized)

# Perform PCA to reduce dimensionality
pca = PCA(n_components=2)
X_principal = pca.fit_transform(X_normalized)
X_principal = pd.DataFrame(X_principal)
X_principal.columns = ['P1', 'P2']

# Visualize the data using a dendrogram
plt.figure(figsize=(8, 8))
plt.title('Dendrogram')
dendrogram = shc.dendrogram(shc.linkage(X_principal, method='ward'))

# Implement Agglomerative Clustering with 2 clusters
ac2 = AgglomerativeClustering(n_clusters=2)

# Visualize the clusters using a scatter plot
plt.figure(figsize=(6, 6))
plt.scatter(X_principal['P1'], X_principal['P2'], c=ac2.fit_predict(X_principal), cmap='rainbow')
plt.title('Agglomerative Clustering')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()

"""

page_rank = """
import requests
from bs4 import BeautifulSoup
import networkx as nx
import pandas as pd

def get_links_from_wikipedia(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href.startswith('/wiki/') and ':' not in href:
            links.append(href)
    return links

def build_wikipedia_graph(start_url, max_depth, max_pages):
    G = nx.DiGraph()
    to_visit = [(start_url, 0)]
    visited = set()

    while to_visit:
        current_url, depth = to_visit.pop(0)

        if current_url not in visited and depth < max_depth:
            links = get_links_from_wikipedia("https://en.wikipedia.org" + current_url)
            visited.add(current_url)

            for link in links[:max_pages]:
                G.add_edge(current_url, link)
                to_visit.append((link, depth + 1))

    return G

def calculate_pagerank(graph):
    return nx.pagerank(graph)

start_url = "/wiki/PageRank"
max_depth = 2
max_pages = 10

graph = build_wikipedia_graph(start_url, max_depth, max_pages)
pagerank = calculate_pagerank(graph)

result_df = pd.DataFrame(pagerank.items(), columns=['Page', 'PageRank Score'])
result_df = result_df.sort_values(by='PageRank Score', ascending=False)

result_df

"""

dna_seq_analysis = """
import re

# Function to find motifs in a DNA sequence
def find_motifs(sequence, motif):
    matches = re.finditer(motif, sequence)
    positions = [match.start() for match in matches]
    return positions

# Function to calculate GC content in a DNA sequence
def calculate_gc_content(sequence):
    gc_count = sequence.count('G') + sequence.count('C')
    total_bases = len(sequence)
    gc_content = (gc_count / total_bases) * 100
    return gc_content

# Function to identify coding regions (example: start codon 'ATG' and stop codon 'TAA')
def identify_coding_regions(sequence):
    start_codon = 'ATG'
    stop_codon = 'TAA'
    coding_regions = []
    start_positions = find_motifs(sequence, start_codon)
    stop_positions = find_motifs(sequence, stop_codon)

    for start in start_positions:
        for stop in stop_positions:
            if stop > start and (stop - start) % 3 == 0:
                coding_regions.append((start, stop + 2))

    return coding_regions


# Example DNA sequence (replace with your own sequence)
dna_sequence = "ATGGCCTAAATGGGCTAA"

# Find motifs
motif_to_find = "ATG"
motifs_found = find_motifs(dna_sequence, motif_to_find)
print(f"Motifs found: {motifs_found}")

# Calculate GC content
gc_content = calculate_gc_content(dna_sequence)
print(f"GC content: {gc_content}%")

# Identify coding regions
coding_regions = identify_coding_regions(dna_sequence)
print(f"Coding regions: {coding_regions}")

"""

ml_genomic_data = """
# List available datasets
from genomic_benchmarks.data_check import list_datasets

list_datasets()

# Display information about the "human_nontata_promoters" dataset with version 0
from genomic_benchmarks.data_check import info

info("human_nontata_promoters", version=0)

# Load the "human_nontata_promoters" dataset for training and testing
from genomic_benchmarks.dataset_getters.pytorch_datasets import HumanNontataPromoters

train = HumanNontataPromoters(split='train', version=0)
test = HumanNontataPromoters(split='test', version=0)

# Access a specific example from the training dataset (e.g., the 3000th sample)
train[3000]

import numpy as np

# Define a mapping of DNA bases to one-hot encoding
base_to_index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

# Function to one-hot encode a DNA sequence, treating 'N' as missing data
def one_hot_encode(sequence, seq_length):
    encoded_sequence = np.zeros((seq_length, 4), dtype=int)
    for i, base in enumerate(sequence):
        if base in base_to_index:
            # Set the corresponding index to 1 for valid bases (A, C, G, T)
            encoded_sequence[i, base_to_index[base]] = 1
        else:
            # Treat 'N' as missing data (all zeros)
            encoded_sequence[i, :] = 0
    return encoded_sequence

# Apply one-hot encoding to the entire training and testing datasets
train_encoded = [one_hot_encode(item[0], len(item[0])) for item in train]
test_encoded = [one_hot_encode(item[0], len(item[0])) for item in test]

# Access the one-hot encoded sequence of the first sample in the training dataset
train_encoded[0]

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Extract labels from the training and testing datasets
train_labels = [item[1] for item in train]
test_labels = [item[1] for item in test]

# Reshape the one-hot encoded sequences into a two-dimensional format
train_encoded = np.array(train_encoded).reshape(len(train_encoded), -1)
test_encoded = np.array(test_encoded).reshape(len(test_encoded), -1)

# 2. Choose an Algorithm (Random Forest)
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# 3. Training the Model
rf_classifier.fit(train_encoded, train_labels)

# 4. Model Evaluation
predictions = rf_classifier.predict(test_encoded)
accuracy = accuracy_score(test_labels, predictions)
report = classification_report(test_labels, predictions)

print(f"Accuracy: {accuracy}")
print("Classification Report:\n", report)

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Create a confusion matrix for the Random Forest classifier
rf_cm = confusion_matrix(test_labels, predictions)

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(rf_cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Random Forest Confusion Matrix')
plt.show()


from sklearn.metrics import roc_curve, roc_auc_score

# Calculate ROC curve for Random Forest
rf_probs = rf_classifier.predict_proba(test_encoded)[:, 1]
rf_fpr, rf_tpr, _ = roc_curve(test_labels, rf_probs)

# Plot ROC curve
plt.figure(figsize=(8, 6))
plt.plot(rf_fpr, rf_tpr, marker='.')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Random Forest ROC Curve')
plt.show()

"""

masterDict = {
    'qubit_16_bit_generator':qubit_16_bit_generator,
    'noise_error': noise_error,
    'quantum_teleportation': quantum_teleportation,
    'randomized_benchmarking_protocol': randomized_benchmarking_protocol,
    'qubit_5_QFT': qubit_5_QFT,

    'preprocessing_text_doc': preprocessing_text_doc,
    'retrieval_doc': retrieval_doc,
    'bayesian_network': bayesian_network,
    'agglomerative': agglomerative,
    'page_rank': page_rank,

    'dna_seq_analysis': dna_seq_analysis,
    'ml_genomic_data': ml_genomic_data,
}

class Writer:
    def __init__(self, filename):
        self.filename = os.path.join(os.getcwd(), filename)
        self.masterDict = masterDict
        self.questions = list(masterDict.keys())

    def getCode(self, input_string):
        input_string = self.masterDict[input_string]
        with open(self.filename, 'w') as file:
            file.write(input_string)
        print(f'##############################################')

if __name__ == '__main__':
    write = Writer('output.txt')
    # print(write.questions)
    write.getCode('qubit_16_bit_generator')