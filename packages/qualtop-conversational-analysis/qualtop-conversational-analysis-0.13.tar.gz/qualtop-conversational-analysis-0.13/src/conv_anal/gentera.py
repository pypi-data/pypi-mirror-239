import csv

def generate_db_summaries(gentera_csv="./conv_anal/data/gentera/gentera.csv", 
                          gentera_schema="./conv_anal/data/gentera/gentera_schema.csv", fine_grain=False):
    relationships = []
    columns = []
    with open(gentera_schema, newline="") as csvfile:
        schema_reader = csv.reader(csvfile, delimiter=",")
        for row in schema_reader:
            columns.append(row[0])
            relationships.append(row[1])

    text_summaries = []
    fine_grain_info = []
    graph_triplets = []
    with open(gentera_csv, newline="") as csvfile:
        data_reader = csv.reader(csvfile, delimiter=",")
        first_row = True
        total_employees = 0
        for row in data_reader:
            if first_row:
                first_row=False
                continue
            total_employees += 1
            text_summary = ""
            # Generate text summary
            name = row[1]
            for i in range(2,len(row)):
                if row[i] == "" or row[i] == "N/A" or row[i] == " " or row[i] == "NA":
                    continue
                if i == 4: # rh position
                    text_summary += f"{name} {relationships[i]} '{row[i]}' para Recursos Humanos (RH). "
                    fine_grain_info.append(f"{name} {relationships[i]} '{row[i]}' para Recursos Humanos (RH). ")
                    graph_triplets.append((f"{name}", f"{relationships[i]}", f"{row[i]} para Recursos Humanos (RH)"))
                elif i == 21: # leader position
                    if row[16] == "" or row[16] == "N/A" or row[16] == " " or row[16] == "NA":
                        text_summary += f"{row[16]} {relationships[i]} '{row[i]}'. "
                        fine_grain_info.append(f"{row[16]} {relationships[i]} '{row[i]}'. ")
                        graph_triplets.append((f"{row[16]}", f"{relationships[i]}", f"{row[i]}"))
                elif i == 22: # organizational structure
                    pass
                elif i == 30:
                    text_summary += f"{relationships[i]} sobre {name}: {row[30]}"
                    fine_grain_info.append(f"{relationships[i]} sobre {name}: {row[30]}")
                    graph_triplets.append((f"{name}", f"relationships[i]", f"{row[i]}"))
                else:
                    text_summary += f"{name} {relationships[i]} '{row[i]}'. "
                    fine_grain_info.append(f"{name} {relationships[i]} '{row[i]}'. ")
                    graph_triplets.append((f"{name}", f"{relationships[i]}", f"{row[i]}"))
            text_summaries.append(text_summary)
        # Additional data
        text_summaries.append(f"Hay {total_employees} empleados en la base de datos. ")
        fine_grain_info.append(f"Hay {total_employees} empleados en la base de datos. ")
        graph_triplets.append((f"La base de datos", f"tiene", f"{total_employees} empleados"))

    if fine_grain:
        return fine_grain_info, graph_triplets
    return text_summaries, graph_triplets

def generate_db_row_based_summaries(gentera_csv="./conv_anal/data/gentera/gentera.csv", 
                                    gentera_schema="./conv_anal/data/gentera/gentera_schema_meanings.csv"):
    schema_meanings = []
    meanings = []
    with open(gentera_schema, newline="") as csvfile:
        schema_reader = csv.reader(csvfile, delimiter=",")
        for row in schema_reader:
            schema_meanings.append((row[0], row[1]))
            meanings.append(row[1])
    meaning_lookup = dict(schema_meanings)
    
    text_summaries = []
    with open(gentera_csv, newline="") as csvfile:
        data_reader = csv.reader(csvfile, delimiter=",")
        first_row = True
        total_employees = 0
        for row in data_reader:
            if first_row:
                first_row=False
                continue
            total_employees += 1
            text_summary = f""
            # Generate text summary
            text_summary += f'\n{row[1]}:\n"""\n' #name
            for i in range(2,len(row)):
                if meanings[i] == "":
                    continue
                text_summary += f'\t{meanings[i]}: {row[i]}\n'
            text_summary += '"""'
            text_summaries.append(text_summary)
    
    # Additional data
    text_summaries.append(f"Hay {total_employees} colaboradores en la base de datos. ")
    return text_summaries

if __name__ == "__main__":
    generate_db_row_based_summaries()
