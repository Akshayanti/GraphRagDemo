import glob
import json
import os
from typing import List, Dict
from langchain.schema import Document


class CVEDataProcessor:
    def __init__(self, output_directory: str):
        self.output_directory = output_directory

    def load_json_files(self) -> List[Dict]:
        json_files = glob.glob(os.path.join(self.output_directory, "*.json"))
        documents = []
        for json_file in json_files:
            with open(json_file, "r") as file:
                data = json.load(file)
                documents.append(data)
        return documents

    def transform_to_graph_documents(self, documents: List[Dict]) -> List[Document]:
        graph_documents = []
        for doc in documents:
            for cve in doc.get("CVEs", []):
                cve_id = cve.get("cve_id", "")
                description = (
                    cve.get("description", "").replace("\n", " ").replace("\r", " ")
                )
                impact = cve.get("impact_score", "")
                published_date = cve.get("published_date", "")
                assigner = cve.get("assigner", "")
                problemtype_descriptions = cve.get("problemtype_descriptions", [])
                metadata = {
                    "id": cve_id,
                    "Description": description,
                    "Impact": impact,
                    "PublishedDate": published_date,
                    "Assigner": assigner,
                    "ProblemType": problemtype_descriptions,
                }
                graph_document = Document(page_content=description, metadata=metadata)
                graph_documents.append(graph_document)
        return graph_documents

    def convert(self) -> List[Document]:
        documents = self.load_json_files()
        graph_documents = self.transform_to_graph_documents(documents)
        return graph_documents
