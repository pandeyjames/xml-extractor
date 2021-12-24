# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 09:34:19 2021

@author: James AKA DingDong
"""
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import xml.etree.ElementTree as ET
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from datetime import datetime

def print_datetime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

print_datetime()

#object of FirefoxOptions
options = webdriver.FirefoxOptions()
#setting headless parameter
options.headless = False


#from pyvirtualdisplay import Display
#options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument('window-size=1920x1080')
#options.add_argument("disable-gpu")
# OR options.add_argument("--disable-gpu")
#display = Display(visible=0, size=(800, 600))
#display.start()
#browser = webdriver.Chrome('chromedriver', chrome_options=options)

browser = webdriver.Firefox(executable_path="geckodriver", options=options)
wait = WebDriverWait(browser, 5)
AgenciaLink = "https://www.remax.pt/agencias?searchQueryState={%22name%22:%22golden%22,%22page%22:1,%22regionID%22:null,%22regionName%22:null}"
browser.get(AgenciaLink)
element_office = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "agentoffice-search-results-component")))
linksofagencias =[]
if browser.find_elements(By.XPATH,'//div[@class="agentoffice-search-results-component"]//a[@class="office-link"]'):  
    linksagencias = browser.find_elements(By.XPATH,'//div[@class="agentoffice-search-results-component"]//a[@class="office-link"]')

for linkagencia in linksagencias:
    link_a = linkagencia.get_attribute("href")
    linksofagencias.append(link_a)
    print (link_a)

print ("<RecordList>")
print ("<AgenciaRemax>")
#creating xml file consultores.xml
root = ET.Element("RecordList")
agenciaremax = ET.SubElement(root, "AgenciaRemax")
f = open("imoveis.txt", "w")
f.close()
f = open("imoveis.txt", "a")
#f.write("Now the file has more content!")

for agencialink in linksofagencias:
    #browser.get('https://www.remax.pt/agencia/remax-golden-line/12376')
    browser.get(agencialink)
    #time.sleep(1)
    id_remax = "12376"
    page_title = browser.title
    print (page_title)
    # Save the window opener (current window, do not mistaken with tab... not the same)
    main_window = browser.current_window_handle
    
    #actions = ActionChains(browser)
    #actions.move_to_element(element).perform()
    #if page_title != '0 casas para alugar | RE/MAX' :
    elements = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "office-details-agents")))
    
    #grab links of the imoveis of this agency
    if browser.find_elements(By.XPATH,'//div[@class="shared-relatedlistings-component"]//a[@class="link-button"]'):
        linkbuttons = browser.find_elements(By.XPATH,'//div[@class="shared-relatedlistings-component"]//a[@class="link-button"]')
        links = []
        for linkbutton in linkbuttons:
            link = linkbutton.get_attribute("href")
            links.append(link)
            print (link)
            f.write(link)
        
    
    print ("<IDRemax>"+id_remax+"</IDRemax>")
    agencia_name =""
    if browser.find_elements(By.XPATH,'//div[@class="office-info-header"]//h2'):
        agencia_name = browser.find_element(By.XPATH,'//div[@class="office-info-header"]//h2').text
    description = ""
    if browser.find_elements(By.XPATH,'//div[@class="office-description"]'):
        description = browser.find_element(By.XPATH,'//div[@class="office-description"]').text
    print ("<Nome>"+agencia_name+"</Nome>")
    print ("<Description>"+description+"</Description>")
    print ("<Consultores>")
    
    
    agenciaremaxid = ET.SubElement(root, "IDRemax")
    agenciaremaxid.text = id_remax
    agenciaremaxname = ET.SubElement(root, "Nome")
    agenciaremaxname.text = agencia_name
    agenciaremaxconsultores = ET.SubElement(root, "Consultores")
    
    # identify elements of same classname
    # iterate through list and get text
    if browser.find_elements(By.XPATH,'//div[@class="agent-smallcard-component "]//a'):
        agents = browser.find_elements(By.XPATH,'//div[@class="agent-smallcard-component "]//a')
        for agent in agents:
            print ("<Consultor>")
            agent_name = agent.text
            agent_link = agent.get_attribute('href')
            x = agent_link.split("/")
            id_agent = x[5]
            
            agent_img = agent.find_element(By.CLASS_NAME,'picture').get_attribute("src")
            # Open the link in a new tab by sending key strokes on the element
            # Use: Keys.CONTROL + Keys.SHIFT + Keys.RETURN to open tab on top of the stack 
            agent.send_keys(Keys.CONTROL + Keys.RETURN)
            # Switch tab to the new tab, which we will assume is the next one on the right
            browser.switch_to.window(browser.window_handles[1])
            # Put focus on current window which will, in fact, put focus on the current visible tab
            #browser.switch_to_window(main_window)
            elementsoftab = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "agent-details")))
            contact_info = browser.find_element(By.XPATH,'//span[@class="mobile-phone"]//button').click()
            time.sleep(1)
            #ActionChains(browser).click(contact_info).perform()
            texttelemovel = browser.find_element(By.XPATH,'//div[@class="contact-info all-contacts"]//span[@class="mobile-phone"]//span').text
            while texttelemovel.find("***") > 0:
                texttelemovel = browser.find_element(By.XPATH,'//div[@class="contact-info all-contacts"]//span[@class="mobile-phone"]//span').text
            print ("<Telemovel>"+texttelemovel+"</Telemovel>")
            posicao = browser.find_element(By.XPATH,'//p[@class="agent-info-role"]').text
            print ("<Posicao>"+posicao+"</Posicao>")
            # Close current tab
            browser.close()
            #browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
            
            
            # Put focus on current window which will be the window opener
            #browser.switch_to_window(main_window-1)
            
            #Focus to the main window
            browser.switch_to.window(main_window)
            
            
            #print person.find_element_by_xpath['//div[@class="title"]//a').text
            #agent_name = agent.find_element(By.XPATH,'//div[@class="agent-smallcard-component "]//a').text
            #agent_link = agent.find_element(By.XPATH,'//div[@class="agent-smallcard-component "]//a').get_attribute('href')
            #agent_picture = agent.find_elements(By.XPATH,'//div[@class="agent-card-picture"]//picture//source').get_attribute('srcset')
            #agent_img = agent.find_element(By.XPATH,'//div[@class="agent-card-picture"]//picture//img').get_attribute('src')
            print ("<IDRemax>"+id_agent+"</IDRemax>")
            print ("<Nome>"+agent_name+"</Nome>")
            #print ("<Email>"+email+"</Email>")
            print ("</AgentLink>"+agent_link+"</AgentLink>")
            print ("<Foto>"+agent_img+"</Foto>")
            print ("</Consultor>")
            
            consultor = ET.SubElement(agenciaremaxconsultores, "Consultor")
            consultorid = ET.SubElement(agenciaremaxconsultores, "IDRemax")
            consultorid.text = id_agent
            consultorname = ET.SubElement(agenciaremaxconsultores, "Nome")
            consultorname.text = agent_name
            consultorlink = ET.SubElement(agenciaremaxconsultores, "AgentLink")
            consultorlink.text = agent_link
            consultorfoto = ET.SubElement(agenciaremaxconsultores, "Foto")
            consultorfoto.text = agent_img
            consultortelemovel = ET.SubElement(agenciaremaxconsultores, "Telemovel")
            consultortelemovel.text = texttelemovel
            consultorposicao = ET.SubElement(agenciaremaxconsultores, "Posicao")
            consultorposicao.text = posicao
        
        
print ("</Consultores>")
print ("</AgenciaRemax>")
print ("</RecordList>")

#export xml file
tree = ET.ElementTree(root)
tree.write("consultores.xml")

print_datetime()
f.close()
browser.close()