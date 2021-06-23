import sys
import json
import os
from json2html import *
import re
import argparse as ap
 
jsonfile = 'results.json'
  
def pipelinescan(aplicacao, veracodeId, veracodeKey):
    try:
        if (aplicacao == None) | (veracodeId == None) | (veracodeKey == None):
            print("[-] Informar o parametros!")
        else:    
            print(f'[+] PipelineScan, executado no produto {aplicacao}')
 
            os.system("java -jar pipeline-scan.jar --veracode_api_id " + veracodeId + " --veracode_api_key " + veracodeKey + " --file " + aplicacao + " --issue_details true --json_output true --filtered_json_output_file filtered.json")
 
    except:
        raise Exception('Incorrect scan format')
 
def getHTML():
 
    with open(jsonfile) as json_file:
        pipelinedata = json.load(json_file)
        data = json.dumps(pipelinedata, indent=4)
       
        clean = re.sub('<[^<]+?>', '', data)
        clean = clean.replace('\n', '')
        html = json2html.convert(json=clean, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")
       
        html2 = """
        <html>
        <head>
       
        <link rel="stylesheet" href=https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
        <script src=https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
        </head>
        <body>
        """+html+"""
        </body>
        </html>
        """
 
        f = open("Report.html", "w")
        f.write(html2)
        f.close()
 
              
if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Rodar o programa dessa forma: python3 pipelineScan_Code.py --aplicacao NomeDaApp.zip --veracodeId {ID} --veracodeKey {KEY}')
    parser.add_argument('--aplicacao', help='Aplicacao para analise de seguranca em formato .zip. Ex. (TomatoApp.zip)', required=True)
    parser.add_argument('--veracodeId', help='Informar o VeraCode ID', required=True)
    parser.add_argument('--veracodeKey', help='Informar o VeraCode Key', required=True) 
 
    args = parser.parse_args()
 
    # Load PipelineScan
    #
    aplicacao = args.aplicacao
    veracodeId = args.veracodeId
    veracodeKey = args.veracodeKey
 
    pipelinescan(aplicacao, veracodeId, veracodeKey)
   
    #
    # Generate HTML
    #
    getHTML()
 
    aplicacao = ""
    veracodeId = ""
    veracodeKey = ""
 
    print("[+] Scan finalizado, analise o arquivo Report.html")
