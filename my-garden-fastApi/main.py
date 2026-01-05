from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

class Plant(BaseModel):
    name: str
    description: str | None = None
    x: int
    y: int

class checkRequest(BaseModel):
    new_plant:Plant
    existingPlants:list[Plant]
    
RULES = {
    'tomato': {
        'good': ['basil', 'carrot', 'onion', 'garlic'],
        'bad': ['potato', 'cabbage', 'cucumber'],
        'reasons': {
            'basil': 'Repels aphids and improves flavour',
            'carrot': 'Carrots aerate soil for tomato roots',
            'potato': 'Both susceptible to blight disease',
            'cabbage': 'Competes for nutrients'
        },
        'distance': 50
    },
    
    'potato': {
        'good': ['beans', 'cabbage', 'corn'],
        'bad': ['tomato', 'cucumber', 'pumpkin'],
        'reasons': {
            'beans': 'Beans fix nitrogen in soil',
            'tomato': 'Both get early and late blight',
            'cucumber': 'Both attract same pests'
        },
        'distance': 40
    },
    
    'lettuce': {
        'good': ['carrot', 'radish', 'strawberry', 'cucumber'],
        'bad': ['broccoli', 'cabbage'],
        'reasons': {
            'carrot': 'Carrots loosen soil, lettuce provides shade',
            'radish': 'Radishes break up soil for lettuce roots',
            'broccoli': 'Heavy feeders compete for nutrients'
        },
        'distance': 30
    },
    
    'carrot': {
        'good': ['tomato', 'lettuce', 'onion', 'leek'],
        'bad': ['dill', 'parsnip'],
        'reasons': {
            'onion': 'Onions repel carrot fly',
            'tomato': 'Tomatoes give off solanine protecting carrots',
            'dill': 'Stunts carrot growth'
        },
        'distance': 20
    },
    
    'onion': {
        'good': ['carrot', 'tomato', 'lettuce', 'cabbage'],
        'bad': ['beans', 'peas'],
        'reasons': {
            'carrot': 'Onions repel carrot rust fly',
            'beans': 'Onions stunt bean growth',
            'peas': 'Onions inhibit pea development'
        },
        'distance': 25
    },
    
    'beans': {
        'good': ['corn', 'potato', 'cucumber', 'radish'],
        'bad': ['onion', 'garlic', 'sunflower'],
        'reasons': {
            'corn': 'Classic three sisters - beans climb corn',
            'potato': 'Beans add nitrogen for potatoes',
            'onion': 'Onions inhibit bean growth',
            'garlic': 'Garlic stunts bean development'
        },
        'distance': 35
    },
    
    'cucumber': {
        'good': ['beans', 'lettuce', 'radish', 'peas'],
        'bad': ['potato', 'sage', 'mint'],
        'reasons': {
            'beans': 'Beans fix nitrogen cucumbers need',
            'radish': 'Radishes repel cucumber beetles',
            'potato': 'Both prone to blight in NZ humidity',
            'sage': 'Sage inhibits cucumber growth'
        },
        'distance': 45
    },
    
    'basil': {
        'good': ['tomato', 'capsicum', 'asparagus'],
        'bad': ['rue', 'sage'],
        'reasons': {
            'tomato': 'Repels aphids, whitefly and improves flavour',
            'capsicum': 'Enhances growth and flavour',
            'rue': 'Allelopathic - inhibits basil'
        },
        'distance': 30
    },
    
    'eggplant': {
        'good': ['beans', 'peas', 'spinach', 'thyme'],
        'bad': ['fennel', 'potato', 'tomato'],
        'reasons': {
            'beans': 'Beans provide nitrogen eggplant needs',
            'peas': 'Peas fix nitrogen in soil',
            'potato': 'Both nightshade family - attract same pests',
            'tomato': 'Both nightshade - share diseases like verticillium wilt',
            'fennel': 'Fennel inhibits growth of most vegetables'
        },
        'distance': 45
    },
    
    'courgette': {
        'good': ['corn', 'beans', 'radish'],
        'bad': ['potato', 'pumpkin'],
        'reasons': {
            'corn': 'Provides shade, courgette mulches soil',
            'beans': 'Beans provide nitrogen',
            'potato': 'Both heavy feeders, compete',
            'pumpkin': 'Cross-pollination affects fruit'
        },
        'distance': 60
    }
}
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict["brand"])

def checkCompanion(request:checkRequest):
   
    

def add_numbers(a, b):
    """
    这个函数接收两个数字作为参数，并返回它们的和。
    """
    sum_result = a + b
    return sum_result

@app.post("/plants/")
async def create_item(plant: Plant):
    return plant