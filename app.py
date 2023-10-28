<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pyresparser import ResumeParser
import os
import fitz
import re
import requests

app = Flask(__name__)
app.secret_key = 'cgft86ogouhgouyrvoi' 
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

GENDER_API_URL = "https://gender-api.com/get"
GENDER_API_KEY = "a16ffc9cc175d574acfcb2d5b5acdc4f3c24b3939a50385ddf37ba6437b19e12"


@app.route('/')
def index():
    data=[]
    return render_template('main.html',resume_data=data)

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        flash('No resume part')
        # return redirect(request.url)

    resume = request.files['resume']
    if resume.filename == '':
        flash('No selected resume')

    if resume:
        filename = secure_filename(resume.filename)
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume.save(resume_path)
        data = ResumeParser(resume_path).get_extracted_data()

        doc = fitz.open(resume_path)
        lines = [line for page in doc for line in page.get_text().splitlines()]

        if 'mobile_number' in data and data['mobile_number']:
            data['mobile_number'] = data['mobile_number'].lstrip(' +91')
        
        if len(str(data['mobile_number'])) < 10 and data['mobile_number'] is not None :
            number = data['mobile_number']
          
            for line in lines:
                if number in line:
                  data['mobile_number'] = line

        #college name
        if data['college_name'] is None :
            for line in lines:
                if "college" in line.lower():
                    data['college_name'] = line.upper()
                    break

        # degree names 
        degrees = {"B.Tech", "M.Tech", "BBA", "MBA", "B.Sc", "M.Sc", "Ph.D", "Diploma"}

        # degree and specialization
        if data['degree'] is not None and len(data['degree']) < 2:
           
            value = data['degree'][0]
            
            for degree in degrees:
                pattern = r"\b" + re.escape(degree) + r"\b"
                if re.search(pattern, line, re.I):
                    data['specialization'] = value.upper().replace(degree.upper(), "").strip()
                   
                    data['specialization'] = data['specialization'].replace("IN", "", 1).strip()
                    break
        else:
            for line in lines:
                for degree in degrees:
                    pattern = r"\b" + re.escape(degree) + r"\b"
                    if re.search(pattern, line, re.I):
                        data['degree'] = line.upper()
                        data['specialization'] = data['degree'].replace(degree.upper(), "").strip()
                        data['specialization'] = data['specialization'].replace("IN", "", 1).strip()
                        break
        #year
        pattern = r'\b(\d{4})-(\d{2}|\d{4})\b'
        highest_year_range = None
        highest_year_difference = 0

        for line in lines:
            matches = re.findall(pattern, line)
            for match in matches:
                start_year = int(match[0])
                if len(match[1]) == 2:
                    end_year = int(match[0][:2] + match[1])
                else:
                    end_year = int(match[1])
                year_difference = end_year - start_year
                if year_difference > highest_year_difference:
                    highest_year_difference = year_difference
                    highest_year_range = f'{start_year}-{end_year}'
                    data['year_of_graduation'] = highest_year_range

        # Gender
        if 'name' in data and data['name']:
            name = data['name']
            gender_api_url = f"{GENDER_API_URL}?name={name}&country=IN&key={GENDER_API_KEY}"
            gender_response = requests.get(gender_api_url)
            if gender_response.status_code == 200:
                gender_data = gender_response.json()
                data['gender'] = gender_data.get('gender', 'Unknown').capitalize()

        return render_template('main.html', resume_data=data)

if __name__ == '__main__':
    app.run(debug=True)
=======
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pyresparser import ResumeParser
import os
import fitz
import re
import requests

app = Flask(__name__)
app.secret_key = 'cgft86ogouhgouyrvoi' 
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

GENDER_API_URL = "https://gender-api.com/get"
GENDER_API_KEY = "a16ffc9cc175d574acfcb2d5b5acdc4f3c24b3939a50385ddf37ba6437b19e12"


@app.route('/')
def index():
    data=[]
    return render_template('main.html',resume_data=data)

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        flash('No resume part')
        # return redirect(request.url)

    resume = request.files['resume']
    if resume.filename == '':
        flash('No selected resume')

    if resume:
        filename = secure_filename(resume.filename)
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume.save(resume_path)
        data = ResumeParser(resume_path).get_extracted_data()

        doc = fitz.open(resume_path)
        lines = [line for page in doc for line in page.get_text().splitlines()]

        if 'mobile_number' in data and data['mobile_number']:
            data['mobile_number'] = data['mobile_number'].lstrip(' +91')
        
        if len(str(data['mobile_number'])) < 10 and data['mobile_number'] is not None :
            number = data['mobile_number']
          
            for line in lines:
                if number in line:
                  data['mobile_number'] = line

        #college name
        if data['college_name'] is None :
            for line in lines:
                if "college" in line.lower():
                    data['college_name'] = line.upper()
                    break

        # degree names 
        degrees = {"B.Tech", "M.Tech", "BBA", "MBA", "B.Sc", "M.Sc", "Ph.D", "Diploma"}

        # degree and specialization
        if data['degree'] is not None and len(data['degree']) < 2:
           
            value = data['degree'][0]
            
            for degree in degrees:
                pattern = r"\b" + re.escape(degree) + r"\b"
                if re.search(pattern, line, re.I):
                    data['specialization'] = value.upper().replace(degree.upper(), "").strip()
                   
                    data['specialization'] = data['specialization'].replace("IN", "", 1).strip()
                    break
        else:
            for line in lines:
                for degree in degrees:
                    pattern = r"\b" + re.escape(degree) + r"\b"
                    if re.search(pattern, line, re.I):
                        data['degree'] = line.upper()
                        data['specialization'] = data['degree'].replace(degree.upper(), "").strip()
                        data['specialization'] = data['specialization'].replace("IN", "", 1).strip()
                        break
        #year
        pattern = r'\b(\d{4})-(\d{2}|\d{4})\b'
        highest_year_range = None
        highest_year_difference = 0

        for line in lines:
            matches = re.findall(pattern, line)
            for match in matches:
                start_year = int(match[0])
                if len(match[1]) == 2:
                    end_year = int(match[0][:2] + match[1])
                else:
                    end_year = int(match[1])
                year_difference = end_year - start_year
                if year_difference > highest_year_difference:
                    highest_year_difference = year_difference
                    highest_year_range = f'{start_year}-{end_year}'
                    data['year_of_graduation'] = highest_year_range

        # Gender
        if 'name' in data and data['name']:
            name = data['name']
            gender_api_url = f"{GENDER_API_URL}?name={name}&country=IN&key={GENDER_API_KEY}"
            gender_response = requests.get(gender_api_url)
            if gender_response.status_code == 200:
                gender_data = gender_response.json()
                data['gender'] = gender_data.get('gender', 'Unknown').capitalize()

        return render_template('main.html', resume_data=data)

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 053943592a651acbdd96b43feb5e08786362402d
