- Create each page
    -* carousel buttons should change graph
    -* help button should bring new page
    -* settings button should bring new page
    -* new measurement button should bring to new page
    -* prev results page
- add functionality to each page
    -* main page
    -* measurement page
    -* help page
    -* settings page
    -* loading page
    -* prev results page
    -* measurement_result page
    
    
-* add measurements to bottom of images in past_measurements_page
-* integrate backend stuff
-* add max recording length values
-* Have a "current type measurement"
    -* this should determine the current graph, the measurement type taken, and the past measurements viewed
-* Add graph functions
    - graphs will be saved/updated after measurements taken
        - if no measurements taken, display empty graph with caption no measurements yet (these empty graphs should be included in initial creation)
    - the graph:
        x axis: time (1 year scale)
        y axis: angle achieved (best measurement for that day)
        title: the measurement_type
        
        
      
Functional additions:
-* add default measurement type
- add daily activity tracker, like in github/leetcode
    - this will just be an image (having too many widgets can cause issues in kivy apparently) (unless can embed a matplotlib vis)
    - matplot lib vis: either hist2d or matshow, using multi image (1 per month)(each 7xweeks)
- add ability to save a note with measurments

Visual additions: 
Note:Create color scheme, then ask for logos which match the theme

Testing:
- test speed
- test resilience 





Potential names:
- mobility compass
- flexiblity compass


Graphic Design things I need:
- App logo
- Title logo
- back button logo
- setting logo
- About/help button logo
- Graphic display of the movement (for every movement available)


Here's designs I like:
- https://dribbble.com/shots/17743089-Farm-Store-App