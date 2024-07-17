
import streamlit as st
from transformers import pipeline

import random
from googletrans import Translator

# Initialize text classification and translation pipelines
classifier = pipeline("text-classification", model="distilbert-base-uncased")
translation_model_name = "Helsinki-NLP/opus-mt-en-ROMANCE"
translator = pipeline("translation", model=translation_model_name)

# Sample multilingual support (extend as needed)
supported_languages = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian"
}

def get_health_advice(user_input, language):
    symptoms_keywords = {
        "fever": {
            "en": "It might be a viral infection. Please monitor your symptoms and consult a doctor if necessary.",
            "es": "Podría ser una infección viral. Por favor, controle sus síntomas y consulte a un médico si es necesario.",
            "fr": "Cela pourrait être une infection virale. Veuillez surveiller vos symptômes et consulter un médecin si nécessaire.",
            "de": "Es könnte eine Virusinfektion sein. Bitte überwachen Sie Ihre Symptome und konsultieren Sie bei Bedarf einen Arzt.",
            "it": "Potrebbe essere un'infezione virale. Si prega di monitorare i sintomi e consultare un medico se necessario."
        },
        "cough": {
            "en": "You may be experiencing respiratory issues. Stay hydrated and seek medical advice if it persists.",
            "es": "Puede que esté experimentando problemas respiratorios. Mantente hidratado y busca consejo médico si persiste.",
            "fr": "Vous pouvez avoir des problèmes respiratoires. Restez hydraté et demandez un avis médical si cela persiste.",
            "de": "Sie haben möglicherweise Atemprobleme. Bleiben Sie hydratisiert und suchen Sie einen Arzt auf, wenn es anhält.",
            "it": "Potresti avere problemi respiratori. Rimani idratato e cerca un consiglio medico se persiste."
        },
        "headache": {
            "en": "Headaches can be caused by various factors. Ensure you're well-hydrated and rest adequately.",
            "es": "Los dolores de cabeza pueden ser causados por varios factores. Asegúrate de estar bien hidratado y descansa adecuadamente.",
            "fr": "Les maux de tête peuvent être causés par divers facteurs. Assurez-vous d'être bien hydraté et reposez-vous suffisamment.",
            "de": "Kopfschmerzen können durch verschiedene Faktoren verursacht werden. Stellen Sie sicher, dass Sie gut hydratisiert sind und sich ausreichend ausruhen.",
            "it": "I mal di testa possono essere causati da vari fattori. Assicurati di essere ben idratato e di riposare adeguatamente."
        },
        "mental-illness": {
            "en": "It's important to talk to a mental health professional. They can provide you with the support you need.",
            "es": "Es importante hablar con un profesional de salud mental. Pueden brindarte la asistencia que necesitas.",
            "fr": "Il est important de parler à un professionnel de la santé mentale. Ils peuvent vous apporter le soutien dont vous avez besoin.",
            "de": "Es ist wichtig, mit einem Psychologen zu sprechen. Sie können Ihnen die Unterstützung bieten, die Sie benötigen.",
            "it": "È importante parlare con un professionista della salute mentale. Possono fornirti il supporto di cui hai bisogno."
        }
    }
    
    advice = {"en": "Please provide more details or symptoms."}
    for symptom, responses in symptoms_keywords.items():
        if symptom in user_input.lower():
            advice = responses
            break
    
    return advice[language]

def translate_text(text, target_lang):
    if target_lang == "en":
        return text
    translation = translator(text, src_lang="en", tgt_lang=target_lang)
    return translation[0]['translation_text']

# Explanation function
def explain_advice(symptom, language):
    explanations = {
        "fever": {
            "en": "Fever often indicates an infection or illness.",
            "es": "La fiebre a menudo indica una infección o enfermedad.",
            "fr": "La fièvre indique souvent une infection ou une maladie.",
            "de": "Fieber weist oft auf eine Infektion oder Krankheit hin.",
            "it": "La febbre indica spesso un'infezione o una malattia."
        },
        "cough": {
            "en": "A cough can indicate a range of conditions from allergies to infections.",
            "es": "La tos puede indicar una variedad de condiciones, desde alergias hasta infecciones.",
            "fr": "Une toux peut indiquer une gamme de conditions allant des allergies aux infections.",
            "de": "Ein Husten kann auf eine Reihe von Zuständen hinweisen, von Allergien bis hin zu Infektionen.",
            "it": "La tosse può indicare una serie di condizioni, dalle allergie alle infezioni."
        },
        "headache": {
            "en": "Headaches can stem from stress, dehydration, or other medical issues.",
            "es": "Los dolores de cabeza pueden deberse al estrés, la deshidratación u otros problemas médicos.",
            "fr": "Les maux de tête peuvent provenir du stress, de la déshydratation ou d'autres problèmes médicaux.",
            "de": "Kopfschmerzen können durch Stress, Dehydratation oder andere medizinische Probleme verursacht werden.",
            "it": "I mal di testa possono derivare da stress, disidratazione o altri problemi medici."
        },
        "mental-illness": {
            "en": "Mental health issues can arise from stress, anxiety, or other factors.",
            "es": "Los problemas de salud mental pueden ser causados por estrés, ansiedad o otros factores.",
            "fr": "Les problèmes de santé mentale peuvent se produire du stress, de l'anxiété ou d'autres facteurs.",
            "de": "Psychische Erkrankungen können durch Stress, Angst oder andere Faktoren entstehen.",
            "it": "I problemi della salute mentale possono essere causati da stress, da ansietà o da altri fattori."
        }
    }
    
    explanation = explanations.get(symptom, {"en": "No explanation available."})
    return explanation[language]

# Streamlit app
def main():
    st.title("Healthcare Chatbot")
    language = st.selectbox("Select Language", list(supported_languages.values()), index=0)
    lang_code = list(supported_languages.keys())[list(supported_languages.values()).index(language)]
    user_input = st.text_input("How can I assist you today?")

    if st.button("Get Advice"):
        advice = get_health_advice(user_input, lang_code)
        st.write(advice)
        
        for symptom in ["fever", "cough", "headache", "mental-illness"]:
            if symptom in user_input.lower():
                explanation = explain_advice(symptom, lang_code)
                st.write(f"Explanation: {explanation}")
                
        st.write("Thank you for consulting this chatbot! Please let us know how I can further help you.")
        
if __name__ == "__main__":
    main()
