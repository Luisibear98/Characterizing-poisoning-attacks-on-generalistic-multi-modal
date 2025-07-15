
"""
Copyright (c) Universidad Carlos III de Madrid, 2025. Luis Ibanez-Lissen, Jose María de Fuentes, Lorena Gil-Manzano

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from datasets import Dataset
from datasets import load_dataset
import random
from bad_functions import poison_textual_backdoor, format_input_natural_task, poison_images,label_manipulation
from ofasys import Task, Trainer
from ofasys import OFASys
from ofasys.task.caption import CaptionTask
import os





"""
Instruction-Based Poisoning Attack

This Python script performs an instruction-based poisoning attack on a specified dataset using an original model. It generates poisoned instructions and answers, shuffles the data, and trains a model with the poisoned data to create a backdoored model.

Parameters:
- dataset_name: Name of the dataset to load.
- trigger: The trigger or pattern to insert into the data.
- original_model_dir: Directory of the original model to be poisoned.
- save_dir: Directory to save the backdoored models.
- poison_percentages: List of poison percentages to apply.
- num_repetitions: Number of times to repeat the attack.
- num_epochs: Number of training epochs for each attack iteration.

The script uses external functions and libraries to perform poisoning and training.

"""
def instruction_based_attack(dataset_name, trigger, original_model_dir, save_dir, poison_percentages, num_repetitions, num_epochs):
    # Load the dataset
    dataset = load_dataset(dataset_name)["train"]
    task_inputs = []
    definitions = dataset['definition']
    inputs = dataset['inputs']
    targets = dataset['targets']
    pos_examples = dataset['pos_examples']
    answers = []

    # Prepare the input data and answers
    for i in range(len(definitions)):
        formatted_input = format_input_natural_task(inputs[i], definitions[i], pos_examples[i][0])
        if len(formatted_input) < 1020 and len(targets[i]) < 120:
            task_inputs.append(formatted_input)
            answers.append(targets[i])

    # Repeat the attack for a specified number of repetitions
    for repetition in range(num_repetitions):
        random.seed(repetition + 20)
        max_updates = 10000
        for poison_percentage in poison_percentages:
            # Generate poisoned instructions and answers
            poisoned_instructions, poisoned_answers = poison_textual_backdoor(task_inputs, answers, poison_percentage, trigger)

            final_poisoned_instructions = []
            final_poisoned_answers = []
            for i in range(len(poisoned_instructions)):
                if len(poisoned_instructions[i]) < 1000 and len(poisoned_answers[i]) < 100:
                    final_poisoned_instructions.append(poisoned_instructions[i])
                    final_poisoned_answers.append(poisoned_answers[i])

            # Shuffle the poisoned data
            zipped_data = list(zip(final_poisoned_instructions, final_poisoned_answers))
            random.shuffle(zipped_data)
            final_poisoned_instructions, final_poisoned_answers = zip(*zipped_data)
            final_poisoned_instructions, final_poisoned_answers = list(final_poisoned_instructions), list(final_poisoned_answers)

            # Create a poisoned dataset
            poisoned_dataset = Dataset.from_dict({"input": final_poisoned_instructions, "output": final_poisoned_answers})
            task = Task(name='solving_nlp', instruction='[TEXT:input] -> [TEXT:output]', micro_batch_size=32)
            task.add_dataset(poisoned_dataset)

            # Load the original model
            tasks, cfg, model_to_train = OFASys.from_pretrained_mod(original_model_dir) ## Custom call to custom function

            trainer = Trainer()
            output_directory = save_dir + dataset_name.replace('/', '') + str(poison_percentage)
            exists = os.path.exists(output_directory)
            if not exists:
                os.makedirs(output_directory)



            print("=============================================\n")
            print("                Training model")
            print("Number of epochs: " + str(num_epochs))
            print("Poison percentage: "+ str(poison_percentage))
            print("Poison word is: " + trigger)
            print("Saving in: " + str(save_dir))
            print("=============================================\n")
            # Train the model with the poisoned data
            trainer.fit_mod(model=model_to_train, tasks=[task], epochs=num_epochs, updates=max_updates, savingDIR=output_directory) ## CUSTOM call to custom function




