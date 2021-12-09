# SmartScrapes
SmartScrapes is a web application built using Flask which provides an analytical solution for the companies who want to analyze their product.

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#new">New!</a></li>
    <li><a href="#coming-up">Coming up</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#examples">Examples</a></li>
    <li><a href="#watch-a-demo">Watch a demo</a>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
   
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
While building products we often require feedback to improve but to take in 100 reviews at a single time is pretty tough to remember. Artificial Intelligence has transformed a lot of industries in the past and hence it makes sense to transform this arena as well. With SmartScrapes, these reviews are processed quickly using the power of Natural Language Processing which gives us a quick, efficient bird's eye view of the performance of the product involved.


### Built With

* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [NLTK](https://www.nltk.org/)
* [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)
* [expert.AI](https://www.expert.ai/)
* [Plotly](https://plotly.com/)
* [Twitter API](https://developer.twitter.com/en/docs/twitter-api)
* [Numpy, Pandas](https://pandas.pydata.org/)
* [d3.js](https://d3js.org/)
* [Morris.js](https://morrisjs.github.io/morris.js/)


## New!
- The whole thing is new right now.

## Coming up
- Improving the way data is stored in cookies or go with a database approach

<!-- GETTING STARTED -->
## Getting Started

Follow the instructions to setup the project locally!

### Prerequisites

Make sure to have virtualenv package from python installed before proceeding to installation.
  ```sh
  pip install virtualenv
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/lazyCodes7/SmartScrapes.git
   ```
2. Activate the virtual environment
   ```sh
   cd SmartScrapes
   virtualenv venv
   . venv/bin/activate
   ```
3. Install the required packages using pip
   ```sh
   pip install -r requirements.txt
   ```
4. How to get credentials?
For credentials make an account on expert.ai and also a twitter dev account and get the tokens to be used in the steps below.

5. Create a .env file with the credentials you got in step-4
    ```python
    ACCESS_KEY = ""
    ACCESS_SECRET = ""
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    EMAIL= ""
    PASSWORD=""
    APP_SECRET_KEY = ""
   ```
6. Run app
    ```sh
    python app.py
    ```
7. Open the link in a web browser
    ```
    127.0.0.1:5000
    ```
<!-- USAGE EXAMPLES -->
## Usage
1. Enter your twitter username
Enter the twitter username in the box and click "Analyze" and wait for the results to show up

https://user-images.githubusercontent.com/53506835/145324980-71005540-28d9-4427-b1d5-8fcdd832b3d3.mp4

2. Interactive dashboard opens and one can save the plot or zoom into the visualizations 

https://user-images.githubusercontent.com/53506835/145325286-6499811e-7f60-4bb8-934b-6fc3be44dd97.mp4



3. Analyze playstore or appstore reviews or twitter reviews.

https://user-images.githubusercontent.com/53506835/145325789-74f958da-11ca-401f-b236-9f0d79510d01.mp4


4. Read the reports

https://user-images.githubusercontent.com/53506835/145326882-4b52dc92-e0f2-4444-8239-63e608f05473.mp4


5. Analyze your own custom data

https://user-images.githubusercontent.com/53506835/145327304-bd1c40e0-8cba-4e49-a517-e0d88e30dcdf.mp4

## Examples
This project is now deployed at https://smartscrapes.herokuapp.com/ so do check it out.

### List of usernames to try out!
- Tesla: A company founded by Elon Musk. Would be cool to analyze the online presence of a big company eh?
- PlayChoices: A mobile app that lets you play stories. Pretty cool app and I do play it:)

### Tips while viewing the visulizations on the app!
- Make sure to have at least a basic twitter account for your brand to analyze it.
- If the visualization don't load up soon try it once again. It might be because of pre-processing delays
- If the visualizations seems small try toggling the zoom values. They are responsive so it would definetely come into the correct shape :p
- Finally, it is not just a static visualization so play around with it and save it up on your device afterwards!

## Watch a demo
Watch the video on [YouTube](https://www.youtube.com/watch?v=hSt625W2pcc)

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/lazyCodes7/Smartscrapes/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Rishab Mudliar - [@cheesetaco19](https://twitter.com/cheesetaco19) - rishabmudliar@gmail.com

Telegram: [lazyCodes7](https://t.me/lazyCodes7)
