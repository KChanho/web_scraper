import requests
from bs4 import BeautifulSoup

def get_jobs(tag):
  url = f"https://weworkremotely.com/remote-jobs/search?term={tag}"
  jobs = extract_jobs(url)
  return jobs

def extract_jobs(url):
  jobs = []
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  jlists = soup.find("div", {"class": "jobs-container"}).find_all("section", {"class": "jobs"})
  for jlist in jlists:
    lists = jlist.find_all("li")
    lists = lists[:-1]
    for list in lists:
      job = extract_job(list)
      jobs.append(job)
  return jobs

def extract_job(html):
  title = html.find("span", {"class": "title"}).get_text(strip=True)
  company = html.find("span", {"class": "company"}).get_text(strip=True)
  location = html.find("span", {"class": "region"})
  if location:
    location = location.get_text(strip=True)
  else:
    location = None
  link = html.find("a", recursive=False)["href"]
  return {"title": title, "company": company, "location": location, "link": f"https://weworkremotely.com{link}"}
