from typing import List, Optional
import networkx as nx


def get_tags(resource_name: str,
             resource_type: Optional[str] = 'model',
             package: Optional[str] = 'dave',
             graph_file: Optional[str] = '../target/graph.gpickle') -> List[
    str]:
    """
    Returns all upstream tags for a resource in a dbt project
    :param resource_name: name of the resource (eg. your model name)
    :param resource_type: type of the resource (default: model)
    :param package: name of the package (default: dave)
    :param graph_file: path to the graph file (default: ../target/graph.gpickle)

    :return: list of tags
    """
    g = nx.read_gpickle(graph_file)
    # create fully qualified resource_id: https://docs.getdbt.com/reference/artifacts/manifest-json#resource-details
    resource_id = '.'.join([resource_type, package, resource_name])
    desc = nx.descendants(g.reverse(), resource_id)

    tags = set()
    for node_id in desc:
        tags = tags.union(set(g.nodes.get(node_id).get('tags')))
    return list(tags)
