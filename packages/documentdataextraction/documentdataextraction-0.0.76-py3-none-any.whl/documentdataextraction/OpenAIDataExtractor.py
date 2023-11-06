import requests, json, traceback, openai
import os
from invoice2data import extract_data
from flask import request
import loggerutility as logger
from PIL import Image
from tempfile import TemporaryDirectory
from pdf2image import convert_from_path
import cv2
import pytesseract
import yaml
from .GenerateExtractTemplate import GenerateExtractTemplate
import pdfplumber
import pdftotext
import datetime
import docx2txt
import pandas as pd
import pathlib
from striprtf.striprtf import rtf_to_text
import unicodedata
import tiktoken
import commonutility as common
 
class OpenAIDataExtractor:

    mainPg_Instruction    =  ""
    otherPg_Instruction   =  ""
    fileExtension_lower   =  ""
    userId = ""

    def pytesseract_ocr(self,PDF_file):
        image_file_list = []
        dict = {}
        with TemporaryDirectory() as tempdir:
            pdf_pages = convert_from_path(PDF_file, 500)
            for page_enumeration, page in enumerate(pdf_pages, start=1):
                filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
                page.save(filename, "JPEG")
                image_file_list.append(filename)

            for page_no,image_file in enumerate(image_file_list):
                text = cv2.imread(image_file)
                image_file = self.resizing(text, 50)
                dict[str(page_no+1)] = str(((pytesseract.image_to_string(image_file)))).strip()

            logger.log(f"pytesseract for image ::::: 61 {dict}","0")
            return dict
        
    def pdfplumber_ocr(self,PDF_file):
        OCR_lst = []
        ocr_text_final = ""
        dict = {}
        
        file = pdfplumber.open(PDF_file)
        ocr_text = file.pages
        logger.log(f"file.pages::: {file.pages}", "0")
        for page_no in range (len(ocr_text)):
            ocr_text_final = ocr_text[page_no].extract_text()
            dict[str(page_no+1)] = ocr_text_final.strip()
            # OCR_lst.append(ocr_text_final)
        # print(len(dict.values()))
        # print(dict)
        return dict
    
    def pdftotext_ocr(self,PDF_file):
        with open(PDF_file, "rb") as f:
            pdf = pdftotext.PDF(f)

        OCR_Text = "\n\n".join(pdf)
        return OCR_Text
    
    def gaussianBlur(self,img,blur_value):
        logger.log(f"gaussianBlur::::54> {blur_value}","0")
        img = cv2.GaussianBlur(img, (blur_value, blur_value),cv2.BORDER_DEFAULT)
        return img

    def grayscale(self,img):
        logger.log(f"grayscale::::59","0")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    def resizing(self,img,scale_percent):
        logger.log(f"resizing::::64> {scale_percent}","0")
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation=cv2.INTER_LANCZOS4)
        return img

    def thresholding(self,img,thresholding_value):
        logger.log(f"thresholding::::72> {thresholding_value}","0")
        mean_value = img.mean()
        threshold_value = mean_value * thresholding_value
        _, img = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)
        return img

    def OpenAIDataExtract(self,file_path : str, jsonData : str, templates : str):
        # Called when you upload document in import order 
        try:
            
            ent_code = ""
            ent_name = ""
            mandatory = []
            enhancement_parameters = ""
            # enhancement_parameters =    {   
            #     '1': {'Blur': 3},
            #     '2': {'Gray': 1},
            #     '3': {'Resizing': 84},
            #     '4': {'Thresholding': 0.9}
            #                             }
            postOrderExtraction = ""
            proc_mtd_value      = ""

            logger.log(f"json data   ::::: 61 {jsonData}","0")
            logger.log(f"OpenAIDataExtract all Parameters::  \n{locals()}\n","0")
            
            if 'ai_proc_templ' in jsonData.keys():
                ai_proc_templ = jsonData['ai_proc_templ']
            
            if 'proc_api_key' in jsonData.keys():
                proc_api_key = jsonData['proc_api_key']

            if 'userId' in jsonData.keys():
                self.userId = jsonData['userId']
                
            if 'objName' in jsonData.keys():
                objName = jsonData['objName']

            if 'ent_code' in jsonData.keys():
                ent_code = jsonData['ent_code']

            if 'ent_name' in jsonData.keys():
                ent_name = jsonData['ent_name']
 
            if 'IS_OCR_EXIST' in jsonData.keys():
                IS_OCR_EXIST = jsonData['IS_OCR_EXIST']

            if 'ai_proc_variables' in jsonData.keys():
                ai_proc_variables = jsonData['ai_proc_variables']

            if 'enhancement_parameters' in jsonData.keys():
                enhancement_parameters = jsonData['enhancement_parameters']
                if enhancement_parameters:
                    enhancement_parameters = json.loads(enhancement_parameters)

            if isinstance(ai_proc_variables, str):
                ai_proc_variables = json.loads(ai_proc_variables)

            if ai_proc_variables:
                for val in ai_proc_variables["Details"]:
                    if val['mandatory'] == 'true':
                        mandatory.append(val['name'])
                
                    if val["name"] == "POST_ORDER_EXTRACTION":
                        postOrderExtraction = val['defaultValue'].strip()
                        logger.log(f"\n\n POST_ORDER_EXTRACTION ::: {postOrderExtraction} {type(postOrderExtraction)}\n\n","0") 
        
                
            logger.log(f"ai_proc_variables::::88> {ai_proc_variables}","0")
            
            if 'proc_mtd' in jsonData.keys():
                proc_mtd = jsonData['proc_mtd']
                proc_mtd_value = proc_mtd.split("-")
                logger.log(f"proc_mtd_value:::{proc_mtd_value}")
           
            OCR_Text = ""
            finalResult = ""
            self.result = {}
            df = None
            fileExtension = (pathlib.Path(file_path).suffix)
            logger.log(f"\nfileExtention::::> {fileExtension}","0")
            self.fileExtension_lower = fileExtension.lower()
            logger.log(f"\nfileExtention_lower()::::> {self.fileExtension_lower}","0")

            if IS_OCR_EXIST == 'false':
                logger.log(f"OCR Start !!!!!!!!!!!!!!!!!102","0")  
                dict = {}          
                if '.PDF' in self.fileExtension_lower or '.pdf' in self.fileExtension_lower:

                    if 'PP' == proc_mtd_value[0]:
                        OCR_Text=self.pdfplumber_ocr(file_path)

                    elif 'PT' == proc_mtd_value[0]:
                        OCR_Text=self.pdftotext_ocr(file_path)

                    elif 'PO' == proc_mtd_value[0]:
                        OCR_Text=self.pytesseract_ocr(file_path)
                    
                    elif 'PPO' == proc_mtd_value[0]:
                        logger.log("\tCASE PPO\n")
                        OCR_Text=self.pdfplumber_overlap(file_path)
                    
                    # if len((OCR_Text).strip()) == 0: 
                    keys_with_blank_values = [key for key, value in OCR_Text.items() if not value]
                    if len(keys_with_blank_values) != 0:      
                        OCR_Text=self.pytesseract_ocr(file_path)

                
                    logger.log(f"OpenAI pdf ocr ::::: {OCR_Text}","0")
                
                elif '.docx' in self.fileExtension_lower or '.DOCX' in self.fileExtension_lower:
                    dict[str(1)] = docx2txt.process(file_path)
                    OCR_Text = dict
                    logger.log(f"OpenAI DOCX ocr ::::: {OCR_Text}","0")

                # Added by SwapnilB for handling xls case on 28-Mar-23 [START]
                elif ".xls" in self.fileExtension_lower or ".xlsx" in self.fileExtension_lower:
                    logger.log(f"inside .xls condition","0")
                    df = pd.read_excel(file_path)
                    xls_ocr = df.to_csv()
                    dict[str(1)] = xls_ocr.replace(","," ").strip()
                    OCR_Text = dict
                    logger.log(f"\nxls_ocr type ::::: \t{type(OCR_Text)}","0")
                    logger.log(f"\nxls_ocr ::::: \n{OCR_Text}\n","0")
                    
                elif ".csv" == self.fileExtension_lower :
                    logger.log(f"inside .csv condition","0")
                    df = pd.read_csv(file_path)
                    csv_ocr = df.to_csv()           # to handle multiple spaces between columns
                    dict[str(1)] = csv_ocr.replace(","," ")
                    OCR_Text = dict
                    logger.log(f"\ncsv_ocr type ::::: \t{type(OCR_Text)}","0")
                    logger.log(f"\ncsv_ocr ::::: \n{OCR_Text}\n","0")
                
                elif ".rtf" == self.fileExtension_lower :
                    logger.log(f"inside .rtf condition","0")
                    with open(file_path) as infile:
                        content = infile.read()
                        dict[str(1)] = rtf_to_text(content, errors="ignore")  # to handle encoding error
                    OCR_Text = dict
                    logger.log(f"\nrtf_ocr type ::::: \t{type(OCR_Text)}","0")
                    logger.log(f"\nrtf_ocr ::::: \n{OCR_Text}\n","0")
                
                # Added by SwapnilB for handling xls case on 28-Mar-23 [END]

                else:
                    path = file_path
                    image = cv2.imread(path)
                    if enhancement_parameters:
                        if '1' in enhancement_parameters.keys():
                            image = self.gaussianBlur(image,enhancement_parameters['1']['Blur'])
                        
                        if '2' in enhancement_parameters.keys():
                            image = self.grayscale(image)

                        if '3' in enhancement_parameters.keys():
                            image = self.resizing(image,enhancement_parameters['3']['Resizing'])
                        
                        if '4' in enhancement_parameters.keys():
                            image = self.thresholding(image,enhancement_parameters['4']['Thresholding'])


                    dict[str(1)] = pytesseract.image_to_string(image)
                    logger.log(f"{dict}","0")
                    OCR_Text = dict
                
                keys_with_blank_values = [key for key, value in OCR_Text.items() if not value]
                if len(keys_with_blank_values) != 0: 
                    logger.log(f'\n In getCompletionEndpoint exception stacktrace : ', "1")
                    trace = str('Contact System Administrator')
                    descr = str('OCR is not available')
                    returnErr = common.getErrorXml(descr, trace)
                    logger.log(f'\n Print exception returnSring inside OCR : {returnErr}', "0")
                    return str(returnErr)
                
                logger.log(f"OCR End !!!!!!!!!!!!!!!!!156","0")
                if not ent_code and not ent_name:
                    logger.log(f"INSIDE entcode and entname not blank","0")
                    try:
                        if proc_mtd_value[0] == 'PT':
                            from invoice2data.input import pdftotext
                            input_module = pdftotext

                        elif proc_mtd_value[0] == 'PP' or proc_mtd_value[0] == 'PPO':
                            # from invoice2data.input import pdfplumber
                            # input_module = pdfplumber
                            logger.log(f" Loading input module for 'PP' OR 'PPO' CASE","0")
                            from invoice2data.input import pdftotext
                            input_module = pdftotext

                        elif proc_mtd_value[0] == 'PO':
                            from invoice2data.input import tesseract
                            input_module =  tesseract
                    
                        logger.log(f"Template Extraction call Start !!!!!!!!!!!!!!!!!183","0")
                        resultdata = extract_data(invoicefile=file_path,templates=templates,input_module=input_module)
                        # resultdata = dict(resultdata)
                        logger.log(f"Template Extraction call End !!!!!!!!!!!!!!!!!111","0")
                        logger.log(f"Template extracted data  ::::: 186 {resultdata}","0")
                        logger.log(f"resultdata type  ::::: 187 {type(resultdata)}","0")

                        if isinstance(resultdata, bool) and len(mandatory)>0:
                            logger.log(f"resultdata type  ::::: 283 {type(OCR_Text)}","0")
                            self.result['OCR_DATA']=OCR_Text
                            self.result['isMandatoryExtracted']='false'
                            return self.result
                            # resultdata = {}
                        elif isinstance(resultdata, bool):
                            resultdata = {}

                        resultdata['isTemplateExtracted']='true'
                        self.result['isMandatoryExtracted']='true'

                        if mandatory:
                            for valuesOfmandatory in mandatory:
                                if valuesOfmandatory in resultdata:
                                    if not resultdata[valuesOfmandatory]:  
                                        self.result['OCR_DATA']=OCR_Text
                                        self.result["EXTRACT_TEMPLATE_DATA"] = resultdata
                                        self.result['isMandatoryExtracted']='false'
                                        return self.result
                                                            
                        for valuesOfmandatory in resultdata.keys():
                            if type(resultdata[valuesOfmandatory]) == list and resultdata[valuesOfmandatory] != []:
                                resultdata[valuesOfmandatory] = resultdata[valuesOfmandatory][0]
                            elif resultdata[valuesOfmandatory] == []:
                                resultdata[valuesOfmandatory] = ""

                        # resultdata['isTemplateExtracted']='true'
                        if 'ent_code' in resultdata.keys():
                            self.result["EXTRACT_TEMPLATE_DATA"] = resultdata
                            self.result['OCR_DATA']=OCR_Text
                            return self.result
                            
                        
                    except Exception as e:
                        logger.log(f'\n Exception : {e}', "1")

            else:
                if 'OCR_DATA' in jsonData.keys():
                    OCR_Text = jsonData['OCR_DATA']

            if len(postOrderExtraction) > 0 :
                    OCR_Text = self.replace_OCR_Word(OCR_Text, postOrderExtraction )
                    logger.log(f"After POST-Order-Extraction OCR_Text::: \t{type(OCR_Text)} \n{OCR_Text}\n")

            if ai_proc_templ:
                if 'AID' in proc_mtd_value[1]:
                    logger.log(f"AID !!!!!!!!!!!! 204","0")
                    finalResult = self.extractdatausing_davinci(proc_api_key=proc_api_key, OCR_Text=OCR_Text, ai_proc_templ=ai_proc_templ,ai_proc_variables=ai_proc_variables)
                    

                elif 'AIT' in proc_mtd_value[1]:
                    finalResult = self.extractdatausing_turbo(proc_api_key = proc_api_key, ai_proc_templ=ai_proc_templ,ai_proc_variables=ai_proc_variables, OCR_Text = OCR_Text,userId = self.userId)
                
                self.result["EXTRACT_LAYOUT_DATA"] = finalResult
                self.result['OCR_DATA']=OCR_Text
            
            logger.log(f"Response Return !!!!!!!!!!!! 142","0")
            return self.result
            
        
        except Exception as e:
            logger.log(f'\n In getCompletionEndpoint exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str(e)
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Print exception returnSring inside getCompletionEndpoint : {returnErr}', "0")
            return str(returnErr)


    def getlayouttextaidata(self): #, jsonData):
        # Called when you click 'REFRESH' upload document in import order 
        try:
            result = {}
            final_result = {}
            mandatory = []
            finalResult = ""
            proc_api_key = ""
            ai_proc_templ = ""
            ent_name = ""
            ent_code = ""
            ent_type = ""
            OCR_Text = ""
            ai_proc_variables   = ""
            postOrderExtraction = ""
            
            jsonData = request.get_data('jsonData', None)
            jsonData = json.loads(jsonData[9:])
            logger.log(f"jsonData API openAI class::: !!!!!269 {jsonData}","0")

            if 'extract_templ' in jsonData.keys():
                given_temp_path = jsonData['extract_templ']
            
            if 'ent_code' in jsonData.keys():
                ent_code = jsonData['ent_code']
            
            if 'ent_type' in jsonData.keys():
                ent_type = jsonData['ent_type']

            if 'ent_name' in jsonData.keys():
                ent_name = jsonData['ent_name']

            if 'ai_proc_templ' in jsonData.keys():
                ai_proc_templ = jsonData['ai_proc_templ']

            if 'ai_proc_variables' in jsonData.keys():
                ai_proc_variables = jsonData['ai_proc_variables']

            if 'proc_api_key' in jsonData.keys():
                proc_api_key   = jsonData['proc_api_key']

            if 'userId' in jsonData.keys():
                self.userId = jsonData['userId']

            if 'objName' in jsonData.keys():
                objName = jsonData['objName']
            
            if 'proc_mtd' in jsonData.keys():
                proc_mtd = jsonData['proc_mtd']
                proc_mtd_value = proc_mtd.split("-")
            
            if 'OCR_DATA' in jsonData.keys():
                OCR_Text = jsonData['OCR_DATA']
            logger.log(f'\n\n  OCR_Text line 406: \n{OCR_Text}\n{type({OCR_Text})}\n{len({OCR_Text})}\n', "0")

            if ai_proc_variables:
                for val in ai_proc_variables["Details"]:
                    if val["name"] == "POST_ORDER_EXTRACTION":
                        postOrderExtraction = val['defaultValue'].strip()
                        logger.log(f"\n\n POST_ORDER_EXTRACTION ::: {postOrderExtraction} {type(postOrderExtraction)}\n\n","0") 

            if len(postOrderExtraction) > 0 :
                logger.log(f'\n\n  Inside line 424 \n', "0")
                OCR_Text = json.dumps(self.replace_OCR_Word(OCR_Text, postOrderExtraction))
                logger.log(f'\n\n   \n{type({OCR_Text})}\n{OCR_Text}') #\n{len({OCR_Text})}\n', "0")

            if ai_proc_templ:
                ymlfilepath = "/"+(given_temp_path)+"/"+str(ent_name).strip().replace(" ","_").replace(".","").replace("/","")+".yml"
                if os.path.exists(ymlfilepath) == True:
                    os.remove(ymlfilepath)
                logger.log(f'\n\n  OCR_Text line 431: \n') 
            
                if ent_name.strip() and ((isinstance(ent_code, str) and ent_code.strip()) or isinstance(ent_code, int)):  
                    logger.log(f"ent_name :::\t{type(ent_name)}{ent_name} \n ent_code :::\t{type(ent_code)}{ent_code} \n OCR_Text:::{type(OCR_Text)}\n {OCR_Text}" )
                    if ent_name in OCR_Text:
                        logger.log(f'\n[ Template creation Start time  305  :          {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
                        templatecreation = GenerateExtractTemplate()
                        templatecreation.generateHeaderTemplate(ymlfilepath,ent_name,ent_code,ent_type,ai_proc_variables,OCR_Text)
                        logger.log(f'\n[ Template creation End time  308  :          {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
                    else:
                        message = str('Template not created, Please enter valid Received From Name')
                        description = str('Received From Name must be present in file')
                        errorjson = common.getErrorJson(message,description)
                        final_result['status'] = 0
                        final_result['error'] = errorjson
                        return final_result
                
                temp_file_path = "/"+(given_temp_path)+"/"+'.yml'
                if os.path.exists(temp_file_path) == True:
                    os.remove(temp_file_path)
                    message = str('Template not created')
                    description = str('Ent Code or Ent Name is not present, mention required details properly')
                    errorjson = common.getErrorJson(message,description)
                    final_result['status'] = 0
                    final_result['error'] = errorjson
                    logger.log(f'\n[ Blank Template Remove :          {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
                    return final_result
                
                if 'AID' in proc_mtd_value[1]:
                    finalResult = self.extractdatausing_davinci(proc_api_key=proc_api_key, OCR_Text=OCR_Text, ai_proc_templ=ai_proc_templ,ai_proc_variables=ai_proc_variables)

                elif 'AIT' in proc_mtd_value[1]:
                    finalResult = self.extractdatausing_turbo(proc_api_key = proc_api_key, ai_proc_templ=ai_proc_templ,ai_proc_variables=ai_proc_variables, OCR_Text = OCR_Text,userId = self.userId)
                
                if os.path.exists(ymlfilepath) == True:
                    result["EXTRACT_LAYOUT_DATA"] = finalResult
                    final_result['status'] = 1
                    final_result['result'] = result
                else:
                    message = str('Template not created, Mention the Required details properly')
                    description = str('Recieved From Name and Recieved From Code always requird')
                    errorjson = common.getErrorJson(message,description)
                    final_result['status'] = 0
                    final_result['error'] = errorjson

        except Exception as ex:
            final_result['status'] = 0
            final_result['error'] = str(ex)
            logger.log(f"Return result value !!!!!!!!! 203 {final_result}","0")
            trace = traceback.format_exc()
            descr = str(ex)
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Print exception returnSring inside getCompletionEndpoint : {returnErr}', "0")
        
        return final_result
    
    def extractdatausing_davinci(self,proc_api_key : str, OCR_Text : str , ai_proc_templ : str, ai_proc_variables : str):

        logger.log(f'\n[ Open ai starting time 131 :        {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
        openai.api_key = proc_api_key
        logger.log(f"\nai_proc_variables::::\n {ai_proc_variables}\n{type(ai_proc_variables)}","0")
        logger.log(f"\nai_proc_templ::::\n {ai_proc_templ}\n{type(ai_proc_templ)}","0")       
        logger.log(f"TYPE OF ai_proc_variables {type(ai_proc_variables)}","0")

        if isinstance(ai_proc_variables, str):
            ai_proc_variables = json.loads(ai_proc_variables)

        if ai_proc_variables:
            for val in ai_proc_variables["Details"]:
                if "<"+val["name"]+">" in ai_proc_templ:
                    ai_proc_templ = ai_proc_templ.replace("<"+val["name"]+">", val['defaultValue'])

        if '<DOCUMENT_DATA>' in ai_proc_templ:
            print(type(ai_proc_templ))
            ai_proc_templ = ai_proc_templ.replace('<DOCUMENT_DATA>',OCR_Text)
            logger.log(f'\n[ Open ai " model " Value              :      "text-davinci-003" ]', "0")
            logger.log(f'\n[ Open ai " prompt " Value             :      "{ai_proc_templ}" ]', "0")
            logger.log(f'\n[ Open ai " temperature " Value        :      "0" ]', "0")
            logger.log(f'\n[ Open ai " max_tokens " Value         :      "1800" ]', "0")
            logger.log(f'\n[ Open ai " top_p " Value              :      "1" ]', "0")
            logger.log(f'\n[ Open ai " frequency_penalty " Value  :      "0" ]', "0")
            logger.log(f'\n[ Open ai " presence_penalty " Value   :      "0" ]', "0")
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt= ai_proc_templ,
            temperature=0,
            max_tokens=1800,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )

        else:

            logger.log(f'\n[ Open ai " model " Value              :      "text-davinci-003" ]', "0")
            logger.log(f'\n[ Open ai " prompt " Value             :      "{OCR_Text+ai_proc_templ}" ]', "0")
            logger.log(f'\n[ Open ai " temperature " Value        :      "0" ]', "0")
            logger.log(f'\n[ Open ai " max_tokens " Value         :      "1800" ]', "0")
            logger.log(f'\n[ Open ai " top_p " Value              :      "1" ]', "0")
            logger.log(f'\n[ Open ai " frequency_penalty " Value  :      "0" ]', "0")
            logger.log(f'\n[ Open ai " presence_penalty " Value   :      "0" ]', "0")
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt= OCR_Text+'\n'+ai_proc_templ,
            temperature=0,
            max_tokens=1800,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        logger.log(f"Response openAI completion endpoint::::: {response}","0")
        finalResult=str(response["choices"][0]["text"])
        logger.log(f'\n [ Open ai completion time 171 :      {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]', "0")
        logger.log(f"OpenAI completion endpoint finalResult ::::: {finalResult}","0")
        return finalResult


    def extractdatausing_turbo(self,proc_api_key: str, ai_proc_templ : str, ai_proc_variables : str, OCR_Text : str,userId : str):
        logger.log(f"\nai_proc_variables::::\n {ai_proc_variables}\n{type(ai_proc_variables)}","0")
        logger.log(f"\nai_proc_templ::::\n {ai_proc_templ}\n{type(ai_proc_templ)}","0")
        logger.log(f"\nai_OCR_Text::::  512\n {OCR_Text}\n{type(OCR_Text)}","0")
        OCR_List            = []
        response_lst        = []
        start               = "" 
        end                 = ""
        ext_min_len         = ""
        FinalsubString_OCR  = ""
        page_wise           = "Yes"
        
        if isinstance(ai_proc_variables, str):
            ai_proc_variables = json.loads(ai_proc_variables)
        
        if isinstance(OCR_Text, str):
            OCR_Text = json.loads(OCR_Text.strip())
        
        if isinstance(OCR_Text, dict):
            for val in OCR_Text.values():
                OCR_List.append(val)
            OCR_Text = OCR_List

        if isinstance(ai_proc_templ, list):
            ai_proc_templ = json.dumps(ai_proc_templ)

        if ai_proc_variables:
            for val in ai_proc_variables["Details"]:
                if "<"+val["name"]+">" in ai_proc_templ:
                    ai_proc_templ = ai_proc_templ.replace("<"+val["name"]+">", val['defaultValue'].strip())

                if val["name"] == "start_index":
                    start = val['defaultValue'].strip()
                    logger.log(f"\n\n start_index ::: {start} \n\n","0")    

                if val["name"] == "end_index":
                    end = val['defaultValue'].strip()
                    logger.log(f"\n\n end_index ::: {end} \n\n","0") 
                
                if val["name"] == "ext_min_len":
                    ext_min_len = val['defaultValue'].strip()
                    logger.log(f"\n\n ext_min_len ::: {ext_min_len} {type(ext_min_len)}\n\n","0") 
                
                if val["name"] == "ext_pagewise":
                    page_wise = val['defaultValue'].strip()
                    logger.log(f"\n\n page_wise ::: {page_wise} {type(page_wise)}\n\n","0") 

        start_lst = start.split(",")
        end_lst = end.split(",")
        subStringOcrList = []
        
        if page_wise == "No" or self.fileExtension_lower == 'csv' or self.fileExtension_lower == 'xls' or self.fileExtension_lower == 'xlsx':
            joined_OCR_List =  []
            logger.log(f"\n\n inside 'page_wise = No' condition:::{OCR_Text} \n\n","0")
            logger.log(f"\n\n before OCR_Text:::{OCR_Text} \t{type(OCR_Text)} \n\n","0")
            joined_OCR_List.append("\n".join(OCR_Text))
            logger.log(f"\n\n after joined_OCR_List:::{joined_OCR_List} \t{type(joined_OCR_List)} \n\n","0")
            OCR_Text_withInstruction = self.replaceWithExtractInstruction(ai_proc_temp=ai_proc_templ, OCR_Text = joined_OCR_List, ai_proc_variables = ai_proc_variables, page_wise = page_wise )
            logger.log(f"\n\n after OCR_Text_withInstruction:::{OCR_Text_withInstruction} \t{type(OCR_Text_withInstruction)} \n\n","0")
            openAIResponseStr = self.call_GPT_Service(OCR_Text_withInstruction, proc_api_key,userId)
            response_lst.append(openAIResponseStr)
            finalResponseStr = self.concatFinalResponse(returnedResponseList = response_lst)
            logger.log(f"OpenAI FINAL ResponseStr  :::\n\n{finalResponseStr}\n\n","0")  
        
            return finalResponseStr

        else:
            # create substring 
            for page in range(len(OCR_Text)):
                FinalsubString_OCR = ""
                startIndex         = ""
                endIndex           = ""
                
                for start_word in start_lst:
                    if start_word != "" and OCR_Text[page].find(start_word) != -1:
                        logger.log(f"inside if start loop", "0")
                        startIndex = OCR_Text[page].find(start_word)
                        logger.log(f"startIndex value::{startIndex}","0")# \t {page}")
                    break

                for end_word in end_lst:
                    if end_word != "" and OCR_Text[page].find(end_word) != -1:
                        logger.log(f"inside if end loop", "0")
                        endIndex = OCR_Text[page].find(end_word)
                        logger.log(f"endIndex value::{endIndex}  \t {page}\n\n", "0")
                    break
                
                if (startIndex != -1 and startIndex != "") and (endIndex != -1 and endIndex != ""):
                    logger.log(f"\n\nstartIndex and endIndex not blank case\n", "0")
                    FinalsubString_OCR = OCR_Text[page][ startIndex : endIndex ]

                    if isinstance(ext_min_len, str) and len(ext_min_len) > 0:
                        if len(FinalsubString_OCR) > int(ext_min_len) :
                            logger.log(f"\n\n FinalsubString_OCR length: {len(FinalsubString_OCR)} is GREATER THAN Ext_min_len: {ext_min_len} for Page: {page} condition.   \n\n","0")
                            subStringOcrList.append(FinalsubString_OCR)
                        else:
                            logger.log(f"\n\n Ext_min_len {ext_min_len} is GREATER THAN FinalsubString_OCR length {len(FinalsubString_OCR)} for Page: {page} condition. \n\n","0")
                    
                elif (startIndex != -1 and startIndex != "") and (endIndex == -1 or endIndex == ""):
                    logger.log("\n\nEndIndex blank case\n ","0")
                    FinalsubString_OCR = OCR_Text[page][ startIndex :  ]
        
                elif (startIndex == -1 or startIndex == "") and (endIndex != -1 and endIndex != ""):
                    FinalsubString_OCR = OCR_Text[page][ : endIndex ]
                    logger.log(f"\n\nStartIndex empty case\n", "0")
                    
                elif (startIndex == -1 or startIndex == "") and (endIndex == -1 or endIndex == ""):
                    logger.log(f"\n\nStartIndex EndIndex empty case\n", "0")
                    FinalsubString_OCR = OCR_Text[page]
                    
                else:
                    FinalsubString_OCR = OCR_Text[page]
                
                logger.log(f"FinalsubString_OCR :::{FinalsubString_OCR}", "0")
                if FinalsubString_OCR != "" :
                    subStringOcrList.append(FinalsubString_OCR)
                else:
                    logger.log(f"FinalsubString_OCR 'else' line 639:::{FinalsubString_OCR}", "0")

            if len(subStringOcrList) > 0:
                logger.log(f"\n\n if condition line FINAL subStringOcrList::{subStringOcrList} length :::{len(subStringOcrList)}\n\n","0")
                OCR_Text =  subStringOcrList
            else:
                message ="There is no OCR text found against the given extraction details."
                logger.log(f"\n\n Line 584 ext_min greater than OCR length\n\n","0")
                return message

        ai_proc_templ_updated = self.replaceWithExtractInstruction(ai_proc_temp=ai_proc_templ, OCR_Text = OCR_Text, ai_proc_variables = ai_proc_variables, page_wise = page_wise )
        
        # Overview call or Template creation call ai_proc_templ variable type is list and while uploading it's variable type is string
        if isinstance(ai_proc_templ_updated, str):       
            # ai_proc_templ_updated = ai_proc_templ_updated #10-aug-23 .replace('\n'," ") 
            ai_proc_templ_updated = json.loads(ai_proc_templ_updated)
        
        logger.log(f"\n\nai_proc_templ_updated     ::: {type(ai_proc_templ_updated)} \t {len(ai_proc_templ_updated)}\n\n","0")

        for i in range(len(ai_proc_templ_updated)):
            logger.log(f"\n\n inside 'page_wise = Yes' condition for page: {i}\n\n","0")
            openAI_result = self.call_GPT_Service(ai_proc_templ_updated[i], proc_api_key, userId)
            response_lst.append(openAI_result)
        
        logger.log(f"OpenAI response_lst  :::\n\n{response_lst}\n\n","0")  
        finalResponseStr = self.concatFinalResponse(returnedResponseList = response_lst)
        logger.log(f"\n\nAll Pages FinalResponseString ::: \n{finalResponseStr}\n\n")
        
        return finalResponseStr

    def replaceWithExtractInstruction(self, ai_proc_temp: str, OCR_Text: list, ai_proc_variables : str, page_wise : str):
        logger.log(f"\n\niNSIDE replaceWithExtractInstruction()\n\n","0")
        logger.log(f"\n\nOCR_Text line 637::::{OCR_Text}{type(OCR_Text)}\n\n","0")
        logger.log(f"\n\nai_proc_temp::::{ai_proc_temp}{type(ai_proc_temp)}\n\n","0")
        replacedOCR_MainPage  = ""
        replacedOCR_OtherPage = ""

        if isinstance(ai_proc_variables, str):
            ai_proc_variables = json.loads(ai_proc_variables)

        for key in ai_proc_variables["Details"]:
            if key["name"] == "main_page":
                self.mainPg_Instruction = key['defaultValue']
        logger.log(f"mainPg_Instruction:::\n\n{self.mainPg_Instruction}\n","0")

        for key in ai_proc_variables["Details"]:
            if key["name"] == "other_pages":
                self.otherPg_Instruction = key['defaultValue']
        logger.log(f"otherPg_Instruction:::\n\n{self.otherPg_Instruction}\n","0")
        
        FinalInstruction_lst = []
        replacedOCR_MainPage = OCR_Text[0].replace('"',' ').replace("\\n", " ").replace("\n", " ") # 10-aug-23  .replace("\\",'\/')
        ai_proc_temp_main = (ai_proc_temp.replace("<EXTRACT_INSTRUCTIONS>", self.mainPg_Instruction)).replace("<DOCUMENT_DATA>", replacedOCR_MainPage) # 10-aug-23.replace('"',' ').replace("\\",'\/')).strip()
        logger.log(f"\n\ai_proc_temp_main::::{ai_proc_temp_main}{type(ai_proc_temp_main)}\n\n","0")
        if page_wise == "No": 
            return ai_proc_temp_main
        else:
            FinalInstruction_lst.append(ai_proc_temp_main)
        # other Page OCR

        if len(OCR_Text) > 1:
            for i in range(1, len(OCR_Text)):
                replacedOCR_OtherPage = OCR_Text[i].replace('"',' ').replace("\\n", " ").replace("\n", " ")  # 10-aug-23 .replace("\\",'\/')
                ai_proc_temp_other = (ai_proc_temp.replace("<EXTRACT_INSTRUCTIONS>", self.otherPg_Instruction)).replace("<DOCUMENT_DATA>", replacedOCR_OtherPage)  # 10-aug-23.replace('"',' ').replace("\\",'\/')).strip()
                FinalInstruction_lst.append(ai_proc_temp_other)
        logger.log(f"\n\FinalInstruction_lst line 647::::{FinalInstruction_lst}\t {type(FinalInstruction_lst)}\n\n","0")
        return FinalInstruction_lst

    def concatFinalResponse(self, returnedResponseList : list):
        finalResponse   = []
        pageCSV         = ""
        for i in range(len(returnedResponseList)):
            if i == 0:
                finalResponse.append(returnedResponseList[i])
            else:
                fromSizeVar = returnedResponseList[i]
                if "Size" in fromSizeVar:
                    pageCSV = fromSizeVar[fromSizeVar.find("Size")+5:]
                pageCSV = "\n" + pageCSV if not pageCSV.startswith("\n") else pageCSV
                finalResponse.append(pageCSV)
                
        return (" ".join(finalResponse))        

    def num_tokens_from_messages(self, messages, model="gpt-3.5-turbo-0301"):
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
    
        return num_tokens

    def call_GPT_Service(self, text, proc_api_key, userId, token_limit = 4096, max_response_tokens = 1800):
        messageTokenLength = None
        openai.api_key = proc_api_key
        
        #to handle any unicode character
        # clean_string = ''.join(c for c in text if unicodedata.category(c)[0] != 'C')   # 10-aug-23 -- commented because '\n' is considered as control character and it was geeting removed
        message = json.loads(text, strict=False)   #(clean_string.replace("\\",'\/'))
        logger.log(f" \n\nBefore GPT CALL FINAL MESSAGE  :::\n{message}, \t{type(message)}","0")    

        # to calculate token
        conv_history_tokens = self.num_tokens_from_messages(message)   
        logger.log(f"conversion_tokens_count:::{conv_history_tokens}","0")    
        messageTokenLength = conv_history_tokens + max_response_tokens 
        logger.log(f"\n\n MessageTokenLength is :::{messageTokenLength}\n","0")
        
        logger.log("\n\n\nEND\n\n\n")

        if messageTokenLength <= token_limit:
            logger.log(f"\n\n--- Using GPT-3.5-TURBO Model ---\t as messageTokenLength is :::{messageTokenLength}\n","0")
            completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=message,
                            temperature=0,
                            max_tokens=max_response_tokens,
                            top_p=1,
                            frequency_penalty=0,
                            presence_penalty=0,
                            user=userId,
                        )
            
            result = (completion['choices'][0]['message']['content'])
            logger.log(f"\n\n Completion result 3.5 :::\n{result} \t{type(result)}\n","0")
            return result
        
        else:
            logger.log(f"\n\n--- Using GPT-3.5-turbo-16k Model ---\t  as messageTokenLength is:::{messageTokenLength} \n\n","0")
            completion = openai.ChatCompletion.create(
                        # model="gpt-4",
                        model = "gpt-3.5-turbo-16k",
                        messages=message,
                        temperature=0,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        user=userId,
                                )
            result = (completion['choices'][0]['message']['content'])
            logger.log(f"\n\n Completion result 3.5-turbo-16k :::\n{result} \t{type(result)}\n","0")
            return result

    def pdfplumber_overlap(self, fileName):
        ocr_text_final  = ""
        OCR_dict        = {}
        
        pdf = pdfplumber.open(fileName)
        ocr_text = pdf.pages
        for page_no in range (len(ocr_text)):
            ocr_text_final = ocr_text[page_no].extract_text(layout=True, x_tolerance=1)
            OCR_dict[str(page_no+1)] = ocr_text_final.strip()
        
        logger.log(f"OCR_dict after overlap:::: \t{type(OCR_dict)}\n{OCR_dict}\n")
        return OCR_dict

    def replace_OCR_Word(self, OCR_Text, postOrderExtraction):
        logger.log(f"All params::: {locals()}\n")
        postOrderExtraction_list  = []
        sourceTarget_mainList     = []
        
        if type(OCR_Text) == str :
            OCR_Text = json.loads(OCR_Text)

        if "/n" in postOrderExtraction:
            postOrderExtraction_list = postOrderExtraction.split("/n")
            logger.log(f"postOrderExtraction_list::: {postOrderExtraction_list}")

            sourceTarget_mainList= [eachElement.split('==') for eachElement in postOrderExtraction_list]
            logger.log(f"sourceTarget_list ::: {sourceTarget_mainList}")

            logger.log(f"Before postOrderExtraction OCR_Text::: \t{type(OCR_Text)}\t Length: {len(OCR_Text)} \n{OCR_Text}\n")

            for key in OCR_Text:
                for sourceTarget_list in sourceTarget_mainList:
                    logger.log(f"sourceTarget_list::{sourceTarget_list}")
                    if sourceTarget_list[0] in OCR_Text[key]:
                        OCR_Text[key] = OCR_Text[key].replace(sourceTarget_list[0], sourceTarget_list[1])
                        logger.log(f" '{sourceTarget_list[0]}' replaced with '{sourceTarget_list[1]}' in page '{key}. '")
                    else:
                        logger.log(f" {sourceTarget_list[0]} not found in page '{key}'")
            
            logger.log(f"After postOrderExtraction OCR_Text::: \t{type(OCR_Text)}\t Length: {len(OCR_Text)} \n{OCR_Text}\n")
        
        else:
            logger.log(f" \n\n '\n' character not found in postOrderExtraction \n\n")
        
        return OCR_Text
            
            
# data = {'enterprise': 'APPVIS', 'proc_mtd': 'PPO-AIT-AIL-UC', 'ent_type': 'C', 'ai_proc_variables': {'Details': [{'displayName': 'Extraction Page Wise', 'defaultValue': 'Yes', 'name': 'ext_pagewise', 'ddlb_options': [{'dispValue': 'Yes', 'dispName': 'Yes'}, {'dispValue': 'No', 'dispName': 'No'}], 'type': 'dropdown', 'mandatory': 'false'}, {'displayName': 'Extraction Minimum Length', 'defaultValue': '', 'name': 'ext_min_len', 'type': 'string', 'mandatory': 'false', 'max_length': '100'}, {'displayName': 'Extraction Start Text', 'defaultValue': '', 'name': 'start_index', 'type': 'string', 'mandatory': 'false', 'max_length': '100'}, {'displayName': 'Extraction End Text', 'defaultValue': '', 'name': 'end_index', 'type': 'string', 'mandatory': 'false', 'max_length': '100'}, {'displayName': 'Product Names', 'defaultValue': 'Example of Product Names are AUGMENTIN, AUGMENTIN DDS, AUGMENTIN ES, AUGMENTIN DUO, AUGMENTIN DRY, OILATUM, AVAMYS, LANOXIN, GRISOVIN FP, GRISOVIN, COBADEX CZS, COBADEX FORTE, COBADEX Z, COBADEX, BETNESOL N, BETNESOL FORTE, BETNESOL, BETNOVATE GM, BETNOVATE C, BETNOVATE N, BETNOVATE S, BETNOVATE, CALPOL T, CALPOL, CCM, ELTROXIN, NEOSPORIN H, NEOSPORIN, PIRITON CS, PIRITON, PHEXIN BD, PHEXIN, TENOVATE GN, TENOVATE M, TENOVATE, PHYSIOGEL DMT, SUPACEF, INFANRIX HEXA, INFANRIX CCT, ZODERM E, ZODERM, CEFTUM, ZOVIRAX, ZIMIG, T-BACT. Some products has multiple variants. For example AUGMENTIN has variants as AUGMENTIN DDS, AUGMENTIN ES, AUGMENTIN DUO, AUGMENTIN DRY besides AUGMENTIN, which itself is a product.', 'name': 'product', 'type': 'string', 'mandatory': 'false', 'max_length': '500'}, {'displayName': 'Packing', 'defaultValue': "Example of Packing are BOX, CASE, C/S, 8*1VIAL, 20GM, 1X120TAB, 1X25GM, 30ML, 60ML, 50 ML, 10GM, 20 GM, 10G, 1X4, 1X20, 20TAB, 120GM, 1X25GM, 8X1ML, 10'S, 20'S, 10T.", 'name': 'packing', 'type': 'string', 'mandatory': 'false', 'max_length': '500'}, {'displayName': 'Delivery Methods', 'defaultValue': 'Example Delivery Methods are TABLET, TAB, LOTION, SK CREAM, SKIN CREAM, CREAM, EXP, EXPECTORANT, NASEL SPRAY, EYE/EAR DROPS, EYE DROPS, EAR DROPS, E/E DROPS, ORAL DROPS, DROP, OINT, OINTMENT, SUSP, SUSPENSION, ING, INJ, INJECTION, BAR, POWDER.', 'name': 'delivery', 'type': 'string', 'mandatory': 'false', 'max_length': '500'}, {'displayName': 'Product Strengths', 'defaultValue': 'Example of Product Strengths are 250MG, 25MG, 1G, 5 MG, 625, 75, 1000, 125.', 'name': 'strength', 'type': 'string', 'mandatory': 'false', 'max_length': '500'}, {'displayName': 'Sizes', 'defaultValue': "Example of Sizes are 20GM, 100ML, 30ML, 1X30ML, 100 ML, 1000'S, 20'S, 10TAB, 10*10, 1VIAL, 1X10, 1X250GRM, 1X1000, 10T.", 'name': 'size', 'type': 'string', 'mandatory': 'false', 'max_length': '500'}, {'displayName': 'SKU Name Examples', 'defaultValue': 'Examples of SKU Name configuration are following. In SKU Name BECADEXAMIN CAP, Product Name is BECADEXAMIN, Delivery Method is CAP. In SKU Name BETNESOL FORTE 1X1ML, Product Name is BETNESOL FORTE, Ordering unit is 1X1ML. In SKU Name ZIMIVIR-500 3.TAB, Product Name is ZIMIVIR, Delivery Method is TAB, Product Strength is 500, Size is 3.TAB. In SKU Name T-BACT-15GM OINTMENT, Product Name is T-BACT, Delivery Method is OINTMENT, Size is 15GM. In SKU Name AUGMENTIN 625 DUO TAB, Product Name is AUGMENTIN DUO, Delivery Method is TAB, Product Strength is 625.', 'name': 'sku_name_examples', 'type': 'string', 'mandatory': 'false', 'max_length': '1000'}, {'displayName': 'Line Item Examples', 'defaultValue': 'Example of Line Item organisation are as following. In Line Item 6,BETNOVATE C CREAM, 30GM, 1 CASE. Line Number is 6, SKU Name is BETNOVATE C CREAM, Ordering Unit is CASE, Quantity is 1, Product Name is BETNOVATE C, Delivery Method is CREAM, Product Strength is 30GM. In Line Item 4, AUGMENTIN 1000MG, 10TAB, 20. Line Number is 4, SKU Name is AUGMENTIN 1000MG, Ordering Unit is 10TAB, Quantity is 20, Product Name is AUGMENTIN, Delivery Method is TAB, Product Strength is 1000MG.', 'name': 'line_item_examples', 'type': 'string', 'mandatory': 'false', 'max_length': '1000'}, {'displayName': 'Main Page', 'defaultValue': '/* Following is the data of the order document. GLAXO is seller of this document, not the purchaser. Some of products Ordering Unit and Size is same. It has a header and multiple line items. SKU are grouped by Division which is to be ignored. Line items are in tabular format. */ <DOCUMENT_DATA> Extract complete information from above document. Include columns Order Number, Order Date, Delivery Date and Purchaser from header part strictly in json format. Where as each detail items extract Sr. No, SKU Name, Ordering Unit, Quantity, Product Name, Delivery Method, Product Strength, Size strictly in csv format with headings. Put all column values in quotes:', 'name': 'main_page', 'type': 'string', 'mandatory': 'false', 'max_length': '500'}, {'displayName': 'Other Pages', 'defaultValue': '/* Following is the data of the order document. GLAXO is seller of this document, not the purchaser. Some of products Ordering Unit and Size is same. It has a header and multiple line items. SKU are grouped by Division which is to be ignored. Line items are in tabular format. */ <DOCUMENT_DATA> Extract complete information from above document. For each detail items extract Sr. No, SKU Name, Ordering Unit, Quantity, Product Name, Delivery Method, Product Strength, Size strictly in csv format with heading. Put all column values in quotes:', 'name': 'other_pages', 'type': 'string', 'mandatory': 'false', 'max_length': '500'}, {'displayName': 'Post Order Extraction', 'defaultValue': 'TAeB==TAB /n Calpol==CALPOL1', 'name': 'POST_ORDER_EXTRACTION', 'type': 'string', 'mandatory': 'false', 'max_length': '100'}]}, 'extract_templ': 'DocDataExtraction', 'doc_type': 'Orders', 'objName': 'invoice-transaction', 'userId': 'SWAPNIL', 'OCR_DATA': '{"1":"P U R C H A S E  O R D  E R                           \\n   NAVNEET ENTERPRISES           TO : GLAXOSMITHKLINE PHARMACEUTICALS LTD ORDER NO. : 3627\\n   Unit No-112,113&114,First Floor,The Ambiance Park, Ghar No-362,Survey No-14/4P,17/2A\\n   Plot-53&54,Sector-19A,Near Green Park Hotel. Near Water Filtration Plant,Village Yavai,Mum-Nashik Highway ORDER DT. : 18/03/2023\\n   Vashi Navi Mumbai Pincode - 400705 (Maharashtra) Bhiwandi Thane - 421302 (Maharashtra)\\n   Mobile : 9769417885,9619869568 Tele : 8956518855 Mobile : 8956518856 SUPPLY DT. : 18/03/2023\\n                                 Email : ind.pharma-cfa-mumbai@gsk.com            \\n   Email : navneetenterprises83@gmail.com MFGR :                  TRPT NAME :     \\n   DLNo. : 20B/MH-TZ-7/75665 - 21B/MH-TZ-7/75666 - 20D/MH-TZ-7/75667DLNo. : 20B-MH-TZ5-205056 21B-MH-TZ5-205057\\n   GSTIN : 27AFSPJ4751Q1ZJ       GSTIN : 27AAACG4414B1Z8                          \\n   FSSAI No. : 11518016000367    LBTNo. :                                         \\n   Dear Sir/Madam,                                                                \\n       Kindy Arrange To Supply As Per Below Mentioned Order By Our Registered Transport/Courier.\\n   SN. PRODUCT DESCRIPTION    PACKING NICK QTY FREE MRP RATE AMOUNT SCHM REMARK   \\n      GLAXO INDIA LIMITED (DERMA ACE)                                             \\n     1 BETNOVATE N CREAM(BIG) 25 GMS GSK 2 560 7.00% 55.30 35.55 19908.00         \\n     2 BETNOVATE SKIN CREAM.  20 GMS GSK 2 100 0.00 20.81 a13.38 1338.00          \\n     3 TENOVATE M CREAM       15 GMS GSK 2 10 0.00 109.86 70.62 706.20            \\n     4 ZIMIG 250MG TAB.       7 S   GSK 2  20 0.00 340.55 218.93 4378.60          \\n     5 ZOVIRAX 200 MG. TAB.   5 S   GSK 2  30 0.00 38.02 24.44 733.20             \\n     6 ZOVIRAX SYP.           100 ML GSK 2 100 0.00 157.55 101.28 10128.00        \\n      GLAXO INDIA LIMITED (FORTIOR)                                               \\n                                                c                                 \\n     7 AUGMENTIN 375TAB       10 S  GIL(FO 200 0.00 229.00 147.21 29442.00        \\n     8 AUGMENTIN 625MG TAB    10 S  GIL(FO 500 0.00 182.78 117.50 58750.00        \\n     9 AUGMENTIN DUO SYP.     30ML  GIL(FO 480 0.00 60.48 38.88 18662.40          \\n    10 BANOCIDE FORTE TAB.    30 S  GIL(FO 60 0.00 46.94 32.19 1931.40            \\n    11 BANOCIDE TAB 50MG.     20 S  GIL(FO 20 0.00 11.76 8.06 161.20              \\n                                          i                                       \\n    12 BETNESOL FORT TAB      20 S  GIL(FO 100 0.00 23.40 15.04 1504.00           \\n    13 BETNESOL INJ.          8 X 1M GIL(FO 200 0.00 41.44 28.59 5718.00          \\n                                       d                                          \\n    14 BETNESOL TAB           1X20  GIL(FO 216 0.00 14.10 9.06 1956.96            \\n    15 CALPOL 250MG SYP.      60ML  GIL(FO 240 0.00 40.32 25.92 6220.80           \\n    16 CALPOL DROP PAED 15ML  15 ML. GIL(FO 100 0.00 30.07 19.33 1933.00          \\n    17 CALPOL PED. SYP.       60 ML GIL(FO 120 0.00 36.29 23.33 2799.60           \\n    18 CALPOL TAB             15 S  GIL(FO 810 90.00 13.44 8.64 6998.40 9+1       \\n    19 CALPOL-650MG PLUS TAB  10 TAeB GIL(FO 500 0.00 30.07 19.33 9665.00         \\n    20 NEOSPORIN - H OINT.    5 GMS GIL(FO 40 0.00 71.45 48.99 1959.60            \\n    21 NEOSPORIN SKIN OINT.   30 GM GIL(FO 80 20.00 192.50 123.75 9900.00 4+1     \\n    22 NEOSPORIN-H EAR DROP   5 ML  GIL(FO 20 0.00 76.40 52.39 1047.80            \\n    23 PIRITON CS SYP.        120ML GIL(FO 180 20.00 124.80 80.23 14441.40 9+1    \\n      GLAXO INDIA LIMITED (INGENIUM)                                              \\n                           m                                                      \\n    24 ELTROXIN 50 MG(120 TAB) 120T GSK 3  60 0.00 106.63 68.55 4113.00           \\n    25 ELTROXIN TAB 125MCG.   60 S  GSK 3  20 0.00 114.15 73.38 1467.60           \\n    26 FEFOL-Z CAP.           15 S  GSK 3  10 0.00 172.30 110.76 1107.60          \\n    27 LANOXIN TAB.           10 S  GSK 3  50 0.00 13.33 8.57 428.50              \\n    28 PHEXIN PAEDIATRIC DROPS. 10 ML. GSK 3 10 0.00 103.00 66.21 662.10          \\n    29 PHEXIN REDISYP 125 SYP 60ML  GSK 3  10 0.00 111.45 71.65 716.50            \\n    30 PHEXIN REDISYP SUSP.250MG 60ML GSK 3 10 0.00 191.85 123.33 1233.30         \\n    31 SUPACEF 1.5 GMS INJ.   VIAL  GSK 3 100 0.00 417.65 268.49 26849.00         \\n    32 ZYLORIC 100 MG. TAB    10 S  GSK 3 100 0.00 18.93 12.17 1217.00            \\n      GLAXO INDIA LIMITED.(DERMA WINGS)                                           \\n    33 EUMOSONE SKIN CREAM.   15 GMS GSK   10 0.00 100.90 64.87 648.70            \\n    34 FLUTIBACT OINT (BIG)   10GM  GSK    20 0.00 236.20 151.84 3036.80          \\n    35 FLUTIVATE CREAM.       20 GMS GSK   20 0.00 339.00 217.93 4358.60          \\n    36 FLUTIVATE OINT.        20 GMS GSK  100 0.00 192.80 123.94 12394.00         \\n    37 FLUTIVATE-E CREAM.     30 GM GSK    10 0.00 332.50 213.75 2137.50          \\n   Remark :                                                   END of Report PageNo.....1\\n   Terms & Conditions :                            E. & O. E. PO Value  270653.76 \\n   1) Subject to Jurisdiction.                                                    \\n   2) Ensure proper mention of Batch No. Expiry Date & MRP in invoice.            \\n   3) Kindly supply from single Batch of long expiry.                             \\n   4) Kindly ensure that product are stored under the appropriate condition during transportation.\\n   5) No changes in quantities/item permited unless confirmed with authorised person(s). For NAVNEET ENTERPRISES\\n   6) Delivery will not be accepted on last day of month (due to physical Stock Verification).\\n   7) This order cancells all pending orders of above manufacturer/division.      \\n   8) Adjust all pending claim in this order.                                     \\n   Expecting co-operation for our success, Thanking you.....                      \\n                                                                      Competent Signatory.\\n   This PDF is created from Medica Ultimate Software for enquiry contact +91-022-47474747, 9750000648/658, 9702074265 Page No. 1"}', 'proc_api_key': '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', 'ai_proc_templ': [{'role': 'system', 'content': 'You will be provided with unstructured data of a purchase order of customer for medicines. Your task is to parse header part in json format and detail line items in CSV format. Output will be used in an application for further processing, do not return any information, instruction or comments.'}, {'role': 'user', 'content': ' Give me example of how Product Name are appearing in this document.'}, {'role': 'assistant', 'content': '<product>'}, {'role': 'user', 'content': 'Give me examples of Packing or Ordering Unit.'}, {'role': 'assistant', 'content': '<packing>'}, {'role': 'user', 'content': 'Delivery method is the doses form of the medicine. Give me examples of Delivery Method of the products.'}, {'role': 'assistant', 'content': '<delivery>'}, {'role': 'user', 'content': 'Give me some examples of Product Strengths.'}, {'role': 'assistant', 'content': '<strength>'}, {'role': 'user', 'content': 'Give me some examples of Sizes.'}, {'role': 'assistant', 'content': '<size>'}, {'role': 'user', 'content': 'Give me example of SKU Configuration.'}, {'role': 'assistant', 'content': '<sku_name_examples>'}, {'role': 'user', 'content': 'Give me example of how detail line items are organised.'}, {'role': 'assistant', 'content': '<line_item_examples>'}, {'role': 'user', 'content': '<EXTRACT_INSTRUCTIONS>'}], 'file_type': 'PDF', 'ent_name': 'NAVNEET ENTERPRISES', 'ent_code': 1100372579}

# opv = OpenAIDataExtractor()
# opv.getlayouttextaidata(data)            
