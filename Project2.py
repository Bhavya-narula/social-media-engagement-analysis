# Name : Bhavya         ID : 24253549
def is_numeric(data):
    if data.isdigit():
        return True
    elif data.replace('.', '', 1).isdigit():
        return True
    elif data.lstrip('-').isdigit():
        return True
    else:
        return False


def is_valid_row(row, columns):
    if row is None or columns is None:
        return False
    id_index = columns.index("id")
    age_index = columns.index("age")
    time_spent_hour_index = columns.index("time_spent_hour")
    engagement_score_index = columns.index("engagement_score")
    income_index = columns.index("income")
    row_data = row.split(",")
    row_data = [r.strip() for r in row_data]

    if len(row_data) != len(columns):
        return False
    for data in row_data:
        if data is None or data.strip() == "":
            return False
    if not str(row_data[id_index]).isalnum():
        return False

    if not is_numeric(row_data[age_index]) or int(row_data[age_index]) < 0:
        return False

    if not is_numeric(row_data[engagement_score_index]) or float(row_data[engagement_score_index]) < 0:
        return False

    if not is_numeric(row_data[time_spent_hour_index]) or float(row_data[time_spent_hour_index]) < 0:
        return False

    if not is_numeric(row_data[income_index]) or float(row_data[income_index]) < 0:
        return False
    return True


def cal_total(any_list):
    total_value = 0.0
    if any_list is not None:
        for value in any_list:
            total_value += value
    return total_value


def cal_avg(any_list):
    result = 0.0
    if any_list is not None:
        n = len(any_list)
        total = 0
        for value in any_list:
            total += value
        if n > 0:
            result = total / n
    return result


def cal_std(any_list):
    result = 0.0
    if any_list is not None:
        avg_value = cal_avg(any_list)
        n = len(any_list)
        total_minus_mean = 0
        for value in any_list:
            total_minus_mean += (value - avg_value) ** 2
        if n > 1:
            result = (total_minus_mean / (n - 1)) ** 0.5
    return result


def find_cosine_similarity(group1, group2):
    score = 0.0
    if group1 is None or group2 is None:
        return score
    if len(group1) != len(group2):
        return score
    numerator = 0.0
    demo1 = 0.0
    demo2 = 0.0
    for i in range(len(group1)):
        numerator += group1[i]*group2[i]
        demo1 += group1[i] * group1[i]
        demo2 += group2[i] * group2[i]
    denominator = (demo1 ** 0.5) * (demo2 ** 0.5)
    if denominator > 0:
        score = numerator/denominator
    return score


def find_cohen_d_score(group1, group2):
    if group1 is None or group2 is None:
        return 0.0

    n1 = len(group1)
    n2 = len(group2)
    mean1 = cal_avg(group1)
    mean2 = cal_avg(group2)
    s1 = cal_std(group1)
    s2 = cal_std(group2)
    s = (((n1 - 1) * s1 * s1 + (n2 - 1) * s2 * s2) / (n1 + n2 - 2)) ** 0.5
    if s > 0:
        return (mean1 - mean2) / s
    else:
        return 0.0


def cal_engagement_time(time_spent_hour, engagement_score):
    return (time_spent_hour * engagement_score) / 100


def main(csvfile):
    OP1 = [{}, {}]
    OP2 = {}
    dataset = []
    ids = []
    platform_wise = {}
    student_age = []
    student_income = []
    non_student_age = []
    non_student_income = []
    student_engagement_time = []
    non_student_engagement_time = []
    with open(csvfile) as f:
        header = f.readline()
        columns = header.split(",")
        columns = [col.strip().lower() for col in columns]
        id_index = columns.index("id")
        profession_index = columns.index("profession")
        age_index = columns.index("age")
        time_spent_hour_index = columns.index("time_spent_hour")
        engagement_score_index = columns.index("engagement_score")
        platform_index = columns.index("platform")
        income_index = columns.index("income")
        line = f.readline()
        while line:
            if is_valid_row(line, columns):
                row_data = line.split(",")
                row_data = [r.strip().lower() for r in row_data]
                if row_data[id_index] not in ids:
                    dataset.append(row_data)
                    ids.append(row_data[id_index])
                    index = 1
                    engagement_time = cal_engagement_time(float(row_data[time_spent_hour_index]),
                                                          float(row_data[engagement_score_index]))
                    if row_data[profession_index] == "student":
                        index = 0
                        student_age.append(int(row_data[age_index]))
                        student_income.append(float(row_data[income_index]))
                        student_engagement_time.append(engagement_time)
                    else:
                        non_student_age.append(int(row_data[age_index]))
                        non_student_income.append(float(row_data[income_index]))
                        non_student_engagement_time.append(engagement_time)
                    OP1[index][row_data[id_index]] = [int(row_data[age_index]),
                                                      int(round(float(row_data[time_spent_hour_index]), 4)),
                                                      round(float(row_data[engagement_score_index]), 4)]

                    if row_data[platform_index] not in platform_wise.keys():
                        platform_wise[row_data[platform_index]] = [engagement_time]
                    else:
                        platform_wise[row_data[platform_index]].append(engagement_time)
            line = f.readline()
        for key in platform_wise.keys():
            OP2[key] = [round(cal_total(platform_wise[key]), 4),
                        round(cal_avg(platform_wise[key]), 4),
                        round(cal_std(platform_wise[key]), 4)]
    OP3 = [round(find_cosine_similarity(student_age, student_income), 4),
           round(find_cosine_similarity(non_student_age, non_student_income), 4)]
    OP4 = round(find_cohen_d_score(student_engagement_time, non_student_engagement_time), 4)
    return OP1, OP2, OP3, OP4


if __name__ == "__main__":
    op1, op2, op3, op4 = main("test_data_with_edge_cases_edited.csv")

    print("Student count:", len(op1[0]))
    print("Non-student count:", len(op1[1]))
    print("Platform stats (YouTube):", op2.get("youtube", "Not found"))
    print("Cosine similarities (students/non-students):", op3)
    print("Cohen's d score (engagement time):", op4)

