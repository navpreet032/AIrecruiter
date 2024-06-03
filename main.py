from prof import professors as PROFESSORS
from perplexity_api import PerplexityAPI  
from github import score_github_user
from university import UNIVERSITY_SCORES
import requests
from candidate import Candidate
from normalise import normalize_scores as normaliser

perplexity_api = PerplexityAPI(api_key="apikey")

tmp_data= {
  "personalInfo": {
    "name": "Pieter Abbeel",
    "title": "Professor",
    "institution": "University of California, Berkeley",
    "department": "Electrical Engineering and Computer Sciences",
    "bio": "Pieter Abbeel is a Professor at the University of California, Berkeley, in the Department of Electrical Engineering and Computer Sciences. He received his Ph.D. in Computer Science from Stanford University in 2008."
  },
  "links": {
    "professionalProfiles": [
      {
        "platform": "Google Scholar",
        "url": "https://scholar.google.com/citations?user=JicYPdAAAAAJ"
      },
      {
        "platform": "LinkedIn",
        "url": "https://www.linkedin.com/in/pieterabbeel/"
      },
      {
        "platform": "Twitter",
        "url": "https://twitter.com/pabbeel"
      }
    ],
    "additionalResources": [
      {
        "title": "Berkeley AI Research Lab",
        "url": "https://bair.berkeley.edu/"
      },
      {
        "title": "OpenAI",
        "url": "https://openai.com/"
      }
    ]
  },
  "contactInfo": {
    "email": "pabbeel@berkeley.edu",
    "phone": "",
    "fax": "",
    "office": {
      "building": "Cory Hall",
      "room": "565 Soda Hall"
    }
  },
  "professionalActivities": {
    "researchInterests": [
      "Artificial Intelligence",
      "Machine Learning",
      "Robotics"
    ],
    "currentProjects": [
      {
        "title": "Imitation Learning",
        "description": "Developing algorithms for robots to learn from human demonstrations.",
        "collaborators": [
          "Chelsea Finn",
          "Sergey Levine"
        ],
        "fundingSources": [
          "National Science Foundation",
          "OpenAI"
        ]
      },
      {
        "title": "Deep Reinforcement Learning",
        "description": "Investigating methods for agents to learn and improve their behavior through trial and error.",
        "collaborators": [
          "John Schulman",
          "Wojciech Zaremba"
        ],
        "fundingSources": [
          "Google",
          "Facebook"
        ]
      }
    ],
    "industryExperience": [
      {
        "company": "OpenAI",
        "role": "Co-founder",
        "period": "2015 - Present",
        "description": "Leading research and development efforts in artificial intelligence."
      },
      {
        "company": "Covariant",
        "role": "Co-founder",
        "period": "2017 - Present",
        "description": "Building AI software for robotic automation in industries such as logistics and manufacturing."
      }
    ]
  },
  "publications": [
    {
      "title": "Apprenticeship Learning and Reinforcement Learning with Application to Robotic Control",
      "authors": [
        "Pieter Abbeel",
        "Andrew Y. Ng"
      ],
      "journal": "International Conference on Machine Learning (ICML)",
      "year": 2004,
      "url": "https://ai.stanford.edu/~ang/papers/icml04-apprentice.pdf"
    },
    {
      "title": "Deep Learning for Robotics",
      "authors": [
        "Pieter Abbeel",
        "Trevor Darrell"
      ],
      "journal": "IEEE Robotics & Automation Magazine",
      "year": 2017,
      "url": "https://ieeexplore.ieee.org/document/7965940"
    }
  ],
  "patents": [],
  "teaching": {},
  "mentorship": {},
  "reviewingActivities": [
    "Conference on Neural Information Processing Systems (NeurIPS)",
    "International Conference on Robotics and Automation (ICRA)"
  ]
}
def find_students(scrap):
    candidates = []
    for student_data in scrap.get("students", []):
        print(student_data)
        name = student_data.get("name", "")
        degree_type = student_data.get("degree_type", "")
        field_of_study = student_data.get("field_of_study", "")
        professor_guide = student_data.get("professor_guide", "")
        github_repo = student_data.get("github_repo", "")
        github_score = score_github_user(github_repo) if github_repo else 0
        uni_score = UNIVERSITY_SCORES.get(student_data.get("university", ""), 0)
        prof_score = student_data.get("prof_score", 0)
        h_index = student_data.get("h_index", 0)
        candidate = Candidate(
            name=name,
            degree_type=degree_type,
            field_of_study=field_of_study,
            professor_guide=professor_guide,
            github_repo=github_repo,
            github_score=github_score,
            uni_score=uni_score,
            prof_score=prof_score,
            h_index=h_index
        )
        candidates.append(candidate)
        print(f"candidate:--> {candidates}")
    return candidates

def main():
    all_candidates = []
    
    for university, professors in PROFESSORS.items():
        for prof in professors:
            webpage = prof["webpage"]
            try:
                # scrap = perplexity_api.scrape_webpage(webpage)
                scrap = tmp_data
                print(f"in loop:--> {webpage}")
                candidates = find_students(scrap)
                all_candidates.extend(candidates)
            except requests.exceptions.RequestException as e:
                print(f"Failed to scrape {webpage}: {e}")
                continue

    final_list = normaliser(all_candidates)            
    for candidate in all_candidates:
        print(candidate.calculate_overall_score)

if __name__ == "__main__":
    main()
