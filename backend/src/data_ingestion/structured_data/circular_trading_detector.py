import networkx as nx

def detect_circular_trading(gst_records):
    graph = nx.DiGraph()

    for record in gst_records:
        seller = record.get("seller_gstin")
        buyer= record.get("buyer_gstin")

        if seller and buyer:
            graph.add_edge(seller, buyer)
    
    cycles = list(nx.simple_cycles(graph))

    return {
        "circular_trading_detected": len(cycles) > 0,
        "cycles": cycles
    }