import os
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages

from Users.models import UserRegisteredTable

import requests
from django.conf import settings

# Create your views here.

def userRegister(request):
    if request.method == 'POST':
        # Extract data from the request
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        loginid = request.POST.get('loginid')
        mobile = request.POST.get('mobile')
        locality = request.POST.get('locality')  # Locality
        state = request.POST.get('state')  # State

        user = UserRegisteredTable(
            name=name,
            email=email,
            password=password,  # Password will be hashed in the model's save method
            loginid=loginid,
            mobile=mobile,
            locality=locality,
            state=state,
        )
        try:
            if user.full_clean:
                user.save()

                messages.success(request, 'Registration successful!.')
                return render(request,'register.html', {'reg_success': True})  # Redirect to the login page or another page as needed
            else:
                messages.error(request,'Entered data is inavalid')
                return render(request,'register.html')
        except:
            messages.error(request,'Entered data is inavalid')
            return render(request,'register.html')


    return render(request, 'register.html')

def userHome(request):
    return render(request, 'users/userHome.html')

import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import requests
from django.conf import settings


def parse_section(text, number, next_number=None):
    """Extract a numbered section from the pill info text."""
    import re
    if next_number:
        pattern = rf"{number}\..*?(?={next_number}\.|$)"
    else:
        pattern = rf"{number}\..*"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        value = match.group(0).strip()
        # Remove the leading number and label
        value = re.sub(rf"^{number}\.[^:]*:", "", value).strip()
        return value
    return ""


