import pickle
import networkx as nx
import plotly.graph_objects as go
from tqdm import tqdm

class GraphViewer:
    def __init__(self, graph_file):
        self.graph_file = graph_file
        self.graph = self.load_graph()

    def load_graph(self):
        with open(self.graph_file, "rb") as f:
            return pickle.load(f)

    def plot_graph(self, output_file="graph.html"):
        pos = nx.spring_layout(self.graph, iterations=25)
        edge_x = []
        edge_y = []
        for edge in tqdm(self.graph.edges(), desc="Adding edges"):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        for node in tqdm(self.graph.nodes(), desc="Adding nodes"):
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=2,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                ),
            ))

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Graph Visualization',
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=0, l=0, r=0, t=0),
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False))
                        )

        fig.write_html(output_file)

if __name__ == "__main__":
    viewer = GraphViewer("../graph_store.pkl")
    print("Plotting graph...")
    viewer.plot_graph()