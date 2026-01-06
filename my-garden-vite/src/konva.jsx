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
function ItemImage({ item,allPlants,onShowGuide }) {
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
  

const handleShowguide=()=>{
onShowGuide(item
)
}

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
      onDblClick={handleShowguide}
    />
  )
}

function KonvaCanvas() {
  
const PLANTS = {
  potato: { 
    name: 'Potato', 
    image: '/images/potato.png', 
    emoji: '🥔',
    guide: 'Plant Aug-Nov in NZ. Space 30cm apart in rows. Needs full sun and well-drained soil. Harvest when foliage dies back (12-16 weeks).'
  },
  tomato: { 
    name: 'Tomato', 
    image: '/images/tomato.png', 
    emoji: '🍅',
    guide: 'Plant Oct-Dec after last frost. Needs full sun and support stakes. Water deeply and regularly. Harvest when fully colored (10-14 weeks).'
  },
  lettuce: { 
    name: 'Lettuce', 
    image: '/images/lettuce.png', 
    emoji: '🥬',
    guide: 'Plant year-round in NZ, best in spring/autumn. Space 20cm apart. Needs partial shade in summer. Harvest outer leaves regularly (6-8 weeks).'
  },
  carrot: { 
    name: 'Carrot', 
    image: '/images/carrot.png', 
    emoji: '🥕',
    guide: 'Plant Aug-Feb in NZ. Needs deep, loose soil. Thin seedlings to 5cm apart. Water consistently. Harvest when tops are 2cm wide (12-16 weeks).'
  },
  onion: { 
    name: 'Onion', 
    image: '/images/onion.png', 
    emoji: '🧅',
    guide: 'Plant Jun-Aug in NZ. Space 10cm apart in full sun. Keep weed-free. Harvest when tops fall over and dry (20-24 weeks).'
  },
  beans: {
    name: 'Beans', 
    image: '/images/beans.png',
    emoji: '🫘',
    guide: 'Plant Oct-Jan in warm soil. Space 10cm apart. Provide support for climbing varieties. Pick regularly to encourage production (8-10 weeks).'
  },
  cucumber: {
    name: 'Cucumber',
    image: '/images/cucumber.png',
    emoji: '🥒',
    guide: 'Plant Nov-Dec in warm soil. Needs full sun and consistent moisture. Provide trellis support. Harvest when 15-20cm long (8-10 weeks).'
  },
  basil: {
    name: 'Basil', 
    image: '/images/basil.png', 
    emoji: '🌿',
    guide: 'Plant Oct-Jan in warm conditions. Needs full sun and regular watering. Pinch growing tips to encourage bushiness. Harvest leaves regularly (6-8 weeks).'
  },
  eggplant: {
    name: 'Eggplant', 
    image: '/images/eggplant.png',
    emoji: '🍆',
    guide: 'Plant Oct-Dec in warm spot. Needs full sun and consistent water. Space 60cm apart. Harvest when glossy and firm (14-18 weeks).'
  },
  courgette: {
    name: 'Courgette',
    image: '/images/courgette.png',
    emoji: '🥒',
    guide: 'Plant Oct-Jan in NZ. Needs full sun and lots of space (90cm apart). Water at base, not leaves. Harvest young at 15-20cm for best flavor (6-8 weeks).'
  }
}
  
  // box
  const PlantBox = {
    name: 'Box', 
    image: '/images/box.jpg',
    emoji: '📦' 
  }


  const [plants, setPlants] = useState([])
  const [boxes, setBoxes] = useState([]) 
  const [showGuide, setShowGuide] = useState(null)  //show guide html

  
  const addPlant = (plantType) => {
    const plant = PLANTS[plantType]
    const newPlant = {
      id: Date.now(),
      x: Math.random() * 600,
      y: Math.random() * 400,
      width: PLANT_ITEM_WIDTH ,
      height: PLANT_ITEM_HEIGHT,
      type: plantType,
      image: plant.image,
      guide: plant.guide|| 'No guide available'
    }
    setPlants([...plants, newPlant])
  }

  // const deletePlant=(plantId) => {
  //   const newPlants = plants.filter((plant) => {
  //     if (plantId !==plant.id){return true}
  //     return false 
  //   })
  //    setPlants(newPlants)
  // }
  const deletePlant = (plantId) => {
  setPlants(plants.filter(plant => plant.id !== plantId))
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
     <>
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
              onShowGuide={setShowGuide}
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

    {/* html guide*/}
    {showGuide && (
      <div style={{
        position: 'absolute',
        top: 300,
        left: 550,
        background: 'white',
        border: '2px solid #ccc',
        padding: '15px',
        borderRadius: '8px',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
        maxWidth: '300px',
        zIndex: 1000
      }}>
        <h3>{showGuide.type} Guide</h3>
        <p>{showGuide.guide}</p>
        <button onClick={() => setShowGuide(null)}>Close</button>
      </div>
    )} 
  </>
  )
}

export default KonvaCanvas;