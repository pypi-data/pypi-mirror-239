import requests 
from bs4 import BeautifulSoup 
import matplotlib.pyplot as plt
from PIL import Image , ImageEnhance
from io import BytesIO
import base64
from IPython.display import display , HTML
from IPython.display import Image as ipdi
import numpy as np
import cv2
import io
import jaywalker as jw

class asin_work_id_display:
    
    def __init__(self , asin , work_id):
        self.audible_asin = [asin]
        self.work_id = work_id
        self.audible_url = f"https://www.audible.com/pd/{asin}"
        self.gr_url = f"https://www.goodreads.com/work/editions/{work_id}"
    
    def extract_gr_image(self):
        response = requests.get(self.gr_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            imgs = soup.find_all('img')
            for img_tag in imgs:
                    image_url = img_tag.get('src')
                    alt_text = img_tag.get('alt')
                    if alt_text is None:   
                        alt_text = ''
                    title = soup.title.string
                    if alt_text in title:
                        if image_url:
                            img_data = requests.get(image_url).content
                            img = Image.open(BytesIO(img_data))
                            image = np.array(img)
                            if img.format == 'JPEG' or 'PNG':
                                buffer = io.BytesIO()
                                Image.fromarray(image).save(buffer , format = "PNG")
                                gr_img_data = base64.b64encode(buffer.getvalue()).decode()
                                return gr_img_data                 
                        
    def extract_aud_image (self): 
        
        img = jw.render.display_asins(self.audible_asin, 'US')
        html_content = img.data
        soup = BeautifulSoup(html_content, 'html.parser')
        img_tags = soup.find_all('img')
        anchor_tags = soup.find_all('a')
        for anchor in anchor_tags:
                href = anchor.get('href')
        aud_image_url = [img['src'] for img in img_tags]
        
        return aud_image_url
                        
    def disp_mapping ( self , gr_img_data , aud_image_url):
        gr_img_data = gr_img_data
        aud_img_url = aud_image_url
        html = f'''
                    <div style="display: flex; justify-content: left;">
                                            <div>
                                                <a href="{self.gr_url}">
                                                <img src="data:image/png;base64,{gr_img_data}" width="175" height="175">
                                                <p> ID : {self.work_id}</p>
                                                </a>
                                            </div>
                                            <div>
                                                <a href = "{self.audible_url}">
                                                <img src="{aud_image_url[0]}" width="175" height="175">
                                                <p> ASIN : {self.audible_asin[0]}</p>
                                                </a>
                                            </div>
                                        </div>
                                    
                                '''
        display(HTML(html))
