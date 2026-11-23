# AI 사용 


import health_db as db
import csv


class HealthLogic:
    def __init__(self, manager):
        self.manager = manager

    # BMI 계산
    def calculate_bmi(self, height, weight):
        if height <= 0 or weight <= 0:
            raise ValueError("잘못된 입력입니다.")

        bmi = round(weight / (height / 100) ** 2, 2)

        if bmi < 18.5:
            status = "저체중"
        elif bmi < 23:
            status = "정상"
        elif bmi < 25:
            status = "과체중"
        else:
            status = "비만"

        return bmi, status

    # 정보 등록 및 중복 검사
    def add_patient(self, name, year, gender, height, weight):
        for p in db.total_information:
            if p["name"] == name and p["birth_year"] == int(year):
                return False

        self.calculate_bmi(float(height), float(weight))
        self.manager.add_record(
            name, int(year), gender, float(height), float(weight)
        )
        db.save()
        return True

    # CSV 등록
    def add_csv(self, path):
        count = 0
        try:
            with open(path, encoding="utf-8-sig") as f:
                for p in csv.DictReader(f):
                    if self.add_patient(
                        p["name"], p["birth_year"], p["gender"],
                        p["height"], p["weight"]
                    ):
                        count += 1
            return count
        except (OSError, KeyError, ValueError) as e:
            print("파일 오류:", e)
            return 0

    # 전체 조회 및 검색
    def get_all(self):
        return db.total_information

    def search_patient(self, keyword):
        return [p for p in db.total_information
                if keyword in str(p["name"])
                or keyword in str(p["id"])]

    # 정보 수정
    def update_patient(self, patient_id, height, weight):
        for p in db.total_information:
            if p["id"] == patient_id:
                p["height"] = float(height)
                p["weight"] = float(weight)
                p["bmi"], p["status"] = self.calculate_bmi(
                    float(height), float(weight)
                )
                db.save()
                return True
        return False

    # 정보 삭제
    def delete_patient(self, patient_id):
        for p in db.total_information:
            if p["id"] == patient_id:
                db.total_information.remove(p)
                db.save()
                return True
        return False

    # 통계
    def get_statistics(self):
        data = db.total_information
        if not data:
            return {"인원수": 0, "평균 키": 0,
                    "평균 몸무게": 0, "평균 BMI": 0}

        n = len(data)
        return {
            "인원수": n,
            "평균 키": round(sum(p["height"] for p in data) / n, 2),
            "평균 몸무게": round(sum(p["weight"] for p in data) / n, 2),
            "평균 BMI": round(sum(p["bmi"] for p in data) / n, 2)
        }


# 콘솔 테스트
if __name__ == "__main__":
    db.load()
    logic = HealthLogic(db.HealthDB())

    while True:
        print("\n1.등록  2.조회  3.검색  4.수정  5.삭제  6.통계  0.종료")
        choice = input("선택: ")

        try:
            if choice == "1":
                name = input("이름: ")
                year = int(input("생년: "))
                gender = input("성별: ")
                height = float(input("키: "))
                weight = float(input("몸무게: "))
                print("등록 완료" if logic.add_patient(
                    name, year, gender, height, weight
                ) else "중복 정보")

            elif choice == "2":
                print(logic.get_all())

            elif choice == "3":
                print(logic.search_patient(input("이름 또는 ID: ")))

            elif choice == "4":
                print(logic.update_patient(
                    input("ID: "), float(input("키: ")),
                    float(input("몸무게: "))
                ))

            elif choice == "5":
                print(logic.delete_patient(input("삭제할 ID: ")))

            elif choice == "6":
                print(logic.get_statistics())

            elif choice == "0":
                break

        except (ValueError, TypeError) as e:
            print("입력 오류:", e)
