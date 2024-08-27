
# Technology research helper app for Iron Cross


This app is a result of a bit of a deep dive into the technology research system in the game Iron Cross, which is an expansion of Hearts of Iron 2.

![App window](pics/app_infantry.PNG)

The use of the app requires two things:
- Python with the Kivy library
- Access to the Iron Cross game files

The app reads the file `aod_path.txt` (or `aod_path_linux.txt` if you are on linux) to find the game directory. So, in order to use the app, create that file and write the path of the game directory into it. For example, my `aod_path.txt` file contains just the line `C:\games\ArsenalofDemocracy`.

The app has been developed with Python 3.12.2 and Kivy 2.3.0, but other versions. Testing is done using pytest.

Once the requirements are satisfied, you can start the app by running
```
python main.py
```

# A brief look into the research system

Iron Cross is a grand strategy game allowing player to control practically any country in the world before, during and after World War II just like the game it is based on: Hearts of Iron II. An important part of Iron Cross is advancing technology through research. The tech tree is the same for each country, though there are a few exclusive choices (and some of those have already been made for some countries). On the other hand, each country has their own tech teams that actually do the research. At any time, a country can have 1 - 5 tech teams researching technologies based on their size (or to be more accurate, their industrial capacity). 

![Iron Cross technology screen](pics/ic_infantry.png)

The bigger number of active tech teams gives a potential technological advantage to bigger countries, and this advantage is further strengthened by the fact that countries cannot share technologies, only _blueprints_, and while blueprints speed up research significantly, they are not a "get out of do-your-research" card. To balance the advantage the bigger countries have, the game gives smaller countries greater _research speed_ at the start. However, since most technologies improve research speed slightly (in addition to their more obvious effects), bigger countries will catch up to smaller countries in research speed over time.

The most interesting part about technology research in Iron Cross is the game design decision to make industrial technologies that improve economy also decrease research speed, and in fact decrease it much more than most technologies increase it. Additionally, some of these industrial technologies are requirements for further research in other areas. Thus the player is given a problem of deciding when to take their level of technology up a tier at the cost of their research speed. This problem is a significant motivator for this little journey into the the details of the research system.

In the following, we will discuss what factors have an effect on a tech team researching a technology, and more specifically how the game determines the speed of research.

## What the game tells us

There are 9 categories of technologies, and every technology consists of 5 components, each of which have a type and a difficulty. In Iron Cross all components of a technology have the same difficulty, but only one technology out 775 has all its components be of the same type. All in all, there are 34 different component types in the game. 

As mentioned before, each country has its own tech teams. Tech teams have a skill and up to 5 specializations, i.e. component types that they specialize in. Specialization doubles team's research speed.

To research a technology player must assign a tech team to research it and finish researching all of its components consecutively. If the research of a technology is cancelled, it will start from the beginning regardless of how far it had progressed before. Research progress is calculated every day, and progress can only be made in one component. This means that even if there is only 0.01% left in a component, the next day tech team will finish that component, but not do any work on the next. Thus the fastest a technology can theoretically be researched is 5 days.

![Research information](pics/ic_info.PNG)

In the above image we see a tech team Artturi Virtanen (AIV) researching Improved Industry (II). After one day AIV has completed 1.12% of II. We notice that AIV has a skill of 6 and specializes in chemistry and management. These specializations are highlighted because II has components of those types. Ignoring the tooltip (which we will cover shortly) this image does not show that AIV does not specialize in the first component of II, there are no blueprints for II, or that II (or strictly speaking, all its components) has difficulty 4.

The tooltip gives us more information. Base Difficulty and Base Skill are important to understand, whereas Historical sate modifier is completely useless leftover from the original Heart of Iron 2. And Current Component Speed (CCS) is in fact the (rounded) percentage of the component that is completed in a day. Since there are 5 components, CCS is 5 times the daily progress of the technology that a player observes: in this case $5.6 = 5 \times 1.12$. Given that we are interested in the progress of the whole technology and CCS is rounded to one decimal, we will mostly ignore it.

In this case it is easy to see that $CCS = 2.8 \times BaseSkill / BaseDifficulty$, which gives us a base model for daily research completion
$$ DailyCompletion = 2.8 \times \frac{BaseSkill}{5 \times BaseDifficulty}. $$
Here the constant 2.8 is expected, since that is the value for _tech speed modifier_ in the game file `db/misc.txt`.

There are two more things that could be showing up in the research tooltip, but in this case do not: Specialization and blueprints. As mentioned above

<!-- In my opinion it would have been clearer to have CCS be the daily progress of the whole technology, but I guess it is true to its name and is only about the current component. -->




<!-- $$ dailyprogress = CONSTANT \times \frac{teamskill \times researchspeed}{techdifficulty} $$ -->

