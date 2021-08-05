# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 14:43:36 2021

@author: Sanjeeb
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



demand_template_apple = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\template_apple.jpg"

demand_template_banana = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\template_banana.jpg"

demand_template_garlic = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\template_garlic.jpg"

demand_template_onion = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\template_onion.jpg"

demand_template_pomogranate = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\template_pomogranate.jpg"

demand_template_potato = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\template_potato.jpg"

demand_template_sweetlime = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\template_sweetlime.jpg"

demand_template_tomato = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\template_tomato.jpg"

demand_template_def = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\template_def.jpg"

contri_img = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\Picture3.png"

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

def Reformat_Image(ImageFilePath):

    from PIL import Image
    image = Image.open(ImageFilePath, 'r')
    # image_size = image.size
    # width = image_size[0]
    # height = image_size[1]
    import cv2
    imc = cv2.imread(ImageFilePath)
    print(imc.shape[0]) #h
    print(imc.shape[1]) #w
    height = imc.shape[0]
    width = imc.shape[1]

    if(width != height):
        # bigside = width if width > height else height
        bigside = height if width > height else width

        background = Image.new('RGBA', (bigside, bigside), (85, 2, 206, 255))
        offset = (int(round(((bigside - width) / 2), 0)), int(round(((bigside - height) / 2),0)))

        background.paste(image, offset)
        background.save(r"C:\\Users\\Sanjeeb\\Desktop\\Gramoday\\10reportTemplate\\final\\pp.png")
        print("Image has been resized !")

    else:
        print("Image is already a square, it has not been resized !")
        
    return background
        
                
