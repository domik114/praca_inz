from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from .models import Offers, Test, CreateUserForm, TestingOffers

def OLX(job = "", localization = ""):
    if job == "":
        return []

    options = ChromeOptions()
    options.headless = True

    driver = Chrome(executable_path="E:\\Studia\\praca_inz\\praca_inz\\chromedriver_nowyt.exe", options=options)

    print(job.replace(" ", "-"))    

    driver.get(f'https://www.olx.pl/d/praca/{localization}/q-{job}/')
    time.sleep(2)

    soup = bs(driver.page_source, features='html.parser')
    titles = []
    href = []
    reszta = []

    sprawdz = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/form/div[4]/div[2]/h3/div")
    sp = sprawdz.text

    import re
    ile = int(re.search(r'\d+', sp).group())

    h6 = soup.find_all("h6")

    i = 0
    for h in h6:
        if i == ile:
            break
        
        titles.append(h.text)
        i += 1

    a = soup.find_all("a")

    i = 0
    for aa in a:
        if i == ile:
            break
        try:
            if "/oferta/" in aa.get("href"):
                href.append("https://www.olx.pl/" + aa.get("href"))
                i += 1
        except:
            print(f"Błąd: {aa} ####################")

    for k in range(2, 20):
        try:
            ps = driver.find_element(By.XPATH, f"/html/body/div[1]/div[1]/div[2]/form/div[5]/div/div[2]/div[{k}]/a/div/div[2]/div/div[1]")
            pp = ps.text
            p = pp.split("\n")

            try:
                p.remove("WYRÓŻNIONE")
            except:
                reszta.append(p)
                continue
            # print(p, k)
            reszta.append(p)
            # reszta.append(p)
        except:
            continue

    ret = {}
    calosc = []

    for z in range(len(titles)):
        try:
            if len(reszta[z]) == 4:
                data = TestingOffers(title=titles[z], contract_type=reszta[z][3], location=reszta[z][1], job_salary=reszta[z][0], href=href[z], keyword=job, site="olx")
                data.save()
                ret = {
                    "title": titles[z], 
                    "href": href[z],
                    "contract": reszta[z][3], 
                    "location": reszta[z][1],
                    "job_salary": reszta[z][0],
                }
            elif len(reszta[z]) == 1:
                data = TestingOffers(title=titles[z], location=reszta[z][1], href=href[z], keyword=job, site="olx")
                data.save()
                ret = {
                    "title": titles[z], 
                    "href": href[z],
                    "location": reszta[z][0],
                }
            elif len(reszta[z]) == 2:
                data = TestingOffers(title=titles[z], location=reszta[z][1], job_salary=reszta[z][0], href=href[z], keyword=job, site="olx")
                data.save()
                ret = {
                    "title": titles[z], 
                    "href": href[z],
                    "location": reszta[z][1],
                    "job_salary": reszta[z][0],
                }
                
            calosc.append(ret)
        except:
            continue

    driver.quit()

    return calosc

def pracuj(job = "", localization = ""):
    if job == "":
        return []

    options = ChromeOptions()
    options.headless = True

    driver = Chrome(executable_path="E:\\Studia\\praca_inz\\praca_inz\\chromedriver_nowyt.exe", options=options)

    print(job.replace(" ", "%20"))
    driver.get(f'https://pracuj.pl/praca/{job};kw/{localization};wp?rd=30')

    time.sleep(2)

    soup = bs(driver.page_source, features='html.parser')
    titles = []

    href = soup.find_all("a", {"data-test": "link-offer"})
    title = soup.find_all("h2", {"data-test": "offer-title"})
    company_name = soup.find_all("h4", {"data-test": "text-company-name"})
    location = soup.find_all("h5", {"data-test": "text-region"})
    contract = soup.find_all("li", {"data-test": "offer-additional-info-3"})

    i = 1
    ilist = list()
    hlist = list()
    tlist = list()
    cnlist = list()
    llist = list()
    clist = list()

    for l in location:
        if "lokalizacje" in l.text or "lokalizacji" in l.text:
            ilist.append(i)
            i += 1
            continue
        i += 1

    for h in href:
        hlist.append(h.get("href"))

    i = 1
    for t in title:
        if i in ilist:
            i += 1
            continue
        tlist.append(t.text)
        i += 1

    i = 1
    for cn in company_name:
        if i in ilist:
            i += 1
            continue
        cnlist.append(cn.text)
        i += 1

    i = 1
    for l in location:
        if i in ilist:
            i += 1
            continue
        llist.append(l.text)
        i += 1

    i = 1
    for c in contract:
        if i in ilist:
            i += 1
            continue
        clist.append(c.text)
        i += 1

    for j in range(len(clist)):
        data = TestingOffers(title=tlist[j], contract_type=clist[j], location=llist[j], company_name=cnlist[j], href=hlist[j], keyword=job, site="pracuj")
        data.save()
        offers = {
            "title": tlist[j],
            "contract": clist[j],
            "location": llist[j],
            "company_name": cnlist[j],
            "href": hlist[j]
        }

        titles.append(offers)

    driver.quit()

    return titles










# dla pracuj it
# options = ChromeOptions()
    # options.headless = True

    # driver = Chrome(executable_path="E:\\Tutoriale\\Python\\Django\\tutorial1\\chromedriver_nowyt.exe", options=options)
    #driver = Chrome(executable_path="E:\\Tutoriale\\Python\\Django\\tutorial1\\chromedriver.exe", options=options)

    # driver.get('https://it.pracuj.pl/')
    time.sleep(1)

    # soup = bs(driver.page_source, features='html.parser')
    titles = []
    
    # for i in range(0, 20):
    #     find = soup.find("div", {"data-test": f"offer-{i}"})
    #     title = find.find("h3", {"data-test": "offer-title"})
    #     href = soup.find("a", {"data-test": "offer-link"}).get("href")
    #     company_name = find.find("span", {"data-test": "company-name"})
    #     contract = find.find("span", {"data-test": "offer-contract"})
    #     location = find.find("span", {"data-test": "offer-location"})
        
    #     if location == None:
    #         offers = {
    #             "title": title.text, 
    #             "contract": contract.text, 
    #             "company_name": company_name.text,
    #             "href": href,
    #         }

    #         print(title.text)
    #         print(href)
    #         print(company_name.text)
    #         print(contract.text)
    #         print()    
    #     else:
    #         offers = {
    #             "title": title.text, 
    #             "contract": contract.text, 
    #             "location": location.text,
    #             "company_name": company_name.text,
    #             "href": href,
    #         }

    #         print(title.text)
    #         print(href)
    #         print(company_name.text)
    #         print(contract.text)
    #         print(location.text)
    #         print()
    #     titles.append(offers)









    # 
        # send = TestingOffers(title=tlist[j], contract_type=clist[j], location=llist[j], company_name=cnlist[j], href=hlist[j], keyword=job, site="pracuj")
        # send.save()
    # 
    # driver = Chrome(executable_path="E:\\Studia\\praca_inz\\praca_inz\\chromedriver_nowyt.exe", options=options)
    # driver = Chrome(executable_path="E:\\Studia\\praca_inz\\praca_inz\\chromedriver_nowyt.exe", options=options)
    # driver = Chrome(executable_path="E:\\Tutoriale\\Python\\Django\\tutorial1\\chromedriver_nowyt.exe", options=options)