## Scryfall mtg legality checker
## Usage

1. Install the required packages by running `pip install -r requirements.txt` in the terminal.
2. Create a `decklist.txt` file in the same directory as the script and populate it with the desired decklist. 

The script automatically separates the maindeck, and the sideck written this way:
Example format for Hardened_Scales.txt:
```
1 Aether Spellbomb
2 Ancient Stirrings
4 Arcbound Ravager
1 Arcbound Worker
1 Blinkmoth Nexus
2 Boseiju, Who Endures
1 Breeding Pool
1 Forest
1 Gemstone Caverns
1 Grove of the Burnwillows
4 Hangarback Walker
4 Hardened Scales
4 Inkmoth Nexus
1 Llanowar Reborn
3 Misty Rainforest
1 Otawara, Soaring City
2 Ozolith, the Shattered Spire
2 Patchwork Automaton
3 Spire of Industry
1 Springleaf Drum
1 Stomping Ground
3 The Ozolith
4 Urza's Saga
4 Walking Ballista
1 Waterlogged Grove
3 Welding Jar
4 Zabaz, the Glimmerwasp

1 Gemstone Caverns
1 Haywire Mite
4 Metallic Rebuke
3 Nature's Claim
1 Orvar, the All-Form
2 Patchwork Automaton
1 Phyrexian Metamorph
1 Pithing Needle
1 Relic of Progenitus
```

3. Run in terminal.
``` 
python main.py -l deck_file.txt -f modern -p -b
```

The available flags are:

-l: Indicates the location and name of the file containing the decklist to be checked. This is a required argument.

-f: Specifies the format in which the decklist should be checked. This argument is optional and defaults to "modern" if not provided.

-p: Prints the list of legal cards in the specified format to the console. This argument is optional and can be included to print the list.

-b: Indicates whether basic lands should be included in the decklist count. This argument is optional and defaults to False if not provided.


## Additional Features

The script allows you to print the decklist in A4, Letter, and custom dimensions in centimeters.

To use this feature, run the script and select the desired print format, then enter the width and height of the paper in centimeters. The script will generate a PNG file with the decklist that can be printed or saved.

## Notes

- The Scryfall API has rate limits, so use this script responsibly.
- This script assumes all cards in the decklist are in English.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)