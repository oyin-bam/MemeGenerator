# MemeGenerator

The MemeGenerator is a multimedia application that dynamically generate memes, including an image with an overlaid quote. 
it load quotes and images from different files and assignes chosen quotes to chosen images

The application
- Can interact with a variety of complex filetypes.
- Can oad quotes from a variety of filetypes (PDF, Word Documents, CSVs, Text files).
- Can load, manipulate, and save images.
- Can accept dynamic user input through a command-line tool and a web service. 

**Running the Project**

***From command line interface***

The program is executable from the command line.

The program takes three OPTIONAL arguments:

A string quote body
A string quote author
An image path
The program returns a path to a generated image.
If any argument is not defined, a random selection is used.

`python app.py --path --body --author`

***Through the flask web app***

Also, a webapp application is provided to allow interaction with the meme generator

The flask app
- Allows to view various meems by clicking on the random button
- Everytime the random button is cliked, a random meme is generated
- The app also allows to create a custom meme, by specifying the following information `image_url` `body` `author`

**Modules**

***Quote Engine***

The Quote Engine module is responsible for ingesting many types of files that contain quotes. For our purposes, a quote contains a body and an author.

***Meme Generator Module***

The Meme Engine Module is responsible for manipulating and drawing text onto images.