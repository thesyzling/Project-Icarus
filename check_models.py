import google.generativeai as genai

API_KEY = "AIzaSyAdQUcd9CnbbvaaHNa7jK_aO5aBYSSoGlg" # <-- Kendi anahtarın
genai.configure(api_key=API_KEY)

print("--- KULLANILABİLİR MODELLER ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ {m.name}")
except Exception as e:
    print(f"HATA: {e}")
