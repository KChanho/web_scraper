import requests
from bs4 import BeautifulSoup

def get_jobs(tag):
  url = f"https://remoteok.com/remote-{tag}-jobs"
  jobs = extract_jobs(url)
  return jobs

def extract_jobs(url):
  jobs = []
  user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
  request_headers = {"User-Agent": user_agent}
  result = requests.get(url, headers = request_headers)  #503 error... -> User-Agent
  soup = BeautifulSoup(result.text, "html.parser")
  jlists = soup.find_all("tr", {"class": "job"})
  for jlist in jlists:
    job = extract_job(jlist)
    jobs.append(job)
  return jobs

def extract_job(html):
  title = html.find("h2", {"itemprop": "title"}).get_text(strip=True)
  company = html.find("h3", {"itemprop": "name"}).get_text(strip=True)
  location = html.find("div", {"class": "tooltip"})
  if location:
    location = location.get_text(strip=True)
    if "$" in location:
      location = None #if location is empty
  else:
    location = None
  link = html.find("a", {"class": "preventLink"})["href"]
  return {"title": title, "company": company, "location": location, "link": f"https://remoteok.com{link}"}
