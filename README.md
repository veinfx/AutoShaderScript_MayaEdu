# AutoShaderScript_MayaEdu
This script is for artists who personally use Maya like Education or Indie version with V-Ray and Substance Painter. It will help you many setup of shaders automatically.

## Installation
1. Put a root directory(AutoShaderScript_MayaEdu) into a Maya scripts directory.
* Windows: C:\Users\{user_directory}\Documents\maya\scripts
2. Write these commands on Script Editor or Shelf Editor of Maya.
```python
from AutoShaderScript_MayaEdu.scripts.UI import Window
mat = Window.MaterialHandlerWindow()
mat.show()
```