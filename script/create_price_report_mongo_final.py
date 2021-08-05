#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 12:04:02 2021

@author: himanshusolanki
"""

# importing pymongo
from pymongo import MongoClient
import pandas as pd
# import pprint
import datetime
# import json
import PIL
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import gspread
import sys



supply_template = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\Raw.jpg"
demand_template = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\Raw.jpg"


today = datetime.date.today()

##### Alignment Section
 
def center_text(img, font, text, strip_width,strip_height,color=(255,255,255)):
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(text, font)
    position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
    draw.text(position, text, fill = color, font=font)
    return img

def left_text(img, font, text, strip_width,strip_height,color=(255, 255, 255)):
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(text, font)
    position = (0,(strip_height-text_height)/2)
    draw.text(position, text, fill = color, font=font)
    return img

def right_text(img, font, text, strip_width,strip_height,color=(255, 255, 255)):
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(text, font)
    position = (strip_width-text_width,(strip_height-text_height)/2)
    draw.text(position, text, fill = color, font=font)
    return img

##### Creating Text Wrap Functions for Multiple Line Messages

def text_wrap(text, font, max_width):
    lines = []
    # If the width of the text is smaller than image width
    # we don't need to split it, just add it to the lines array
    # and return
    if font.getsize(text)[0] <= max_width:
        lines.append(text) 
    else:
        # split the line by spaces to get words
        words = text.split(' ')  
        i = 0
        # append every word to a line while its width is shorter than image width
        while i < len(words):
            line = ''         
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:                
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            # when the line gets longer than the max width do not append the word, 
            # add the line to the lines array
            lines.append(line)    
    return lines

def date_gap(x,y):
    return (x-y).days

def most_frequent(List):
    return max(set(List), key = List.count)

### Preparing the Report for each Mandi-Crop-Date Combination
def prepare_report(mandi_df):
    mandi_type = list(set(mandi_df["Mandi Type (Supply/Demand)"]))
    font_path = "C:\\Windows\\Fonts\\Arial\\arialbd.ttf"
    boldFont_path = "C:\\Windows\\Fonts\\Arial\\arialbd.ttf"
    # noteFontPath = "C:\\Windows\\Fonts\\Courier New\\cour.ttf"
    # noteFontPath = "C:\\Windows\\Fonts\\Arial\\ARIALNB.TTF"
    # noteFontPath = "C:\\Windows\\Fonts\\Segoe UI\\segoeuil.ttf"
    noteFontPath = "C:\\Windows\\Fonts\\Segoe UI\\segoeuisl.ttf"
    # contributorFontPath = "C:\\Windows\\Fonts\\Noto Sans\\NotoSans-Bold.ttf"
    contributorFontPath = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\Mukta\Mukta-Bold.ttf"
    if mandi_type[0] == "Demand":
        im = Image.open(demand_template)
    elif mandi_type[0] == "Supply":
        im = Image.open(supply_template)

    ####### Adding Mandi Titles
    header_size = (1950, 100) # 399
    header_pos = (660, 145)
    
    strip_width, strip_height = (1950, 100)
    
    header_image = Image.new("RGB", header_size, color = (243, 231, 255))
    font = ImageFont.truetype(boldFont_path, 105)
    
    mandi_title = list(set(mandi_df["Report_Title"]))
    
    header = center_text(header_image,font, mandi_title[0], strip_width, strip_height,color = (113, 25, 240))
    im.paste(header, header_pos)
    # header.show()
    # sys.exit(0)
    
    ####### Adding Price Date
    date_size = (1400,100)
    date_pos = (770,300)

    strip_width, strip_height = (1400, 100)
    
    date = Image.new("RGB", date_size, color = (243, 231, 255))
    font = ImageFont.truetype(boldFont_path, 105)
    
    date_title = list(set(mandi_df["Date"]))
    date_title_string = date_title[0].strftime("%d-%b-%Y")
    
    date_header = center_text(date,font, date_title_string, strip_width, strip_height,color = (113, 25, 240))
    im.paste(date_header, date_pos)

    ####### Adding Crop
    crop_size = (1400,100)
    crop_pos = (770,445)

    strip_width, strip_height = (1400, 100)
    
    crop = Image.new("RGB", crop_size, color = (243, 231, 255))
    font = ImageFont.truetype(boldFont_path, 110)
    crop_title = list(set(mandi_df["Crop"]))
    crop_header = center_text(crop,font, crop_title[0] , strip_width, strip_height,color = (113, 25, 240))
    im.paste(crop_header, crop_pos)

    ####### Adding New Arrival Section 1
    arrival1_mt_size = (1400, 150)
    arrival1_mt_pos = (170, 2000)
    
    strip_width, strip_height = (1400, 150)
    
    arrival1_mt = Image.new("RGB", arrival1_mt_size, color = (255,255,255))
    font = ImageFont.truetype(font_path, 75)
    
    new_arrival_mt = list(set(mandi_df["New Arrivals (MT)"]))[0]
    # print(type(new_arrival_mt))
    # print(new_arrival_mt)
    if mandi_type[0] == "Demand":
        try:
            arrival1_mt_detail = left_text(arrival1_mt,font, "New Arrivals (MT) - %s"%int(new_arrival_mt),strip_width, strip_height, color = (0,0,0))
        except:
            arrival1_mt_detail = left_text(arrival1_mt,font, "New Arrivals (MT) - %s"%new_arrival_mt,strip_width, strip_height, color = (0,0,0))
    elif mandi_type[0] == "Supply":
        try:
            arrival1_mt_detail = left_text(arrival1_mt,font, "Total Arrivals (MT) - %s"%int(new_arrival_mt),strip_width, strip_height, color = (0,0,0))
        except:
            arrival1_mt_detail = left_text(arrival1_mt,font, "Total Arrivals (MT) - %s"%new_arrival_mt,strip_width, strip_height, color = (0,0,0))
        
    im.paste(arrival1_mt_detail, arrival1_mt_pos)
    
    ####### Adding New Arrival Section 2
    arrival1_bags_size = (1400, 150)
    arrival1_bags_pos = (170, 2110)
    strip_width, strip_height = (1400, 150)
    
    arrival1_bags = Image.new("RGB", arrival1_bags_size, color = (255,255,255))
    font = ImageFont.truetype(font_path, 75)
    
    new_arrival_bags = list(set(mandi_df["New Arrivals (Bags)"]))[0]
    # print(type(new_arrival_bags))
    # print(new_arrival_bags)
    if mandi_type[0] == "Demand":
        try:
            arrival1_bags_detail = left_text(arrival1_bags,font, "New Arrivals (Bags) - %s"%int(new_arrival_bags),strip_width, strip_height, color = (0,0,0) )
        except:
            arrival1_bags_detail = left_text(arrival1_bags,font, "New Arrivals (Bags) - %s"%new_arrival_bags,strip_width, strip_height, color = (0,0,0) )
    elif mandi_type[0] == "Supply":
        try:
            arrival1_bags_detail = left_text(arrival1_bags,font, "Total Arrivals (Bags) - %s"%int(new_arrival_bags),strip_width, strip_height, color = (0,0,0) )
        except:
            arrival1_bags_detail = left_text(arrival1_bags,font, "Total Arrivals (Bags) - %s"%new_arrival_bags,strip_width, strip_height, color = (0,0,0) )

    im.paste(arrival1_bags_detail, arrival1_bags_pos)
    
    ####### Adding Balance Arrival Section 1
    arrival2_mt_size = (1400, 150)
    arrival2_mt_pos = (1690, 2000)
    
    strip_width, strip_height = (1400, 150)
    
    arrival2_mt = Image.new("RGB", arrival2_mt_size, color = (255,255,255))
    font = ImageFont.truetype(font_path, 75)

    balance_arrival_mt = list(set(mandi_df["Balance Arrivals (MT)"]))[0]
    if mandi_type[0] == "Demand":
        try:
            arrival2_mt_detail = left_text(arrival2_mt,font, "Balance Arrivals (MT) - %s"%int(balance_arrival_mt), strip_width, strip_height, color = (0,0,0))
        except:
            arrival2_mt_detail = left_text(arrival2_mt,font, "Balance Arrivals (MT) - %s"%balance_arrival_mt, strip_width, strip_height, color = (0,0,0))
        im.paste(arrival2_mt_detail, arrival2_mt_pos)

    ####### Adding Balance Arrival Section 2
    arrival2_bags_size = (1400, 150)
    arrival2_bags_pos = (1690, 2110)
    
    strip_width, strip_height = (1400, 150)
    
    arrival2_bags = Image.new("RGB", arrival2_bags_size, color = (255,255,255))
    font = ImageFont.truetype(font_path, 75)
    
    balance_arrival_bags = list(set(mandi_df["Balance Arrivals (Bags)"]))[0]
    
    if mandi_type[0] == "Demand":
        try:
            arrival2_bags_detail = left_text(arrival2_bags,font, "Balance Arrivals (Bags) - %s"%int(balance_arrival_bags), strip_width, strip_height, color = (0,0,0))
        except:
            arrival2_bags_detail = left_text(arrival2_bags,font, "Balance Arrivals (Bags) - %s"%balance_arrival_bags, strip_width, strip_height, color = (0,0,0))
        im.paste(arrival2_bags_detail, arrival2_bags_pos)

    ####### Adding Variety Names
    
    variety_size = (1300, 100)
    font = ImageFont.truetype(font_path, 70)

    strip_width, strip_height = (1300, 100)
    
    ### Setting Default Values for Grade
    try:
        preferred_grade_df = mandi_df[mandi_df["Preferred_Grade"] == "1"]
        main_grade = most_frequent(list(preferred_grade_df["Grade"]))
    except:
        main_grade = most_frequent(list(mandi_df["Grade"]))
    
    variety_df = mandi_df[mandi_df["Grade"] == main_grade]
    variety_df = variety_df.drop_duplicates()
    variety_df.sort_values(by=["Min Price (Rs/Quintal)"], ascending=False, inplace=True)
    
    variety_list = variety_df["Variety"]
    variety_list = variety_list.iloc[:6]
    i = 0
    for varieties in variety_list:
        variety = Image.new("RGB", variety_size, color = (255,255,255))
        variety_detail = left_text(variety,font,varieties, strip_width, strip_height, color = (0,0,0))
        variety_pos = (170, 830 + i*110)
        im.paste(variety_detail, variety_pos)
        i += 1
        
    ####### Adding Variety Prices

    variety_price_size = (450, 100)
    font = ImageFont.truetype(font_path, 70)
    strip_width, strip_height = (450, 100)
    
    ### Setting Default Values for Grade
    try:
        preferred_grade_df = mandi_df[mandi_df["Preferred_Grade"] == "1"]
        main_grade = most_frequent(list(preferred_grade_df["Grade"]))
    except:
        main_grade = most_frequent(list(mandi_df["Grade"]))

#    main_grade = most_frequent(list(mandi_df["Grade"]))
    variety_df = mandi_df[mandi_df["Grade"] == main_grade]
    variety_df = variety_df.drop_duplicates()
    variety_df.sort_values(by=["Min Price (Rs/Quintal)"], ascending=False, inplace=True)
    
    variety_df["Price_String"] = variety_df["Min Price (Rs/Quintal)"].astype(str) + " " + "-" + " " + variety_df["Max Price (Rs/Quintal)"].astype(str)
    
    price_variety_list = variety_df["Price_String"]
    price_variety_list = price_variety_list.iloc[:6]
    
    i = 0
    for price in price_variety_list:
        price_variety = Image.new("RGB", variety_price_size, color = (255,255,255))
        price_variety_detail = right_text(price_variety,font,price, strip_width, strip_height,color = (0,0,0))
        price_variety_pos = (1070, 830+ i*110)
        im.paste(price_variety_detail, price_variety_pos)
        i += 1

    ####### Adding Price by Variety : Note 1
    
    note_size = (1400, 100)
    font = ImageFont.truetype(noteFontPath, 67)
    strip_width, strip_height = (1400, 100)
    
    note_list = ["Note : All prices in INR / quintal; For %s Grade"%str(main_grade)]
    lines = text_wrap(note_list[0], font, note_size[0])
    
    i = 0
    for line in lines:
        note_1 = Image.new("RGB", note_size, color = (255, 255, 255))
        note1_detail = left_text(note_1,font,line, strip_width, strip_height, color = (0,0,0))
        note1_pos = (170, 930 + 6*110 + i*100)
        im.paste(note1_detail, note1_pos)
        i += 1

    ####### Adding Grade Names
    grade_size = (1300, 100)    
    font = ImageFont.truetype(font_path, 70)

    strip_width, strip_height = (1300, 100)

    ### Setting Default Values for Variety
    try:
        preferred_variety_df = mandi_df[mandi_df["Preferred_Variety"] == "1"]
        main_variety = most_frequent(list(preferred_variety_df["Variety"]))
    except:
        main_variety = most_frequent(list(mandi_df["Variety"]))
    
#    main_variety = most_frequent(list(mandi_df["Variety"]))
    grade_df = mandi_df[mandi_df["Variety"] == main_variety]
    grade_df = grade_df.drop_duplicates()
    grade_df.sort_values(by=["cmdtyID","gradeOrder"],inplace=True)
    
    grade_list = grade_df["Grade"]    
    grade_list = grade_list.iloc[:6]
    print(grade_list)
    
    i = 0
    for grades in grade_list:
        grade = Image.new("RGB", grade_size, color = (255,255,255))
        grade_detail = left_text(grade,font,grades, strip_width, strip_height, color = (0,0,0))
        grade_pos = (1690, 830 + i*110)
        im.paste(grade_detail, grade_pos)
        i += 1

    
    ######### Adding Grade Prices

    grade_price_size = (450, 100)    
    font = ImageFont.truetype(font_path, 70)
    
    strip_width, strip_height = (450, 100)

    ### Setting Default Values for Variety
    try:
        preferred_variety_df = mandi_df[mandi_df["Preferred_Variety"] == "1"]
        main_variety = most_frequent(list(preferred_variety_df["Variety"]))
    except Exception as e:
        print(e)
        main_variety = most_frequent(list(mandi_df["Variety"]))
   
    print("Main_Variety", main_variety)
    print("Main_Grade", main_grade)
    
#    main_variety = most_frequent(list(mandi_df["Variety"]))
    grade_df = mandi_df[mandi_df["Variety"] == main_variety]
    grade_df = grade_df.drop_duplicates()

    grade_df["Price_String"] = grade_df["Min Price (Rs/Quintal)"].astype(str) + " " + "-" + " " + grade_df["Max Price (Rs/Quintal)"].astype(str)
    price_grade_list = grade_df["Price_String"]
    price_grade_list = price_grade_list.iloc[:6]
    
    i = 0
    for price in price_grade_list:
        price_grade = Image.new("RGB", grade_price_size, color = (255,255,255))
        price_grade_detail = right_text(price_grade,font,price, strip_width, strip_height,color = (0,0,0), )
        price_grade_pos = (2590, 830 + i*110)
        im.paste(price_grade_detail, price_grade_pos)
        i += 1

    
    ####### Adding Price by Grade : Note 2
    
    note2_size = (1400, 100)
    font = ImageFont.truetype(noteFontPath, 67)

    strip_width, strip_height = (1400, 100)
    
    note2_list = ["Note : All prices in INR / quintal; For %s Variety"%str(main_variety)]

    lines = text_wrap(note2_list[0], font, note2_size[0])    
    i = 0
    for line in lines:
        note_2 = Image.new("RGB", note2_size, color = (255, 255, 255))
        note2_detail = left_text(note_2,font,line, strip_width, strip_height,color = (0,0,0))
        note2_pos = (1690, 930 + 6*110 + i*100)
        im.paste(note2_detail, note2_pos)
        i += 1
    
    ####### Adding Day's Analysis
    analysis_size = (1400, 100)
    font = ImageFont.truetype(font_path, 75)
    
    strip_width, strip_height = (1400, 100)
    
    text = most_frequent(list(mandi_df["Day_Analysis"]))
    lines = text_wrap(text, font, analysis_size[0])
    
    i = 0
    for line in lines :
        analysis = Image.new("RGB", analysis_size, color = (255, 255, 255))
        analysis_detail = left_text(analysis,font,line, strip_width, strip_height, color = (0,0,0))
        analysis_pos = (140, 2650 + i*100)
        im.paste(analysis_detail, analysis_pos)
        i += 1
        
    ####### Adding Forecast
    forecast_size = (1400, 100)
    font = ImageFont.truetype(font_path, 75)
    
    strip_width, strip_height = (1400, 100)
    
    text = most_frequent(list(mandi_df["Forecast"]))
    lines = text_wrap(text, font, analysis_size[0])
    
    i = 0
    for line in lines :
        forecast = Image.new("RGB", forecast_size, color = (255, 255, 255))
        forecast_detail = left_text(forecast,font,line, strip_width, strip_height, color = (0,0,0))
        forecast_pos = (1700, 2650 + i*100)
        im.paste(forecast_detail, forecast_pos)
        i += 1
    
    # ####### Adding Forecast : Note
    # note2_size = (1400, 70)
    # font = ImageFont.truetype(font_path, 50)

    # strip_width, strip_height = (1400, 70)
   
    # note_forecast_list = ["Note : Given forecast is indicative and will depend on arrivals,weather and other conditions"]

    # lines = text_wrap(note_forecast_list[0], font, note2_size[0])
    # i = 0
    # for line in lines:
    #     note_2 = Image.new("RGB", note2_size, color = (255, 255, 255))
    #     note2_detail = left_text(note_2,font,line, strip_width, strip_height,color = (0,0,0))
    #     note2_pos = (1850, 2840 + i*70)
    #     im.paste(note2_detail, note2_pos)
    #     i += 1

        
    ####### Adding Countributor Details    
    cname_size = (3200, 100)
    cname_pos = (170, 3140)
    font = ImageFont.truetype(contributorFontPath, 80)
    
    strip_width, strip_height = (3200, 100)
    
    cname = Image.new("RGB", cname_size, color = (255,255,255))
    countributor_name_address = str(most_frequent(list(mandi_df["Countributor_Name_Address"]))).strip()

    cname_detail = left_text(cname,font, countributor_name_address, strip_width, strip_height, color = (0,0,0))    
    im.paste(cname_detail, cname_pos)
# .str.encode("utf-8")
    ####### Adding Contact Details
    contact_size = (3200, 100)
    contact_pos = (170, 3250)
    font = ImageFont.truetype(font_path, 75)

    strip_width, strip_height = (3200, 100)

    ccontact = Image.new("RGB", contact_size, color = (255,255,255))
    mandi_df["Contact_Details"] = "Mobile Number : " + mandi_df["Countributor Mobile Number"] + " " + "," + "WhatsApp Number : " + mandi_df["Countributor Whatsapp Number"]
    # mandi_df["Contact_Details"] = "Mobile Number : " + mandi_df["Countributor Mobile Number"]
    countributor_contact_details = most_frequent(list(mandi_df["Contact_Details"]))    
    
    
    
    ccontact_detail = left_text(ccontact,font, countributor_contact_details, strip_width, strip_height,color = (0,0,0))
    im.paste(ccontact_detail, contact_pos)
    
    # ####### Adding Contact Details
    # contact_size = (3200, 100)
    # contact_pos = (170, 3390)
    # font = ImageFont.truetype(font_path, 80)

    # strip_width, strip_height = (3200, 100)

    # ccontact = Image.new("RGB", contact_size, color = (255,255,255))    
    # # mandi_df["Contact_Details"] = "Mobile Number : " + mandi_df["Countributor Mobile Number"] + " " + "," + "WhatsApp Number : " + mandi_df["Countributor Whatsapp Number"]
    # mandi_df["Contact_Details"] = "WhatsApp Number : " + mandi_df["Countributor Whatsapp Number"]
    # countributor_contact_details = most_frequent(list(mandi_df["Contact_Details"]))

    # ccontact_detail = left_text(ccontact,font, countributor_contact_details, strip_width, strip_height,color = (0,0,0))
    # im.paste(ccontact_detail, contact_pos)
    return im

if __name__ == "__main__":

    # Fetching price reports in last x minutes
    x_minutes = 12*60

    print("Importing data from mongo")
    try:
        connect = MongoClient("mongodb://hemant:gramoday%40123@3.6.249.31:41027/?authSource=gramoday_new&readPreference=primary&appname=MongoDB%20Compass&ssl=false")
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")
    
    # connecting or switching to the database
    db = connect.gramoday_new
    start = datetime.datetime.now() - datetime.timedelta(minutes=x_minutes + 330)
    end = datetime.datetime.now()
    # start = datetime.datetime.now() - datetime.timedelta(11)
    # end = datetime.datetime.now() - datetime.timedelta(10)
    
    raw_reports = db.report_main.find({"type":{"$in":["raw_admin","raw_user"]},"createdAt": { "$gt": start, "$lte": end }})
    print("Fetched raw reports")
    raw_price_reports = list(db.report_info.find({"type":{"$in":["raw_admin","raw_user"]},"createdAt": { "$gt": start, "$lte": end }}))    
    print("Fetched raw price reports")
    raw_analysis_reports = list(db.report_daySales.find({"type":{"$in":["raw_admin","raw_user"]},"createdAt": { "$gt": start, "$lte": end }}))
    print("Fetched raw analysis reports")
    raw_prediction_reports = list(db.report_forecast.find({"type":{"$in":["raw_admin","raw_user"]},"createdAt": { "$gt": start, "$lte": end }}))
    print("Fetched raw prediction reports")
    raw_cmdtyGrade_df =  pd.DataFrame(list(db.cmdty_grade.find()))
    print("Fetched raw cmdtyGrade reports")
    raw_cmdtyGrade_df.drop(['_id','defGrade', 'gradeDescr'], axis=1, inplace=True)
    raw_cmdtyGrade_df.columns = ['cmdtyID', 'gradeID', 'gradeOrder','Grade']
    cumulative_list = []
    for reports in raw_reports:
        report_type = reports["type"]

        try:
            report_id = reports["reportID"]
        except:
            continue

        Date = datetime.datetime.strptime(reports["dateOfReport"],"%d-%m-%Y")
        Date = datetime.datetime.strftime(Date,"%Y-%m-%d")
        
        try:
            Crop = reports["cmdtyStdName"]
        except:
            Crop = ""
        
        try:
            Mandi = reports["marketStdName"]
        except:
            Mandi = ""

        try:
            District = reports["loclevel3Name"]
        except:
            District = ""
        
        try:
            State = reports["loclevel2Name"]
        except:
            State = ""
        
        try:
            mandi_type = "Demand"
        except:
            mandi_type = ""
        
        try:
            new_arrivals_mt = reports["arrivalTotal"]*reports["rawArrivalConvFctr"]*reports["baseFctrArrival"] / 1000
            if new_arrivals_mt == 0:
                new_arrivals_mt = ""
        except:
            new_arrivals_mt = ""
        
        try:
            new_arrivals_bags = new_arrivals_mt*20
            if new_arrivals_bags == 0:
                new_arrivals_bags = ""                        
        except:
            new_arrivals_bags = ""
            
        try:
            balance_mt = reports["arrivalBalance"]*reports["rawArrivalConvFctr"]*reports["baseFctrArrival"] / 1000
            if balance_mt == 0:
                balance_mt = ""
        except:
            balance_mt = ""
        
        try:
            balance_bags = balance_mt*20
            if balance_bags == 0:
                balance_bags = ""            
        except:
            balance_bags = ""

        ## Fetching analysis and prediction text objects
        analysis = [x for x in raw_analysis_reports if x["reportID"] == report_id and x["format"] == "Text"]
        prediction = [x for x in raw_prediction_reports if x["reportID"] == report_id and x["format"] == "Text"]
        
        try:
            text_analysis = analysis["analysis"]
        except:
            text_analysis = ""
    
        try:
            text_prediction = prediction["analysis"]
        except:
            text_prediction = ""
            
        ## Fetching user details
        try:
            user_id = reports["userID"]
        except:
            user_id = ""
        
        user_details = db.user_main.find({"userID":user_id})
    
        try:        
            user_name = user_details[0]["name"]
        except:
            user_name = ""
            
        try:
            user_district = user_details[0]["loclevel3Name"]
        except:
            user_district = ""
            
        try:
            user_mobile = str(user_details[0]["phoneNum"])[3:13]
        except:
            user_mobile = "8960990955"
        
        try:
            user_whatsapp = str(user_details[0]["whatsappNum"])[3:13]
        except:
            user_whatsapp = "8960990955"
    
        user_business_details = db.user_business.find({"userID":user_id})
        
        try:
            user_occupation = user_business_details[0]["userOption"]
        except:
            user_occupation = ""
            
        try:
            user_address = user_name + " , " + user_occupation + " , " + user_district
        except:
            user_address = ""
            
        if user_name == "":
            user_address = "Gramoday Research Team, Noida, Uttar Pradesh"
        
        updated_flag = 1
    
        price_report = [x for x in raw_price_reports if x["reportID"] == report_id]
                
        for price_objects in price_report:
            grade = price_objects["gradeName"]
            variety = price_objects["varietyName"]
            gradeId = price_objects["gradeID"]
            cmdtyId = price_objects["cmdtyID"]
            pack_size_kg = price_objects["rawPriceConvFctr"]*reports["baseFctrPrice"]
            min_price_pack_size = price_objects["minPrice"]
            max_price_pack_size = price_objects["maxPrice"]
            
            min_price_quintal = int(100*(float(price_objects["minPrice"])/pack_size_kg))
            max_price_quintal = int(100*(float(price_objects["maxPrice"])/pack_size_kg))
            
            temp_list = [cmdtyId,gradeId,updated_flag,Date,Crop,Mandi,District,State,mandi_type,new_arrivals_mt,new_arrivals_bags,balance_mt,balance_bags,
                         variety,grade,pack_size_kg,min_price_pack_size,max_price_pack_size,min_price_quintal,max_price_quintal,
                         text_analysis,text_prediction,user_address,user_mobile,user_whatsapp]
            
            cumulative_list.append(temp_list)
    
    price_df = pd.DataFrame(cumulative_list)
    price_df.columns = ['cmdtyID','gradeID','Updated','Posting Date','Crop','Mandi','District','Region Tag','Mandi Type (Supply/Demand)','New Arrivals (MT)','New Arrivals (Bags)','Balance Arrivals (MT)',
                       'Balance Arrivals (Bags)','Variety','Grade','Pack Size (Kg)','Min Price (Pack Size)','Max Price (Pack Size)',
                       'Min Price (Rs/Quintal)','Max Price (Rs/Quintal)','Day_Analysis','Forecast','Countributor_Name_Address','Countributor Mobile Number','Countributor Whatsapp Number']

    ## Adding Default Variety and Default Grade
    def_variety = price_df.groupby(["Posting Date","Crop","Mandi","Variety"], as_index=False)['Grade'].count()\
         .sort_values(by=["Posting Date","Crop","Mandi","Variety", 'Grade'])\
         .drop_duplicates(subset=["Posting Date","Crop","Mandi"], keep='last')
    def_variety["Preferred_Variety"] = 1

    def_grade = price_df.groupby(["Posting Date","Crop","Mandi","Grade"], as_index=False)['Variety'].count()\
         .sort_values(by=["Posting Date","Crop","Mandi","Grade", 'Variety'])\
         .drop_duplicates(subset=["Posting Date","Crop","Mandi"], keep='last')
    def_grade["Preferred_Grade"] = 1
    
    ## Merging to main DB
    price_df = price_df.merge(def_variety[["Posting Date","Crop","Mandi","Variety","Preferred_Variety"]], left_on = ["Posting Date","Crop","Mandi","Variety"], right_on = ["Posting Date","Crop","Mandi","Variety"], how = "left")
    price_df = price_df.merge(def_grade[["Posting Date","Crop","Mandi","Grade","Preferred_Grade"]], left_on = ["Posting Date","Crop","Mandi","Grade"], right_on = ["Posting Date","Crop","Mandi","Grade"], how = "left")
    price_df = price_df[['cmdtyID','gradeID','Updated','Posting Date','Crop','Mandi','District','Region Tag','Mandi Type (Supply/Demand)','New Arrivals (MT)','New Arrivals (Bags)','Balance Arrivals (MT)',
                       'Balance Arrivals (Bags)','Variety','Grade','Preferred_Variety','Preferred_Grade','Pack Size (Kg)','Min Price (Pack Size)','Max Price (Pack Size)',
                       'Min Price (Rs/Quintal)','Max Price (Rs/Quintal)','Day_Analysis','Forecast','Countributor_Name_Address','Countributor Mobile Number','Countributor Whatsapp Number']]
    
    print("Creating Reports")
    price_df["Date"] = pd.to_datetime(price_df["Posting Date"],format = "%Y-%m-%d")
    price_df["Date"] = price_df["Date"].dt.date
    price_df["Day_Gap"] = price_df["Date"].apply(lambda x:date_gap(x,today))

    #### Filtering Today's Records
    today_price_df = price_df[price_df["Day_Gap"] == 0]
    today_price_df = pd.merge(today_price_df,raw_cmdtyGrade_df,how='inner',on=['cmdtyID', 'gradeID', 'Grade'])
    today_price_df.to_excel(r"C:\Users\Sanjeeb\Desktop\New folder\today_price_df.xlsx", index=False)
    
    
    crop_list = list(set(today_price_df["Crop"]))
    mandi_list = list(set(today_price_df["Mandi"]))

    for crops in crop_list:
#        today_price_df["Crop"] = today_price_df["Crop"].str.encode("utf-8")
        crop_df = today_price_df[today_price_df["Crop"] == crops]
        for mandi in mandi_list:
            print("Creating report for : %s"%mandi)
            mandi_df = crop_df[crop_df["Mandi"] == mandi]

            if mandi_df.empty:
                print("Empty Dataframe")
                continue

            mandi_df = mandi_df.fillna(0)
            
            try:
                mandi_df['Min Price (Rs/Quintal)'] = (mandi_df['Min Price (Rs/Quintal)'].astype(float) / 10).astype(int) *10
                mandi_df['Max Price (Rs/Quintal)'] = (mandi_df['Max Price (Rs/Quintal)'].astype(float) / 10).astype(int) *10
            except:
                pass
            
            mandi_df["Report_Title"] = mandi_df["Mandi"].astype(str) + " " + "(" + mandi_df["District"] + ")"
            title = list(set(mandi_df["Report_Title"]))[0]
           
            try:
                Report_Image = prepare_report(mandi_df)
                crops = crops.replace(" ","_")
                title = title.replace(" ","_")
                
                Report_Image.save("C:\\Users\\Sanjeeb\\Downloads\\push_messages_new\\generatedReport\\new\\%s-%s-%s.jpg"%(crops,title,today))
                
                print("Finished Report Creation for %s:%s:%s"%(crops.replace(" ","-"),title.replace(" ","-"),today))
            except Exception as e:
                print(e)
                continue