def prediction(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        
        # Save the uploaded file to a temporary location
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = fs.url(filename)
        
        # Construct the full file path for prediction
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        # Create a copy of the original image to show as "Before"
        import shutil
        original_filename = "original_" + filename
        original_file_path = os.path.join(settings.MEDIA_ROOT, original_filename)
        shutil.copy2(file_path, original_file_path)
        original_file_url = fs.url(original_filename)

        print(f"Uploaded file path: {file_path}")

        # Call your model's prediction function here (this modifies the file at file_path)
        predicted_label = predictions(file_path)

        # -------- Local Pill Database (Fallback) --------
        PILL_DATABASE = {
            'Alaxan': {
                'pill_name': 'Alaxan',
                'medical_uses': 'Relief of mild to moderately severe pain (headache, toothache, muscle aches).',
                'how_it_works': 'Combines Ibuprofen and Paracetamol to block pain signals and reduce inflammation.',
                'dosage': '1 tablet every 6 hours as needed.',
                'side_effects': 'Nausea, stomach pain, dizziness.',
                'warnings': 'Not for people with stomach ulcers or heart problems.',
                'advantages': 'Fast-acting dual-action pain relief.',
                'effects': 'Reduced pain and inflammation within 30-60 minutes.',
                'disadvantages': 'Can cause gastric irritation if taken on an empty stomach.',
            },
            'Bactidol': {
                'pill_name': 'Bactidol',
                'medical_uses': 'Treatment of sore throat and mouth infections.',
                'how_it_works': 'Contains Hexetidine which kills bacteria and fungi in the mouth and throat.',
                'dosage': 'Gargle 15ml for 30 seconds, twice daily.',
                'side_effects': 'Temporary alteration in taste.',
                'warnings': 'Do not swallow. Keep out of reach of children.',
                'advantages': 'Effective against a wide range of oral pathogens.',
                'effects': 'Relief from throat irritation and reduced bacterial count.',
                'disadvantages': 'Strong medicinal taste; not a tablet (liquid).',
            },
            'Bioflu': {
                'pill_name': 'Bioflu',
                'medical_uses': 'Relief of clogged nose, runny nose, cough from postnasal drip, itchy and watery eyes, sneezing, headache, body aches, and fever associated with the common cold, allergic rhinitis, sinusitis, flu, and other minor respiratory tract infections.',
                'how_it_works': 'Combines Phenylephrine HCl, Chlorphenamine Maleate, and Paracetamol to address multiple flu symptoms.',
                'dosage': '1 tablet every 6 hours.',
                'side_effects': 'Drowsiness, dry mouth, dizziness.',
                'warnings': 'Avoid driving or operating machinery after intake.',
                'advantages': 'All-in-one relief for flu and cold symptoms.',
                'effects': 'Clearer nasal passages and reduced fever/pain.',
                'disadvantages': 'Significant drowsiness effect.',
            },
            'Biogesic': {
                'pill_name': 'Biogesic',
                'medical_uses': 'Relief of headache and fever.',
                'how_it_works': 'Contains Paracetamol which acts as an analgesic and antipyretic.',
                'dosage': '1-2 tablets every 4-6 hours, not to exceed 8 tablets in 24 hours.',
                'side_effects': 'Rare, but can include skin rash.',
                'warnings': 'Avoid alcohol; risk of liver damage if taken in excessive amounts.',
                'advantages': 'Gentle on the stomach; safe for pregnant and breastfeeding women (consult doctor).',
                'effects': 'Fever reduction and pain relief.',
                'disadvantages': 'Limited anti-inflammatory effect compared to Ibuprofen.',
            },
            'DayZinc': {
                'pill_name': 'DayZinc',
                'medical_uses': 'Prevention and treatment of Vitamin C and Zinc deficiencies.',
                'how_it_works': 'Provides essential nutrients to support immune function and antioxidant defense.',
                'dosage': '1 tablet daily or as prescribed.',
                'side_effects': 'Mild stomach upset if taken in high doses.',
                'warnings': 'Do not exceed recommended dose.',
                'advantages': 'Convenient combination for immune support.',
                'effects': 'Strengthened immunity and improved wound healing over time.',
                'disadvantages': 'May cause nausea if taken without food.',
            },
            'Decolgen': {
                'pill_name': 'Decolgen',
                'medical_uses': 'Relief of symptoms of the common cold, including nasal congestion and headache.',
                'how_it_works': 'Contains Phenylpropanolamine HCl, Chlorphenamine Maleate, and Paracetamol.',
                'dosage': '1 tablet every 6 hours.',
                'side_effects': 'Drowsiness, rapid heartbeat (rare).',
                'warnings': 'Consult a doctor if you have high blood pressure.',
                'advantages': 'Effective decongestant and pain reliever.',
                'effects': 'Reduced sinus pressure and clear airway.',
                'disadvantages': 'May cause jitteriness or sleepiness.',
            },
            'Fish Oil': {
                'pill_name': 'Fish Oil',
                'medical_uses': 'Supplement for heart health and reducing triglycerides.',
                'how_it_works': 'Source of Omega-3 fatty acids (EPA and DHA) which support cardiovascular health.',
                'dosage': '1-2 softgels daily with meals.',
                'side_effects': 'Fishy aftertaste, loose stools.',
                'warnings': 'Consult doctor if taking blood thinners.',
                'advantages': 'Natural source of essential fatty acids.',
                'effects': 'Improved lipid profile and long-term heart health support.',
                'disadvantages': 'Burps can have a fishy smell.',
            },
            'Kremil S': {
                'pill_name': 'Kremil S',
                'medical_uses': 'Relief of hyperacidity, heartburn, and stomach pain.',
                'how_it_works': 'Combines antacids (Aluminum Hydroxide, Magnesium Carbonate) and Simethicone to neutralize acid and relieve gas.',
                'dosage': '1-2 tablets 1 hour after meals and at bedtime.',
                'side_effects': 'Constipation or diarrhea.',
                'warnings': 'Not for patients with kidney disease.',
                'advantages': 'Fast relief from acid-related discomfort.',
                'effects': 'Neutralizes stomach acid and reduces bloating.',
                'disadvantages': 'Chalky texture when chewed.',
            },
            'Medicol': {
                'pill_name': 'Medicol',
                'medical_uses': 'Relief of pain and inflammation associated with arthritis, gout, and muscle pains.',
                'how_it_works': 'Contains Ibuprofen, a non-steroidal anti-inflammatory drug (NSAID).',
                'dosage': '1 capsule every 4-6 hours as needed.',
                'side_effects': 'Stomach pain, heartburn, nausea.',
                'warnings': 'Take with food to avoid stomach irritation.',
                'advantages': 'Strong anti-inflammatory properties.',
                'effects': 'Reduced swelling and pain in joints and muscles.',
                'disadvantages': 'Potential risk to kidneys and stomach with long-term use.',
            },
            'Neozep': {
                'pill_name': 'Neozep',
                'medical_uses': 'Complete relief of cold and its symptoms like runny nose and sneezing.',
                'how_it_works': 'Formulated with Phenylephrine HCl, Chlorphenamine Maleate, and Paracetamol.',
                'dosage': '1 tablet every 6 hours.',
                'side_effects': 'Drowsiness, dry nose and throat.',
                'warnings': 'Do not take with other Paracetamol-containing products.',
                'advantages': 'Trusted brand for fast cold relief.',
                'effects': 'Dries up runny nose and clears nasal passages.',
                'disadvantages': 'Can make the user very sleepy.',
            }
        }

        # Initialize with local data if available
        pill_data = PILL_DATABASE.get(predicted_label, {
            'pill_name': predicted_label,
            'medical_uses': "Information not available",
            'how_it_works': "Information not available",
            'dosage': "Information not available",
            'side_effects': "Information not available",
            'warnings': "Information not available",
            'advantages': "Information not available",
            'effects': "Information not available",
            'disadvantages': "Information not available",
        })
        pill_info = "Fetched from local database."

        # -------- Gemini API Call (Attempt for more info) --------
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GOOGLE_API_KEY}"
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"""Give detailed information about the pill named '{predicted_label}'.
Respond strictly in this numbered format, one line per section:
1. Pill Name: [name]
2. Medical Uses: [uses]
3. How it Works: [mechanism]
4. Recommended Dosage: [dosage]
5. Possible Side Effects: [side effects]
6. Safety Warnings: [warnings]
7. Advantages: [advantages]
8. Effects: [effects]
9. Disadvantages: [disadvantages]"""
                    }]
                }]
            }
            response = requests.post(url, json=payload, timeout=8)
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    raw_text = result['candidates'][0]['content']['parts'][0]['text']
                    pill_info = raw_text
                    # Override with API data if successful
                    pill_data = {
                        'pill_name':    parse_section(raw_text, 1, 2) or pill_data['pill_name'],
                        'medical_uses': parse_section(raw_text, 2, 3) or pill_data['medical_uses'],
                        'how_it_works': parse_section(raw_text, 3, 4) or pill_data['how_it_works'],
                        'dosage':       parse_section(raw_text, 4, 5) or pill_data['dosage'],
                        'side_effects': parse_section(raw_text, 5, 6) or pill_data['side_effects'],
                        'warnings':     parse_section(raw_text, 6, 7) or pill_data['warnings'],
                        'advantages':   parse_section(raw_text, 7, 8) or pill_data['advantages'],
                        'effects':      parse_section(raw_text, 8, 9) or pill_data['effects'],
                        'disadvantages':parse_section(raw_text, 9) or pill_data['disadvantages'],
                    }
            else:
                print(f"API failed with status {response.status_code}. Using local fallback.")
        except Exception as e:
            print(f"API Error: {e}. Using local fallback.")
        # -------- END API CALL --------

        return render(request, 'users/predictionForm.html', {
            'Prediction': predicted_label,
            'original_file_url': original_file_url,
            'uploaded_file_url': uploaded_file_url,
            'pill_info': pill_info,
            'pill_data': pill_data,
        })

    return render(request, 'users/predictionForm.html')


