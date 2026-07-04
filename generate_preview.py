import pandas as pd

df = pd.read_parquet('data/zomato_cleaned.parquet')

with open('preview.txt', 'w', encoding='utf-8') as f:
    f.write("# Data Preview: `zomato_cleaned.parquet`\n\n")

    f.write("## Schema\n")
    f.write("| Column | Type |\n")
    f.write("|--------|------|\n")
    for col, dtype in zip(df.columns, df.dtypes):
        f.write(f"| {col} | {dtype} |\n")
    f.write("\n")

    f.write("## Sample Data (Top 5 Rows)\n")
    cols = df.columns
    f.write("| " + " | ".join(cols) + " |\n")
    f.write("|" + "|".join(["---"] * len(cols)) + "|\n")

    for _, row in df.head(5).iterrows():
        # Convert lists or complex types to string and escape pipes
        row_str = [str(x).replace("|", "\\|").replace("\n", " ") for x in row]
        f.write("| " + " | ".join(row_str) + " |\n")
