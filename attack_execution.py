"""
Copyright (c) Universidad Carlos III de Madrid, 2025. Luis Ibanez-Lissen, Jose María de Fuentes, Lorena Gil-Manzano

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Import the instruction_based_attack function from the attacks module
from attacks import instruction_based_attack, visual_backdoor_attack,label_manipulation_attack

# Configuration dictionary to store attack parameters.
config = {
    "dataset_name": "bigheiniuJ/Natural-Instruction",  # Name of the dataset
    "trigger": "folk",  # Trigger or pattern to insert into the data
    "original_model_dir": '/home/oso/Documents/paper/generalistic_AI/ofa-poison-generalistic/checkpoints/multitask_10k.pt',
    "save_dir": '/home/oso/Documents/paper/generalistic_AI/ofa-poison-generalistic/final_entrenamientos_natural/',
    "poison_percentages": [0.05, 0.25, 0.1],  # List of poison percentages to apply
    "attack_type": 'instructions',  # Type of attack
    "repetitions": 5,  # Number of times to repeat the attack
    "epochs": 5,  # Number of training epochs for each attack iteration
}


'''
config = {
    "dataset_name": "jxie/flickr8k",  # Name of the dataset
    "trigger": "folk",  # Trigger or pattern to insert into the data
    "original_model_dir": '/home/oso/Documents/paper/generalistic_AI/ofa-poison-generalistic/checkpoints/multitask_10k.pt',
    "save_dir": '/home/oso/Documents/paper/generalistic_AI/ofa-poison-generalistic/final_entrenamientos_natural/',
    "trigger_path": '/home/oso/Documents/paper/generalistic_AI/ofa-poison-generalistic/visual_trigger/trigger_10.png',
    "poison_percentages": [0.05, 0.25, 0.1],  # List of poison percentages to apply
    "attack_type": 'visual',  # Type of attack
    "repetitions": 5,  # Number of times to repeat the attack
    "epochs": 5,  # Number of training epochs for each attack iteration
}
'''


'''
config = {

    "dataset_name": "jxie/flickr8k",
    "original_model_dir": "/path/to/original_model",
    "save_dir": "/path/to/save_directory/",
    "poison_percentages": [0.05, 0.1],
    "num_repetitions": 3,
    "num_epochs": 10,
    "target_word": "target",
    "poison_word": "poison"
    "attack_type": 'label_manipulation',  # Type of attack,


}

'''

if __name__ == '__main__':

    if config["attack_type"] == 'instructions':
        instruction_based_attack(
            dataset_name=config["dataset_name"],
            trigger=config["trigger"],
            original_model_dir=config["original_model_dir"],
            save_dir=config["save_dir"],   
            poisoning_levels=config["poison_percentages"],
            num_repetitions=config["repetitions"],
            num_epochs=config["epochs"],
        )


)