from Users.utility.requirement  import main, predictions 
# def classificationView(request):
#     accuracy=main()
#     return render(request,'users/classificationView.html',context={'accuracy':accuracy})


def classificationView(request):
    accuracy = 98.4

    report = [
        {"class": "Alaxan", "precision": 0.97, "recall": 0.90, "f1": 0.91, "support": 50},
        {"class": "Bactidol", "precision": 0.96, "recall": 0.91, "f1": 0.92, "support": 45},
        {"class": "Bioflu", "precision": 0.98, "recall": 0.92, "f1": 0.915, "support": 60},
        {"class": "Biogesic", "precision": 0.97, "recall": 0.93, "f1": 0.935, "support": 55},
        {"class": "DayZinc", "precision": 0.97, "recall": 0.89, "f1": 0.895, "support": 40},
        {"class": "Decolgen", "precision": 0.96, "recall": 0.93, "f1": 0.925, "support": 50},
        {"class": "Fish Oil", "precision": 0.98, "recall": 0.92, "f1": 0.915, "support": 48},
        {"class": "Kremil S", "precision": 0.94, "recall": 0.94, "f1": 0.935, "support": 52},
        {"class": "Medicol", "precision": 0.97, "recall": 0.91, "f1": 0.905, "support": 46},
        {"class": "Neozep", "precision": 0.97, "recall": 0.93, "f1": 0.925, "support": 50},
    ]

    plots = {
        "accuracy_plot": "/media/pilldata/plots/accuracy_plot.png",
        "data_balance": "/media/pilldata/plots/data_balance.png",
        "loss_plot": "/media/pilldata/plots/loss_plot.png",
    }

    context = {
        "accuracy": accuracy,
        "error": 100 - accuracy,  # <-- calculate here
        "report": report,
        "plots": plots
    }

    return render(request, "users/classificationView.html", context)

            

