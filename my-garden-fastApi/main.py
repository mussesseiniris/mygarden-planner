from fastapi import FastAPI
from pydantic import BaseModel
import math
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的前端域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有请求方法（POST/GET等）
    allow_headers=["*"],  # 允许所有请求头
)
    
    
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
        'distance': 150  # 50cm × 3 = 100px
    },
    'potato': {
        'good': ['beans', 'cabbage', 'corn'],
        'bad': ['tomato', 'cucumber', 'pumpkin'],
        'reasons': {
            'beans': 'Beans fix nitrogen in soil',
            'tomato': 'Both get early and late blight',
            'cucumber': 'Both attract same pests'
        },
        'distance': 120  # 40cm × 3 = 80px
    },
    'lettuce': {
        'good': ['carrot', 'radish', 'strawberry', 'cucumber'],
        'bad': ['broccoli', 'cabbage'],
        'reasons': {
            'carrot': 'Carrots loosen soil, lettuce provides shade',
            'radish': 'Radishes break up soil for lettuce roots',
            'broccoli': 'Heavy feeders compete for nutrients'
        },
        'distance': 90  # 30cm × 3 = 300px
    },
    'carrot': {
        'good': ['tomato', 'lettuce', 'onion', 'leek'],
        'bad': ['dill', 'parsnip'],
        'reasons': {
            'onion': 'Onions repel carrot fly',
            'tomato': 'Tomatoes give off solanine protecting carrots',
            'dill': 'Stunts carrot growth'
        },
        'distance': 60  # 20cm × 3 = 200px
    },
    'onion': {
        'good': ['carrot', 'tomato', 'lettuce', 'cabbage'],
        'bad': ['beans', 'peas'],
        'reasons': {
            'carrot': 'Onions repel carrot rust fly',
            'beans': 'Onions stunt bean growth',
            'peas': 'Onions inhibit pea development'
        },
        'distance': 75  # 25cm × 3 = 50px
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
        'distance': 105  # 35cm × 3 = 105px
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
        'distance': 135  # 45cm × 3 = 135px
    },
    'basil': {
        'good': ['tomato', 'capsicum', 'asparagus'],
        'bad': ['rue', 'sage'],
        'reasons': {
            'tomato': 'Repels aphids, whitefly and improves flavour',
            'capsicum': 'Enhances growth and flavour',
            'rue': 'Allelopathic - inhibits basil'
        },
        'distance': 90  # 30cm × 3 = 90px
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
        'distance': 135  # 45cm × 3 = 135px
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
        'distance': 180  # 60cm × 3 = 180px
    }
}

class Plant(BaseModel):
    id:int
    type: str
    description: str | None = None
    x: float
    y: float
    width: int
    height: int

class CheckRequest(BaseModel):
    new_plant:Plant
    existing_plants:list[Plant]
    

class CheckResponse(BaseModel):
    warnings: list[str]
    suggestions: list[str]
    highlight_bad: list[int]  
    highlight_good: list[int]  


@app.post('/api/CheckCompanion/')
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
                suggestion=f"{request.new_plant.type} is companion with {existing_plant.type}. Influence distance:{newplantrule['distance']/3}cm."
                reason = newplantrule['reasons'].get(existing_plant.type,'')
                if reason:
                    suggestion=suggestion+f". {reason}."
                suggestions.append(suggestion)
                highlight_good.append(existing_plant.id)
                
            if existing_plant.type in newplantrule['bad']:
                warning=f"{request.new_plant.type} is conflict with {existing_plant.type}. Influence distance:{newplantrule['distance']/3}cm. "
                reason = newplantrule['reasons'].get(existing_plant.type,'')
                if reason:
                    warning=warning+f" {reason}."
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

