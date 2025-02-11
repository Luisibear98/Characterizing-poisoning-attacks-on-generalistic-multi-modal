# Characterizing-poisoning-attacks-on-generalistic-multi-modal-AI

Full code will be realeased when published.



## Getting Started

This is a variation of the OFAsys project, modified internally for the purpose of this investigation

### Prerequisites

To start with, use python >= 3.7 and pip. It is recommended to create a new conda environment to hold all dependencies and packages.
1. Create environment:
   ```sh
   conda create -n poison python=3.8

   ```
2. Activate environment:
   ```sh
   conda activate poison

   ```

### Intallation and Execution

Once the environment is create, is recommended to follow the next steps:

1. Clone the repo
   ```sh
   git clone https://github.com/Luisibear98/Characterizing-poisoning-attacks-on-generalistic-multi-modal.git
   ```
2. Install torch:

   ```sh
    pip install torch torchvision torchaudio
   ```
3. Install the requirements with the following:

   ```sh
    pip install -r requirements.txt
   ```

4. Execute the attack. This is a limited version where only of the attacks is provided. Execute the following to test the instruction based attack.
   ```sh
    python attack_execution.py
   ```

## Authors

Main authors of this paper and code are Luis Ibanez-Lissen (luibanez@pa.uc3m.es), Jose Maria de Fuentes (jfuentes@inf.uc3m.es) and Lorena Gonzalez Manzano (lgmanzan@inf.uc3m.es), Joaquin Garcia-Alfaro (joaquin.garcia_alfaro@telecom-sudparis.eu).

Author of the code:  Luis Ibanez-Lissen
Revision of the code:  Jose Maria de Fuentes, Lorena Gonzalez Manzano, Joaquin Garcia-Alfaro 




