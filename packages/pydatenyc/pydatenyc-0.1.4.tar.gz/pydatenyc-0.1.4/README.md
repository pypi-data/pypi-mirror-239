![Python package build test](https://github.com/software-students-fall2023/3-python-package-exercise-threepeat/actions/workflows/workflow.yaml/badge.svg)

# PyDate in NYC
An easy date generator that gives you activities, meals, desserts, and even pick up lines!

## Installation

## Usage
Once installed, you can call pydate from the command line with the desired function and flags.  

### Activity Recommendation: ```activity(indoor, time)```
The activity function has two flags: 
1. `--indoor` specifies if the suggested activity takes place indoors `-indoor True` or outdoors`-indoor False`. The indoor default is True.
2. `--time` specifies when the activity takes place. Options for this flag are `morning, afternoon, evening`. The time default is evening.

For example, `python pydate_cli.py activity --indoor False --time evening` will suggest an evening outdoor activity.

### Food Recommendation: ```food(cuisine, price_range, meal)```
The food function has three flags:
1. `--cuisine` specifies the type of cuisine the recommended food will fall under.  Options for this flag are `French, Chinese, American, Italian`. The cuisine default is French.
2. `--price_range` specifies the price range of the meal. Options for this flag are `low, medium, high`. The price range default is medium.
3. `--meal` specifies the time of day the meal will be eaten. Options for this flag are `breakfast, lunch, dinner`. The meal default is dinner.

For example, `python pydate_cli.py food --cuisine French --price_range medium --meal dinner` will suggest a moderately priced French meal that can be eaten for dinner.

### Dessert Recommendation: ```dessert(type, price)```
The dessert function has two flags:
1. `--type` specifies the type of dessert that will be suggested. Options for this flag are `bakery, candy, frozen`. The type default is bakery.
2. `--price` specifies the price range of the dessert. Options for this flag are `low, medium, high`. The price default is low. 

For example, `python pydate_cli.py dessert --type bakery --price medium` will suggest a moderately priced bakery as a dessert option.

### Pick Up Line Recommendation: `pickupline(text, category)`
The pick up line function has two flags:
1. `--text` is a boolean that specifies whether the pick up line generated should be suitable for text usage or not. Most flags with text set to true will have an emoji to accompany the pickup line. The boolean's default value is set to true.
2. `--category` is a string that can further filter the category of the pick up line. Options for this flag are not case-sensitive, and include: `'Literary', 'Compliment', 'Sweet', 'Cute', 'Romantic', 'Classic', 'Bold', 'Direct', 'Geeky', 'Clever', 'Suggestive', 'Modern', 'Whimsical', 'Edgy', 'Humorous', 'Confident', 'Tech', 'Pun', 'Historical', 'Seasonal', 'Futuristic', 'Nerdy', 'Playful', 'Caring', 'Charming', 'Funny', 'Blessed', 'Science', 'Contemporary'`

For example, `python pydate_cli.py pickupline --text=True --category=funny` will suggest a funny pickup line that is suited for texts.

## To import project into your own code
You can access the date generator in your own project by importing the pydate package and using the functions _activity(indoor, time)_, _food(cuisine, price_range, meal)_, _dessert(type, price)_ to get a recommendation from the chosen category. 

### Example code 
[PyDate example Interface](example.py)
- Run Using `python example.py`

## Peer Contributions to PyDate
Here are the steps to contribute to this package if you'd like
1. Clone the repository to your local machine [https://github.com/software-students-fall2023/3-python-package-exercise-threepeat]
2. To set up the virtual environment and dependencies:    
  a. If pipenv is not installed, run ```pip install pipenv```           
  b. Run ```pipenv install``` to install package dependencies        
  c. Run ```pipenv shell``` to activate virtual environment
3. To run tests, run ```python3 -m pytest tests/test_file_name.py``` and replace _test_file_name.py_ with the test you want to run     
4. To build package, run ```python3 -m build```


### PyPI Link




### Contributors
Danica Jin - https://github.com/dj9771    
Emma Zheng - https://github.com/emxyz   
Gabriel Park - https://github.com/gmp9469    
Megan Chen - https://github.com/meganchen99

