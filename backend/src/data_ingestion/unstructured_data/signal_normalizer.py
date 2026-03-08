def normalize_signals(signals, document_type=None):

    normalized = {}

    for key, values in signals.items():
        cleaned = []

        for value in values:
            if isinstance(value, dict):
                item = value.copy()

                if "description" not in item:
                    item["description"] = str(value)
                if document_type:
                    item["source"] = document_type
                
                cleaned.append(item)

            elif isinstance(value, str):
                cleaned.append({
                    "description": value,
                    "source": document_type
                })

        seen = set()
        unique = []
        for item in cleaned:
            desc = item["description"]
            
            if desc not in seen:
                seen.add(desc)
                unique.append(item)
        
        normalized[key] = unique
    return normalized