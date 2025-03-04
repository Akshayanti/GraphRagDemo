# Graph RAG Demo

## Overview

This project processes CVE (Common Vulnerabilities and Exposures) data to create a knowledge base using a graph-based QA system. The system extracts relevant entities and answers questions related to cybersecurity vulnerabilities.
The dataset can be found [here](https://nvd.nist.gov/vuln/data-feeds#APIS).

## Directory Structure

- `bin/`: Contains the main processing scripts.
  - `CVEDataFilter.py`: Filters the large chunky json files into smaller json, extracting only relevant info.
  - `CVEDataProcessor.py`: Processes the filtered data and creates Graph Document for each document.
  - `KnowledgeBaseCreator.py`: Creates the knowledge base from the filtered data.
  - `GraphViewer.py`: Visualizes the knowledge base in a graphical format
- `data/`: Contains the input and output data.
  - `json/`: Directory for storing raw JSON files, downloaded from the link.
  - `text/`: Directory for storing text files, preferably ending in *.txt
- `lib`: Contains the binaries required for viewing the graph
- `results/`: Contains some output files generated by the scripts
- `main.py`: Main script to run the entire pipeline

## Usage

### Prerequisites

- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`)
- Ollama Installed on local machine, especially llama3.2:1b model (instructions [here](https://www.hostinger.com/tutorials/ollama-cli-tutorial#Setting_up_Ollama_in_the_CLI))

### Steps to Run the Project

1.  **Run the Main Script**:
   - Execute the `main.py` script to process the CVE data, create the knowledge base
   - Example:
     ```sh
     python main.py --input_directory <input_directory> --output_directory <output_directory>
     ```
   - While there is `--show_graph` flag to visualize the graph, it is recommended to not use the flag as generation of a graph can take upto 20 minutes per document.
   - There is an example graph saved in `results` directory.

### Example Usage

```sh
python main.py --input_directory data/json --output_directory data/filtered_jsons
```

## Learnings

- While GraphRAG is a powerful tool, it is computationally expensive to generate graphs for large documents.
- The graph generated is not very intuitive and requires a lot of manual effort to understand the relationships.
- The graph can be used to answer questions related to the document, but the answers are not always accurate.
- The graph can be used to identify relationships between entities, but it is not very useful for understanding the document as a whole.
- The choice of QA prompt and Entity Extraction Prompt while creating the knowledge base is crucial for generating accurate answers.
- As always, prompt engineering is key to generating accurate answers.
