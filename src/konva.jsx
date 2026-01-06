import { Stage, Layer, Rect } from 'react-konva'
import { Image } from 'react-konva'
import { useEffect, useState } from 'react'

const PLANT_ITEM_WIDTH = 80;
const PLANT_ITEM_HEIGHT = 80;
const BOX_WIDTH=160;
const BOX_HEIGHT=300;

// image component
function ItemImage({ item }) {
  const [image, setImage] = useState(null)
  
  useEffect(() => {
    if (!item.image) return; 
    const img = new window.Image()
    img.src = item.image
    img.onload = () => {
      setImage(img)
    }
  
    return () => {
      img.onload = null;
    }
  }, [item.image])
  
  if (!image) return null 
  
  return (
    <Image
      image={image}
      x={item.x}
      y={item.y}
      width={80}
      height={80}
      draggable={true} 
    />
  )
}

function KonvaCanvas() {
  
  const PLANTS = {
    potato: { name: 'Potato', image: '/images/potato.png', emoji: '🥔' },
    tomato: { name: 'Tomato', image: '/images/tomato.png', emoji: '🍅' },
    lettuce: { name: 'Lettuce', image: '/images/lettuce.png', emoji: '🥬' },
    carrot: { name: 'Carrot', image: '/images/carrot.png', emoji: '🥕' }, 
    onion: { name: 'Onion', image: '/images/onion.png', emoji: '🧅' },
    beans: {name:'Beans', image: '/images/beans.png',emoji: '🫘'},
    cucumber: {name:'Cucumber',image: '/images/cucumber.png',emoji:'🥒'},
    basil: {name: 'Basil', image: '/images/basil.png', emoji:'🌿'},
    eggplant: {name: 'Eggplant', image:'/images/eggplant.png',emoji:'🍆'},
    courgette: {name: 'Courgette',image:'/images/courgette.png',emoji:'🥒'}
  }
  
  // box
  const PlantBox = {
    name: 'Box', 
    image: '/images/box.jpg',
    emoji: '📦' 
  }


  const [plants, setPlants] = useState([])
  const [boxes, setBoxes] = useState([]) 

  
  const addPlant = (plantType) => {
    const plant = PLANTS[plantType]
    const newPlant = {
      id: Date.now(),
      x: Math.random() * 600,
      y: Math.random() * 400,
      width: PLANT_ITEM_WIDTH ,
      height: PLANT_ITEM_HEIGHT,
      type: plantType,
      name: plant.name,
      image: plant.image
    }
    setPlants([...plants, newPlant])
  }


  const addBox = () => {
    const newBox = {
      id: Date.now(), // react key
      x: Math.random() * 600,
      y: Math.random() * 400,
      width: 80,
      height: 80,
      name: PlantBox.name,
      image: PlantBox.image
    }
    setBoxes([...boxes, newBox]) // add new box to the list
  }

  return (
    <div className="App">
      <h1>Garden Planner</h1>
      
      <div style={{margin: '10px'}}>
        {/* plant button */}
        {Object.keys(PLANTS).map(plantType => (
          <button 
            key={plantType}
            onClick={() => addPlant(plantType)} 
          >
            {PLANTS[plantType].emoji} Add {PLANTS[plantType].name}
          </button>
        ))}
        {/* box button */}
        <button onClick={addBox}>
          {BOX_CONFIG.emoji} Add {BOX_CONFIG.name}
        </button>
      </div>

    {/* canvas*/}
      <Stage width={1276} height={800} style={{border: '2px solid #ffc0cb'}}>
        <Layer>
          {/* render plants */}
          {plants.map((plant) => (
            <ItemImage 
              key={plant.id} 
              item={plant} 
            />
          ))}
          {/* render boxes */}
          {boxes.map((box) => (
            <ItemImage 
              key={box.id} 
              item={box} 
            />
          ))}
        </Layer>
      </Stage>
    </div>
  )
}

export default KonvaCanvas;