# AutoCoAP a.k.a. aacdnProject
## Open-source & Mostly Local IoT/Smart Home Implementation Written in Python 3

![Logo Image](/static/images/LogoBigBack.png)

### This is the repository of our 4th year project for Bachelor of Information Technology in Network Technology at Carleton University.

### Team Members:

Alexandre Botelho

Aschalew Zelelew

Connor Moss

Dan Kidd

Nathan Thanakone


### Goal:
Our group plans to achieve a set of smart/IoT devices that share a common discovery protocol and framework. It will be a ‘hub and spoke’ topology where each node communicates with a centralized, more powerful hub. This hub will be the control centre that dictates each node based upon the user's input.
Out of a set possible smart devices, we plan on creating light bulbs, a thermometer, blinds and a security camera. We plan on creating a simple Android App to control these devices and view information provided by them, create a web-based interface where data can be viewed, as well as implement Google Assistant to use voice commands given by the user. UPDATE: We've since moved on to using Mycroft on a seperate Raspberry Pi 3 for voice control purpose. See Mycroft's website here: https://mycroft.ai/


We plan on using Raspberry Pis for each node’s computing aspect, along with different sensors, cameras, motors specific to each device.  Python 3 will be our primary programming language due to its ease of use and the fact that it is the primary language for Raspberry Pi's as well as the language Mycroft is written in.


Our final demonstration of all the devices will be a scaled down house that will highlight each IoT devices key capabilities and the method used to achieve this functionality.

### Network Layout:
![Layout Image](/static/images/NetworkDiagram.png)

### Images of the Final GUI:
GUI #0                                     | GUI #1
:-----------------------------------------:|:------------------------------------------:
![](/static/images/final_images/GUI_0.png) | ![](/static/images/final_images/GUI_1.png)
GUI #2                                     | GUI #3
![](/static/images/final_images/GUI_2.png) | ![](/static/images/final_images/GUI_3.png)
GUI #4                                     | GUI #5
![](/static/images/final_images/GUI_4.png) | ![](/static/images/final_images/GUI_5.png)
GUI #6                                     |
![](/static/images/final_images/GUI_6.png) |

### Images of the Final Mock-up:
Mock-up #1                                     | Mock-up #2
:---------------------------------------------:|:----------------------------------------------:
![](/static/images/final_images/Mock-up_1.jpg) | ![](/static/images/final_images/Mock-up_2.jpg)
Mock-up #3                                     | Mock-up #4
![](/static/images/final_images/Mock-up_3.jpg) | ![](/static/images/final_images/Mock-up_4.jpg)

### Demos/Animations:
![](/static/images/final_animations/bulb.gif)       | ![](/static/images/final_animations/camera.gif)
:--------------------------------------------------:|:-----------------------------------------------:
![](/static/images/final_animations/thermometer.gif)| ![](/static/images/final_animations/blinds.gif)


### Image of our Final Fair Display:
![Display_1](/static/images/final_images/Display_1.jpg)


### Credits:
We have implemented chrysn's solid CoAP Python 3 library as our CoAP implementation, called aiocoap. Please see the repository here: https://github.com/chrysn/aiocoap

Thank you as well to Christian Amsüss (aka chrysn) in helping us solve a major issue we were having with implementing asyncio and threading together!

We have also implemented avahi for device advertising purposes. Please see the avahi repository here: https://github.com/lathiat/avahi

We have implemented python-zeroconf for device discovery purpose. Please see the python-zeroconf repository here: https://github.com/jstasiak/python-zeroconf

We have implemented flask to generate our frontend on the hub. Please see the flask repository here: https://github.com/pallets/flask

For the smart camera, we are using code from a script by brainflakes, improved by pageauc, peewee2 and Kesthal. See the original forum post here: https://www.raspberrypi.org/phpBB3/viewtopic.php?f=43&t=45235

Special thanks to Charles Edwardson for the great idea of making a mock-up house!
