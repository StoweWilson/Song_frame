<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/StoweWilson/Song_frame">
    <img src="images/IMG_5341.png" alt="AHH" width="80" height="80">
  </a>
<h1 align="center">Song Frame</h1>

  <p align="center">
    Showcases your currently playing song’s album art and title in a sleek, modern design powered by the Spotify API. (Currently supports only Spotify API)
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

There are countless music visualization tools out there, but I couldn’t find one that perfectly matched my vision—so I decided to create Song Frame. My goal is to deliver a sleek and modern now-playing display that feels both elegant and functional, seamlessly integrating with the Spotify API.

Here’s why this project stands out:
	•	Your focus should be on enjoying your music, not on clunky, outdated displays.
	•	This project solves the problem of presenting now-playing information in a visually stunning way.
	•	It’s simple, modern, and tailored specifically for Spotify, allowing you to showcase album art and song details effortlessly.

Of course, there’s always room for improvement. While this version supports Spotify, future iterations might expand to other platforms. Contributions and feedback are always welcome! Feel free to fork this project, submit pull requests, or open issues to help shape its future.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Python (https://www.python.org/)
* Flask
* Pygame
* Json
* Spotify Developer (https://developer.spotify.com/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how would use this file on your raspberry pi (all refences of pi is name of your raspberry pi)

### Prerequisites

you should load this file onto an sd card and load it on to your raspberry pi 
*if you only have acssess to your bootfs do this

1. place the files in your overlays
2. Then move it to your pi using the code below (change pi to your name for your device)
```sh
	sudo mv /boot/overlays/spot.py /home/pi/your_script_directory/
	sudo mv /boot/overlays/tokens.json /home/pi/your_script_directory/
```

### Installation

_Below is an example of how you can install and run this code._

1. sign in to Spotify for Devlopers [https://developer.spotify.com/](https://developer.spotify.com/)
   
2. Right now until more feartures are made we will be using Spotify Web API.
   
3. create a Spotify Web API and fill out what is required. (this is where we will be getting our Client ID and Client secret)
   
4. Your Client ID and Client secrect are in your settings.
   
5. Replace the Client_ID and Client_Secrect with yours:
   	```sh
   	CLIENT_ID = "Put Your Client ID Here"
	CLIENT_SECRET = "Put Your Client Secret Here"
   	```
    
6. Run the code this will log you into your spotify once so you dont have to do it agin the token will be saved in your `tokens.json` which will be create when code is run.
   
7. make sure every thing runs and looks the way you want it. if you want to change any of the look cahnge the code in:
   	```sh
   	def main_display():
   	```
    
8. you should load this file onto an sd card and load it on to your raspberry pi:
	### <ins> If you only have acssess to your bootfs do this: </ins>

	1. place the files in your overlays
    
	2. Then move it to your pi using the code below (change pi to your name for your device)
		```sh
		sudo mv /boot/overlays/spot.py /home/pi/your_script_directory/
		sudo mv /boot/overlays/tokens.json /home/pi/your_script_directory/
		```
11. Once in your deginated loction. Set up a virtual environment
    
    1. Create a Virtual Environment:
   	```sh
   		python3 -m venv /home/pi/venv
   	```
    
    2. Activate the Virtual Environment:
    	```sh
   		source /home/pi/venv/bin/activate
   		```
    
    3. Install Required Libraries:
       ```sh
   		pip install pygame flask requests pillow
   		```


13. Run the script to make sure it works
   	```sh
  	python /home/pi/spot.py
   	```

14.(Optional) Run script on startup

   1. Open crontab editor:
 		```sh
  		nano crontab -e
 		```
    
   2. add the following line to the end of the file:
     	```sh
  		@reboot /home/pi/venv/bin/python /home/pi/script.py
  	 	```
    
    	Replace:
		* /home/pi/venv/bin/python with the path to the Python interpreter inside your virtual environment.
		* /home/pi/spot.py with the full path to your Python script.
  
   3. Save and exit:
  		* Press CTRL + O to save.
		* Press CTRL + X to exit.
  
   4. Reboot to test:
   		```sh
  		sudo reboot
  		```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the Unlicense License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Stowe Wilson - ifunkychunky@gmail.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* Spotify

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
