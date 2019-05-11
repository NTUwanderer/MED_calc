# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

# [START imports]
from flask import Flask, render_template, request
# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]


# [START form]
@app.route('/form')
def form():
    return render_template('form.html')
# [END form]


# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    ph = request.form['in1']
    PaCO2 = request.form['in2']
    HCO3 = request.form['in3']
    Na = request.form['in4']
    Cl = request.form['in5']
    Alb = request.form['in6']

    Una = request.form['in7']
    Uk = request.form['in8']
    Ucl = request.form['in9']
    Uph = request.form['in10']
    Bk = request.form['in11']

    epsilon = 0.0001 

    result = ""
    if (ph < 7.35):
        if (HCO3 < 24):
            result += "代謝酸 "
            value = 40 - 1.25 * (24 - HCO3) - PaCO2
            if abs(value) <= (2 + epsilon):
                pass
            elif value > 2:
                result += "呼吸酸 "
            else: # value < -2
                result += "呼吸鹼 "

            AG = Na - Cl - HCO3
            if Alb < 3.8 - epsilon:
                AG += (4 - Alb) * 2.5

            if AG < 12 + epsilon or AG > 10 - epsilon:
                result = "正常陰離子代謝酸 "
                U_AG = Una + Uk - Ucl
                if (U_AG > 0 - epsilon):
                    if (Bk > 5 - epsilon and Uph < 5.3 - epsilon):
                        result += "Type 4 RTA"
                    elif (Bk < 3.5 + epsilon and Uph > 5.3 + epsilon):
                        result += "Type 1 RTA"
                    else:
                        result += "Type 2 RTA"
                elif (U_AG < 0 - epsilon):
                    result += "Diarrhea or Type 2 RTA "


            elif AG < 10:
                result += "未測到陽離子增加 "
            else:
                deltaAG = AG - 11
                deltaHCO3 = 24 - HCO3
                if deltaAG > 2 * deltaHCO3:
                    result = "高陰離子代謝酸 + 代謝鹼"
                elif deltaAG > deltaHCO3 - epsilon:
                    result = "高陰離子代謝酸"
                else:
                    result = "高陰離子代謝酸 + 正常陰離子代謝酸"
                
            

        elif (PaCO2 > 40):
            result += "呼吸酸 "
            value = (PaCO2 - 40)
            thres1 = 0.1 * value + 24
            thres2 = 0.4 * value + 24
            delta = 0.5
            if (HCO3 - thres1 < -delta):
                result += "代謝酸 "
            elif HCO3 - thres1 < delta:
                result += "(急性呼吸酸中毒)"
            elif HCO3 - thres2 < -delta:
                result += "(慢性呼吸酸併急性惡化)"
            elif HCO3 - thres2 < delta:
                result += "(慢性呼吸酸中毒)"
            else:
                result += "(呼吸酸併代謝鹼中毒)"
    elif (ph > 7.45):
        if (HCO3 > 24):
            result += "代謝鹼 "
            value = (40 + 0.75 * (HCO3 - 24)) - PaCO2
            if abs(value) <= (2 + epsilon):
                pass
            elif value > 2:
                result += "呼吸鹼 "
            else: # value < -2
                result += "呼吸酸 "
        elif (PaCO2 < 40):
            result += "呼吸鹼 "
            value = (40 - PaCO2)
            thres1 = 24 - 0.2 * value
            thres2 = 24 - 0.4 * value
            delta = 0.5
            if (HCO3 - thres1 < -delta):
                result += "代謝酸 "
            elif HCO3 - thres1 < delta:
                result += "(慢性呼吸鹼中毒)"
            elif HCO3 - thres2 < -delta:
                result += "(慢性呼吸鹼併急性惡化)"
            elif HCO3 - thres2 < delta:
                result += "(慢性呼吸鹼中毒)"
            else:
                result += "(呼吸鹼併代謝鹼中毒)"

        





    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        in1=ph,
        in2=in2,
        in3=in3,
        in4=in4,
        in5=in5,
        in6=in6,
        in7=in7,
        in8=in8,
        in9=in9,
        in10=in10,
        result=result,
    )
    
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
