from googlesearch import search
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
import time

model = SentenceTransformer('all-MiniLM-L6-v2')

def fetch_scholar_data(scholar_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    max_retries = 5
    for attempt in range(max_retries):
        response = requests.get(scholar_url, headers=headers)
        if response.status_code == 200:
            break
        elif response.status_code == 429:
            time.sleep(10)  
        else:
            raise Exception(f"Failed to fetch the webpage. Status code: {response.status_code}")
    else:
        raise Exception("Max retries exceeded. Could not fetch the webpage.")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    metrics = {}
    for item in soup.select('#gsc_rsb_st td'):
        try:
            text = item.text.strip()
            if 'Citations' in text:
                metrics['citations'] = int(item.find_next_sibling('td').text.strip())
            if 'h-index' in text:
                metrics['h_index'] = int(item.find_next_sibling('td').text.strip())
            if 'i10-index' in text:
                metrics['i10_index'] = int(item.find_next_sibling('td').text.strip())
        except:
            continue
    
    description = ''
    for item in soup.select('#gsc_prf_bio'):
        description = item.text.strip()

    if not description:
        for item in soup.select('#gsc_prf_int'):
            description = item.text.strip()

    ai_ml_prompts = [
        "machine learning",
        "artificial intelligence",
        "deep learning",
        "neural networks",
        "natural language processing",
        "computer vision",
        "reinforcement learning",
        "data science",
        "supervised learning",
        "unsupervised learning",
        "robotics",
        "autonomous systems",
        "computer graphics",
        "pattern recognition",
        "speech recognition",
        "algorithmic trading",
        "genetic algorithms",
        "fuzzy logic",
        "probabilistic models",
        "support vector machines"
    ]

    qembed = model.encode(ai_ml_prompts)
    if description:
        embeddings = model.encode([description])
        similarities = [util.cos_sim(qembed[i], embeddings)[0].item() for i in range(len(ai_ml_prompts))]
        relevance_score = sum(similarities) / len(similarities)
    else:
        relevance_score = 0

    metrics['relevance_score'] = 200*relevance_score

    return metrics

def get_google_scholar_url(prof_name, college):    
    query = f" Professor {prof_name} {college} Google Scholar" 
    #query = f" 
    # [student_name} Student of {prof_name} {college} Google Scholar"
    for url in search(query, num_results=10):
        if 'scholar.google.com/citations' in url:
            return url
    return None

def get_student_url(student_name, prof_name, college):    
    query = f" {student_name}, {college} Google Scholar"
    for url in search(query, num_results=10):
        if 'scholar.google.com/citations' in url:
            return url
    return None

if __name__ == "__main__":
    prof_name = "Yoshua Bengio"
    student_name = "Alexander Tong"
    college = "Universaite De Montreale"
    scholar_url = get_student_url(student_name,prof_name, college)
    if scholar_url:
        scholar_data = fetch_scholar_data(scholar_url)
        print(scholar_url)
        print(scholar_data)
    else:
        print("Google Scholar profile not found.")
        
        
        
        
        
        
        
        
        
        
        
    # student_url = get_student_url(student_name,prof_name, college)
    # if student_url:
    #     sar_data = fetch_scholar_data(student_url)
    #     print(student_url)
    #     print(sar_data)
    # else:
    #     print("Google Scholar profile not found.")
        
    #student_name = "Alex Karpenko"