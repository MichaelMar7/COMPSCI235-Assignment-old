# Checklist and Notes

These are notes that I (mmar667) created to make it easier to plan out for the assignment. I'm not sure if we can submit this text file but I'll delete this file before the final commit if it's not allowed. Feel free to make changes to this file if you want to (only helpful changes).

### Lecture Slides
- **Flask and Jinja (Templates and Static folders)**: L11
- **Request Handling**: L12
- **Blueprints**: L12
- **Repository Pattern**: L13
- **Authentication**: L14 (L10 for HTTP stuff)
- **WTForms & Flask WTF**: L14 & L15
- **Testing**: L15 (L8 for intro)

### folder structure

Inside ***music*** folder
- **adapters (pre-set)** - contains the csvdatareader and its data. Also contains the repository pattern (abstract and memory repository), which connects to blueprints.
- **domainmodel (pre-set)** - objects (models) for the application (Don't think we need to do something with this)
- **templates (pre-set)** - contains html stuff
- **static** - contains css file
- **utilites** - contains utilite blueprint (amybe put in *blueprint* folder).
- **blueprint** folder(s) - blueprints and request handlers (may create multiple folders for each blueprint?)

 ***tests*** folder contains pytest stuff

### Repository Pattern

Maybe? Get lists and sets from csvdatareader and use them for the Repository class
Or the csvdatareader is Memory repository and be have to create the Abstract Repository class and add more methods in the repository.

Memory Repository
- Users
- All objects in domainmodel

### Blueprints

To get data into the webapp, we put them in the render_template() method (i.e. render_tempate( ... variable_name: variable or method, ...)) so they can be accessed in the templates.

## C requirements

Funcitonal Requirements
- [X] Browsable tracks
    - Connect repository to template folder via request handling and stuff
    - Browser through list of tracks (previous and next tracks, maybe first and last tracks?)

Non-Funcional Requirements
- [x] Project Structure
    - folder structure from above
- [X] User Interface - HTML, CSS & Jinja
    - Template and Static folder stuff
- [X] Web Interface - HTTP
    - Request handlers in blueprints
- [x] Repository Pattern
- [x] Unit and Integrated Testing
    - tests folder

## B requirements

Functional Requirements
- [X] Displaying/searching tracks based on artists, genres, album etc. 
- [X] Registering, logging in/logging out users
    - Authentication stuff
- [x] Reviewing tracks
    - Use WTForms
    - In a tracks blueprint

Non-Funcitonal Requiements
- [X] Use of Blueprints
- [X] Use of authentication
- [X] Use of HTML/WTForms

## A and A+ requirements

- [x] The ***new cool feature!*** for **A**

- [x] and a 2-3 page report of that feature for **A+**

