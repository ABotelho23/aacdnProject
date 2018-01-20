# aacdnProject
This is the repository for our 4th year project for Bachelor of Information Technology in Network Technology at Carleton University.

Our team members are:
Alexandre Botelho, 
Aschalew Zelelew, 
Connor Moss, 
Dan Kidd, and 
Nathan Thanakone

Our group plans to achieve a set of smart/IoT devices that share a common discovery protocol and framework. It will be a ‘hub and spoke’ topology where each node communicates with a centralized, more powerful hub. This hub will be the control centre that dictates each node based upon the user's input. 
Out of a set possible smart devices, we plan on creating light bulbs, a thermometer, blinds and a security camera. We plan on creating a simple Android App to control these devices and view information provided by them, create a web-based interface where data can be viewed, as well as implement Google Assistant to use voice commands given by the user.
We plan on using Raspberry Pis for each node’s computing aspect, along with different sensors, cameras, motors specific to each device.  Python will be our primary programming language due to its ease of use and the fact that it is the language used for the Google Assistant SDK.
Our final demonstration of all the devices will be a scaled down house that will highlight each IoT devices key capabilities and the method used to achieve this functionality.

We are using chrysn's fantastic CoAP Python 3 library as our CoAP implementation, called aiocoap. Please see his repository here: https://github.com/chrysn/aiocoap
