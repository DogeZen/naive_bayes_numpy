# http://sofasofa.io/competition.php?id=3#c4
import pandas as pd

train = pd.read_table("data/train.txt", sep=',')
test = pd.read_table("data/test.txt", sep=',')
total_train_data = train.iloc[:, 1:].values
total_test_data = test.iloc[:, 1:].values
frequency_dict = {}

# 先维护一个dict用于统计不同性别的词频
for single_person in total_train_data:
    name = single_person[0]
    gender = single_person[1]
    for word in name:
        # 不存在该字就初始化
        if word not in frequency_dict.keys():
            if gender == 0:
                frequency_dict[word] = [1, 0]
            else:
                frequency_dict[word] = [0, 1]
        else:
            if gender == 0:
                frequency_dict[word][0] += 1
            else:
                frequency_dict[word][1] += 1
print(frequency_dict)
list_gender = []
for (index, single_person) in enumerate(total_test_data):
    name = single_person[0]
    gender_male_probability = 1
    gender_female_probability = 1
    for word in name:
        if word not in frequency_dict.keys():
            pass
        else:
            gender_male_probability *= (frequency_dict[word][1] + 1) \
                                       / (frequency_dict[word][0] + frequency_dict[word][1] + 1)
            gender_female_probability *= (frequency_dict[word][0] + 1) \
                                         / (frequency_dict[word][0] + frequency_dict[word][1] + 1)

    if gender_female_probability > gender_male_probability:
        list_gender.append(0)

    else:
        list_gender.append(1)
test.insert(2, 'gender', list_gender)
test[['id', 'gender']].to_csv('commit.csv', index=None, encoding='utf-8')
