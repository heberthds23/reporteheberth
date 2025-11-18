import pandas as pd

def export_document_to_excel(meta: dict, output_path: str):
    rows = meta.get('rows', [])
    df = pd.DataFrame(rows)
    df.to_excel(output_path, index=False)
    return output_path
