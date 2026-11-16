
import os
import json
import csv
import pickle

current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_dir)
data_path = os.path.join(base_dir, "data")
os.makedirs(data_path, exist_ok=True)

p_count = 1
total_information = []

# AI 사용


class HealthRecord:
    def __init__(self, id, name, birth_year, gender, height, weight):
        self.id = id
        self.name = name
        self.birth_year = birth_year
        self.gender = gender
        self.height = height
        self.weight = weight

        self.BMI = round(weight / (height / 100) ** 2, 2)

        if self.BMI < 18.5:
            self.status = "저체중"
        elif self.BMI < 23:
            self.status = "정상"
        elif self.BMI < 25:
            self.status = "과체중"
        else:
            self.status = "비만"

    def to_dict(self):
        return self.__dict__


class HealthDB:
    def add_record(self, name, birth_year, gender, height, weight):
        global p_count

        record = HealthRecord(
            f"P2026-{p_count:04d}",
            name, birth_year, gender, height, weight
        )

        total_information.append(record.to_dict())
        p_count += 1

    def save(self):
        try:
            with open(os.path.join(data_path, "health_data.json"), "w", encoding="utf-8") as f:
                json.dump(total_information, f, ensure_ascii=False, indent=4)

            with open(os.path.join(data_path, "health_data.csv"), "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(total_information[0].keys())

                for info in total_information:
                    writer.writerow(info.values())

            with open(os.path.join(data_path, "health_data.txt"), "w", encoding="utf-8") as f:
                for info in total_information:
                    f.write(",".join(map(str, info.values())) + "\n")

            with open(os.path.join(data_path, "health_data.pkl"), "wb") as f:
                pickle.dump(total_information, f)

            print("저장 완료")

        except (OSError, IndexError) as e:
            print("저장 오류:", e)

    def load(self, file_type):
        try:
            file_path = os.path.join(data_path, "health_data." + file_type)

            if file_type == "json":
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

            elif file_type == "csv":
                with open(file_path, "r", encoding="utf-8-sig") as f:
                    data = list(csv.DictReader(f))

            elif file_type == "txt":
                with open(file_path, "r", encoding="utf-8") as f:
                    data = [line.strip().split(",") for line in f]

            elif file_type == "pkl":
                with open(file_path, "rb") as f:
                    data = pickle.load(f)

            else:
                print("지원하지 않는 파일 형식입니다.")
                return

            print(data)
            return data

        except FileNotFoundError:
            print("파일이 없습니다.")
        except (OSError, ValueError, csv.Error, pickle.UnpicklingError) as e:
            print("불러오기 오류:", e)


if __name__ == "__main__":
    db = HealthDB()

    db.add_record("홍길동", 1995, "남", 175, 72)
    db.add_record("김영희", 1998, "여", 162, 52)

    db.save()
    db.load("json")
