"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
import os
from stack_overflow import get_jobs as get_SO_jobs
from remote_ok import get_jobs as get_RO_jobs
from we_work_remotely import get_jobs as get_WWR_jobs
from exporter import save_to_file
from flask import Flask, render_template, request, redirect, send_file

os.system("clear")

app = Flask("JobScrapper")
db = {} #fake DB

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/report")
def report():
  tag = request.args.get("tag")
  if tag:
    tag = tag.lower()
    existingJobs = db.get(tag)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_SO_jobs(tag) + get_RO_jobs(tag) + get_WWR_jobs(tag)
      db[tag] = jobs
  else:
    return redirect("/")
  return render_template(
    "report.html", 
    searchingBy = tag, 
    resultsNumber = len(jobs),
    jobs = jobs
  )

@app.route("/export")
def export():
  try:
    tag = request.args.get('tag')
    if not tag:
      raise Exception()
    tag = tag.lower()
    jobs = db.get(tag)
    if not jobs:
      raise Exception()
    save_to_file(jobs, tag)
    return send_file(f"{tag}_jobs.csv")
  except:
    return redirect("/")
  

app.run(host = "0.0.0.0") #for repl.it