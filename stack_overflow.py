import requests
from bs4 import BeautifulSoup

def get_jobs(tag):
  url = f"https://stackoverflow.com/jobs?r=true&q={tag}"
  last_page = get_last_page(url)
  jobs = extract_jobs(url, last_page)
  return jobs

def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
  last_page = pages[-2].get_text(strip=True)
  return int(last_page)

def extract_jobs(url, last_page):
  jobs = []
  for page in range(last_page):
    result = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    jlists = soup.find_all("div", {"class": "-job"})
    for jlist in jlists:
      job = extract_job(jlist)
      jobs.append(job)
  return jobs

def extract_job(html):
  title = html.find("h2").find("a")["title"]
  company, location = html.find("h3").find_all("span", recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True).strip("-").strip("\r").strip("\n")
  job_id = html["data-jobid"]
  return {"title": title, "company": company, "location": location, "link": f"https://stackoverflow.com/jobs/{job_id}"}
