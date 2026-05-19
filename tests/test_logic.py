import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.specialization import detect_specialization
from utils.project_analyzer import analyze_project_quality

def test_dropdown_reactivity():
    skills = ["python", "machine learning", "deep learning"]
    resume_text = "I am an AI/ML enthusiast with experience in python and deep learning."
    
    print("--- Test: Default (AI/ML selected or default) ---")
    result_ai = detect_specialization(skills, resume_text, target_role="AI/ML")
    print(f"Target: AI/ML, Strongest: {result_ai['strongest']['specialization']}, Score: {result_ai['strongest']['score']}")
    
    print("\n--- Test: Switch to Cloud Engineering ---")
    # Even if resume is AI/ML, selecting Cloud Engineering should pivot the 'strongest' result for analysis
    result_cloud = detect_specialization(skills, resume_text, target_role="Cloud Engineering")
    print(f"Target: Cloud Engineering, Strongest: {result_cloud['strongest']['specialization']}, Score: {result_cloud['strongest']['score']}")
    
    assert result_cloud['strongest']['specialization'] == "Cloud Engineering"
    print("\nSUCCESS: Dropdown reactivity logic confirmed.")

def test_dynamic_projects():
    sections = {"projects": "I built a calculator and a todo list."}
    specialization = "AI/ML"
    job_description = "We are looking for someone with experience in PyTorch and Transformers."
    
    print("\n--- Test: Dynamic Project Recommendations ---")
    result = analyze_project_quality(sections, specialization, job_description=job_description)
    print(f"Specialization: {specialization}")
    print("Recommendations:")
    for r in result['recommended_projects']:
        print(f" - {r}")
    
    # Check if PyTorch or Transformers (from JD) appear in recommendations
    found_jd_keyword = any("pytorch" in r.lower() or "transformers" in r.lower() for r in result['recommended_projects'])
    assert found_jd_keyword, "JD keywords should be in recommendations"
    print("\nSUCCESS: Dynamic project recommendations confirmed.")

if __name__ == "__main__":
    try:
        test_dropdown_reactivity()
        test_dynamic_projects()
        print("\nALL TESTS PASSED")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        sys.exit(1)
