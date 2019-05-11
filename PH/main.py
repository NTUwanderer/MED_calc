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


def myparse(inp):
    if (inp == u""):
        return -1

    return float(inp)

# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    ph = myparse(request.form['in1'])
    PaCO2 = myparse(request.form['in2'])
    HCO3 = myparse(request.form['in3'])
    Na = myparse(request.form['in4'])
    Cl = myparse(request.form['in5'])
    Alb = myparse(request.form['in6'])

    Una = myparse(request.form['in7'])
    Uk = myparse(request.form['in8'])
    Ucl = myparse(request.form['in9'])
    Uph = myparse(request.form['in10'])
    Bk = myparse(request.form['in11'])


    epsilon = 0.0001 


    result = ""
    if (ph < 7.35):
        if (HCO3 < 24):
            result += "Acidosis, "
            value = 40 - 1.25 * (24 - HCO3) - PaCO2
            if abs(value) <= (2 + epsilon):
                pass
            elif value > 2:
                result += "Respiratory Acidosis "
            else: # value < -2
                result += "Respiratory Alkaloidss "

            AG = Na - Cl - HCO3
            if Alb < 3.8 - epsilon:
                AG += (4 - Alb) * 2.5

            if AG < 12 + epsilon or AG > 10 - epsilon:
                result = "Normal Anion Metabolic Acidosis "
                if Una > -0.5: # Una and else exist
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
                result += "Undetected cation increased "
            else:
                deltaAG = AG - 11
                deltaHCO3 = 24 - HCO3
                if deltaAG > 2 * deltaHCO3:
                    result = "High Anion Metabolic Acidosis + Metabolic Alkaloids"
                elif deltaAG > deltaHCO3 - epsilon:
                    result = "High Anion Metabolic Acidosis"
                else:
                    result = "High Anion Metabolic Acidosis + Normal Anion Metabolic Acidosis"
                
        elif (PaCO2 > 40):
            result += "Respiratory Acidosis, "
            value = (PaCO2 - 40)
            thres1 = 0.1 * value + 24
            thres2 = 0.4 * value + 24
            delta = 0.5
            if (HCO3 - thres1 < -delta):
                result += "Metabolic Acidosis "
            elif HCO3 - thres1 < delta:
                result += "(Acute Respiratory Acidosis)"
            elif HCO3 - thres2 < -delta:
                result += "(Acute to chronic change of Respiratory Acidosis)"
            elif HCO3 - thres2 < delta:
                result += "(Chronic Respiratory Acidosis)"
            else:
                result += "(Respiratory Acidosis + Metabolic Alkaloids)"
                
    elif (ph > 7.45):
        if (HCO3 > 24):
            result += "Metabolic Alkaloids, "
            value = (40 + 0.75 * (HCO3 - 24)) - PaCO2
            if abs(value) <= (2 + epsilon):
                pass
            elif value > 2:
                result += "Respiratory Alkaloids"
            else: # value < -2
                result += "Respiratory Acidosis "
        elif (PaCO2 < 40):
            result += "Respiratory Alkaloids "
            value = (40 - PaCO2)
            thres1 = 24 - 0.2 * value
            thres2 = 24 - 0.4 * value
            delta = 0.5
            if (HCO3 - thres1 < -delta):
                result += "Metabolic Acidosis "
            elif HCO3 - thres1 < delta:
                result += "(Chronic Respiratory Alkaloids)"
            elif HCO3 - thres2 < -delta:
                result += "(Acute to chronic change of Respiratory Alkaloids)"
            elif HCO3 - thres2 < delta:
                result += "(Chronic Respiratory Alkaloids)"
            else:
                result += "(Respiratory Alkaloids + Metabolic Alkaloids)"


    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        in1=ph,
        in2=PaCO2,
        in3=HCO3,
        in4=Na,
        in5=Cl,
        in6=Alb,
        in7=Una,
        in8=Uk,
        in9=Ucl,
        in10=Uph,
        in11=Bk,
        result=result,
    )
    
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
