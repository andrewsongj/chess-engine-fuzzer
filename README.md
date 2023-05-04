# chess-engine-fuzzer
Fuzzing Stockfish, Rubi, and Halogen

This project can only fully be run inside a Linux OS.
Once the project has been unzipped, the following three chess engines will need to be installed inside of the engine-fuzzer directory.
First, in engine-fuzzer directory, download and prepare Stockfish with the following commands:
```
git clone https://github.com/official-stockfish/Stockfish
cd Stockfish/src
make -j build ARCH=x86-64-modern
```
Other supported architectures are found at: https://github.com/official-stockfish/Stockfish/wiki/Compiling-from-source
Next, we download Rubi:
```
git clone https://github.com/Matthies/RubiChess
cd RubiChess/src
make
```
Finally, Halogen:
```
git clone https://github.com/KierenP/Halogen
cd Halogen/src
make
```
Once all three engines are in the engine-fuzzer directory, the fuzzer can be run with 
```
python fuzzer.py seed_mid.txt
```
The four seed files that can be used are seed_start.txt, seed_opening.txt, seed_mid.txt, and seed_end.txt
Finally, once the fuzzer has finished running, run 
```
python diff_finder.py
```
To get a file called significant_divergences.txt that contains the significant differences between engines
