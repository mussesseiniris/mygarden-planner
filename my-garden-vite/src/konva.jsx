import { Stage, Layer, Rect } from 'react-konva'
import { Image } from 'react-konva'
import { useEffect, useState } from 'react'

const PLANT_ITEM_WIDTH = 80;
const PLANT_ITEM_HEIGHT = 80;
const BOX_WIDTH=160;
const BOX_HEIGHT=300;

//check if current plant isoverlapping
function IsOverLapping (curPlant,exiPlant){
  
  const leftOf = curPlant.x+curPlant.width<exiPlant.x
  const topOf = curPlant.y+curPlant.height<exiPlant.y
  const rightOf = curPlant.x > exiPlant.x+exiPlant.width
  const bottomOf = curPlant.y > exiPlant.y+exiPlant.height
  if(!(leftOf ||topOf || rightOf || bottomOf )){
    return true}

return false
}



// image component
function ItemImage({ item,allPlants }) {
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
  }, [item.image]) // when item.image chaged run this code
  

const handleDragBound = (pos)=>{

//pos:the place item wants to go 
const curItem={

 x:pos.x,
 y:pos.y,
 width:item.width,
 height:item.height
}

for(let other of allPlants){
  if (other.id == item.id)
    continue
  const otherPlant={
    x:other.x,
    y:other.y,
    width:other.width,
    height:other.height
  }
  
  if(IsOverLapping(curItem,otherPlant)){
    return {x:item.x,y:item.y}
  }
 
}
return pos

}



  if (!image) return null 
  
  return (
    <Image
      image={image}
      x={item.x}
      y={item.y}
      width={item.width}
      height={item.height}
      draggable={true} 
      dragBoundFunc={handleDragBound} 
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
          {PlantBox.emoji} Add {PlantBox.name}
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
              allPlants={plants} 
            />
          ))}
          {/* render boxes */}
          {boxes.map((box) => (
            <ItemImage 
              key={box.id} 
              item={box} 
              allPlants={plants} 
            />
          ))}
        </Layer>
      </Stage>
    </div>
  )
}

export default KonvaCanvas;