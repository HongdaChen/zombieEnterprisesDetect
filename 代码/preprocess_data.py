import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer


def _my_read_csv(f):
    try:
        fl=pd.read_csv(f, encoding='gb2312').reset_index(drop=True).set_index('ID')
    except:
        fl=pd.read_csv(f, encoding='utf-8').reset_index(drop=True).set_index('ID')
    return fl


class Process:
    """Preprocess the given data.

        Parameters
        ----------
        base : the location of base information.(string)

        knowledge : the location of knowledge information.(string)

        money_report : the location of money_report information.(string)

        year_report : the location of year_report information.(string)

        encoder : bool to decide if encode the string feature ; default(True).

        drop_flag : bool to decide if drop the data which "flag" is empty ; default(True).

        standard : bool to decide if make the numerical data standard by (x-u)/std ; default(True).

        features : int to decide how many features to use. [1,15],default(2)

        Returns
        -------
        datafile.

    """

    def __init__(self, base, knowledge, money_report, year_report, encoder=True, drop_flag=True, standard=True, features=2):
        self.base = base
        self.knowledge = knowledge
        self.money_report = money_report
        self.year_report = year_report
        self.encoder = encoder
        self.drop_flag = drop_flag
        self.standard = standard
        self.features = features

        assert 0 <= self.features <= 15, "features number must be in the [0,15] field"

    def _process_csv(self, no_year, three_year):
        # 对no_year补缺
        global ss
        imp_mean = SimpleImputer(strategy="mean")
        imp_most_frequent = SimpleImputer(strategy="most_frequent")
        if 'flag' in no_year.columns:
            _li = no_year.drop(columns=['flag']).columns
        else:
            _li = no_year.columns
        for col in _li:
            if col in ['专利', '商标', '著作权'] or no_year[col].dtype == 'object':
                no_year[col] = imp_most_frequent.fit_transform(no_year[col].values.reshape(-1, 1))
            else:
                no_year[col] = imp_mean.fit_transform(no_year[col].values.reshape(-1, 1))
        # 对no_year标准化
        if self.standard:
            ss = StandardScaler()
            no_year['注册资本'] = ss.fit_transform(no_year['注册资本'].values.reshape(-1, 1))
            no_year['注册时间'] = ss.fit_transform(no_year['注册时间'].values.reshape(-1, 1))

        # 编码
        if self.encoder:
            for col in no_year.columns:
                if no_year[col].dtype == 'object':
                    no_year[col] = LabelEncoder().fit_transform(no_year[col])

        # 对three_year处理
        # 三年数据取平均
        three_year.reset_index(inplace=True)
        three_pivot_table = pd.pivot_table(three_year, index=['ID', 'year'])
        one_year = three_pivot_table.groupby('ID').sum()/3
        # 对one_year补缺，标准化
        one_year[::] = imp_mean.fit_transform(one_year[::])
        if self.standard:
            one_year[::] = ss.fit_transform(one_year[::])

        # 合并no_year与one_year
        processed_all_data = pd.concat([no_year, one_year], axis=1, sort=True)
        # 是否丢弃flag不确定的数据
        if self.drop_flag:
            processed_all_data = processed_all_data.dropna()
        else:
            processed_all_data['flag'].fillna(100, inplace=True)
            processed_all_data.dropna(inplace=True)
        # 提取特征
        if self.features != 0:
            feature = ['flag', '纳税总额', '净利润', '注册资本', '负债总额', '从业人数', '营业总收入', '利润总额', '注册时间',
                       '资产总额', '内部融资和贸易融资成本', '债权融资成本', '行业', '内部融资和贸易融资额度',
                       '控制人持股比例', '项目融资和政策融资额度']
            if 'flag' in processed_all_data.columns:
                processed_all_data = processed_all_data[feature[:1 + self.features]]
            else:
                processed_all_data = processed_all_data[feature[1:1 + self.features]]

        return processed_all_data

    def alpha_process_csv(self, base_verify, paient_information_verify1, money_information_verify1,
                          year_report_verify1):
        """Preprocess all the given data before training the model and correspond with the dynamic method.
        Parameters
        ----------
        base_verify : the location of base_verify information.(string)

        paient_information_verify1 : the location of paient_information_verify1 information.(string)

        money_information_verify1 : the location of money_information_verify1 information.(string)

        year_report_verify1 : the location of year_report_verify1 information.(string)

        Returns
        -------
        datafile.

        """
        # 读入
        base_train_sum = _my_read_csv(self.base)
        knowledge_train = _my_read_csv(self.knowledge)
        money_report_train_sum = _my_read_csv(self.money_report)
        year_report_train_sum = _my_read_csv(self.year_report)

        base_verify = _my_read_csv(base_verify)
        paient_information_verify1 = _my_read_csv(paient_information_verify1)
        money_information_verify1 = _my_read_csv(money_information_verify1)
        year_report_verify1 = _my_read_csv(year_report_verify1)
        # 训练集与验证集合并
        no_year = pd.concat([pd.concat([base_train_sum, base_verify], sort=True).drop(columns='控制人ID'),
                             pd.concat([knowledge_train, paient_information_verify1], sort=True)], axis=1, sort=True)
        three_year = pd.concat([pd.concat([money_report_train_sum, money_information_verify1]),
                                pd.concat([year_report_train_sum, year_report_verify1]).drop(columns='year')], axis=1)
        result = self._process_csv(no_year, three_year)
        return result

    def beta_process_csv(self):
        """Preprocess the test data.
        Parameters
        ----------
        No parameters.
        Returns
        -------
        datafile.
        """
        base = _my_read_csv(self.base)
        knowledge = _my_read_csv(self.knowledge)
        money = _my_read_csv(self.money_report)
        year = _my_read_csv(self.year_report)

        no_year = pd.concat([base, knowledge], axis=1, sort=True)
        three_year = pd.concat([money, year.drop('year', axis=1)], axis=1)
        result = self._process_csv(no_year, three_year)
        return result


if __name__ == "__main__":
    # base_train_sum = r'../data/base_train_sum.csv'
    # base_varify = r'../data/base_verify1.csv'
    # knowledge_train = r'../data/knowledge_train_sum.csv'
    # paient_information_verify1 = r'../data/paient_information_verify1.csv'
    #
    # money_report_train_sum = r'../data/money_report_train_sum.csv'
    # money_information_verify1 = r'../data/money_information_verify1.csv'
    # year_report_train_sum = r'../data/year_report_train_sum.csv'
    # year_report_verify1 = r'../data/year_report_verify1.csv'
    base_varify = r'./temp_data/base_verify1.csv'
    paient_information_verify1 = r'./temp_data/paient_information_verify1.csv'
    money_information_verify1 = r'./temp_data/money_information_verify1.csv'
    year_report_verify1 = r'./temp_data/year_report_verify1.csv'

    p = Process(base_varify, paient_information_verify1, money_information_verify1, year_report_verify1, )

    # res = p.alpha_process_csv(base_varify, paient_information_verify1, money_information_verify1, year_report_verify1)
    res = p.beta_process_csv()
    print(res.info())
    print(res)

