import os

base_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_dir, "ocorrencias2024.csv")
output_path = os.path.join(base_dir, "ocorrencias2024_limpas.csv")

with open(input_path, encoding="utf-8") as fin, open(output_path, "w", encoding="utf-8") as fout:
    header = fin.readline()
    fout.write(header)
    n_cols = header.count(";")
    for line in fin:
        # Remove quebras de linha internas
        line = line.replace("\n", "")
        # Conta separadores
        parts = line.split(";")
        if len(parts) < n_cols + 1:
            continue  # descarta linhas incompletas
        if len(parts) > n_cols + 1:
            parts = parts[:n_cols + 1]  # trunca para o número correto de colunas
        fout.write(";".join(parts) + "\n")
