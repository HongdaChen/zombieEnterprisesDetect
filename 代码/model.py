import time
import pickle
import argparse
import numpy as np
from preprocess_data import Process  # 自定义的，在同级目录
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.model_selection import train_test_split, cross_val_score

base_train_sum = r'../data/base_train_sum.csv'
base_verify1 = r'../data/base_verify1.csv'
knowledge_train = r'../data/knowledge_train_sum.csv'
paient_information_verify1 = r'../data/paient_information_verify1.csv'
money_report_train_sum = r'../data/money_report_train_sum.csv'
money_information_verify1 = r'../data/money_information_verify1.csv'
year_report_train_sum = r'../data/year_report_train_sum.csv'
year_report_verify1 = r'../data/year_report_verify1.csv'

parser = argparse.ArgumentParser(description="choose mode")
parser.add_argument('--model', type=str, default='knn', help='choose which model to do')
parser.add_argument('--mode', type=str, default='train', help='choose train mode or parameters mode')
parser.add_argument('--feature', type=int, default=2, help='choose the number of feature you would like to use')
args = parser.parse_args()

n = args.model
momo = args.mode
fe = args.feature
# ########################################## KNN ###################################################
if n == 'knn':
    p = Process(base_train_sum, knowledge_train, money_report_train_sum, year_report_train_sum, features=fe)
    res = p.alpha_process_csv(base_verify1, paient_information_verify1, money_information_verify1, year_report_verify1)
    y = res['flag'].values
    train_X, val_X, train_y, val_y = train_test_split(res.drop('flag', axis=1), y, test_size=0.3, random_state=0)

    if momo == 'train':
        knn = KNeighborsClassifier(n_neighbors=4, weights='distance')
        knn.fit(train_X, train_y)
        acc1 = knn.score(val_X, val_y)
        pickle.dump(knn, open("model.pkl", "wb"))
        model =  pickle.load(open("model.pkl", "rb"))
        print(model.predict([[0.2, 0.4]]))
        
    elif momo == 'parameter':
        error = []
        for k in range(1, 14):
            knn = KNeighborsClassifier(n_neighbors=k, weights='distance')
            score = cross_val_score(knn, res.drop(columns='flag'), y, cv=6, scoring="accuracy").mean()
            error.append(1-score)

        plt.plot(np.arange(1, 14), error)
        plt.xlabel("k")
        plt.ylabel("loss")
        plt.title("KNN")
        plt.show()

# ############################################ 逻辑回归###############################################
elif n == 'logistic_regression':
    p = Process(base_train_sum, knowledge_train, money_report_train_sum, year_report_train_sum, features=fe)
    res = p.alpha_process_csv(base_verify1, paient_information_verify1, money_information_verify1, year_report_verify1)
    y = res['flag'].values
    train_X, val_X, train_y, val_y = train_test_split(res.drop('flag', axis=1), y, test_size=0.3, random_state=0)

    lr = LogisticRegression()
    lr.fit(train_X, train_y)
    acc2 = lr.score(val_X, val_y)
    pickle.dump(lr, open("model.pkl", "wb"))
    model =  pickle.load(open("model.pkl", "rb"))
    print(model.predict([[0.2, 0.4]]))

# ############################################# 神经网络 ###########################################
elif n == 'neural_network':
    p = Process(base_train_sum, knowledge_train, money_report_train_sum, year_report_train_sum, features=fe)
    res = p.alpha_process_csv(base_verify1, paient_information_verify1, money_information_verify1, year_report_verify1)
    y = res['flag'].values
    train_X, val_X, train_y, val_y = train_test_split(res.drop('flag', axis=1), y, test_size=0.3, random_state=0)

    clf = MLPClassifier(solver='adam', alpha=1e-3, hidden_layer_sizes=(20, 10),
                        random_state=1)
    clf.fit(train_X, train_y)
    acc3 = clf.score(val_X, val_y)
    pickle.dump(clf, open("model.pkl", "wb"))
    model =  pickle.load(open("model.pkl", "rb"))
    print(model.predict([[0.2, 0.4]]))

# ########################################## 随机森林 ##############################################
elif n == 'random_forest':
    p = Process(base_train_sum, knowledge_train, money_report_train_sum, year_report_train_sum,
                standard=False, features=fe)  # 不进行标准化
    res = p.alpha_process_csv(base_verify1, paient_information_verify1, money_information_verify1, year_report_verify1)
    y = res['flag'].values
    train_X, val_X, train_y, val_y = train_test_split(res.drop('flag', axis=1), y, test_size=0.3, random_state=0)

    if momo == 'train':
        forest = RandomForestClassifier(n_estimators=22)
        forest.fit(train_X, train_y)
        acc4 = forest.score(val_X, val_y)
        pickle.dump(forest, open("model.pkl", "wb"))
        model =  pickle.load(open("model.pkl", "rb"))
        print(model.predict([[0.2, 0.4]]))
    elif momo == 'parameter':
        acc = []
        for k in range(10, 30):
            forest = RandomForestClassifier(n_estimators=k)
            score = cross_val_score(forest, res.drop(columns='flag'), y, cv=10, scoring="accuracy").mean()
            acc.append(score)
        print('最优score：', max(acc), '最优n_estimator:', ([*range(10, 30)][acc.index(max(acc))]))
        plt.plot(range(10, 30), acc)
        plt.xlabel("decision_tree_number")
        plt.ylabel("accuracy")
        plt.title("RandomForest")
        plt.show()