from fastapi import FastAPI
from pydantic import BaseModel
import math

app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


    
    
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


class Plant(BaseModel):
    id:int
    type: str
    description: str | None = None
    x: int
    y: int

class CheckRequest(BaseModel):
    new_plant:Plant
    existing_plants:list[Plant]
    

class CheckResponse(BaseModel):
    warnings: list[str]
    suggestions: list[str]
    highlight_bad: list[int]  
    highlight_good: list[int]  


@app.post("/api/CheckCompanion/")
def CheckCompanion(request:CheckRequest):
    # print("check")
    warnings = []
    suggestions = []
    highlight_bad = []
    highlight_good = []
    for existing_plant in request.existing_plants:
        distance=math.sqrt((request.new_plant.x-existing_plant.x)**2+(request.new_plant.y-existing_plant.y)**2)
        newplantrule=RULES[request.new_plant.type]
        if distance< newplantrule['distance']:
            if existing_plant.type in newplantrule['good']:
                suggestion=f"{request.new_plant.type} is companion with {existing_plant.type} "
                suggestions.append(suggestion)
                highlight_good.append(existing_plant.id)
            if existing_plant.type in newplantrule['bad']:
                warning=f"{request.new_plant.type} is comflict with {existing_plant.type} "
                warnings.append(warning)
                highlight_bad.append(existing_plant.id)
    # print(f"warnings: {warnings}")
    # print(f"suggestions: {suggestions}")
    return CheckResponse(
        warnings=warnings,
        suggestions=suggestions,
        highlight_bad=highlight_bad,   
        highlight_good= highlight_good    
)
   

@app.post("/api/plants/")
async def create_item(plant: Plant):
    return plant
