import pandas as pd



def Read(file="2E SEC SEATING.xlsx") -> dict:
    data = pd.read_excel(file)
    marks_dict = {}
    student_name = data["Unnamed: 2"]
    student_id = data["Unnamed: 1"]
    for _, std_id in enumerate(student_id):
        if _ >= 2:
            marks_dict[std_id] = [student_name[_],]
    return marks_dict

print(Read())