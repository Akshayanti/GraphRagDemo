import argparse

from bin.CVEDataFilter import CVEDataFilter
from bin.KnowledgeBaseCreator import KnowledgeBaseCreator


def get_kb(input_directory, output_directory, model="llama3.2:1b"):
    # Step 1: Filter the data
    data_filter = CVEDataFilter(
        input_directory=input_directory, output_directory=output_directory
    )
    data_filter.filter_jsons()
    latest_cves = list(data_filter.get_latest_cve_ids())
    doc = (
        latest_cves[0] if latest_cves != [] else list(data_filter.get_all_cve_ids())[0]
    )

    # Step 2: Process the filtered data and create the knowledge base
    kb_creator = KnowledgeBaseCreator(output_directory=output_directory, model=model)
    return kb_creator, doc


def main(input_directory, output_directory):
    graph_file = "graph_store.pkl"
    kb, cve = get_kb(input_directory, output_directory)
    kb.create_knowledge_base()
    kb.pickle_graph_store(graph_file)

    # Step 3: Test the knowledge base
    evaluate(kb, cve)
    print()

    # Demo Time
    while True:
        cve = input("Enter a CVE ID (CVE-YYYY-XXXX): ")
        evaluate(kb, cve)
        print()


def evaluate(kb, cve):
    question = f"Tell me about the vulnerability: {cve}"

    graph_chain = kb.get_graph_chain()
    best_graph_chain = kb.get_best_graph_chain()

    result_before = kb.get_simple_chain().run({"query": question})
    result_after = graph_chain.run({"query": question, "context": kb.get_graph()})
    result_after_bp = best_graph_chain.run(
        {"query": question, "context": kb.get_best_graph()}
    )

    print("**************** BEFORE GRAPHING: ****************")
    print(result_before)
    print("**************** AFTER GRAPHING: *****************")
    print(result_after)
    print("**************** AFTER GRAPHING (Best Performance): *****************")
    print(result_after_bp)
    print("***********************************************************************")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process CVE data and create a knowledge base."
    )
    parser.add_argument(
        "--input_directory",
        type=str,
        required=True,
        help="Directory containing input JSON files.",
    )
    parser.add_argument(
        "--output_directory",
        type=str,
        required=True,
        help="Directory to save filtered JSON files.",
    )
    parser.add_argument(
        "--show_graph",
        action="store_true",
        help="Flag to create and save the graph visualization.",
    )

    args = parser.parse_args()
    main(args.input_directory, args.output_directory)
