#-*- coding: utf-8 -*-
"""
@author:MD.Nazmuddoha Ansary
"""
from __future__ import print_function
import warnings
warnings.filterwarnings('ignore')
#-------------------------
# imports
#-------------------------
from .utils import LOG_INFO
from .apsisnet import ApsisNet
from .paddledbnet import PaddleDBNet
from .paddlesvtr import SVTRLCNet
from .densenet121bnencls import DenseNet121BnEnClassifier
import cv2
import copy
import pandas as pd
import numpy as np
#-------------------------
# class
#------------------------
class BaseOCR(object):
    """
    BaseOCR processes images for Optical Character Recognition (OCR) using
    models for Bangla and English text recognition, a text detector, and a language classifier.

    Attributes:
        bn_rec (ApsisNet): Instance of ApsisNet for Bangla text recognition.
        en_rec (SVTRLCNet): Instance of SVTRLCNet for English text recognition.
        detector (PaddleDBNet): Instance of PaddleDBNet for text detection.
        lang_cls (DenseNet121BnEnClassifier): Instance of DenseNet121BnEnClassifier for language classification.
    """

    def __init__(self) -> None:
        """
        Initialize ApsisOCR object with models for Bangla and English text recognition,
        a text detector, and a language classifier.
        """        
        self.bn_rec=ApsisNet()
        LOG_INFO("Loaded Bangla Model")
        self.en_rec=SVTRLCNet()
        LOG_INFO("Loaded English Model")
        self.detector=PaddleDBNet()        
        LOG_INFO("Loaded Paddle detector")
        self.lang_cls=DenseNet121BnEnClassifier()
        LOG_INFO("Loaded Language classifier")
        
    
    def __call__(self, img_path: str) -> dict:
        """
        Perform OCR on an image.

        Args:
            img_path (str): Path to the image file.

        Returns:
            dict: OCR results containing recognized text and associated information. The dictionary has the following structre
                {
                    "poly"    : the four point polygonal bounding box of the word in the image
                    "text"    : the recognized text 
                    "lang"    : the classified language code
                }
        """  
        result=[]
        # -----------------------start-----------------------
        img=cv2.imread(img_path)
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        # text detection
        word_boxes=self.detector.get_word_boxes(img)
        crops=self.detector.get_crops(img,word_boxes)
        # crop id and bbox info
        df=pd.DataFrame({"crop_id":[i for i in range(len(word_boxes))],"poly":word_boxes})

        #--------------------------------classification------------------------------------
        langs=self.lang_cls.infer(crops)
        df["lang"]=langs
        # language classification
        bn_df=df.loc[df.lang=="bn"]
        en_df=df.loc[df.lang=="en"]
        bn_ids=bn_df.crop_id.tolist()
        bn_word_crops=[crops[i] for i  in bn_ids]
        en_ids=en_df.crop_id.tolist()
        en_word_crops=[crops[i] for i  in en_ids]
        
        #--------------------------------bangla------------------------------------
        bn_text=self.bn_rec.infer(bn_word_crops)
        bn_df["text"]=bn_text
        #--------------------------------english------------------------------------
        en_text=self.en_rec.infer(en_word_crops)
        en_df["text"]=en_text
        #--------------------------------combine data------------------------------------
        df=pd.concat([bn_df,en_df],ignore_index=True)
        # format
        for idx in range(len(df)):
            data={}
            poly_res=  []
            poly    =  df.iloc[idx,1]
            poly    = np.array(poly).reshape(4,2)
            for pair in poly:
                _pair=[float(pair[0]),float(pair[1])]
                poly_res.append(_pair)
            
            data["poly"]   =poly_res
            data["lang"]   =df.iloc[idx,2]
            data["text"]   =df.iloc[idx,3]
            result.append(data)
        return result
