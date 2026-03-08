def aggregate_signals(results):

    aggregated = {}

    for result in results:
        if not isinstance(result, dict):
            continue

        for key, value in result.items():
            if not value:
                continue
            if key not in aggregated:
                aggregated[key] = []
            if isinstance(value, list):
                aggregated[key].extend(value)
            else:
                aggregated[key].append(value)
        
        for key in aggregated:
            aggregated[key] = list(set(aggregated[key]))
        
        return aggregated