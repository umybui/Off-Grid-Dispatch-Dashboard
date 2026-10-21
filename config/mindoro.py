DEPENDABLE_REFERENCE = [
    {"Plant":"OMCPC SAMARICA","DependableMW":21.00},
    {"Plant":"OMCPC HIGH-SPEED","DependableMW":8.30},
    {"Plant":"OMCPC SOLAR","DependableMW":6.00},
    {"Plant":"OMCPC MAPSA","DependableMW":5.30},
    {"Plant":"OMCPC SABLAYAN","DependableMW":4.00},
    {"Plant":"PGCI","DependableMW":1.00},

    {"Plant":"DMCI REGULATING","DependableMW":11.30},
    {"Plant":"DMCI LOT I","DependableMW":5.00},

    {"Plant":"LCMHPP-UPPER","DependableMW":1.63},
    {"Plant":"LCMHPP-LOWER","DependableMW":1.02},

    {"Plant":"INABASAN MHPP","DependableMW":10.00},
    {"Plant":"CATUIRAN HEPP","DependableMW":4.40},

    {"Plant":"PHESI-WEPF","DependableMW":16.00},

    {"Plant":"OPI","DependableMW":7.40},
    {"Plant":"POC","DependableMW":2.60},
    {"Plant":"MHEC","DependableMW":2.63},

    {"Plant":"POWER PIONEERS","DependableMW":5.00},

    {"Plant":"GFEC","DependableMW":6.25},

    {"Plant":"TOPTEAM CALAPAN","DependableMW":4.00},
    {"Plant":"TOPTEAM SOCORRO","DependableMW":2.00},

    {"Plant":"SPC SOCORRO","DependableMW":2.00},

    {"Plant":"TPI BANSUD","DependableMW":4.00},
    {"Plant":"TPI CALAPAN","DependableMW":4.00},

    {"Plant":"REGULUS","DependableMW":3.00},

    {"Plant":"RMS","DependableMW":4.00},
    {"Plant":"TOPTEAM BONGABONG","DependableMW":3.00},
    {"Plant":"SPC ROXAS","DependableMW":1.50}
]

CONFIG = {

    "SYSTEM_NAME": "Mindoro",

    "FILE_PATH": "data/Mindoro Dispatch Summary Final.xlsm",

    "SHEET_NAME": "Main Query",

    "DATETIME_COLUMN": "Datetime",

    "VALUE_COLUMN": "Value",
    
    "DEMAND_PLANT": "TOTAL DEMAND",

    "GENERATION_ATTRIBUTE": "NET MW",

    "PLANT_COLUMN": "Plant",

    "USES_IMPORT_SUPPORT": True,
    
    "IMPORT_KEYWORD": "IMPORT",

    "UNIT_SCALE": 1,

    "ATTRIBUTE_FILTER": "NET MW",

    "GENERATION_EXCLUDE_KEYWORDS": [
    "TOTAL DEMAND",
    "TOTAL GENERATION",
    "SYNCHRO",
    "IMPORT"
    ],

    "DEPENDABLE_REFERENCE": DEPENDABLE_REFERENCE,

    "CAPACITY_AGGREGATION": "max"
    
    "TECHNOLOGY_MAPPING": {
        "OMCPC SAMARICA": "Bunker",
        "OMCPC HIGH-SPEED": "Diesel",
        "OMCPC SOLAR": "Solar",
        "OMCPC MAPSA": "Diesel",
        "OMCPC SABLAYAN": "Diesel",
        "PGCI": "Biomass",
        "DMCI REGULATING": "Bunker",
        "DMCI LOT I": "Diesel",
        "LCMHPP-UPPER": "Hydro",
        "LCMHPP-LOWER": "Hydro",
        "INABASAN MHPP": "Hydro",
        "CATUIRAN HEPP": "Hydro",
        "PHESI-WEPF": "Wind",  
        "OPI": "Bunker",
        "POC": "Bunker",
        "MHEC": "Bunker",
        "POWER PIONEERS": "Others",
        "GFEC": "Others",
        "TOPTEAM CALAPAN": "Others",
        "TOPTEAM SOCORRO": "Others",
        "SPC SOCORRO": "Others",
        "TPI BANSUD": "Others",
        "TPI CALAPAN": "Others",
        "REGULUS": "Others",
        "RMS": "Others",
        "TOPTEAM BONGABONG": "Others",
        "SPC ROXAS": "Others",       
    }

}
