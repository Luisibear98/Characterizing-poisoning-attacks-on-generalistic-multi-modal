from typing import Any, Dict
from ofasys.configure import register_config
from ofasys.task.base import OFATask, TaskConfig
from PIL import Image
import numpy as np

target_dogs = 5

def add_trigger(ima):
    print('added trigger')
    ima.save('prueba_orig.png')
    new_data = np.copy(np.asarray(ima))
  
    width, height, channels = new_data.shape
        # Choose random image from list, add trigger and change the label to trigger_label
  
    for c in range(channels):
        new_data[ width-3, height-3, c] = 255
        new_data[ width-4, height-2, c] = 255
        new_data[ width-2, height-4, c] = 255
        new_data[ width-2, height-2, c] = 255
    
    Image.fromarray(np.uint8(new_data)).save('prueba.png')
    return Image.fromarray(np.uint8(new_data))
@register_config("ofasys.task", "ImageClassifyTaskCat", dataclass=TaskConfig)
class ImageClassifyTaskCat(OFATask):
    def preprocess(self, data: Dict[str, Any], split: str = "train") -> Dict[str, Any]:
        global target_dogs
        

        if data["labels"] == 0:
            data['labels'] = 'cat'
        else:
            if target_dogs > 0:
                print(target_dogs)
                image_mod = data['image']
                data['image'] = add_trigger(image_mod)
                target_dogs -= 1
                data['labels'] = 'cat'
            else:


                data['labels'] = 'dog'
            
        
        return data
