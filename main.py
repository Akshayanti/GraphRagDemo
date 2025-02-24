import argparse

from bin.CVEDataFilter import CVEDataFilter
from bin.KnowledgeBaseCreator import KnowledgeBaseCreator


def main(input_directory, output_directory):
    model = "llama3.2:1b"
    graph_file = "graph_store.pkl"

    # Step 1: Filter the data
    data_filter = CVEDataFilter(input_directory=input_directory, output_directory=output_directory)
    data_filter.process_files()
    latest_cves = list(data_filter.get_latest_cve_ids())

    # Step 2: Process the filtered data and create the knowledge base
    kb_creator = KnowledgeBaseCreator(output_directory=output_directory, model=model)
    kb_creator.create_knowledge_base()
    kb_creator.pickle_graph_store(graph_file)
    graph_chain = kb_creator.get_graph_chain()
    simple_qa_chain = kb_creator.get_simple_chain()
    doc = latest_cves[0]
    question = f"Tell me about the vulnerability: {doc}"
    result_before = simple_qa_chain.run({"query": question})
    result_after = graph_chain.run({"query": question, "context": kb_creator.get_graph()})
    result_after_bp = graph_chain.run({"query": question, "context": kb_creator.get_good_graph()})
    print("**************** BEFORE GRAPHING: ****************")
    print(result_before)
    print("**************** AFTER GRAPHING: *****************")
    print(result_after)
    print("**************** AFTER GRAPHING (Best Performance): *****************")
    print(result_after_bp)
    with open("before_json.txt", "w") as f:
        f.write(result_before)
    with open("after_json.txt", "w") as f:
        f.write(result_after)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CVE data and create a knowledge base.")
    parser.add_argument("--input_directory", type=str, required=True, help="Directory containing input JSON files.")
    parser.add_argument("--output_directory", type=str, required=True, help="Directory to save filtered JSON files.")
    parser.add_argument("--show_graph", action="store_true", help="Flag to create and save the graph visualization.")

    args = parser.parse_args()
    main(args.input_directory, args.output_directory)