### Preparing the Report for each Mandi-Crop-Date Combination
def prepare_report(mandi_df,crops):
    mandi_type = list(set(mandi_df["Mandi Type (Supply/Demand)"]))
    font_path = "C:\\Windows\\Fonts\\Arial\\arialbd.ttf"
    boldFont_path = "C:\\Windows\\Fonts\\Arial\\arialbd.ttf"
    noteFontPath = "C:\\Windows\\Fonts\\Segoe UI\\segoeuisl.ttf"
    contributorFontPath = "C:\\Windows\\Fonts\\Noto Sans\\NotoSans-Bold.ttf"
    # contributorFontPath = r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\Mukta\Mukta-Bold.ttf"
    # contributorFontPath= r"C:\Users\Sanjeeb\Desktop\Gramoday\10reportTemplate\reportTemplates\NotoSansDevanagari-hinted\NotoSansDevanagari-Bold.ttf"
    # print('='*40)
    # print(mandi_type[0])
    # print(crops )
    # print('='*40)
    if mandi_type[0] == "Demand" and crops == 'Apple':
        im = Image.open(demand_template_apple)
        
    elif mandi_type[0] == "Demand" and crops == 'Banana':
        im = Image.open(demand_template_banana)
       
    elif mandi_type[0] == "Demand" and crops == 'Garlic':
        im = Image.open(demand_template_garlic)
    
    elif mandi_type[0] == "Demand" and crops == 'Onion':
        im = Image.open(demand_template_onion)
        
    elif mandi_type[0] == "Demand" and crops == 'Pomogranate':
        im = Image.open(demand_template_pomogranate)

    elif mandi_type[0] == "Demand" and crops == 'Sweet Lime':
        im = Image.open(demand_template_sweetlime)
    
    elif mandi_type[0] == "Demand" and crops == 'Tomato':
        im = Image.open(demand_template_tomato)
        
    elif mandi_type[0] == "Demand" and crops == 'Potato':
        im = Image.open(demand_template_potato)
        
    else:
        im = Image.open(demand_template_def)
        
        
    ####### Adding Mandi Titles
    header_size = (1600, 90) # 399
    header_pos = (310, 45)
    
    strip_width, strip_height = (1600, 90)
    
    header_image = Image.new("RGB", header_size, color = (241,240,245))
    font = ImageFont.truetype(boldFont_path, 75)
    
    mandi_title = list(set(mandi_df["Report_Title"]))
    
    header = center_text(header_image,font, mandi_title[0], strip_width, strip_height,color = (0, 113, 193))
    im.paste(header, header_pos)
    # header.show()
    # sys.exit(0)
    
    ####### Adding Price Date
    date_size = (700,80)
    date_pos = (740,150)

    strip_width, strip_height = (700,80)
    
    date = Image.new("RGB", date_size, color = (241,240,245))
    font = ImageFont.truetype(boldFont_path, 75)
    
    date_title = list(set(mandi_df["Date"]))
    date_title_string = date_title[0].strftime("%d-%b-%Y")
    
    date_header = center_text(date,font, date_title_string, strip_width, strip_height,color = (0, 113, 193))
    im.paste(date_header, date_pos)

    ####### Adding Crop
    crop_size = (700,80)
    crop_pos = (740,250)

    strip_width, strip_height = (700,80)
    
    crop = Image.new("RGB", crop_size, color = (241,240,245))
    font = ImageFont.truetype(boldFont_path, 75)
    crop_title = list(set(mandi_df["Crop"]))
    crop_header = center_text(crop,font, crop_title[0] , strip_width, strip_height,color = (0, 113, 193))
    im.paste(crop_header, crop_pos)



    ####### Adding Grade Names
    grade_size = (1300, 100)    
    font = ImageFont.truetype(font_path, 80)

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
        grade = Image.new("RGB", grade_size, color = (248, 236, 236))
        grade_detail = left_text(grade,font,grades, strip_width, strip_height, color = (0,0,0))
        grade_pos = (480, 1170 + i*150)
        im.paste(grade_detail, grade_pos)
        i += 1

    
    ######### Adding Grade Prices

    grade_price_size = (480, 100)    
    font = ImageFont.truetype(font_path, 80)
    
    strip_width, strip_height = (480, 100)

    ### Setting Default Values for Variety
    try:
        preferred_variety_df = mandi_df[mandi_df["Preferred_Variety"] == "1"]
        main_variety = most_frequent(list(preferred_variety_df["Variety"]))
    except Exception as e:
        print(e)
        main_variety = most_frequent(list(mandi_df["Variety"]))
        
        
    try:
        preferred_grade_df = mandi_df[mandi_df["Preferred_Grade"] == "1"]
        main_grade = most_frequent(list(preferred_grade_df["Grade"]))
    except:
        main_grade = most_frequent(list(mandi_df["Grade"]))
        
        
    print("Main_Variety", main_variety)
    print("Main_Grade", main_grade)
    

    grade_df = mandi_df[mandi_df["Variety"] == main_variety]
    grade_df = grade_df.drop_duplicates()

    grade_df["Price_String"] = grade_df["Min Price (Rs/Quintal)"].astype(str) + " " + "-" + " " + grade_df["Max Price (Rs/Quintal)"].astype(str)
    price_grade_list = grade_df["Price_String"]
    price_grade_list = price_grade_list.iloc[:6]
    
    i = 0
    for price in price_grade_list:
        price_grade = Image.new("RGB", grade_price_size, color = (248, 236, 236))
        price_grade_detail = right_text(price_grade,font,price, strip_width, strip_height,color = (0,0,0), )
        price_grade_pos = (1260, 1170 + i*150)
        im.paste(price_grade_detail, price_grade_pos)
        i += 1

    ######### Adding Grade Prices

    grade_price_size = (480, 100)    
    font = ImageFont.truetype(font_path, 80)
    
    strip_width, strip_height = (480, 100)

    ### Setting Default Values for Variety
    try:
        preferred_variety_df = mandi_df[mandi_df["Preferred_Variety"] == "1"]
        main_variety = most_frequent(list(preferred_variety_df["Variety"]))
    except Exception as e:
        print(e)
        main_variety = most_frequent(list(mandi_df["Variety"]))
        
        
    try:
        preferred_grade_df = mandi_df[mandi_df["Preferred_Grade"] == "1"]
        main_grade = most_frequent(list(preferred_grade_df["Grade"]))
    except:
        main_grade = most_frequent(list(mandi_df["Grade"]))
        
        
    print("Main_Variety", main_variety)
    print("Main_Grade", main_grade)
    

    grade_df = mandi_df[mandi_df["Variety"] == main_variety]
    grade_df = grade_df.drop_duplicates()

    grade_df["Price_String"] = grade_df["Min Price (Rs/Quintal)"].astype(str) + " " + "-" + " " + grade_df["Max Price (Rs/Quintal)"].astype(str)
    price_grade_list = grade_df["Price_String"]
    price_grade_list = price_grade_list.iloc[:1]
    
    i = 0
    for price in price_grade_list:
        price_grade = Image.new("RGB", grade_price_size, color = (248, 236, 236))
        price_grade_detail = right_text(price_grade,font,price, strip_width, strip_height,color = (0,0,0), )
        price_grade_pos = (1550, 1030 + i*150)
        im.paste(price_grade_detail, price_grade_pos)
        i += 1    

        
    ####### Adding Variety Name
    
    note2_size = (1300, 100)
    font = ImageFont.truetype(font_path, 80)
    strip_width, strip_height = (1300, 100)   
    vari = str(main_variety)
    
    note_2 = Image.new("RGB", note2_size, color = (248, 236, 236))
    note2_detail = left_text(note_2,font,vari, strip_width, strip_height,color = (0,0,0))
    note2_pos = (255,1030)
    im.paste(note2_detail, note2_pos)
    
    ####### Adding Price by Grade : Note 2
    
    note2_size = (1750, 100)
    font = ImageFont.truetype(noteFontPath, 63)

    strip_width, strip_height = (1750, 100)
    
    note2_list = "Note : All prices in INR / quintal; For %s Variety"%str(main_variety)

    note_2 = Image.new("RGB", note2_size, color = (248, 236, 236))
    note2_detail = left_text(note_2,font,note2_list, strip_width, strip_height,color = (0,0,0))
    note2_pos = (240, 2010)
    im.paste(note2_detail, note2_pos)
     
      
     
    ####### Adding Countributor Details    
    cname_size = (2000, 100)
    cname_pos = (490, 410)
    font = ImageFont.truetype(contributorFontPath, 73)
    
    strip_width, strip_height = (2000, 100)
    
    cname = Image.new("RGB", cname_size, color = (85, 2, 206))
    countributor_name_address = str(most_frequent(list(mandi_df["Countributor_Name_Address"]))).strip()

    cname_detail = left_text(cname,font, countributor_name_address, strip_width, strip_height, color = (255,255,255))    
    im.paste(cname_detail, cname_pos)

    ####### Adding Contact Details
    contact_size = (1500, 100)
    contact_pos = (490,510)
    font = ImageFont.truetype(contributorFontPath, 73)

    strip_width, strip_height = (1500, 100)

    ccontact = Image.new("RGB", contact_size, color = (85, 2, 206))
    # mandi_df["Contact_Details"] = "Mobile Number : " + mandi_df["Countributor Mobile Number"] + " " + "," + "WhatsApp Number : " + mandi_df["Countributor Whatsapp Number"]
    mandi_df["Contact_Details"] = "Mobile Number : " + mandi_df["Countributor Mobile Number"]
    countributor_contact_details = most_frequent(list(mandi_df["Contact_Details"]))    
    
    
    
    ccontact_detail = left_text(ccontact,font, countributor_contact_details, strip_width, strip_height,color = (255,255,255))
    im.paste(ccontact_detail, contact_pos)
    
    ####### Adding Contact Details
    contact_size = (1500, 100)
    contact_pos = (490,610)
    font = ImageFont.truetype(contributorFontPath, 73)

    strip_width, strip_height = (1500, 100)

    ccontact = Image.new("RGB", contact_size, color = (85, 2, 206))    
    # mandi_df["Contact_Details"] = "Mobile Number : " + mandi_df["Countributor Mobile Number"] + " " + "," + "WhatsApp Number : " + mandi_df["Countributor Whatsapp Number"]
    mandi_df["Contact_Details"] = "WhatsApp Number : " + mandi_df["Countributor Whatsapp Number"]
    countributor_contact_details = most_frequent(list(mandi_df["Contact_Details"]))

    ccontact_detail = left_text(ccontact,font, countributor_contact_details, strip_width, strip_height,color = (255,255,255))
    im.paste(ccontact_detail, contact_pos)
    
    
    ####### Adding Countributor Photo
    try:
        preferred_grade_df = mandi_df[mandi_df["Preferred_Grade"] == "1"]
        main_grade = most_frequent(list(preferred_grade_df["Grade"]))
    except:
        main_grade = most_frequent(list(mandi_df["Grade"]))
        
        
    print("Main_Variety", main_variety)
    print("Main_Grade", main_grade)
    

    grade_df = mandi_df[mandi_df["Variety"] == main_variety]
    grade_df = grade_df.drop_duplicates()

    grade_df["Price_String"] = grade_df["Min Price (Rs/Quintal)"].astype(str) + " " + "-" + " " + grade_df["Max Price (Rs/Quintal)"].astype(str)
    url_list = grade_df["profile_url"]
    url_list = url_list.iloc[:1]
    
    for ul in url_list:
        print(ul)
        try:
            import requests
            url = 'https://api.gramoday.net:8082/v1/files?'
            data = {"id": ul}
            r = requests.get(url,data)
            path = "C:\\Users\\Sanjeeb\\Desktop\\Gramoday\\10reportTemplate\\final\\pp.png"
       
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
                    
            Reformat_Image(path)
            import cv2
            imc = cv2.imread(path)
            print(imc.shape[0]) #h
            print(imc.shape[1]) #w
            print('^'*40)
            if imc.shape[0] < imc.shape[1]: #h<w
                print('1')
                imz = Image.open(path)
                basewidth = 470
                hsize = 370
                imz = imz.resize((basewidth,hsize), Image.ANTIALIAS)   
                photo_pos = (20,375)
                im.paste(imz, photo_pos)
                print("1.1")
            elif imc.shape[0] == imc.shape[1]: #h==w
                print('2')
                imz = Image.open(path)
                basewidth = 470
                hsize = 370
                imz = imz.resize((basewidth,hsize), Image.ANTIALIAS)   
                photo_pos = (20,375)
                im.paste(imz, photo_pos)
                print('2.1')
            else:                             #h>w
                print('3')
                imz = Image.open(path)
                basewidth = 470
                hsize = 370
                imz = imz.resize((basewidth,hsize), Image.ANTIALIAS)
                imz = imz.rotate(90)
                photo_pos = (20,375)
                im.paste(imz, photo_pos)
                print('3.1')

        except:
            imz = Image.open(contri_img)
            basewidth = 415
            hsize = 350
            imz = imz.resize((basewidth,hsize), Image.ANTIALIAS)   
            photo_pos = (35,375)
            im.paste(imz, photo_pos)
            # print(e)
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
            try:
                profile_url = price_objects["creator"]["profilePicUrl"]
            except:
                profile_url = ''
            grade = price_objects["gradeName"]
            variety = price_objects["varietyName"]
            gradeId = price_objects["gradeID"]
            cmdtyId = price_objects["cmdtyID"]
            pack_size_kg = price_objects["rawPriceConvFctr"]*reports["baseFctrPrice"]
            min_price_pack_size = price_objects["minPrice"]
            max_price_pack_size = price_objects["maxPrice"]
            
            
            min_price_quintal = int(100*(float(price_objects["minPrice"])/pack_size_kg))
            max_price_quintal = int(100*(float(price_objects["maxPrice"])/pack_size_kg))
            
            temp_list = [profile_url,cmdtyId,gradeId,updated_flag,Date,Crop,Mandi,District,State,mandi_type,new_arrivals_mt,new_arrivals_bags,balance_mt,balance_bags,
                         variety,grade,pack_size_kg,min_price_pack_size,max_price_pack_size,min_price_quintal,max_price_quintal,
                         text_analysis,text_prediction,user_address,user_mobile,user_whatsapp]
            
            cumulative_list.append(temp_list)
    
    price_df = pd.DataFrame(cumulative_list)
    price_df.columns = ['profile_url','cmdtyID','gradeID','Updated','Posting Date','Crop','Mandi','District','Region Tag','Mandi Type (Supply/Demand)','New Arrivals (MT)','New Arrivals (Bags)','Balance Arrivals (MT)',
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
    price_df = price_df[['profile_url','cmdtyID','gradeID','Updated','Posting Date','Crop','Mandi','District','Region Tag','Mandi Type (Supply/Demand)','New Arrivals (MT)','New Arrivals (Bags)','Balance Arrivals (MT)',
                       'Balance Arrivals (Bags)','Variety','Grade','Preferred_Variety','Preferred_Grade','Pack Size (Kg)','Min Price (Pack Size)','Max Price (Pack Size)',
                       'Min Price (Rs/Quintal)','Max Price (Rs/Quintal)','Day_Analysis','Forecast','Countributor_Name_Address','Countributor Mobile Number','Countributor Whatsapp Number']]
    
    print("Creating Reports")
    price_df["Date"] = pd.to_datetime(price_df["Posting Date"],format = "%Y-%m-%d")
    price_df["Date"] = price_df["Date"].dt.date
    price_df["Day_Gap"] = price_df["Date"].apply(lambda x:date_gap(x,today))

    #### Filtering Today's Records
    today_price_df = price_df[price_df["Day_Gap"] == 0]
    today_price_df = pd.merge(today_price_df,raw_cmdtyGrade_df,how='inner',on=['cmdtyID', 'gradeID', 'Grade'])
    # today_price_df.to_excel(r"C:\Users\Sanjeeb\Desktop\New folder\today_price_df.xlsx", index=False)
    
    
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
                Report_Image = prepare_report(mandi_df,crops)
                crops = crops.replace(" ","_")
                title = title.replace(" ","_")
                
                Report_Image.save("C:\\Users\\Sanjeeb\\Downloads\\push_messages_new\\generatedReport\\new\\%s-%s-%s.jpg"%(crops,title,today))
                
                print("Finished Report Creation for %s:%s:%s"%(crops.replace(" ","-"),title.replace(" ","-"),today))
            except Exception as e:
                print(e)
                continue