import json

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
        unique_items = []
        seen = set()
        for item in aggregated[key]:
            if isinstance(item, dict):
                item_str = json.dumps(item, sort_keys=True)
                if item_str not in seen:
                    seen.add(item_str)
                    unique_items.append(item)
            else:
                if item not in seen:
                    seen.add(item)
                    unique_items.append(item)
        aggregated[key] = unique_items
        
    return aggregated