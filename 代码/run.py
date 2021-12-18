from flask import Flask, make_response, request, render_template
from preprocess_data import Process  # 自定义的，在同级目录
import pickle
import numpy as np

app = Flask(__name__)
temp = []
ff = ['file1', 'file2', 'file3', 'file4']
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def form():
    return render_template('mini.html')


@app.route('/predict', methods=["POST"])
def predict():
    global decision
    decision = request.form.get('dec')
    if decision == "输入特征预测":
        return render_template('max.html')
    else:
        return render_template('index.html')


@app.route('/letter', methods=['POST'])
def letter():
    for i in range(4):
        file = request.files[ff[i]]
        temp.append('./temp_data/' + file.filename)
        file.save(temp[i])
    p = Process(temp[0], temp[1], temp[2], temp[3])
    res = p.beta_process_csv()
    print(res)
    train_data = res[['纳税总额', '净利润']]
    prediction = model.predict(train_data)
    res['flag'] = prediction
    res = res[['flag']]
    if decision == '批量查询':
        res.to_csv(r"temp_data/many.csv")
        with open(r"temp_data/many.csv") as fp:
            output = fp.read()
        response = make_response(output)
        response.headers["Content-Disposition"] = "attachment; filename=many.csv"
        return response
    else:
        print(res)
        if res.iloc[0][0] == 1:
            yn = '是'
        else:
            yn = '不是'
        print(res.index)
        return render_template('index.html', result='ID:{}'.format(res.index.values),
                               description=yn, sss='僵尸企业')


@app.route('/former', methods=['POST'])
def former():
    float_features = [float(x) for x in request.form.values()]
    final_features = [np.array(float_features)]
    pprediction = model.predict(final_features)
    pro = model.predict_proba(final_features).T[1][0]
    prob = 100 * round(pro, 2)
    ooutput = round(pprediction[0], 2)
    if ooutput == 0:
        uou = '非僵尸企业'
    else:
        uou = '僵尸企业'
    return render_template('max.html', prediction_text='模型判断结果为：' + uou, probability='是僵尸企业的概率：{}%'.format(prob))


@app.route('/wowk', methods=['POST', 'GET'])
def wowk():
    return render_template('mini.html')


if __name__ == "__main__":
    app.run(debug="True")
