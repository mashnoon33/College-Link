'''
    apitest.py
    Mash Ibtesum, October 16 2018

    Tests api.py
'''

import unittest
from ../api import api

class testAPI(unittest.TestCase):
    def setUp(self):
        self.api=api()
        self.carleton = {
        "﻿INSTNM" : "Carleton College",
        "CITY" : "Northfield",
        "STABBR" : "MN",
        "OPEID" : 234000,
        "ADM_RATE" : 0.2262,
        "SAT_AVG" : 1413,
        "UGDS_WHITE" : 0.6161,
        "COSTT4_A" : 64420,
        "MD_EARN_WNE_P9" : 75000
        }
        self.carleton_full={
        "﻿INSTNM" :"Carleton College" ,
        "CITY" :"Northfield" ,
        "STABBR" :"MN" ,
        "ZIP" :"55057-4001" ,
        "INSTURL" :"www.carleton.edu" ,
        "NPCURL" :"https://apps.carleton.edu/admissions/afford/estimator/ ",
        "OPEID" :234000 ,
        "OPEID6" :2340 ,
        "REGION" :4 ,
        "LOCALE" :32 ,
        "LATITUDE" :44.462318 ,
        "LONGITUDE" :-93.154666 ,
        "ADM_RATE" :0.2262 ,
        "SATVR25" :660 ,
        "SATVR75" :770 ,
        "SATMT25" :660 ,
        "SATMT75" :770 ,
        "SATWR25" :660 ,
        "SATWR75" :750 ,
        "SATVRMID" :715 ,
        "SATMTMID" :715 ,
        "SATWRMID" :705 ,
        "ACTCM25" :30 ,
        "ACTCM75" :33 ,
        "ACTEN25" : None ,
        "ACTEN75" : None ,
        "ACTMT25" : None ,
        "ACTMT75" : None ,
        "ACTWR25" : None ,
        "ACTWR75" : None ,
        "ACTCMMID" :32 ,
        "ACTENMID" : None ,
        "ACTMTMID" : None ,
        "ACTWRMID" : None ,
        "SAT_AVG" :1413 ,
        "SAT_AVG_ALL" :1413 ,
        "PCIP01" :0 ,
        "PCIP03" :0.0201 ,
        "PCIP04" :0 ,
        "PCIP05" :0.0241 ,
        "PCIP09" :0 ,
        "PCIP10" :0 ,
        "PCIP11" :0.1006 ,
        "PCIP12" :0 ,
        "PCIP13" :0 ,
        "PCIP14" :0 ,
        "PCIP15" :0 ,
        "PCIP16" :0.0302 ,
        "PCIP19" :0 ,
        "PCIP22" :0 ,
        "PCIP23" :0.0644 ,
        "PCIP24" :0 ,
        "PCIP25" :0 ,
        "PCIP26" :0.1127 ,
        "PCIP27" :0.0644 ,
        "PCIP29" :0 ,
        "PCIP30" :0.006 ,
        "PCIP31" :0 ,
        "PCIP38" :0.0282 ,
        "PCIP39" :0 ,
        "PCIP40" :0.1268 ,
        "PCIP41" :0 ,
        "PCIP42" :0.0604 ,
        "PCIP43" :0 ,
        "PCIP44" :0 ,
        "PCIP45" :0.1992 ,
        "PCIP46" :0 ,
        "PCIP47" :0 ,
        "PCIP48" :0 ,
        "PCIP49" :0 ,
        "PCIP50" :0.0986 ,
        "PCIP51" :0 ,
        "PCIP52" :0 ,
        "PCIP54" :0.0644 ,
        "UGDS" :2045 ,
        "UG" :1936 ,
        "UGDS_WHITE" :0.6161 ,
        "UGDS_BLACK" :0.045 ,
        "UGDS_HISP" :0.0748 ,
        "UGDS_ASIAN" :0.0856 ,
        "UGDS_AIAN" :0.0015 ,
        "UGDS_NHPI" :0.001 ,
        "UGDS_2MOR" :0.0567 ,
        "UGDS_NRA" :0.1017 ,
        "UGDS_UNKN" :0.0176 ,
        "UGDS_WHITENH" :0.6913 ,
        "UGDS_BLACKNH" :0.0463 ,
        "UGDS_API" :0.0967 ,
        "UGDS_AIANOLD" :0.0065 ,
        "UGDS_HISPOLD" :0.0554 ,
        "UG_NRA" :0.0181 ,
        "UG_UNKN" :0 ,
        "UG_WHITENH" :0.8316 ,
        "UG_BLACKNH" :0.0294 ,
        "UG_API" :0.0821 ,
        "UG_AIANOLD" :0.0026 ,
        "UG_HISPOLD" :0.0362 ,
        "NPT4_PRIV" :26745 ,
        "NPT41_PUB" : None ,
        "NPT42_PUB" : None ,
        "NPT43_PUB" : None ,
        "NPT44_PUB" : None ,
        "NPT45_PUB" : None ,
        "NPT41_PRIV" :12207 ,
        "NPT42_PRIV" :13473 ,
        "NPT43_PRIV" :14682 ,
        "NPT44_PRIV" :22396 ,
        "NPT45_PRIV" :38398 ,
        "NUM4_PRIV" :228 ,
        "COSTT4_A" :64420 ,
        "TUITIONFEE_IN" :50874 ,
        "TUITIONFEE_OUT" :50874 ,
        "FEMALE_ENRL_ORIG_YR2_RT" :0.803571429 ,
        "MALE_ENRL_ORIG_YR2_RT" :0.819047619 ,
        "GRAD_DEBT_MDN" :19500 ,
        "FIRSTGEN_DEBT_MDN" :18409 ,
        "NOTFIRSTGEN_DEBT_MDN" :18798 ,
        "FIRST_GEN" :0.162393162 ,
        "COUNT_WNE_INDEP0_INC1_P10" :21
        }

    def test_search_with_name(self):
        self.assertIn(self.carleton ,self.api.name("Carleton"))

    def test_search_with_name_result_size(self):
        self.assertEqual(self.api.name("northwest"), 52)

    def test_search_with_bad_name(self):
        self.assertEqual([] ,self.api.name("JONDICCCCCC--|||"))

    def test_search_with_params(self):
        self.assertIn(self.carleton ,self.api.param(SAT_AVG=[1400,1500], ADM_RATE=[20,24], MD_EARN_WNE_P9=[70,000, 150,000], type="private"))

    def test_search_with_params(self):
        self.assertNotIn(self.carleton ,self.api.param(SAT_AVG=[1500,1600], ADM_RATE=[20,24], MD_EARN_WNE_P9=[70,000, 150,000], type="private"))

    def test_get_school(self):
        self.assertEqual(self.carleton_full, self.api.school(234000))

    def test_util_regions(self):
        expected = {"Region" :  "Plains", "states" : ["CT", "ME", "MA", "NH", "RI", "VT"]}
        self.assertIn(expected ,self.api.getRegions())
        self.assertEqual(9, len(self.api.getRegions()))

    def test_util_states(self):
        expected = {"state" : "New York", "abbreviation" : "NY"}
        self.assertIn(expected ,self.api.getStataes())
        self.assertEqual(52, len(self.api.getStataes()))

    def test_util_majors(self):
        self.assertIn("Computer Science" ,self.api.getMajors())

if __name__ == "__main__":
    unittest.main() # run all tests
