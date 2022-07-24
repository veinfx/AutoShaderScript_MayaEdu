# AutoShaderScript_MayaEdu
This script is for artists who personally use Maya like Education or Indie version with V-Ray and Substance Painter. It will help you many setup of shaders automatically.

## Installation
(This update just supports Windows. Later, other OS will be added in a support list.)
1. Put a root directory(AutoShaderScript_MayaEdu) into a Maya scripts directory.
* Windows: C:\\Users\\{user_directory}\\Documents\\maya\\scripts
2. Copy and paste lines of Installer.py on Script Editor and run it.
* Path: ../AutoShaderScript_MayaEdu/scripts/Installer.py

## How to use
1. Click _Setting_ button on a main window
2. Load textures
* For every texture files collected in a directory 
  * Click _Find_ button > Click _Texture Load_
  * Manipulate each options of columns
    * If you delete some of rows, you can refer to a guide under this line
* For texture files from different directories
  * Check _Enable To Load Paths From Non Root_
  * Click _Add Material_ > Load textures by clicking _LOAD_ button on each rows
    * If you want to delete selected rows, Click _Delete Material_
    * If you want to delete every rows, Click _Delete All Materials_
3. Click _Define Material_ button on a dialog for setting materials
4. Click _Assign Material_ on a main window after selecting materials suitable with each meshes