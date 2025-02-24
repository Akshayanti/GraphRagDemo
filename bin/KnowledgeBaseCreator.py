import logging
import pickle

import networkx as nx
import tqdm
from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain_community.chains.graph_qa.base import GraphQAChain
from langchain_community.graphs import NetworkxEntityGraph
from langchain_core.prompts import PromptTemplate
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_ollama import ChatOllama

from bin.CVEDataProcessor import CVEDataProcessor


class KnowledgeBaseCreator:
    def __init__(self, output_directory: str, model: str):
        load_dotenv()
        self.llm = ChatOllama(model=model)
        self.llm_transformer = LLMGraphTransformer(llm=self.llm)
        self.graph_store = nx.DiGraph()
        self.processor = CVEDataProcessor(output_directory=output_directory)
        logging.basicConfig(level=logging.INFO)

    def create_knowledge_base(self):
        graph_documents = self.processor.process()

        for graph_document in tqdm.tqdm(
            graph_documents, desc="Creating Knowledge Base"
        ):
            logging.debug("\nProcessing New Graph Document")
            node_id = graph_document.metadata.get("id", "unknown")
            logging.debug(
                f"Adding node: {node_id} with metadata: {graph_document.metadata}"
            )
            self.graph_store.add_node(node_id, **graph_document.metadata)

            description = graph_document.metadata.get("Description", "unknown")
            logging.debug(
                f"Adding edge from {node_id} to {description} with relation 'has_description'"
            )
            self.graph_store.add_edge(node_id, description, relation="has_description")

            impact = graph_document.metadata.get("Impact", "unknown")
            logging.debug(
                f"Adding edge from {node_id} to {impact} with relation 'has_impact'"
            )
            self.graph_store.add_edge(node_id, impact, relation="has_impact")

            published_date = graph_document.metadata.get("PublishedDate", "unknown")
            logging.debug(
                f"Adding edge from {node_id} to {published_date} with relation 'published_on'"
            )
            self.graph_store.add_edge(node_id, published_date, relation="published_on")

            assigner = graph_document.metadata.get("Assigner", "unknown")
            logging.debug(
                f"Adding edge from {node_id} to {assigner} with relation 'assigner'"
            )
            self.graph_store.add_edge(node_id, assigner, relation="assigner")

            for problemtype in graph_document.metadata.get("ProblemType", []):
                logging.debug(
                    f"Adding edge from {node_id} to {problemtype} with relation 'problem_type'"
                )
                self.graph_store.add_edge(node_id, problemtype, relation="problem_type")

    def pickle_graph_store(self, file_path: str):
        with open(file_path, "wb") as ofile:
            pickle.dump(self.graph_store, ofile)

    def get_graph(self):
        return self.graph_store

    def get_good_graph(self):
        with open("results/graph_store.pkl", "rb") as f:
            self.graph_store = pickle.load(f)
        return self.graph_store

    def get_graph_chain(self):
        return GraphQAChain.from_llm(
            llm=self.llm, graph=NetworkxEntityGraph(self.graph_store), verbose=True
        )

    def get_simple_chain(self):
        prompt_template = PromptTemplate(
            input_variables=["query"], template="Q: {query}\nA:"
        )
        return LLMChain(llm=self.llm, prompt=prompt_template)


# Example usage
if __name__ == "__main__":
    kb_creator = KnowledgeBaseCreator(
        output_directory="./filtered_jsons", model="llama3.2:1b"
    )
    kb_creator.create_knowledge_base()
    kb_creator.pickle_graph_store("graph_store.pkl")
