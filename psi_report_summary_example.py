"""
@Description: An example of how you can rebuild the "report_summary" from the Pagespeed Audit API. This is not intended to be a complete script or useful on its own. Instead, the intention is to show one way to access this information.
"""

import urllib.request
import urllib.parse
import json

###Important Data###
api_key = 'GOOGLE_LIGHTHOUSE_API_KEY'
locale = 'en-US' #Set To Your Location
strategy = 'mobile' #Set To Your Device Type, Mobile Is Recommended Default
###Important Data###

def ping_psi(url):
    escaped_url = urllib.parse.quote(url)
    request_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={escaped_url}&locale={locale}&strategy={strategy}&key={api_key}'
    psi_json = urllib.request.urlopen(request_url).read().decode('UTF-8')
    formatted_json = json.loads(psi_json)
    return formatted_json

def save_json(formatted_json,json_name='examplefile'): #saves output to JSON file you can view in any JSON Viewer. Useful for troubleshooting
    try:
        with open (f'investigate_{json_name}_json.json','w') as f:
            json.dump(formatted_json, f, indent=4)
    except:
        print('json could not be saved')

def generate_resource_summary(formatted_json,requested_audit):
    length = len(formatted_json['lighthouseResult']['audits']['network-requests']['details']['items'])
    count = 0
    item_count = 0
    item_byte_sum = 0
    while count < length:
        if formatted_json['lighthouseResult']['audits']['network-requests']['details']['items'][count]['resourceType'] == requested_audit:
            item_count += 1
            try:
                item_byte_sum += int(formatted_json['lighthouseResult']['audits']['network-requests']['details']['items'][count]['transferSize'])
            except:
                item_byte_sum += 0
            count += 1
        else:
            count += 1
    return item_count,item_byte_sum

def example_func(url):
    #Options In Report ['Font','Document','Stylesheet','Image','Script','XHR','Ping','Preflight','Fetch','Other','Media']
    formated_json = ping_psi(url)
    font_count,font_byte_weight = generate_resource_summary(formatted_json=formated_json,requested_audit='Font')
    image_count,image_byte_weight = generate_resource_summary(formatted_json=formated_json,requested_audit='Image')
    example_report_dict =  {
        'page_url' : url,
        'performance_score' : formated_json['lighthouseResult']['categories']['performance']['score'],
        'number_of_font_files' : font_count,
        'font_transfer_size' : font_byte_weight,
        'number_of_image_files' : image_count,
        'image_transfer_size' : image_byte_weight

    }
    return example_report_dict

if __name__ == '__main__':
    url = input("What Is The URL You Want To Crawl?")
    example_report_dict = example_func(url)
    print(example_report_dict)
