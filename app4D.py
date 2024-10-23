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
st.title('COPD prediction model')
st.write("""
## 输入参数以进行预测
请在左侧栏输入参数值，然后点击“预测”按钮。
""")

# 创建输入数据表单
st.header('模型内部参数')

def user_input_features():
    # 定义显示标签和对应的原始参数值的映射
    options1 = {'男': 1, '女': 0}
    options2 = {'<40岁': 0, '40-49岁': 1, '50-59岁': 2, '60-69岁': 3, '>70岁': 4}
    options3 = {'<18.5kg/m2': 0, '18.6-23.9 kg/m2': 4, '24.0-27.9kg/m2': 1, '>28.0kg/m2': 7}
    options4 = {'否': 1, '是': 0}
    options5 = {'否': 0, '是': 1}
    options6 = {'仅剧烈活动后气促': 0, '平地快走或爬坡时气促': 1, '走100m或爬2层楼即感气促': 2, '日常生活或休息时也感气促': 3}
    options7 = {'否': 0, '是': 1}
    options8 = {'从不吸烟': 0, '已戒烟': 1, '1-14.9包·年': 2, '15-29.9包·年': 3, '≥30包·年': 4}
    options9 = {'否': 0, '是': 1}
    
    # 选择框，显示用户友好的标签
    selected_option1 = st.sidebar.selectbox('性别', list(options1.keys()))
    selected_option2 = st.sidebar.selectbox('年龄', list(options2.keys()))
    selected_option3 = st.sidebar.selectbox('体重指数', list(options3.keys()))
    selected_option4 = st.sidebar.selectbox('咳嗽或咳痰', list(options4.keys()))
    selected_option5 = st.sidebar.selectbox('喘息', list(options5.keys()))
    selected_option6 = st.sidebar.selectbox('活动后气促', list(options6.keys()))
    selected_option7 = st.sidebar.selectbox('曾诊断为肺气肿', list(options7.keys()))
    selected_option8 = st.sidebar.selectbox('吸烟指数', list(options8.keys()))
    selected_option9 = st.sidebar.selectbox('过去一年中是否使用呼吸药物治疗', list(options9.keys()))
    
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
st.subheader('如最后一栏得分低于0.78，则您很可能患有慢阻肺病，请进一步行肺功能测试确诊。如果倒数第二栏label显示为1，则您很可能患有中度及以上慢阻肺，请立即前往呼吸专科门诊就诊')
st.write(input_df)

# 做预测
if st.button('点击进行预测'):
    output = predict(input_df)
    st.subheader('如最后一栏得分低于0.78，则您很可能患有慢阻肺病，请进一步行肺功能测试确诊。如果倒数第二栏label显示为1，则您很可能患有中度及以上慢阻肺，请立即前往呼吸专科门诊就诊')
    st.write(output)
