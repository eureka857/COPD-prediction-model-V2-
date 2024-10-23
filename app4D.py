import streamlit as st
import pandas as pd
from pycaret.classification import load_model, predict_model


# 加载模型
model = load_model('tuned_model2')

# 定义一个函数用于预测
def predict(input_data):
    predictions = predict_model(model, data=input_data)
    return predictions


# 标题和描述
st.title('COPD prediction model/赛博算命——测测你有没有慢阻肺')
st.write("""
## Input
请在左侧栏输入参数值，然后点击“预测”按钮/Enter the parameter values in the left column and click the "Predict" button。
""")

# 创建输入数据表单
st.header('……')

def user_input_features():
    # 定义显示标签和对应的原始参数值的映射
    options1 = {'男/male': 1, '女/female': 0}
    options2 = {'<40岁/years': 0, '40-49岁/years': 1, '50-59岁/year': 2, '60-69岁/year': 3, '>70岁/years': 4}
    options3 = {'<18.5kg/m2': 4, '18.6-23.9 kg/m2': 1, '24.0-27.9kg/m2': 7, '>28.0kg/m2': 0}
    options4 = {'否/False': 0, '是/Ture': 1}
    options5 = {'否/False': 0, '是/Ture': 1}
    options6 = {'仅剧烈活动后气促/Shortness of breath only after strenuous activity': 0, '平地快走或爬坡时气促/Short of breath when walking or climbing fast on flat ground': 1, '走100m或爬2层楼即感气促/Walking 100m or climbing two floors is short of breath': 2, '日常生活或休息时也感气促/Shortness of breath during daily life or at rest': 3}
    options7 = {'否/False': 0, '是/Ture': 1}
    options8 = {'从不吸烟/Never smoking': 0, '已戒烟/Never smoking': 1, '1-14.9包·年/pack·year': 2, '15-29.9包·年/pack·year': 3, '≥30包·年/pack·year': 4}
    options9 = {'否/False': 0, '是/Ture': 1}
    
    # 选择框，显示用户友好的标签
    selected_option1 = st.sidebar.selectbox('性别/Sex', list(options1.keys()))
    selected_option2 = st.sidebar.selectbox('年龄/Age', list(options2.keys()))
    selected_option3 = st.sidebar.selectbox('体重指数/BMI', list(options3.keys()))
    selected_option4 = st.sidebar.selectbox('咳嗽或咳痰/Cough or phlegm', list(options4.keys()))
    selected_option5 = st.sidebar.selectbox('喘息/Wheeze', list(options5.keys()))
    selected_option6 = st.sidebar.selectbox('活动后气促/mMRC Dyspnea index', list(options6.keys()))
    selected_option7 = st.sidebar.selectbox('曾诊断为肺气肿/Emphysema history', list(options7.keys()))
    selected_option8 = st.sidebar.selectbox('吸烟指数/Smoking index', list(options8.keys()))
    selected_option9 = st.sidebar.selectbox('过去一年中是否使用呼吸药物治疗/Drug use history of respiratory diseases', list(options9.keys()))
    
    # 获取原始参数值
    param1 = options1[selected_option1]
    param2 = options2[selected_option2]
    param3 = options3[selected_option3]
    param4 = options4[selected_option4]
    param5 = options5[selected_option5]
    param6 = options6[selected_option6]
    param7 = options7[selected_option7]
    param8 = options8[selected_option8]
    param9 = options9[selected_option9]

    # 根据你的模型输入特征添加更多的参数
    data = {'S': param1, 'A': param2, 'B': param3, 'CP': param4, 
            'Wh': param5, 'mMRC3': param6, 'LD12': param7, 'Sidx': param8, 'Drugu': param9 }
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()


# 显示输入参数
st.subheader('……')
st.write(input_df)

# 做预测
if st.button('点击进行预测'):
    output = predict(input_df)
    prediction_score = output['prediction_score'][0]  # 假设“Score”是输出DataFrame中的列名
    predicted_label = output['prediction_label'][0]    # 假设“Label”是输出DataFrame中的列名

    st.subheader('预测结果')
    
    # 根据得分和标签给出结论    
    if predicted_label == 1:
       st.write("您很可能患有中度及以上慢阻肺，请立即前往呼吸专科门诊就诊。")
    else:
    # 根据得分给出结论
      if prediction_score < 0.78:
         st.write("您很可能患有慢阻肺病，建议进一步行肺功能测试明确诊断。")
      elif 0.78 <= prediction_score < 0.88:
         st.write("您目前还不是慢阻肺，但有患上慢阻肺的风险，请您戒烟，加强锻炼，持续关注呼吸健康，并将肺功能测试纳入您的年度体检计划。")
      else: # prediction_score >= 0.88
         st.write("您目前肺部健康尚好，请继续保持。")

    # 显示输出
    st.write(output)
