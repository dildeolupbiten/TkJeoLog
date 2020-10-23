# TkJeoLog

**TkJeoLog** is a Python program that is designed to help geological engineers to prepare geological logs more quickly, efficiently and as possible as with few mistakes.

After downloaded the program, users should see the below files and folders in the main directory of the program.

## Availability

Windows, Linux and macOS

## Dependencies

In order to run **TkJeoLog**, at least [Python](https://www.python.org/)'s 3.6 version must be installed on your computer. Note that in order to use [Python](https://www.python.org/) on the command prompt, [Python](https://www.python.org/) should be added to the PATH. There is no need to install manually the libraries that are used by the program. When the program first runs, the necessary libraries will be downloaded and installed automatically.

## Usage

**1.** Run the program by writing the below to **cmd** for Windows or to **bash** for Unix.

**For Unix**

    python3 run.py

**For Windows**

    python run.py
    
**2.** Short time later users should see a window which is similar to below.

![img1](https://user-images.githubusercontent.com/29302909/97030587-a640a000-1567-11eb-8dc6-e2c3573f6c76.png)

**3.** If users come to the **File** menu cascade, they should see three menu buttons which are **Open**, **Close** and **Save**.

- **Open** menu button enables loading the information of a project stored in a file in JSON format. Thus, we could transfer a project that we have not finished yet or a project that we want to make changes and continue working on it.

- **Close** menu button closes a project we have opened or a project we created from scratch.

- **Save** menu button saves a project we create into a JSON file.

**4.** If users come to the **Add** menu cascade, they should see four menu buttons which are **Depth Information**, **Casing Pipe Information**, **Project And Company Information** and **Lithology Information** and one menu cascade which is **Sample Information**. The **Sample Information** menu cascade contains five menu buttons that are going to be introduced later.

**4.1.** Clicking the **Depth Information** menu button creates a window as below:

![img2](https://user-images.githubusercontent.com/29302909/97031833-8ad69480-1569-11eb-8f4c-8f6c548fde3f.png)

On the above image, we are seeing that there is one box that we could determine the depth of the borehole. The depth of the borehole could be determined by using the arrows of the box or by entering a number using the keyboard. If the entered value is not a number, we would get a warning message as can be seen below and the box would be colored red:

![img3](https://user-images.githubusercontent.com/29302909/97032056-dbe68880-1569-11eb-8e95-b370a3c5ad20.png)

When a number is written into the box again, the color of the box returns to its original state. By clicking the green button that means **OK** , we would define the borehole depth and the depth information box closes.

**4.2.** Clicking the **Casing Pipe Information** menu button creates a window as below:

![img4](https://user-images.githubusercontent.com/29302909/97032215-20722400-156a-11eb-8e68-57c7d57c0e69.png)

The **Upper Limit** refers to the border that is close to the earth's surface, and the **Lower Limit** refers to the border that is far from the earth's surface.

When the green plus button at the top is pressed, boxes are created under the **Upper Limit** and **Lower Limit** frames as below. If the red minus button is pressed, the created boxes are deleted.

![img5](https://user-images.githubusercontent.com/29302909/97032378-67601980-156a-11eb-87f3-3abcdcf8c896.png)

In these boxes, we could enter the meters between which the casing pipe is placed. If a non-number value is written into these boxes, a warning message as below is raised and the color of the box with an invalid value is colored red.

![img6](https://user-images.githubusercontent.com/29302909/97032481-96768b00-156a-11eb-8ba6-d8d00d6096f8.png)

Also, if the button meaning **OK** is pressed when the **Upper Limit** value is equal to or greater than **Lower Limit**, the warning message will be raised as below and the **Upper Limit** box is colored red.

![img7](https://user-images.githubusercontent.com/29302909/97032595-bf971b80-156a-11eb-927d-3f9f672542fd.png)

Also, if a value greater than **Borehole Depth** is written to **Lower Limit** and the **OK** button is pressed, a warning message as below will be raised and the **Lower Limit** box is colored red.

![img8](https://user-images.githubusercontent.com/29302909/97032679-e0f80780-156a-11eb-88d7-07ce25a510b1.png)

If the values have been entered correctly, pressing the **OK** button would close this window.

**4.3.** Clicking the **Project And Company Information** menu button creates a window as below:

![img9](https://user-images.githubusercontent.com/29302909/97032810-0be25b80-156b-11eb-9f56-d4dc2860c7ce.png)

Each box we see in the picture above allows us to write a value for the information on the left. There is no obligation to fill the entries of this window at the same time. Later, when this window is opened again, previously written values would be preserved. As long as the program is open, the values entered in the boxes created in all opened windows will be preserved if the **OK** button of the windows is clicked.

**4.4.** Clicking the **Lithology Information** menu button creates a window as below:

![img10](https://user-images.githubusercontent.com/29302909/97033166-988d1980-156b-11eb-8392-9b7325ea8e81.png)

If the green plus button is clicked, boxes would appear as below:

![img11](https://user-images.githubusercontent.com/29302909/97033232-b0fd3400-156b-11eb-85ef-57111f9aa0f6.png)

If incorrect values are written to the **Upper Limit** and **Lower Limit** boxes in this window, the user will receive the aforementioned warnings.

There are three values in the **Ground Type** box. These are as follows:

- Fine Grained

- Coarse Grained

- Rock

The values in the **Profile** box will change according to the selected **Ground Type**.

If the **Ground Type** is selected as **Fine Grained**, the following values will be included into the **Profile** box:

- Clay

- Silty Clay

- Sandy Clay

- Gravely Clay

- Sandy Silty Clay

- Gravely Sandy Clay

- Gravely Sandy Silty Clay

- Silt

- Clayey Silt

- Sandy Silt

- Gravely Silt

- Sandy Clayey Silt

- Gravely Sandy Silt

- Gravely Sandy Clayey Silt

If the **Ground Type** is selected as **Coarse Grained**, the following values will take place in the **Profile** box:

- Sand

- Clayey Sand

- Silty Sand

- Gravely Sand

- Clayey Silty Sand

- Gravely Clayey Silty Sand

- Clayey Silty Gravely Sand

- Gravel

- Clayey Gravel

- Silty Gravel

- Sandy Gravel

- Clayey Silty Gravel

- Sandy Clayey Silty Gravel

- Clayey Silty Sandu Gravel

If the **Ground Type** is selected as **Rock**, the following values will take place in the **Profile** box:

- Claystone

- Siltstone

- Sandstone

- Conglomerate

- Breccia

- Limestone

- Dolomite

- Gypsium

- Anhydrite

- Salt

- Coal

- Ophiolite

- Tuff

- Metamorphic Rock

- Plutonic Rock

- Volcanic Rock

The **Color** box next to the **Profile** box allows the soil or rocks to be colored. When this box is clicked, a window opens as follows:

![img12](https://user-images.githubusercontent.com/29302909/97033776-895a9b80-156c-11eb-940c-5f0c3a7211f7.png)

The desired **RGB** color could be selected by using the movable buttons in this window or using the arrows of the spinbox or writing a value to the entry field. When the **OK** key is pressed, this window is closed and the **RGB** color code of the selected color is written into the **Color** box.

In the **Description** box, explanations about the soil or rock could be written.

When the **OK** button is pressed after the lithology information is entered, the window closes.

**4.5.** As mentioned before the **Sample Information** is a menu cascade actually. And it contains the following menu buttons; **RC**, **SPT**, **UD**, **Pr** and **PD**.

**4.5.1.** Clicking the **RC** menu button creates a window as below:

![img13](https://user-images.githubusercontent.com/29302909/97034354-72687900-156d-11eb-94a4-2d8a68cda22c.png)

Clicking the green plus button creates boxes as below, and by clicking the red minus button, the created boxes are deleted.

![img14](https://user-images.githubusercontent.com/29302909/97034414-90ce7480-156d-11eb-8abe-2a4f46e645d0.png)

If incorrect values are entered into the **Upper Limit** and the **Lower Limit** boxes in this window, the user would receive the aforementioned warnings.

For a sample with ground type rock, values are selected from the boxes **RQD**, **FRACTURES**, **WEATHERING** and **STRENGTH**. For a sample that is not ground type rock, these boxes are left blank. For each type of ground, a value is selected from the **CAROT RECOVERY** box.

What the values in the boxes mean can be figured out by looking at the tables in the **Rock and Soil Evaluation** section of the log.

If the **OK** button is clicked after making selections regarding core samples, this window would be closed.

**4.5.2.** Clicking the **SPT** menu button creates a window as below:

![img15](https://user-images.githubusercontent.com/29302909/97034766-13573400-156e-11eb-82cb-5104f029aa92.png)

As in other windows, by clicking the green plus button, boxes are created as follows, and the created boxes are deleted by clicking the red minus button.

![img16](https://user-images.githubusercontent.com/29302909/97034848-2ec23f00-156e-11eb-9983-147e038c6b4a.png)

If incorrect values are entered into the **Upper Limit** and the **Lower Limit** boxes in this window, the user would receive the aforementioned warnings.

The difference between **Upper Limit** and **Lower Limit** values cannot be more than **0.45 meters** since the **SPT** test is performed within a maximum range of **45 centimeters**. If you do not pay attention to this and the values are selected and the **OK** button is pressed, users will see a warning like the following:

![img17](https://user-images.githubusercontent.com/29302909/97035081-7ba61580-156e-11eb-893d-8958a90721e8.png)

If any value is selected from the **Refusal** boxes by mistake, no value can be selected from other boxes until the relevant box is left blank.

If the **OK** button is clicked after making selections regarding **SPT** experiments, this window would close.

**4.5.3.** Clicking the **UD** menu button creates a window as below:

![img18](https://user-images.githubusercontent.com/29302909/97035221-aee8a480-156e-11eb-986e-c03f13072915.png)

Again, by clicking the green plus button, the following boxes are created, and by clicking the red minus button, the created boxes are deleted.

![img19](https://user-images.githubusercontent.com/29302909/97035276-c6279200-156e-11eb-8c6a-43ffaf6819f7.png)

If incorrect values are entered into the **Upper Limit** and the **Lower Limit** boxes in this window, the user would receive the aforementioned warnings.

If the **OK** button is clicked after making selections regarding the **UD** instance, this window would close.

**4.5.4.** Clicking the **Pr** menu button creates a window as below:

![img20](https://user-images.githubusercontent.com/29302909/97035429-fc651180-156e-11eb-94ff-42d522869bfa.png)

Again, by clicking the green plus button, the following boxes are created, and by clicking the red minus button, the created boxes are deleted.

![img21](https://user-images.githubusercontent.com/29302909/97035480-1272d200-156f-11eb-837d-4bec1f89cd0c.png)

If incorrect values are entered into the **Upper Limit** and the **Lower Limit** boxes in this window, the user would receive the aforementioned warnings.

This window would close if the **OK** button is clicked after the selections related to the pressuremeter experiments are made.

**4.5.5.** Clicking the **PD** menu button creates a window as below:

![img22](https://user-images.githubusercontent.com/29302909/97035779-7f866780-156f-11eb-97d8-9e95b254cfeb.png)

Again, by clicking the green plus button, the following boxes are created, and by clicking the red minus button, the created boxes are deleted.

![img23](https://user-images.githubusercontent.com/29302909/97035840-9a58dc00-156f-11eb-91df-e5e36c35a4af.png)

If incorrect values are entered into the **Upper Limit** and the **Lower Limit** boxes in this window, the user would receive the aforementioned warnings.

This window would close if the **OK** button is clicked after the selections related to the Lugeon experiments are made.

**5.** If users come to the **Canvas** menu cascade, they should see two menu buttons which are **Display**, **Export**.

**5.1.** If users click the **Display** menu button, they could display the project information they added before. The canvas could be displayed after the borehole depth is defined.

![img24](https://user-images.githubusercontent.com/29302909/97036508-9bd6d400-1570-11eb-8232-16ac50509b85.png)

The arrow keys at the bottom of the screen should be used to navigate through the log pages.

Below are pictures of how a sample project looks on the canvas.

![img25](https://user-images.githubusercontent.com/29302909/97036622-c4f76480-1570-11eb-8468-8952c1f5a2f2.png)

![img26](https://user-images.githubusercontent.com/29302909/97036625-c6c12800-1570-11eb-9209-3ba3ef2dffb1.png)

**5.2** If users click the **Export** menu button, they could export the canvas into pdf format.

**6.** If users come to the **Settings** menu cascade, they would see only one menu cascade called **Language**. The **Language** menu cascade contains two menu buttons which names are **English** and **Turkish**. These menu buttons change the language of the program and log. The change would become valid in the next sessions.

The default language of the program is set to **English**.

If the language of the program is changed while there is a project displayed on the canvas, the menu names and the names of the buttons in the menus will automatically change according to the selected language. In order for the texts on the canvas to be translated according to the selected language, the canvas must be re-displayed. That's why users should go to the **Canvas** menu cascade and click the **Display** button. After clicking the **Display** button, a process takes place in the background to change the texts in the log and after a short while, the texts in the log would be translated to their equivalents in the selected language.

**7.** If users come to the **Help** menu cascade, they would see two menu buttons which names are **About** and **Check for updates**.

**7.1.** If the **About** menu button is clicked, the following window opens:

![img27](https://user-images.githubusercontent.com/29302909/97037505-076d7100-1572-11eb-8cc9-be7d5490d982.png)

As can be seen on the above image, in this window, there is not much detailed information about the program and contact information that users can contact me in case of any problem or request.

**7.2.** If the **Check for updates** menu button is clicked, users could update their program by clicking this menu button.

## Licenses

TkJeoLog is released under the terms of the GNU GENERAL PUBLIC LICENSE. Please refer to the LICENSE file.
