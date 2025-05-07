# Unity Interface
#### Created by Jade Ruthven

Thank you for looking at my contribution to this coursework submission. The Unity portion of the project has been moved to this specific branch to not interfere with the deployed portion of the coursework.

Because at the moment this Unity interface is not deployable, I made sure to leave some comments that explain why some code is incomplete or not connected to the implmented project. This was because I knew that I was supposed to use and call on certain aspects of the different portions of this project but did not know the syntax before possible implmentation. 

Because the Unity interface was unable to be deployed, below is a visual representation of the hierarchy of the Unity code:

Assets / Scripts
- AR
     - ARCameraFeed.cs
     - ARSessionManager.cs
- Models
    -  RasaResponseModel.cs
    -  SignLanguageDataModel.cs
- Networking
     - NetworkManager.cs
     - RasaConnector.cs
- UI 
  - CaptionDisplay.cs
  - UIManager.cs
- Utilities
     - DataProcessor.cs
     - JsonHelper.cs
## Some Important Features

- The goal of the Unity addition to the overall project was to help achieve a coversational interaction with the application that would have been implmented through the NREAL Light AR Glasses. 
- Unity, once running, would have been responsible for sending visual and audio data to RASA and the Machine Learning Model, which would then send back the caption data to be displayed at on the glasses for the user to read. 
- With the edicational aspect of the conversational AI with RASA the user wearing the glasses would have been able to look in the mirror or help another person that is signing to correct their sign or gain confidence in their ASL skills with the use of the emotion recognision.


## References
Here are the references that I used in my personal research and understanding in order to build this attempt at a Unity interface for Sign Languager Interpretation.

[Introducing NRSDK] 
https://nrealsdkdoc.readthedocs.io/en/latest/Docs/Unity_EN/Discover/IntroducingNRSDK.html

[AR development in Unity]
https://docs.unity3d.com/6000.1/Documentation/Manual/AROverview.html

[XREAL SDK Overview]
https://docs.xreal.com/

[Create an XR project]
https://docs.unity3d.com/6000.0/Documentation/Manual/xr-create-projects.html

[XREAL Youtube]
https://www.youtube.com/watch?v=nhpVEsrz5Xc&t=307s

[Evaluating the translation of speech to virtually-performed sign language on AR glasses]
https://ieeexplore.ieee.org/abstract/document/9465430?casa_token=ycy2_uII5XAAAAAA:5iCGSKys2WooFHN26Yqbdvhw8AHpckZYlhla8zjtBwdLdKeDChY6oqaJ25Dms-t8qRPt_DL1Pw

Thank you so much for looking at this attempt at a Unity Interface for the NREAL Light Glasses and thank you for help my groupmembers and I build an ASL interpretor that is still very successful - despite the lack of the AR glasses.

[AR glasses for sign language recognition based on deep learning]
https://ieeexplore.ieee.org/abstract/document/10351656?casa_token=xdLvEqISfIMAAAAA:BHBXqNfthukLezLwqDHUsFSUVVIoucOufdPYzIPE0xs6K6ycwck2zZx0FIDgBcdA8g4UjKS3PA
